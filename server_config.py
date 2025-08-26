#!/usr/bin/env python3
"""
Configuración de servidor para diferentes tipos de hardware.
"""

import multiprocessing
import os

class ServerConfig:
    """Configuración automática basada en el hardware del servidor."""
    
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.memory_gb = self._get_memory_gb()
        self.server_type = self._determine_server_type()
        
    def _get_memory_gb(self):
        """Obtiene la memoria RAM en GB."""
        try:
            import psutil
            return psutil.virtual_memory().total / (1024**3)
        except ImportError:
            # Fallback si psutil no está disponible
            return 8  # Asumir 8GB por defecto
    
    def _determine_server_type(self):
        """Determina el tipo de servidor basado en recursos."""
        if self.cpu_count >= 16 and self.memory_gb >= 32:
            return "enterprise"
        elif self.cpu_count >= 8 and self.memory_gb >= 16:
            return "production"
        elif self.cpu_count >= 4 and self.memory_gb >= 8:
            return "standard"
        else:
            return "development"
    
    def get_uvicorn_workers(self):
        """Número óptimo de workers Uvicorn."""
        configs = {
            "enterprise": self.cpu_count - 2,  # 14+ workers
            "production": self.cpu_count - 1,  # 7+ workers
            "standard": self.cpu_count,        # 4+ workers
            "development": max(2, self.cpu_count)
        }
        return configs.get(self.server_type, 2)
    
    def get_soffice_workers(self):
        """Número óptimo de workers LibreOffice."""
        configs = {
            "enterprise": self.cpu_count - 1,  # 15+ workers
            "production": self.cpu_count,      # 8+ workers
            "standard": self.cpu_count,        # 4+ workers
            "development": min(3, self.cpu_count)
        }
        return configs.get(self.server_type, 2)
    
    def get_rate_limit(self):
        """Rate limit por minuto."""
        configs = {
            "enterprise": 1000,  # 1000 req/min
            "production": 500,   # 500 req/min
            "standard": 300,     # 300 req/min
            "development": 100   # 100 req/min
        }
        return configs.get(self.server_type, 100)
    
    def get_max_concurrent_requests(self):
        """Máximo de requests concurrentes."""
        configs = {
            "enterprise": 50,   # 50 simultáneos
            "production": 25,   # 25 simultáneos
            "standard": 15,     # 15 simultáneos
            "development": 10   # 10 simultáneos
        }
        return configs.get(self.server_type, 10)
    
    def get_timeout_seconds(self):
        """Timeout para conversiones."""
        configs = {
            "enterprise": 60,   # 60 segundos
            "production": 45,   # 45 segundos
            "standard": 30,     # 30 segundos
            "development": 30   # 30 segundos
        }
        return configs.get(self.server_type, 30)
    
    def print_config(self):
        """Imprime la configuración actual."""
        print("🔧 CONFIGURACIÓN DEL SERVIDOR")
        print("=" * 50)
        print(f"💻 CPU Cores: {self.cpu_count}")
        print(f"🧠 Memoria RAM: {self.memory_gb:.1f} GB")
        print(f"🏷️  Tipo de servidor: {self.server_type.upper()}")
        print()
        print("⚙️  Configuración optimizada:")
        print(f"   📊 Workers Uvicorn: {self.get_uvicorn_workers()}")
        print(f"   🔄 Workers LibreOffice: {self.get_soffice_workers()}")
        print(f"   🚦 Rate Limit: {self.get_rate_limit()} req/min")
        print(f"   🔀 Requests concurrentes: {self.get_max_concurrent_requests()}")
        print(f"   ⏱️  Timeout: {self.get_timeout_seconds()}s")
        print()
        
        # Proyección de rendimiento
        workers = self.get_uvicorn_workers()
        soffice_workers = self.get_soffice_workers()
        
        # Estimación de throughput
        if self.server_type == "enterprise":
            estimated_throughput = "1000+ req/min"
            estimated_concurrency = "50+ simultáneos"
        elif self.server_type == "production":
            estimated_throughput = "500+ req/min"
            estimated_concurrency = "25+ simultáneos"
        elif self.server_type == "standard":
            estimated_throughput = "300+ req/min"
            estimated_concurrency = "15+ simultáneos"
        else:
            estimated_throughput = "100+ req/min"
            estimated_concurrency = "10+ simultáneos"
        
        print("📈 Proyección de rendimiento:")
        print(f"   🚀 Throughput esperado: {estimated_throughput}")
        print(f"   🔄 Concurrencia esperada: {estimated_concurrency}")
        print(f"   ⚡ Tiempo promedio: < 0.3s")
        print("=" * 50)

# Instancia global
server_config = ServerConfig()

if __name__ == "__main__":
    server_config.print_config()
