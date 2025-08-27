#!/usr/bin/env python3
"""
Script para debuggear las coordenadas de firma
"""

import requests
import json
import base64
from PIL import Image
import io

def debug_signature_coordinates():
    """Debuggear las coordenadas de firma paso a paso"""
    
    template_id = "4beba2ce11614d36bd066809e2f52115"
    base_url = "http://localhost:8080"
    
    print("🔍 Debuggeando coordenadas de firma...")
    print("=" * 60)
    
    # 1. Obtener datos del template
    print("\n📋 1. Obteniendo datos del template:")
    try:
        response = requests.get(f"{base_url}/api/templates/{template_id}")
        if response.status_code == 200:
            template_data = response.json()
            print(f"✅ Template obtenido: {template_data.get('name', 'Sin nombre')}")
            
            # Buscar coordenadas de firma en el mapping
            mapping = template_data.get('mapping', {})
            positions = mapping.get('_positions', {})
            
            print(f"\n📍 Posiciones encontradas:")
            for field_name, coords in positions.items():
                print(f"   {field_name}: {coords}")
                
                if "firma" in field_name.lower():
                    print(f"   ⭐ CAMPO DE FIRMA DETECTADO")
                    print(f"   📍 Coordenadas originales: x={coords[0]}, y={coords[1]}")
        else:
            print(f"❌ Error obteniendo template: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error obteniendo template: {e}")
        return
    
    # 2. Probar renderizado con imagen
    print("\n🖼️  2. Probando renderizado con imagen:")
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
            
            # Mostrar información de la imagen
            image_info = result.get("image_info", {})
            print(f"✅ Imagen generada:")
            print(f"   📏 Dimensiones imagen: {image_info.get('width')} x {image_info.get('height')}")
            print(f"   📏 Dimensiones PDF original: {image_info.get('original_pdf_width_points')} x {image_info.get('original_pdf_height_points')}")
            print(f"   📐 Factores de escala: x={image_info.get('scale_x'):.4f}, y={image_info.get('scale_y'):.4f}")
            
            # Mostrar coordenadas de firma calculadas
            signatures = result.get("signatures", {})
            print(f"\n✍️  Coordenadas de firma calculadas:")
            for key, coords in signatures.items():
                print(f"   {key}:")
                print(f"      x: {coords.get('x')}")
                print(f"      y: {coords.get('y')}")
                print(f"      width: {coords.get('width')}")
                print(f"      height: {coords.get('height')}")
                
                # Calcular posición relativa
                x_rel = coords.get('x', 0) / image_info.get('width', 1) * 100
                y_rel = coords.get('y', 0) / image_info.get('height', 1) * 100
                print(f"      Posición relativa: {x_rel:.1f}% desde izquierda, {y_rel:.1f}% desde arriba")
                
                # Verificar si las coordenadas coinciden con las esperadas
                expected_x = 446
                expected_y = 1464
                x_diff = abs(coords.get('x', 0) - expected_x)
                y_diff = abs(coords.get('y', 0) - expected_y)
                
                print(f"      📊 Diferencia con coordenadas esperadas:")
                print(f"         Esperado: x={expected_x}, y={expected_y}")
                print(f"         Calculado: x={coords.get('x')}, y={coords.get('y')}")
                print(f"         Diferencia: x={x_diff}, y={y_diff}")
                
                if x_diff < 10 and y_diff < 10:
                    print(f"      ✅ Coordenadas coinciden (diferencia < 10 píxeles)")
                else:
                    print(f"      ❌ Coordenadas NO coinciden (diferencia > 10 píxeles)")
        else:
            print(f"❌ Error en renderizado: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error en renderizado: {e}")
        return
    
    # 3. Guardar imagen para inspección manual
    print("\n💾 3. Guardando imagen para inspección manual:")
    try:
        image_base64 = result.get("image_base64", "")
        if image_base64:
            image_bytes = base64.b64decode(image_base64)
            with open("debug_signature_image.png", "wb") as f:
                f.write(image_bytes)
            print(f"✅ Imagen guardada como 'debug_signature_image.png'")
            print(f"   📏 Tamaño: {len(image_bytes)} bytes")
        else:
            print(f"❌ No se pudo obtener la imagen")
    except Exception as e:
        print(f"❌ Error guardando imagen: {e}")
    
    print("\n" + "=" * 60)
    print("📋 Resumen del debug:")
    print("   • Se obtuvieron las coordenadas del template")
    print("   • Se calculó el escalado de PDF a imagen")
    print("   • Se compararon con las coordenadas esperadas")
    print("   • Se guardó la imagen para inspección manual")

if __name__ == "__main__":
    debug_signature_coordinates()
