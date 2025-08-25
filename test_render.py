#!/usr/bin/env python3
import requests
import json

def test_render():
    print("🧪 Probando render con imagen...")
    
    url = "http://localhost:8080/admin/templates/4beba2ce11614d36bd066809e2f52115/test_render"
    
    data = {
        "Alumno": "Diego Pérez",
        "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
    }
    
    try:
        print(f"📤 Enviando datos: {json.dumps(data, indent=2)}")
        response = requests.post(url, data={"data_json": json.dumps(data)}, timeout=30)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📏 Content-Length: {len(response.content)} bytes")
        print(f"🎨 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ Render exitoso")
            # Guardar el PDF para verificar
            with open("test_output.pdf", "wb") as f:
                f.write(response.content)
            print("💾 PDF guardado como test_output.pdf")
        else:
            print(f"❌ Error en render: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_render()
