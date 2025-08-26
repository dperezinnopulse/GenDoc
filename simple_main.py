from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routes import web, api
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🔄 Creando aplicación FastAPI simplificada...")
app = FastAPI(title="PDFGen Service", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("🔄 Incluyendo routers...")
app.include_router(web.router, prefix="")
app.include_router(api.router, prefix="/api")
logger.info("✅ Routers incluidos")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return "<meta http-equiv='refresh' content='0; url=/admin' />"

logger.info("✅ Aplicación FastAPI simplificada creada")
