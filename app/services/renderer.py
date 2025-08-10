import os
import tempfile
import math
from typing import Dict, Any, List
from .template_store import TemplateStore
from ..utils.soffice import convert_to_pdf
from ..utils.validation import validate_payload
from ..utils.pdf_preview import get_preview_scale
from docxtpl import DocxTemplate
from openpyxl import load_workbook
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
import io


class Renderer:
    def __init__(self, store: TemplateStore):
        self.store = store

    def render_to_pdf(self, template_id: str, data: Dict[str, Any]) -> bytes:
        meta = self.store.get_template_meta(template_id)
        kind = meta["kind"]
        tpl_path = self.store.get_template_file(template_id)
        mapping = meta.get("mapping", {})
        repeat_sections = meta.get("repeat_sections", {})
        schema = meta.get("schema")

        validate_payload(data, schema)

        context = self._apply_mapping(data, mapping)
        if kind == "docx":
            return self._render_docx_to_pdf(tpl_path, context)
        if kind == "xlsx":
            return self._render_xlsx_to_pdf(tpl_path, context)
        if kind == "pdf":
            # Prefer overlay if positions mapping exists; otherwise try AcroForm then fallback
            if mapping.get("_positions"):
                return self._render_pdf_overlay(tpl_path, context, original_data=data, mapping=mapping)
            try:
                return self._render_pdf_acroform(tpl_path, context)
            except Exception:
                return self._render_pdf_overlay(tpl_path, context, original_data=data, mapping=mapping)
        raise ValueError("Tipo de plantilla no soportado")

    def _apply_mapping(self, data: Dict[str, Any], mapping: Dict[str, Any]) -> Dict[str, Any]:
        if not mapping:
            return data
        def get_path(d: Dict[str, Any], path: str):
            cur: Any = d
            for part in path.split('.'):
                if isinstance(cur, dict):
                    cur = cur.get(part)
                else:
                    cur = None
                if cur is None:
                    break
            return cur
        out: Dict[str, Any] = {}
        for k, src in mapping.items():
            if isinstance(src, str):
                out[k] = get_path(data, src)
        out.update({k: v for k, v in mapping.items() if not isinstance(v, str)})
        out.update(data)
        return out

    def _render_docx_to_pdf(self, tpl_path: str, context: Dict[str, Any]) -> bytes:
        with tempfile.TemporaryDirectory() as td:
            out_docx = os.path.join(td, "out.docx")
            out_pdf = os.path.join(td, "out.pdf")
            doc = DocxTemplate(tpl_path)
            doc.render(context)
            doc.save(out_docx)
            convert_to_pdf(out_docx, out_pdf)
            with open(out_pdf, "rb") as f:
                return f.read()

    def _render_xlsx_to_pdf(self, tpl_path: str, context: Dict[str, Any]) -> bytes:
        with tempfile.TemporaryDirectory() as td:
            out_xlsx = os.path.join(td, "out.xlsx")
            out_pdf = os.path.join(td, "out.pdf")
            wb = load_workbook(tpl_path)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for cell in row:
                        if isinstance(cell.value, str):
                            new_val = cell.value
                            for k, v in context.items():
                                placeholder = f"{{{{{k}}}}}"
                                if placeholder in new_val:
                                    new_val = new_val.replace(placeholder, str(v) if v is not None else "")
                            cell.value = new_val
            wb.save(out_xlsx)
            convert_to_pdf(out_xlsx, out_pdf)
            with open(out_pdf, "rb") as f:
                return f.read()

    def _render_pdf_acroform(self, tpl_path: str, context: Dict[str, Any]) -> bytes:
        with tempfile.TemporaryDirectory() as td:
            reader = PdfReader(tpl_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            fields = {}
            for key, val in context.items():
                if key.startswith("_"):
                    continue
                fields[key] = "" if val is None else str(val)
            writer.update_page_form_field_values(writer.pages[0], fields)
            out_path = os.path.join(td, "out.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            with open(out_path, "rb") as f:
                return f.read()

    def _render_pdf_overlay(self, tpl_path: str, context: Dict[str, Any], original_data: Dict[str, Any], mapping: Dict[str, Any]) -> bytes:
        positions = mapping.get("_positions", {})
        repeat_rows_cfg = mapping.get("_repeat_rows", {})
        header_positions = mapping.get("_header_positions", {})
        footer_positions = mapping.get("_footer_positions", {})
        styles = mapping.get("_styles", {})
        default_style = mapping.get("_default_style", {"font": "Helvetica", "size": 10, "color": "#111111"})

        preview_scale = float(mapping.get("_preview_scale", get_preview_scale()))
        offset_conf = mapping.get("_offset", {"x": 0, "y": 0})
        offset_x = float(offset_conf.get("x", 0) or 0)
        offset_y = float(offset_conf.get("y", 0) or 0)

        def apply_style_for_key(key: str):
            style = styles.get(key, default_style)
            font = style.get("font", default_style.get("font", "Helvetica"))
            size = float(style.get("size", default_style.get("size", 10)))
            color = style.get("color", default_style.get("color", "#111111"))
            try:
                c.setFont(font, size)
            except Exception:
                c.setFont("Helvetica", size)
            try:
                c.setFillColor(HexColor(color))
            except Exception:
                c.setFillColor(HexColor("#111111"))

        def draw_text(key: str, x: float, y: float, value: Any):
            apply_style_for_key(key)
            c.drawString(float(x) + offset_x, float(y) + offset_y, "" if value is None else str(value))

        def draw_cross(x: float, y: float, size: float = 4.0):
            cx = float(x) + offset_x
            cy = float(y) + offset_y
            c.setLineWidth(0.5)
            c.line(cx - size, cy, cx + size, cy)
            c.line(cx, cy - size, cx, cy + size)

        def get_path(d: Dict[str, Any], path: str):
            cur: Any = d
            for part in path.split('.'):
                if isinstance(cur, dict):
                    cur = cur.get(part)
                else:
                    cur = None
                if cur is None:
                    break
            return cur

        with tempfile.TemporaryDirectory() as td:
            overlay_path = os.path.join(td, "overlay.pdf")
            base_reader = PdfReader(tpl_path)
            first_page = base_reader.pages[0]
            width = float(first_page.mediabox.width)
            height = float(first_page.mediabox.height)

            def to_pdf_coords(xy: tuple[float, float]) -> tuple[float, float]:
                # positions are stored in image pixels; preview_scale expresses pixels per PDF point
                px, py = float(xy[0]), float(xy[1])
                return (px / preview_scale, py / preview_scale)

            def norm_positions_dict(d: Dict[str, Any]) -> Dict[str, tuple[float, float]]:
                out = {}
                for k, v in d.items():
                    try:
                        out[k] = to_pdf_coords(v)
                    except Exception:
                        out[k] = v
                return out

            positions_pdf = norm_positions_dict(positions)
            header_pdf = norm_positions_dict(header_positions)
            footer_pdf = norm_positions_dict(footer_positions)

            images_cfg = mapping.get("_images", {}) or {}
            image_previews = mapping.get("_image_previews", {}) or {}

            arr_path = None
            arr_def = None
            if repeat_rows_cfg:
                arr_path, arr_def = next(iter(repeat_rows_cfg.items()))
            items: List[Any] = get_path(original_data, arr_path) if arr_path else []
            if items is None or not isinstance(items, list):
                items = []

            rows_per_page = int(arr_def.get("rowsPerPage", 0)) if arr_def else 0
            start_y = float(arr_def.get("startY", 700)) if arr_def else 700.0
            delta_y = float(arr_def.get("deltaY", 24)) if arr_def else 24.0
            end_y = arr_def.get("endY") if arr_def else None
            if not rows_per_page and end_y is not None:
                try:
                    end_y = float(end_y)
                    if delta_y > 0:
                        rows_per_page = max(1, int((start_y - end_y) / delta_y) + 1)
                except Exception:
                    rows_per_page = 0
            if not rows_per_page:
                rows_per_page = max(1, int((start_y) / max(delta_y, 1)))

            total_pages = max(1, math.ceil(len(items) / rows_per_page))

            c = canvas.Canvas(overlay_path, pagesize=(width, height))

            def draw_header_footer(page_index: int):
                for key, (x, y) in header_pdf.items():
                    val = context.get(key)
                    if key == "_page_number":
                        val = str(page_index + 1)
                    if key == "_page_count":
                        val = str(total_pages)
                    draw_text(key, x, y, val)
                for key, (x, y) in footer_pdf.items():
                    val = context.get(key)
                    if key == "_page_number":
                        val = str(page_index + 1)
                    if key == "_page_count":
                        val = str(total_pages)
                    draw_text(key, x, y, val)

            def draw_fixed_positions():
                for key, value in context.items():
                    if key.startswith("_"):
                        continue
                    if arr_path and key.startswith(arr_path + "."):
                        continue
                    pos = positions_pdf.get(key)
                    if pos:
                        x, y = pos
                        draw_text(key, x, y, value)

            def decode_data_url(data_url_or_b64: str | bytes | None) -> bytes | None:
                if not data_url_or_b64:
                    return None
                if isinstance(data_url_or_b64, bytes):
                    return data_url_or_b64
                s = str(data_url_or_b64)
                try:
                    if s.startswith("data:") and ";base64," in s:
                        b64 = s.split(",",1)[1]
                        import base64
                        return base64.b64decode(b64)
                    # raw base64
                    import base64
                    return base64.b64decode(s)
                except Exception:
                    return None

            def draw_images():
                for key, meta in images_cfg.items():
                    # choose data: prefer context value, else preview
                    data_bytes = None
                    ctx_val = context.get(key)
                    if ctx_val is not None:
                        data_bytes = decode_data_url(ctx_val)
                    if not data_bytes:
                        data_bytes = decode_data_url(image_previews.get(key))
                    if not data_bytes:
                        continue
                    try:
                        img_reader = ImageReader(io.BytesIO(data_bytes))
                    except Exception:
                        continue
                    # convert px to pt and apply offset
                    x_pt = float(meta.get("x", 0.0)) / preview_scale + offset_x
                    y_pt = float(meta.get("y", 0.0)) / preview_scale + offset_y
                    w_pt = float(meta.get("width", 100.0)) / preview_scale
                    h_pt = float(meta.get("height", 100.0)) / preview_scale
                    # y_pt is the top-left anchor in our coordinate? We defined (x,y) as bottom-left of text; for images, assume (x,y) is bottom-left
                    # drawImage expects lower-left
                    c.drawImage(img_reader, x_pt, y_pt - h_pt + h_pt, width=w_pt, height=h_pt, preserveAspectRatio=True, mask='auto')

            for page_idx in range(total_pages):
                draw_header_footer(page_idx)
                draw_fixed_positions()
                draw_images()
                debug_lines = []
                debug_lines.append(f"scale={preview_scale}, offset=({offset_x:.1f},{offset_y:.1f}), page= {page_idx+1}/{total_pages}, size=({width:.1f},{height:.1f})")
                # Fixed fields debug
                for key, (x_pt, y_pt) in positions_pdf.items():
                    if arr_path and key.startswith(arr_path + "."):
                        continue
                    final_x = x_pt + offset_x
                    final_y = y_pt + offset_y
                    x_px, y_px = positions.get(key, (None, None))
                    if x_px is None:
                        continue
                    debug_lines.append(f"{key}: px=({x_px:.1f},{y_px:.1f}) -> pt=({x_pt:.1f},{y_pt:.1f}) final=({final_x:.1f},{final_y:.1f})")
                    # draw crosshair at final position for visual check
                    draw_cross(x_pt, y_pt)
                # Repeat rows debug (only if array defined)
                if arr_path:
                    start_idx = page_idx * rows_per_page
                    end_idx = min(len(items), start_idx + rows_per_page)
                    for idx in range(start_idx, end_idx):
                        y_item = start_y - (idx - start_idx) * delta_y
                        prefix = arr_path + "."
                        for key, (x_pt, y_pt_base) in positions_pdf.items():
                            if key.startswith(prefix):
                                final_x = x_pt + offset_x
                                final_y = y_item + offset_y
                                x_px, y_px = positions.get(key, (None, None))
                                if x_px is None:
                                    continue
                                debug_lines.append(f"{key}[{idx}]: px=({x_px:.1f},{y_px:.1f}) -> base_pt=({x_pt:.1f},{y_pt_base if isinstance(y_pt_base,(int,float)) else 0:.1f}) y_item={y_item:.1f} final=({final_x:.1f},{final_y:.1f})")
                                draw_cross(x_pt, y_item)
                # Draw debug lines in gray at top-left
                try:
                    c.setFont("Helvetica", 6)
                except Exception:
                    pass
                try:
                    c.setFillColor(HexColor("#666666"))
                except Exception:
                    pass
                y_cursor = height - 10
                for line in debug_lines[:100]:
                    c.drawString(10, y_cursor, line)
                    y_cursor -= 8
                # Draw repeated rows content
                if arr_path:
                    start_idx = page_idx * rows_per_page
                    end_idx = min(len(items), start_idx + rows_per_page)
                    for idx in range(start_idx, end_idx):
                        item = items[idx]
                        y_item = start_y - (idx - start_idx) * delta_y
                        prefix = arr_path + "."
                        for key, (x, _) in positions_pdf.items():
                            if key.startswith(prefix):
                                sub_key = key[len(prefix):]
                                val = get_path(item, sub_key)
                                draw_text(key, x, y_item, val)
                if page_idx < total_pages - 1:
                    c.showPage()
            c.save()

            overlay_reader = PdfReader(overlay_path)
            writer = PdfWriter()
            base_page_count = len(base_reader.pages)
            for i in range(total_pages):
                base_page = base_reader.pages[min(i, base_page_count - 1)]
                merged = base_page
                if i < len(overlay_reader.pages):
                    merged.merge_page(overlay_reader.pages[i])
                writer.add_page(merged)

            out_path = os.path.join(td, "out.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            with open(out_path, "rb") as f:
                return f.read()