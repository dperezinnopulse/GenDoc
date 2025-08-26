#!/usr/bin/env python3
"""
Script para iniciar el servidor GenDoc con optimizaciones de concurrencia.
"""

import subprocess
import sys
import os
import multiprocessing

def get_optimal_workers():
    """Calcula el número óptimo de workers basado en CPU cores."""
    # Usar configuración automática del servidor
    try:
        from server_config import server_config
        return server_config.get_uvicorn_workers()
    except ImportError:
        # Fallback si no está disponible
        cpu_count = multiprocessing.cpu_count()
        if cpu_count >= 8:
            return cpu_count - 1
        elif cpu_count >= 4:
            return cpu_count
        else:
            return max(2, cpu_count)

def main():
    """Función principal para iniciar el servidor optimizado."""
    
    # Configuración optimizada
    workers = get_optimal_workers()
    host = "0.0.0.0"
    port = 8080
    
    print("🚀 Iniciando GenDoc Service con optimizaciones de concurrencia")
    print(f"📊 Workers: {workers}")
    print(f"🌐 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"💻 CPU Cores disponibles: {multiprocessing.cpu_count()}")
    print()
    
    # Comando optimizado
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--workers", str(workers),
        "--worker-class", "uvicorn.workers.UvicornWorker",
        "--host", host,
        "--port", str(port),
        "--log-level", "info"
    ]
    
    print(f"📝 Comando: {' '.join(cmd)}")
    print()
    print("🔄 Iniciando servidor...")
    print("=" * 60)
    
    try:
        # Ejecutar el servidor
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
