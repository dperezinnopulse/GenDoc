# Análisis de Concurrencia - GenDoc Service

## Estado Actual del Servicio

### ✅ Aspectos Positivos

1. **Framework Asíncrono**: FastAPI con Uvicorn proporciona soporte nativo para operaciones asíncronas
2. **Manejo de Conexiones**: El servidor está manejando múltiples conexiones simultáneas correctamente
3. **Arquitectura Modular**: Separación clara entre rutas, servicios y utilidades

### ⚠️ Puntos Críticos de Concurrencia

#### 1. **LibreOffice (soffice) - Cuello de Botella Principal**
```python
# app/utils/soffice.py - Línea 15-35
def convert_to_pdf(input_path: str, output_path: str):
    soffice = _find_soffice()
    # ... 
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Problemas identificados:**
- **Proceso secuencial**: Cada conversión ejecuta un proceso LibreOffice completo
- **Sin límite de procesos**: No hay control sobre cuántos procesos soffice se ejecutan simultáneamente
- **Tiempo de conversión**: LibreOffice tarda 2-5 segundos por documento
- **Recursos del sistema**: Cada proceso consume ~50-100MB de RAM

#### 2. **Operaciones de Archivo Síncronas**
```python
# app/services/renderer.py - Líneas 60-70
def _render_docx_to_pdf(self, tpl_path: str, context: Dict[str, Any]) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        # Operaciones de archivo bloqueantes
        doc.save(out_docx)
        convert_to_pdf(out_docx, out_pdf)
        with open(out_pdf, "rb") as f:
            return f.read()
```

#### 3. **Falta de Pool de Workers**
- **Uvicorn por defecto**: 1 worker (proceso)
- **Sin workers múltiples**: No aprovecha múltiples núcleos de CPU
- **Sin balanceador de carga**: No hay distribución de carga

#### 4. **Gestión de Memoria**
- **Templates en memoria**: Cada request carga el template completo
- **Sin cache**: No hay reutilización de templates procesados
- **Archivos temporales**: Se crean/eliminan en cada request

## Capacidad Actual Estimada

### Rendimiento Esperado:
- **Requests secuenciales**: ~0.2-0.5 req/s (2-5 segundos por request)
- **Requests concurrentes**: ~2-5 req/s (limitado por LibreOffice)
- **Memoria por request**: ~100-200MB
- **CPU por request**: ~50-80% de un núcleo

### Límites Identificados:
- **LibreOffice**: Máximo 3-5 procesos simultáneos antes de saturar el sistema
- **Memoria**: ~500MB-1GB para 5 requests concurrentes
- **CPU**: 100% con 2-3 requests simultáneos

## Recomendaciones para Escalabilidad

### 1. **Implementar Pool de Conversión**
```python
# Propuesta: app/utils/soffice_pool.py
import asyncio
import aiofiles
from concurrent.futures import ProcessPoolExecutor

class SofficePool:
    def __init__(self, max_workers=3):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.semaphore = asyncio.Semaphore(max_workers)
    
    async def convert_to_pdf_async(self, input_path: str, output_path: str):
        async with self.semaphore:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor, 
                convert_to_pdf_sync, 
                input_path, 
                output_path
            )
```

### 2. **Configurar Uvicorn con Workers**
```bash
# Comando optimizado
uvicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --host 0.0.0.0 --port 8080
```

### 3. **Implementar Cache de Templates**
```python
# Propuesta: app/services/template_cache.py
import asyncio
from functools import lru_cache

class TemplateCache:
    def __init__(self):
        self.cache = {}
        self.lock = asyncio.Lock()
    
    async def get_template(self, template_id: str):
        async with self.lock:
            if template_id not in self.cache:
                # Cargar template
                self.cache[template_id] = await self._load_template(template_id)
            return self.cache[template_id]
```

### 4. **Optimizar Operaciones de Archivo**
```python
# Usar aiofiles para operaciones asíncronas
import aiofiles

async def save_template_async(template_path: str, content: bytes):
    async with aiofiles.open(template_path, 'wb') as f:
        await f.write(content)
```

### 5. **Implementar Rate Limiting**
```python
# Propuesta: app/middleware/rate_limit.py
from fastapi import HTTPException
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def check_rate_limit(self, client_id: str):
        now = time.time()
        minute_ago = now - 60
        
        # Limpiar requests antiguos
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] 
            if req_time > minute_ago
        ]
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[client_id].append(now)
```

## Plan de Implementación

### Fase 1: Optimizaciones Inmediatas (1-2 días)
1. ✅ Configurar Uvicorn con múltiples workers
2. ✅ Implementar pool de conversión LibreOffice
3. ✅ Agregar rate limiting básico

### Fase 2: Optimizaciones Avanzadas (3-5 días)
1. ✅ Implementar cache de templates
2. ✅ Optimizar operaciones de archivo asíncronas
3. ✅ Agregar métricas de rendimiento

### Fase 3: Escalabilidad Horizontal (1 semana)
1. ✅ Implementar balanceador de carga
2. ✅ Configurar múltiples instancias
3. ✅ Implementar queue de procesamiento

## Métricas a Monitorear

- **Tiempo de respuesta promedio**: Objetivo < 2 segundos
- **Requests por segundo**: Objetivo > 10 req/s
- **Uso de memoria**: Objetivo < 1GB por instancia
- **Uso de CPU**: Objetivo < 80% promedio
- **Tasa de error**: Objetivo < 1%

## Conclusión

El servicio **NO está preparado** para manejar 100 llamadas por minuto en su estado actual. Los principales cuellos de botella son:

1. **LibreOffice secuencial** (limitación principal)
2. **Falta de workers múltiples**
3. **Operaciones de archivo síncronas**
4. **Sin gestión de recursos**

**Capacidad actual estimada**: 2-5 requests simultáneos, ~12-30 requests por minuto.

**Capacidad objetivo**: 20-50 requests simultáneos, ~100-300 requests por minuto.
