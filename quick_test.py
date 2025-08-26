#!/usr/bin/env python3
"""
Prueba rápida de la funcionalidad de imagen.
"""

import requests
import json
import time

def quick_image_test():
    """Prueba rápida de generación de imagen."""
    print("🖼️  PRUEBA RÁPIDA DE GENERACIÓN DE IMAGEN")
    print("=" * 40)
    
    # Datos de prueba
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "nombre": "Ana",
            "apellido": "Pérez",
            "documento": "12345678A",
            "fecha": "2025-01-15",
            "curso": "Matemáticas"
        },
        "output_format": "image"
    }
    
    print("📤 Enviando petición...")
    print(f"🖼️  Output Format: {payload['output_format']}")
    
    try:
        response = requests.post(
            "http://localhost:8080/api/render",
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'image/png' in content_type:
                print("✅ ¡ÉXITO! Imagen generada correctamente")
                
                # Guardar imagen
                filename = f"quick_test_image_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"💾 Guardada como: {filename}")
                
                # Verificar formato PNG
                if response.content.startswith(b'\x89PNG\r\n\x1a\n'):
                    print("✅ Formato PNG válido")
                else:
                    print("⚠️  Formato PNG no válido")
                
                return True
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_image_test()
