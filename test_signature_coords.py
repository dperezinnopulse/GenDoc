import requests
import json

# URL de la API
url = "http://localhost:8080/api/render"

# Datos de prueba
data = {
    "template_id": "4beba2ce11614d36bd066809e2f52115",
    "data": {
        "nombre": "Ana",
        "apellido": "Pérez"
    },
    "output_format": "image"
}

# Headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Hacer la petición
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        # Mostrar información de la imagen
        image_info = result.get("image_info", {})
        print(f"\n📊 Image Info:")
        print(f"  Width: {image_info.get('width')}")
        print(f"  Height: {image_info.get('height')}")
        print(f"  Original PDF Width: {image_info.get('original_pdf_width_points')}")
        print(f"  Original PDF Height: {image_info.get('original_pdf_height_points')}")
        print(f"  Scale X: {image_info.get('scale_x')}")
        print(f"  Scale Y: {image_info.get('scale_y')}")
        
        # Mostrar coordenadas de firma
        signatures = result.get("signatures", {})
        print(f"\n✍️  Signatures:")
        for key, coords in signatures.items():
            print(f"  {key}:")
            print(f"    x: {coords.get('x')}")
            print(f"    y: {coords.get('y')}")
            print(f"    width: {coords.get('width')}")
            print(f"    height: {coords.get('height')}")
            
            # Calcular posición relativa
            x_rel = coords.get('x', 0) / image_info.get('width', 1) * 100
            y_rel = coords.get('y', 0) / image_info.get('height', 1) * 100
            print(f"    Position: {x_rel:.1f}% from left, {y_rel:.1f}% from top")
        
        print(f"\n📏 Image size: {len(result.get('image_base64', ''))} characters (base64)")
        
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
