import asyncio
import aiohttp
import time
import json
from concurrent.futures import ThreadPoolExecutor
import threading
from datetime import datetime

# Configuración de la prueba
BASE_URL = "http://localhost:8080"
TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115"  # Template existente
TOTAL_REQUESTS = 100
CONCURRENT_REQUESTS = 10
TEST_DURATION = 60  # segundos

# Datos de prueba
TEST_DATA = {
    "nombre": "Ana",
    "apellido": "Pérez",
    "documento": "12345678A",
    "fecha": "2025-01-15",
    "curso": "Matemáticas"
}

class ConcurrencyTester:
    def __init__(self):
        self.results = []
        self.lock = threading.Lock()
        self.start_time = None
        self.completed_requests = 0
        self.failed_requests = 0
        
    def log_result(self, request_id, status_code, response_time, success, error=None):
        with self.lock:
            self.results.append({
                'request_id': request_id,
                'status_code': status_code,
                'response_time': response_time,
                'success': success,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
            if success:
                self.completed_requests += 1
            else:
                self.failed_requests += 1
    
    async def make_request(self, session, request_id):
        """Realiza una petición individual al endpoint /api/render"""
        start_time = time.time()
        try:
            payload = {
                "template_id": TEMPLATE_ID,
                "data": TEST_DATA
            }
            
            async with session.post(
                f"{BASE_URL}/api/render",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    content = await response.read()
                    self.log_result(request_id, response.status, response_time, True)
                    print(f"✅ Request {request_id}: {response.status} - {response_time:.2f}s - {len(content)} bytes")
                else:
                    error_text = await response.text()
                    self.log_result(request_id, response.status, response_time, False, error_text)
                    print(f"❌ Request {request_id}: {response.status} - {response_time:.2f}s - {error_text}")
                    
        except Exception as e:
            response_time = time.time() - start_time
            self.log_result(request_id, 0, response_time, False, str(e))
            print(f"💥 Request {request_id}: Error - {response_time:.2f}s - {str(e)}")
    
    async def run_concurrent_test(self):
        """Ejecuta la prueba de concurrencia"""
        print(f"🚀 Iniciando prueba de concurrencia:")
        print(f"   - Total requests: {TOTAL_REQUESTS}")
        print(f"   - Concurrent requests: {CONCURRENT_REQUESTS}")
        print(f"   - Template ID: {TEMPLATE_ID}")
        print(f"   - Base URL: {BASE_URL}")
        print()
        
        self.start_time = time.time()
        
        # Configurar sesión HTTP con límites de conexión
        connector = aiohttp.TCPConnector(
            limit=CONCURRENT_REQUESTS * 2,  # Límite de conexiones
            limit_per_host=CONCURRENT_REQUESTS * 2,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Crear semáforo para limitar concurrencia
            semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
            
            async def limited_request(request_id):
                async with semaphore:
                    await self.make_request(session, request_id)
            
            # Crear todas las tareas
            tasks = [limited_request(i) for i in range(TOTAL_REQUESTS)]
            
            # Ejecutar todas las tareas
            await asyncio.gather(*tasks)
        
        self.print_results()
    
    def print_results(self):
        """Imprime los resultados de la prueba"""
        total_time = time.time() - self.start_time
        
        if not self.results:
            print("❌ No se obtuvieron resultados")
            return
        
        # Calcular estadísticas
        response_times = [r['response_time'] for r in self.results if r['success']]
        status_codes = [r['status_code'] for r in self.results]
        
        print("\n" + "="*60)
        print("📊 RESULTADOS DE LA PRUEBA DE CONCURRENCIA")
        print("="*60)
        print(f"⏱️  Tiempo total: {total_time:.2f} segundos")
        print(f"📈 Requests completados: {self.completed_requests}")
        print(f"❌ Requests fallidos: {self.failed_requests}")
        print(f"📊 Tasa de éxito: {(self.completed_requests/TOTAL_REQUESTS)*100:.1f}%")
        
        if response_times:
            print(f"⚡ Tiempo de respuesta promedio: {sum(response_times)/len(response_times):.2f}s")
            print(f"🚀 Tiempo de respuesta mínimo: {min(response_times):.2f}s")
            print(f"🐌 Tiempo de respuesta máximo: {max(response_times):.2f}s")
            print(f"📈 Requests por segundo: {self.completed_requests/total_time:.1f} req/s")
        
        # Análisis de códigos de estado
        status_counts = {}
        for status in status_codes:
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\n📋 Códigos de estado:")
        for status, count in status_counts.items():
            print(f"   {status}: {count} requests")
        
        # Análisis de errores
        errors = [r for r in self.results if not r['success']]
        if errors:
            print(f"\n❌ Errores encontrados:")
            error_types = {}
            for error in errors:
                error_msg = error.get('error', 'Unknown')
                error_types[error_msg] = error_types.get(error_msg, 0) + 1
            
            for error_msg, count in error_types.items():
                print(f"   {error_msg}: {count} veces")
        
        print("\n" + "="*60)
        
        # Guardar resultados en archivo
        with open('concurrency_test_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'test_config': {
                    'total_requests': TOTAL_REQUESTS,
                    'concurrent_requests': CONCURRENT_REQUESTS,
                    'template_id': TEMPLATE_ID,
                    'base_url': BASE_URL
                },
                'results': self.results,
                'summary': {
                    'total_time': total_time,
                    'completed_requests': self.completed_requests,
                    'failed_requests': self.failed_requests,
                    'success_rate': (self.completed_requests/TOTAL_REQUESTS)*100,
                    'avg_response_time': sum(response_times)/len(response_times) if response_times else 0,
                    'requests_per_second': self.completed_requests/total_time
                }
            }, f, indent=2, ensure_ascii=False)
        
        print("💾 Resultados guardados en 'concurrency_test_results.json'")

async def main():
    """Función principal"""
    tester = ConcurrencyTester()
    await tester.run_concurrent_test()

if __name__ == "__main__":
    asyncio.run(main())
