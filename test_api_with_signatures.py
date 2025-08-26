#!/usr/bin/env python3
"""
Script para probar la API con coordenadas de firma.
"""

import requests
import json
import base64
from PIL import Image
import io

def test_api_with_signatures():
    """Prueba la API para obtener imagen con coordenadas de firma."""
    print("🔄 Probando API con coordenadas de firma")
    print("=" * 50)
    
    # URL de la API
    url = "https://a83581047e68.ngrok-free.app/api/render"
    
    # Datos de prueba
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "output_format": "image"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"📄 Template ID: {payload['template_id']}")
    print(f"📝 Datos: {payload['data']}")
    print(f"🖼️  Formato: {payload['output_format']}")
    
    try:
        # Hacer la llamada a la API
        print("\n🔄 Haciendo llamada a la API...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Parsear la respuesta JSON
            result = response.json()
            
            print("\n✅ Respuesta exitosa!")
            print(f"📏 Tamaño de imagen base64: {len(result.get('image_base64', ''))} caracteres")
            
            # Verificar coordenadas de firma
            signatures = result.get('signatures', {})
            print(f"✍️  Campos de firma encontrados: {len(signatures)}")
            
            for key, coords in signatures.items():
                print(f"   - {key}: x={coords['x']}, y={coords['y']}, width={coords['width']}, height={coords['height']}")
            
            # Decodificar y guardar la imagen
            if 'image_base64' in result:
                image_data = base64.b64decode(result['image_base64'])
                filename = f"test_api_signature_{payload['template_id']}.png"
                
                with open(filename, 'wb') as f:
                    f.write(image_data)
                print(f"💾 Imagen guardada como: {filename}")
                
                # Verificar que es una imagen válida
                try:
                    img = Image.open(io.BytesIO(image_data))
                    print(f"🖼️  Imagen válida: {img.size[0]}x{img.size[1]} píxeles")
                except Exception as e:
                    print(f"⚠️  Error al abrir imagen: {e}")
            
            return True
            
        else:
            print(f"❌ Error en la API: {response.status_code}")
            print(f"📋 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

def test_api_pdf_format():
    """Prueba la API en formato PDF para comparar."""
    print("\n🔄 Probando API en formato PDF")
    print("=" * 30)
    
    url = "https://a83581047e68.ngrok-free.app/api/render"
    
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "output_format": "pdf"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ PDF generado correctamente")
            return True
        else:
            print(f"❌ Error en PDF: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Probar formato imagen con coordenadas de firma
    success1 = test_api_with_signatures()
    
    # Probar formato PDF
    success2 = test_api_pdf_format()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   🖼️  Formato imagen: {'✅ Éxito' if success1 else '❌ Fallo'}")
    print(f"   📄 Formato PDF: {'✅ Éxito' if success2 else '❌ Fallo'}")
    
    if success1 and success2:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    else:
        print("\n⚠️  Algunas pruebas fallaron.")
