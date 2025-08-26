#!/usr/bin/env python3
"""
Ejemplo de llamada a la API para obtener imagen con coordenadas de firma.
"""

import requests
import base64
from PIL import Image
import io

def llamada_api_imagen_con_firmas():
    """
    Ejemplo de llamada a la API para generar imagen con coordenadas de firma.
    """
    
    # URL de la API
    url = "https://a83581047e68.ngrok-free.app/api/render"
    
    # Datos de la petición
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "output_format": "image"  # ← Aquí especificamos que queremos imagen
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🔄 Llamando a la API...")
    
    # Hacer la petición
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        # Parsear la respuesta
        result = response.json()
        
        print("✅ Respuesta exitosa!")
        
        # Obtener la imagen en base64
        image_base64 = result.get('image_base64', '')
        print(f"📏 Tamaño de imagen: {len(image_base64)} caracteres base64")
        
        # Obtener las coordenadas de firma
        signatures = result.get('signatures', {})
        print(f"✍️  Campos de firma encontrados: {len(signatures)}")
        
        # Mostrar las coordenadas de cada campo de firma
        for field_name, coords in signatures.items():
            print(f"   📍 {field_name}:")
            print(f"      x: {coords['x']}")
            print(f"      y: {coords['y']}")
            print(f"      width: {coords['width']}")
            print(f"      height: {coords['height']}")
        
        # Decodificar y guardar la imagen
        if image_base64:
            image_data = base64.b64decode(image_base64)
            filename = "documento_generado.png"
            
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"💾 Imagen guardada como: {filename}")
            
            # Verificar que es una imagen válida
            try:
                img = Image.open(io.BytesIO(image_data))
                print(f"🖼️  Imagen válida: {img.size[0]}x{img.size[1]} píxeles")
            except Exception as e:
                print(f"⚠️  Error al verificar imagen: {e}")
        
        return result
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"📋 Respuesta: {response.text}")
        return None

if __name__ == "__main__":
    print("🚀 Ejemplo de llamada a la API GenDoc")
    print("=" * 50)
    
    result = llamada_api_imagen_con_firmas()
    
    if result:
        print("\n🎉 ¡Llamada exitosa!")
        print("\n📋 Resumen de la respuesta:")
        print(f"   - Imagen: {'✅' if 'image_base64' in result else '❌'}")
        print(f"   - Coordenadas de firma: {'✅' if 'signatures' in result else '❌'}")
        print(f"   - Número de campos de firma: {len(result.get('signatures', {}))}")
    else:
        print("\n❌ La llamada falló")
