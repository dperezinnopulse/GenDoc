#!/usr/bin/env python3
import requests

def test_download():
    print("🧪 Probando descarga de imagen...")
    
    url = "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
    
    try:
        print(f"📥 Descargando: {url}")
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Content-Length: {len(response.content)} bytes")
        print(f"🎨 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ Descarga exitosa")
            # Guardar la imagen para verificar
            with open("test_image.png", "wb") as f:
                f.write(response.content)
            print("💾 Imagen guardada como test_image.png")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_download()
