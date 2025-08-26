from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
from ..services.template_store import TemplateStore
from ..services.renderer import Renderer
import io
import re
from pypdf import PdfReader
from openpyxl import load_workbook

router = APIRouter()

store = TemplateStore(base_path="storage/templates")
renderer = Renderer(store)

class RenderRequest(BaseModel):
    template_id: str
    data: dict
    output_format: Literal["pdf", "image"] = "pdf"  # Nuevo parámetro con valor por defecto

class MappingRequest(BaseModel):
    mapping: dict | None = None
    repeat_sections: dict | None = None
    schema: dict | None = None


def _sample_value_for(name: str) -> str:
    low = name.lower()
    if "nombre" in low:
        return "Ana"
    if "apellido" in low:
        return "Pérez"
    if "documento" in low or "dni" in low or "numero" in low or low == "nif":
        return "123"
    if "fecha" in low:
        return "2025-09-01"
    if "curso" in low:
        return "Matemáticas"
    return "Texto"


def _ensure_path(d: dict, path: str):
    cur = d
    parts = [p for p in path.split('.') if p]
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur.get(p), dict):
            cur[p] = {}
        cur = cur[p]
    return cur, parts[-1] if parts else None


def _normalize_mapping(m):
    if isinstance(m, list):
        if len(m) == 1 and isinstance(m[0], dict):
            return m[0]
        merged = {}
        for item in m:
            if isinstance(item, dict):
                merged.update(item)
        return merged
    return m or {}

@router.get("/templates")
async def list_templates():
    return store.list_templates()

@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    try:
        return store.get_template_meta(template_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

@router.get("/templates/{template_id}/suggested")
async def get_suggested_data(template_id: str):
    try:
        meta = store.get_template_meta(template_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    mapping = _normalize_mapping(meta.get("mapping", {}))
    positions = mapping.get("_positions", {}) or {}
    repeat_rows = mapping.get("_repeat_rows", {}) or {}
    sample: dict = {}
    # arrays
    for arr_path, _def in repeat_rows.items():
        items_fields = [k[len(arr_path)+1:] for k in positions.keys() if k.startswith(arr_path + ".")]
        def build_item():
            item: dict = {}
            for subkey in items_fields:
                parent, leaf = _ensure_path(item, subkey)
                if leaf:
                    parent[leaf] = _sample_value_for(leaf)
            if not item:
                item["valor"] = "Texto"
            return item
        sample[arr_path] = [build_item(), build_item()]
    # fixed
    for key in positions.keys():
        if any(key.startswith(p + ".") for p in repeat_rows.keys()):
            continue
        parent, leaf = _ensure_path(sample, key)
        if leaf:
            parent[leaf] = _sample_value_for(leaf)
    # plain mapping keys
    for k, v in mapping.items():
        if k.startswith("_"):
            continue
        if k not in sample:
            parent, leaf = _ensure_path(sample, k)
            if leaf:
                parent[leaf] = _sample_value_for(leaf)
            else:
                sample[k] = _sample_value_for(k)
    # fallbacks
    if not sample:
        kind = meta.get("kind")
        path = store.get_template_file(template_id)
        if kind == "pdf":
            try:
                reader = PdfReader(path)
                fields = None
                if hasattr(reader, "get_fields"):
                    fields = reader.get_fields() or {}
                if fields:
                    for fname in fields.keys():
                        parent, leaf = _ensure_path(sample, fname)
                        if leaf:
                            parent[leaf] = _sample_value_for(leaf)
            except Exception:
                pass
        elif kind == "xlsx":
            try:
                wb = load_workbook(path)
                placeholder_re = re.compile(r"\{\{\s*([^}]+?)\s*\}\}")
                found = set()
                for ws in wb.worksheets:
                    for row in ws.iter_rows():
                        for cell in row:
                            if isinstance(cell.value, str):
                                for m in placeholder_re.findall(cell.value):
                                    found.add(m)
                for key in sorted(found):
                    parent, leaf = _ensure_path(sample, key)
                    if leaf:
                        parent[leaf] = _sample_value_for(leaf)
            except Exception:
                pass
    if not sample:
        sample = {"nombre": "Ana"}
    return sample

@router.delete("/templates/{template_id}")
async def delete_template(template_id: str):
    ok = store.delete_template(template_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    return {"deleted": True}

@router.post("/templates/{template_id}/mapping")
async def set_mapping(template_id: str, body: MappingRequest):
    try:
        store.save_mapping(template_id, body.mapping or {}, body.repeat_sections or {}, body.schema or {})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    return {"ok": True}

@router.post("/render")
async def render_document(req: RenderRequest):
    try:
        # Debug: Log the request parameters
        print(f"🔍 DEBUG: output_format = {req.output_format}")
        print(f"🔍 DEBUG: template_id = {req.template_id}")
        
        # Get template metadata to check for signatures
        meta = store.get_template_meta(req.template_id)
        mapping = meta.get("mapping", {})
        signatures_cfg = mapping.get("_signatures", {}) or {}
        
        # Render PDF asynchronously
        pdf_bytes = await renderer.render_to_pdf_async(req.template_id, req.data)
        
        # Handle different output formats
        if req.output_format == "image":
            print("🖼️  DEBUG: Converting PDF to image...")
            # Convert PDF to image
            image_bytes = await renderer.convert_pdf_to_image(pdf_bytes)
            print(f"🖼️  DEBUG: Image conversion complete, size: {len(image_bytes)} bytes")
            
            # Prepare response with image and signature coordinates
            import base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            response_data = {
                "image_base64": image_base64,
                "signatures": {}
            }
            
            # Add signature coordinates if any exist
            if signatures_cfg:
                for key, meta in signatures_cfg.items():
                    response_data["signatures"][key] = {
                        "x": meta.get("x", 0),
                        "y": meta.get("y", 0),
                        "width": meta.get("width", 200),
                        "height": meta.get("height", 300)
                    }
            
            return response_data
        
        print("📄 DEBUG: Returning PDF format...")
        # Default: PDF output
        # Prepare response with signature coordinates if any
        response_data = {
            "pdf": pdf_bytes,
            "signatures": {}
        }
        
        # Add signature coordinates if any exist
        if signatures_cfg:
            for key, meta in signatures_cfg.items():
                response_data["signatures"][key] = {
                    "x": meta.get("x", 0),
                    "y": meta.get("y", 0),
                    "width": meta.get("width", 200),
                    "height": meta.get("height", 300)
                }
        
        # If no signatures, return just the PDF
        if not signatures_cfg:
            return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")
        else:
            # Return JSON with PDF as base64 and signature coordinates
            import base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            return {
                "pdf_base64": pdf_base64,
                "signatures": response_data["signatures"]
            }
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))