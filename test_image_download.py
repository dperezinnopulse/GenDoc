#!/usr/bin/env python3
import requests
import base64
from io import BytesIO

def test_image_download():
    print("🧪 Probando descarga de imagen...")
    
    # URL de prueba
    url = "https://www.innopulse.es/img/logo.svg"
    
    try:
        print(f"📥 Descargando: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Content-Length: {len(response.content)} bytes")
        print(f"🎨 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ Descarga exitosa")
            
            # Verificar si es una imagen válida
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type or 'svg' in content_type:
                print("✅ Contenido parece ser una imagen válida")
                
                # Crear data URL
                if 'svg' in content_type:
                    # Para SVG, usar como texto
                    svg_content = response.text
                    data_url = f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"
                else:
                    # Para otras imágenes, usar bytes
                    data_url = f"data:{content_type};base64,{base64.b64encode(response.content).decode()}"
                
                print(f"🔗 Data URL generada (primeros 100 chars): {data_url[:100]}...")
                return True
            else:
                print("❌ El contenido no parece ser una imagen")
                print(f"📄 Primeros 200 caracteres: {response.text[:200]}")
                return False
        else:
            print(f"❌ Error en la descarga: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_image_download()
