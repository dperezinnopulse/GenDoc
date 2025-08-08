from fastapi import APIRouter, Depends, Form, UploadFile, File, Query
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse, Response
from starlette import status
from ..utils.auth import get_session_user, login_user, require_user, set_auth_cookie, clear_auth_cookie
from ..services.template_store import TemplateStore
from ..services.renderer import Renderer
from ..utils.pdf_preview import render_pdf_page_png
from jinja2 import Environment, FileSystemLoader, select_autoescape
import io
import json

router = APIRouter()

templates_env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

store = TemplateStore(base_path="/workspace/pdfgen/storage/templates")
renderer = Renderer(store)

@router.get("/admin", response_class=HTMLResponse)
async def admin_home(user: str | None = Depends(get_session_user)):
    if not user:
        template = templates_env.get_template("login.html")
        return template.render()
    templates = store.list_templates()
    template = templates_env.get_template("dashboard.html")
    return template.render(user=user, templates=templates)

@router.post("/admin/login")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    token = login_user(username, password)
    if token:
        resp = RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
        set_auth_cookie(resp, token)
        return resp
    template = templates_env.get_template("login.html")
    return HTMLResponse(template.render(error="Credenciales inválidas"), status_code=401)

@router.get("/admin/logout")
async def admin_logout():
    resp = RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
    clear_auth_cookie(resp)
    return resp

@router.post("/admin/templates/upload")
async def upload_template(
    user: str = Depends(require_user),
    file: UploadFile = File(...),
    name: str = Form(None)
):
    store.save_template(file, name)
    return RedirectResponse(f"/admin", status_code=status.HTTP_302_FOUND)

@router.get("/admin/templates/{template_id}", response_class=HTMLResponse)
async def view_template(template_id: str, user: str = Depends(require_user)):
    template_meta = store.get_template_meta(template_id)
    template = templates_env.get_template("template_detail.html")
    return template.render(user=user, template=template_meta)

@router.post("/admin/templates/{template_id}/delete")
async def delete_template(template_id: str, user: str = Depends(require_user)):
    store.delete_template(template_id)
    return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)

@router.post("/admin/templates/{template_id}/save_mapping")
async def save_mapping(
    template_id: str,
    mapping_json: str = Form("{}"),
    repeat_json: str = Form("{}"),
    schema_json: str = Form("{}"),
    user: str = Depends(require_user),
):
    try:
        mapping = json.loads(mapping_json) if mapping_json else {}
        repeat_sections = json.loads(repeat_json) if repeat_json else {}
        schema = json.loads(schema_json) if schema_json else {}
    except json.JSONDecodeError as ex:
        tmpl = templates_env.get_template("template_detail.html")
        template_meta = store.get_template_meta(template_id)
        return HTMLResponse(tmpl.render(user=user, template=template_meta, error=f"JSON inválido: {ex}"), status_code=400)
    store.save_mapping(template_id, mapping, repeat_sections, schema)
    return RedirectResponse(f"/admin/templates/{template_id}", status_code=status.HTTP_302_FOUND)

@router.post("/admin/templates/{template_id}/test_render")
async def test_render(template_id: str, data_json: str = Form("{}"), user: str = Depends(require_user)):
    try:
        data = json.loads(data_json) if data_json else {}
        pdf_bytes = renderer.render_to_pdf(template_id, data)
    except Exception as ex:
        tmpl = templates_env.get_template("template_detail.html")
        template_meta = store.get_template_meta(template_id)
        return HTMLResponse(tmpl.render(user=user, template=template_meta, error=str(ex)), status_code=400)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")

# Overlay editor
@router.get("/admin/templates/{template_id}/overlay", response_class=HTMLResponse)
async def overlay_editor(template_id: str, user: str = Depends(require_user)):
    template_meta = store.get_template_meta(template_id)
    if template_meta.get("kind") != "pdf":
        return RedirectResponse(f"/admin/templates/{template_id}")
    template = templates_env.get_template("overlay_editor.html")
    positions = template_meta.get("mapping", {}).get("_positions", {})
    repeat_rows = template_meta.get("mapping", {}).get("_repeat_rows", {})
    styles = template_meta.get("mapping", {}).get("_styles", {})
    default_style = template_meta.get("mapping", {}).get("_default_style", {"font":"Helvetica","size":10,"color":"#111111"})
    header_positions = template_meta.get("mapping", {}).get("_header_positions", {})
    footer_positions = template_meta.get("mapping", {}).get("_footer_positions", {})
    return template.render(
        user=user,
        template=template_meta,
        positions=json.dumps(positions),
        repeat_rows=json.dumps(repeat_rows),
        styles=json.dumps(styles),
        default_style=json.dumps(default_style),
        header_positions=json.dumps(header_positions),
        footer_positions=json.dumps(footer_positions),
    )

@router.get("/admin/templates/{template_id}/overlay/page.png")
async def overlay_editor_page_png(template_id: str, page: int = Query(1, ge=1), user: str = Depends(require_user)):
    path = store.get_template_file(template_id)
    img_bytes = render_pdf_page_png(path, page-1)
    return Response(content=img_bytes, media_type="image/png")

@router.post("/admin/templates/{template_id}/overlay/save")
async def overlay_editor_save(template_id: str, positions_json: str = Form("{}"), repeat_rows_json: str = Form("{}"), header_json: str = Form(None), footer_json: str = Form(None), styles_json: str = Form(None), default_style_json: str = Form(None), user: str = Depends(require_user)):
    meta = store.get_template_meta(template_id)
    try:
        positions = json.loads(positions_json) if positions_json else {}
    except json.JSONDecodeError:
        positions = {}
    try:
        repeat_rows = json.loads(repeat_rows_json) if repeat_rows_json else {}
    except json.JSONDecodeError:
        repeat_rows = {}
    header_positions = {}
    footer_positions = {}
    styles = {}
    default_style = None
    try:
        if header_json:
            header_positions = json.loads(header_json)
    except json.JSONDecodeError:
        header_positions = {}
    try:
        if footer_json:
            footer_positions = json.loads(footer_json)
    except json.JSONDecodeError:
        footer_positions = {}
    try:
        if styles_json:
            styles = json.loads(styles_json)
    except json.JSONDecodeError:
        styles = {}
    try:
        if default_style_json:
            default_style = json.loads(default_style_json)
    except json.JSONDecodeError:
        default_style = None
    mapping = meta.get("mapping", {})
    mapping["_positions"] = positions
    mapping["_repeat_rows"] = repeat_rows
    if header_positions:
        mapping["_header_positions"] = header_positions
    if footer_positions:
        mapping["_footer_positions"] = footer_positions
    if styles is not None:
        mapping["_styles"] = styles
    if default_style is not None:
        mapping["_default_style"] = default_style
    store.save_mapping(template_id, mapping, meta.get("repeat_sections", {}), meta.get("schema", {}))
    return RedirectResponse(f"/admin/templates/{template_id}/overlay", status_code=302)