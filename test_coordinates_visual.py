#!/usr/bin/env python3
"""
Script para visualizar las coordenadas calculadas vs las esperadas
"""

import requests
import json
import base64
from PIL import Image, ImageDraw, ImageFont
import io

def visualize_coordinates():
    """Visualizar las coordenadas calculadas vs las esperadas"""
    
    template_id = "4beba2ce11614d36bd066809e2f52115"
    base_url = "http://localhost:8080"
    
    print("🎨 Visualizando coordenadas...")
    print("=" * 50)
    
    # Obtener la imagen generada
    try:
        data = {
            "template_id": template_id,
            "data": {
                "nombre": "Ana",
                "apellido": "Pérez"
            },
            "output_format": "image"
        }
        
        response = requests.post(f"{base_url}/api/render", json=data)
        if response.status_code == 200:
            result = response.json()
            
            # Decodificar la imagen
            image_base64 = result.get("image_base64", "")
            image_bytes = base64.b64decode(image_base64)
            
            # Cargar la imagen
            img = Image.open(io.BytesIO(image_bytes))
            draw = ImageDraw.Draw(img)
            
            # Coordenadas calculadas por el sistema
            calculated_x = 666
            calculated_y = 1396
            
            # Coordenadas esperadas (según ChatGPT)
            expected_x = 446
            expected_y = 1464
            
            # Dibujar marcadores para las coordenadas calculadas (rojo)
            draw.ellipse([calculated_x-10, calculated_y-10, calculated_x+10, calculated_y+10], fill='red', outline='red')
            draw.text((calculated_x+15, calculated_y-10), "CALCULADO", fill='red')
            
            # Dibujar marcadores para las coordenadas esperadas (verde)
            draw.ellipse([expected_x-10, expected_y-10, expected_x+10, expected_y+10], fill='green', outline='green')
            draw.text((expected_x+15, expected_y-10), "ESPERADO", fill='green')
            
            # Dibujar línea entre ambos puntos
            draw.line([calculated_x, calculated_y, expected_x, expected_y], fill='blue', width=2)
            
            # Mostrar información
            print(f"📏 Dimensiones imagen: {img.size[0]} x {img.size[1]}")
            print(f"📍 Coordenadas calculadas: ({calculated_x}, {calculated_y})")
            print(f"📍 Coordenadas esperadas: ({expected_x}, {expected_y})")
            print(f"📐 Diferencia: ({expected_x - calculated_x}, {expected_y - calculated_y})")
            
            # Guardar imagen con marcadores
            img.save("coordinates_visualization.png")
            print(f"✅ Imagen guardada como 'coordinates_visualization.png'")
            
            # También guardar la imagen original para comparar
            original_img = Image.open(io.BytesIO(image_bytes))
            original_img.save("original_image.png")
            print(f"✅ Imagen original guardada como 'original_image.png'")
            
        else:
            print(f"❌ Error: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "=" * 50)
    print("📋 Instrucciones:")
    print("   1. Abre 'coordinates_visualization.png'")
    print("   2. El punto ROJO muestra las coordenadas calculadas por el sistema")
    print("   3. El punto VERDE muestra las coordenadas esperadas")
    print("   4. La línea AZUL conecta ambos puntos")
    print("   5. Compara con 'original_image.png' para ver la imagen sin marcadores")

if __name__ == "__main__":
    visualize_coordinates()
