# PDFGen Standalone Service

Servicio standalone para gestionar plantillas (DOCX, XLSX, PDF) y generar impresos en PDF vía API.

## Funciones
- Login simple (1 usuario)
- Gestión de plantillas (subir, listar, borrar)
- Mapeo de campos y secciones repetidas
- Render: JSON + plantilla -> PDF
- API REST para integración

## Quickstart
1. Requisitos: Python 3.11+, LibreOffice (soffice) instalado para conversión a PDF
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
3. Variables de entorno (archivo `.env`):
```
ADMIN_USER=admin
ADMIN_PASSWORD=changeme
SECRET_KEY=change-this
```
4. Ejecutar
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## API
- POST `/api/render` -> body: { template_id: string, data: object } -> retorna PDF (application/pdf)
- GET `/api/templates` -> lista de plantillas
- POST `/api/templates` -> subir plantilla (multipart/form-data)
- DELETE `/api/templates/{id}`

Panel web básico en `/admin`.