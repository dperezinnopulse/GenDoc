from typing import Optional
import pypdfium2 as pdfium
import io


def render_pdf_page_png(file_path: str, page_index_zero_based: int, scale: float = 1.5) -> bytes:
    pdf = pdfium.PdfDocument(file_path)
    page_count = len(pdf)
    if page_index_zero_based < 0 or page_index_zero_based >= page_count:
        page_index_zero_based = 0
    page = pdf.get_page(page_index_zero_based)
    pil_image = page.render(scale=scale).to_pil()
    bio = io.BytesIO()
    pil_image.save(bio, format="PNG")
    return bio.getvalue()