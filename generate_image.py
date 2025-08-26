#!/usr/bin/env python3
"""
Script para generar la imagen con la llamada correcta.
"""

import requests
import json
import time

def generate_image():
    """Genera la imagen con la llamada correcta."""
    print("🖼️  GENERANDO IMAGEN CON LLAMADA CORRECTA")
    print("=" * 50)
    
    # Llamada correcta
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "output_format": "image"  # ← FORMATO CORRECTO
    }
    
    print("📤 Enviando petición...")
    print(f"🖼️  Output Format: {payload['output_format']}")
    print(f"📝 Datos: {json.dumps(payload['data'], indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:8080/api/render",
            json=payload,
            timeout=60
        )
        
        print(f"\n📊 Status: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Tamaño: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'image/png' in content_type:
                print("✅ ¡ÉXITO! Imagen generada correctamente")
                
                # Guardar imagen
                filename = f"imagen_generada_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"💾 Imagen guardada como: {filename}")
                
                # Verificar formato PNG
                if response.content.startswith(b'\x89PNG\r\n\x1a\n'):
                    print("✅ Formato PNG válido")
                else:
                    print("⚠️  Formato PNG no válido")
                
                print(f"\n🎯 RESUMEN:")
                print(f"   ✅ Status: 200 OK")
                print(f"   ✅ Content-Type: image/png")
                print(f"   ✅ Tamaño: {len(response.content)} bytes")
                print(f"   ✅ Archivo: {filename}")
                
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
    generate_image()
