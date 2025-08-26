#!/usr/bin/env python3
"""
Script de prueba simple para verificar la funcionalidad de imagen.
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8080"
TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115"

# Datos de prueba
TEST_DATA = {
    "nombre": "Ana",
    "apellido": "Pérez"
}

def test_image_output():
    """Prueba la salida en formato imagen."""
    print("🔄 Probando salida imagen...")
    
    payload = {
        "template_id": TEMPLATE_ID,
        "data": TEST_DATA,
        "output_format": "image"
    }
    
    print(f"📤 Payload enviado: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=30
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image/png' in content_type:
                print("✅ Imagen generada correctamente")
                
                # Guardar imagen para verificación
                with open('test_image.png', 'wb') as f:
                    f.write(response.content)
                print("   💾 Imagen guardada como 'test_image.png'")
                return True
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                print(f"   📝 Primeros 100 bytes: {response.content[:100]}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

if __name__ == "__main__":
    test_image_output()
