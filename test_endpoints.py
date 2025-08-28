#!/usr/bin/env python3
import requests

def test_endpoints():
    print("🔍 Verificando endpoints disponibles...")
    
    base_url = "https://1aca264c0a2c.ngrok-free.app"
    
    # Lista de endpoints a probar
    endpoints = [
        "/",
        "/admin",
        "/api/templates",
        "/api/render/test",
        "/docs",
        "/openapi.json"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Probando: {base_url}{endpoint}")
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                print(f"   ✅ Disponible")
                if 'application/json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"   📋 Items: {len(data)}")
                        elif isinstance(data, dict):
                            print(f"   📋 Keys: {list(data.keys())[:5]}")
                    except:
                        pass
            else:
                print(f"   ❌ No disponible")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_endpoints()




