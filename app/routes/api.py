from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..services.template_store import TemplateStore
from ..services.renderer import Renderer
import io

router = APIRouter()

store = TemplateStore(base_path="/workspace/pdfgen/storage/templates")
renderer = Renderer(store)

class RenderRequest(BaseModel):
    template_id: str
    data: dict

class MappingRequest(BaseModel):
    mapping: dict | None = None
    repeat_sections: dict | None = None
    schema: dict | None = None

@router.get("/templates")
async def list_templates():
    return store.list_templates()

@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    try:
        return store.get_template_meta(template_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")

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
        pdf_bytes = renderer.render_to_pdf(req.template_id, req.data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")