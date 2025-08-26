from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
import logging
from typing import Dict, List, Optional
import asyncio

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter para controlar el número de requests por cliente.
    """
    
    def __init__(self, requests_per_minute: int = 60, window_size: int = 60):
        """
        Inicializa el rate limiter.
        
        Args:
            requests_per_minute: Número máximo de requests por minuto
            window_size: Tamaño de la ventana de tiempo en segundos
        """
        self.requests_per_minute = requests_per_minute
        self.window_size = window_size
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = asyncio.Lock()
        logger.info(f"RateLimiter inicializado: {requests_per_minute} requests por {window_size} segundos")
    
    async def check_rate_limit(self, client_id: str) -> bool:
        """
        Verifica si el cliente ha excedido el límite de requests.
        
        Args:
            client_id: Identificador único del cliente
            
        Returns:
            True si el request está permitido, False si se excede el límite
        """
        async with self.lock:
            now = time.time()
            window_start = now - self.window_size
            
            # Limpiar requests antiguos
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id] 
                if req_time > window_start
            ]
            
            # Verificar límite
            if len(self.requests[client_id]) >= self.requests_per_minute:
                logger.warning(f"Rate limit excedido para cliente {client_id}")
                return False
            
            # Agregar request actual
            self.requests[client_id].append(now)
            return True
    
    def get_remaining_requests(self, client_id: str) -> int:
        """
        Obtiene el número de requests restantes para un cliente.
        
        Args:
            client_id: Identificador único del cliente
            
        Returns:
            Número de requests restantes
        """
        now = time.time()
        window_start = now - self.window_size
        
        # Limpiar requests antiguos
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] 
            if req_time > window_start
        ]
        
        return max(0, self.requests_per_minute - len(self.requests[client_id]))

# Instancia global del rate limiter
_rate_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """Obtiene la instancia global del rate limiter."""
    global _rate_limiter
    if _rate_limiter is None:
        # Usar configuración automática del servidor
        try:
            from ...server_config import server_config
            requests_per_minute = server_config.get_rate_limit()
        except ImportError:
            # Fallback si no está disponible
            import multiprocessing
            cpu_count = multiprocessing.cpu_count()
            requests_per_minute = 100 if cpu_count < 4 else 300
            
        _rate_limiter = RateLimiter(requests_per_minute=requests_per_minute, window_size=60)
    return _rate_limiter

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware de rate limiting para FastAPI.
    
    Args:
        request: Request de FastAPI
        call_next: Función para continuar con el siguiente middleware
        
    Returns:
        Response de FastAPI
    """
    # Solo aplicar rate limiting a endpoints de render
    if request.url.path.startswith("/api/render"):
        # Obtener identificador del cliente (IP + User-Agent)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = f"{client_ip}:{user_agent}"
        
        rate_limiter = get_rate_limiter()
        
        # Verificar rate limit
        if not await rate_limiter.check_rate_limit(client_id):
            remaining_time = rate_limiter.window_size
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Demasiadas requests. Intenta de nuevo en {remaining_time} segundos.",
                    "retry_after": remaining_time
                },
                headers={
                    "Retry-After": str(remaining_time),
                    "X-RateLimit-Limit": str(rate_limiter.requests_per_minute),
                    "X-RateLimit-Remaining": str(rate_limiter.get_remaining_requests(client_id)),
                    "X-RateLimit-Reset": str(int(time.time() + remaining_time))
                }
            )
        
        # Agregar headers de rate limit a la respuesta
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(rate_limiter.get_remaining_requests(client_id))
        return response
    
    # Para otros endpoints, continuar sin rate limiting
    return await call_next(request)
