#!/usr/bin/env python3
import requests
import base64
from io import BytesIO
from reportlab.lib.utils import ImageReader

def test_image_processing():
    print("🔍 Debuggeando procesamiento de imagen...")
    
    # URL de prueba
    url = "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
    
    try:
        print(f"📥 Descargando: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Content-Length: {len(response.content)} bytes")
        print(f"🎨 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ Descarga exitosa")
            
            # Verificar si ReportLab puede leer la imagen
            try:
                img_reader = ImageReader(BytesIO(response.content))
                print(f"✅ ReportLab puede leer la imagen")
                print(f"📐 Dimensiones: {img_reader.getSize()}")
                return True
            except Exception as e:
                print(f"❌ ReportLab no puede leer la imagen: {e}")
                return False
        else:
            print(f"❌ Error en la descarga: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_image_processing()
