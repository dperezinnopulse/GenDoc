import os
import shutil
import uuid
import json
from typing import Any, Dict, List, Optional
from fastapi import UploadFile

SUPPORTED_EXTENSIONS = {".docx": "docx", ".xlsx": "xlsx", ".pdf": "pdf"}


class TemplateStore:
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _template_dir(self, template_id: str) -> str:
        return os.path.join(self.base_path, template_id)

    def _meta_path(self, template_id: str) -> str:
        return os.path.join(self._template_dir(template_id), "meta.json")

    def _original_path(self, template_id: str, ext: str) -> str:
        return os.path.join(self._template_dir(template_id), f"original{ext}")

    def save_template(self, file: UploadFile, name: Optional[str] = None) -> str:
        _, ext = os.path.splitext(file.filename or "")
        ext = ext.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError("Extensión no soportada. Use .docx, .xlsx o .pdf")
        template_id = uuid.uuid4().hex
        tdir = self._template_dir(template_id)
        os.makedirs(tdir, exist_ok=True)
        dst = self._original_path(template_id, ext)
        with open(dst, "wb") as f:
            shutil.copyfileobj(file.file, f)
        meta = {
            "id": template_id,
            "name": name or (file.filename or template_id),
            "ext": ext,
            "kind": SUPPORTED_EXTENSIONS[ext],
            "mapping": {},
            "repeat_sections": {},
            "schema": {},
        }
        with open(self._meta_path(template_id), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        return template_id

    def list_templates(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        for template_id in os.listdir(self.base_path):
            meta_path = self._meta_path(template_id)
            if not os.path.isfile(meta_path):
                continue
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                items.append({
                    "id": meta.get("id"),
                    "name": meta.get("name"),
                    "kind": meta.get("kind"),
                })
            except Exception:
                continue
        return sorted(items, key=lambda x: x["name"].lower())

    def get_template_meta(self, template_id: str) -> Dict[str, Any]:
        meta_path = self._meta_path(template_id)
        if not os.path.isfile(meta_path):
            raise FileNotFoundError("Plantilla no encontrada")
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_template_file(self, template_id: str) -> str:
        meta = self.get_template_meta(template_id)
        ext = meta["ext"]
        path = self._original_path(template_id, ext)
        if not os.path.isfile(path):
            raise FileNotFoundError("Archivo de plantilla no encontrado")
        return path

    def save_mapping(self, template_id: str, mapping: Dict[str, Any], repeat_sections: Optional[Dict[str, Any]] = None, schema: Optional[Dict[str, Any]] = None):
        meta = self.get_template_meta(template_id)
        meta["mapping"] = mapping or {}
        if repeat_sections is not None:
            meta["repeat_sections"] = repeat_sections
        if schema is not None:
            meta["schema"] = schema
        with open(self._meta_path(template_id), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    def delete_template(self, template_id: str) -> bool:
        tdir = self._template_dir(template_id)
        if os.path.isdir(tdir):
            shutil.rmtree(tdir)
            return True
        return False