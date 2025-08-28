#!/usr/bin/env python3
import requests
import json

def test_correct_api():
    print("🧪 Probando API de GenDoc con endpoint correcto...")
    
    # URL de ngrok
    GENDOC_URL = "https://1aca264c0a2c.ngrok-free.app"
    
    # Datos correctos para el endpoint
    data = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-25",
            "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
        }
    }
    
    print(f"📡 URL: {GENDOC_URL}/api/render")
    print(f"🆔 Template ID: {data['template_id']}")
    print(f"📊 Datos: {json.dumps(data['data'], indent=2)}")
    
    try:
        print("\n📤 Enviando request...")
        response = requests.post(
            f"{GENDOC_URL}/api/render",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        print(f"🎨 Content Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            # Guardar el PDF
            filename = "test_correct_output.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ PDF generado exitosamente: {filename}")
            print(f"📄 Tamaño del archivo: {len(response.content)} bytes")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La request tardó demasiado")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_correct_api()




