import os
import shutil
import subprocess
import tempfile
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SofficePool:
    """
    Pool de conversión LibreOffice para manejar múltiples conversiones simultáneamente.
    Limita el número de procesos LibreOffice concurrentes para evitar saturar el sistema.
    """
    
    def __init__(self, max_workers: int = 3):
        """
        Inicializa el pool de conversión.
        
        Args:
            max_workers: Número máximo de procesos LibreOffice simultáneos
        """
        self.max_workers = max_workers
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.semaphore = asyncio.Semaphore(max_workers)
        self._soffice_path = self._find_soffice()
        logger.info(f"SofficePool inicializado con {max_workers} workers")
    
    def _find_soffice(self) -> str:
        """Encuentra la ruta de LibreOffice soffice."""
        for name in ["soffice", "/usr/bin/soffice", "/usr/local/bin/soffice"]:
            if shutil.which(name) or os.path.isfile(name):
                return shutil.which(name) or name
        raise FileNotFoundError("LibreOffice (soffice) no encontrado en PATH")
    
    def _convert_to_pdf_sync(self, input_path: str, output_path: str) -> bool:
        """
        Conversión síncrona a PDF (ejecutada en proceso separado).
        
        Args:
            input_path: Ruta del archivo de entrada
            output_path: Ruta del archivo PDF de salida
            
        Returns:
            True si la conversión fue exitosa
        """
        try:
            outdir = os.path.dirname(output_path)
            os.makedirs(outdir, exist_ok=True)
            
            with tempfile.TemporaryDirectory() as tmp:
                cmd = [
                    self._soffice_path,
                    "--headless",
                    "--norestore",
                    "--nolockcheck",
                    "--nodefault",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    tmp,
                    input_path,
                ]
                
                result = subprocess.run(
                    cmd, 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    timeout=30  # Timeout de 30 segundos
                )
                
                # Mover el PDF resultante
                base = os.path.splitext(os.path.basename(input_path))[0]
                produced = os.path.join(tmp, base + ".pdf")
                
                if not os.path.isfile(produced):
                    # Buscar cualquier PDF en tmp
                    candidates = [p for p in os.listdir(tmp) if p.lower().endswith('.pdf')]
                    if candidates:
                        produced = os.path.join(tmp, candidates[0])
                
                if not os.path.isfile(produced):
                    raise RuntimeError("No se pudo convertir a PDF")
                
                shutil.move(produced, output_path)
                return True
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout en conversión de {input_path}")
            return False
        except Exception as e:
            logger.error(f"Error en conversión de {input_path}: {e}")
            return False
    
    async def convert_to_pdf_async(self, input_path: str, output_path: str) -> bool:
        """
        Conversión asíncrona a PDF con control de concurrencia.
        
        Args:
            input_path: Ruta del archivo de entrada
            output_path: Ruta del archivo PDF de salida
            
        Returns:
            True si la conversión fue exitosa
        """
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            try:
                result = await loop.run_in_executor(
                    self.executor,
                    self._convert_to_pdf_sync,
                    input_path,
                    output_path
                )
                return result
            except Exception as e:
                logger.error(f"Error en conversión asíncrona: {e}")
                return False
    
    def shutdown(self):
        """Cierra el pool de procesos."""
        self.executor.shutdown(wait=True)
        logger.info("SofficePool cerrado")

# Instancia global del pool
_soffice_pool: Optional[SofficePool] = None

def get_soffice_pool() -> SofficePool:
    """Obtiene la instancia global del pool de conversión."""
    global _soffice_pool
    if _soffice_pool is None:
        # Usar configuración automática del servidor
        try:
            from ...server_config import server_config
            max_workers = server_config.get_soffice_workers()
        except ImportError:
            # Fallback si no está disponible
            import multiprocessing
            cpu_count = multiprocessing.cpu_count()
            max_workers = min(3, cpu_count)
            
        _soffice_pool = SofficePool(max_workers=max_workers)
    return _soffice_pool

def shutdown_soffice_pool():
    """Cierra la instancia global del pool."""
    global _soffice_pool
    if _soffice_pool:
        _soffice_pool.shutdown()
        _soffice_pool = None
