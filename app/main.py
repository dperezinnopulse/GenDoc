from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .routes import web, api
from .middleware.rate_limit import rate_limit_middleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🔄 Creando aplicación FastAPI...")
app = FastAPI(title="PDFGen Service")
logger.info("✅ Aplicación FastAPI creada")

# Middleware de rate limiting (comentado temporalmente para debug)
# logger.info("🔄 Configurando middleware de rate limiting...")
# app.middleware("http")(rate_limit_middleware)
# logger.info("✅ Middleware de rate limiting configurado")
logger.info("⚠️  Middleware de rate limiting deshabilitado temporalmente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("🔄 Incluyendo routers...")
app.include_router(web.router, prefix="")
logger.info("✅ Router web incluido")
app.include_router(api.router, prefix="/api")
logger.info("✅ Router API incluido")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return "<meta http-equiv='refresh' content='0; url=/admin' />"

# @app.on_event("startup")
# async def startup_event():
#     """Evento de inicio de la aplicación."""
#     logger.info("🚀 Iniciando GenDoc Service con optimizaciones de concurrencia")
#     logger.info("📊 Rate limiting: 100 requests/minuto por cliente")
#     logger.info("🔄 Pool de conversión LibreOffice: 3 workers")
#     logger.info("✅ Startup completado exitosamente")

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Evento de cierre de la aplicación."""
#     logger.info("🔄 Iniciando proceso de shutdown...")
#     try:
#         from .utils.soffice_pool import shutdown_soffice_pool
#         logger.info("🔄 Cerrando pool de LibreOffice...")
#         shutdown_soffice_pool()
#         logger.info("✅ Pool de LibreOffice cerrado correctamente")
#         logger.info("🛑 GenDoc Service cerrado exitosamente")
#     except Exception as e:
#         logger.error(f"❌ Error en shutdown: {e}")
#         logger.error(f"❌ Tipo de error: {type(e).__name__}")
#         import traceback
#         logger.error(f"❌ Traceback: {traceback.format_exc()}")
#     finally:
#         logger.info("🏁 Proceso de shutdown finalizado")