#!/usr/bin/env python3
import requests
import json

def check_templates():
    print("🔍 Verificando plantillas disponibles...")
    
    base_url = "https://1aca264c0a2c.ngrok-free.app"
    
    try:
        # Listar plantillas
        print(f"📡 Obteniendo plantillas desde: {base_url}/api/templates")
        response = requests.get(f"{base_url}/api/templates", timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"🎨 Content Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            templates = response.json()
            print(f"📋 Plantillas encontradas: {len(templates)}")
            
            for template in templates:
                print(f"  - ID: {template.get('id', 'N/A')}")
                print(f"    Nombre: {template.get('name', 'N/A')}")
                print(f"    Tipo: {template.get('kind', 'N/A')}")
                print(f"    Creado: {template.get('created_at', 'N/A')}")
                print()
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_templates()



