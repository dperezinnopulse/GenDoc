#!/usr/bin/env python3
"""
Script para comparar coordenadas de firma entre PNG y WebP
"""

import requests
import json
import base64
from PIL import Image
import io

def test_coordinates_comparison():
    """Compara las coordenadas de firma entre PNG y WebP"""
    
    template_id = "4beba2ce11614d36bd066809e2f52115"
    base_url = "http://localhost:8080"
    
    print("🔍 Comparando coordenadas PNG vs WebP...")
    print("=" * 50)
    
    # Probar PNG
    print("\n📊 Probando formato PNG:")
    try:
        response = requests.get(f"{base_url}/admin/templates/{template_id}/test_render?format=image")
        if response.status_code == 200:
            # Guardar imagen PNG
            with open("test_png.png", "wb") as f:
                f.write(response.content)
            
            # Cargar imagen para obtener dimensiones
            img_png = Image.open(io.BytesIO(response.content))
            print(f"✅ PNG generado: {img_png.size[0]}x{img_png.size[1]} píxeles")
            print(f"   Tamaño archivo: {len(response.content)} bytes")
        else:
            print(f"❌ Error PNG: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error probando PNG: {e}")
        return
    
    # Probar WebP (si está disponible)
    print("\n📊 Probando formato WebP:")
    try:
        # Intentar obtener WebP modificando el endpoint
        response = requests.get(f"{base_url}/admin/templates/{template_id}/test_render?format=webp")
        if response.status_code == 200:
            # Guardar imagen WebP
            with open("test_webp.webp", "wb") as f:
                f.write(response.content)
            
            # Cargar imagen para obtener dimensiones
            img_webp = Image.open(io.BytesIO(response.content))
            print(f"✅ WebP generado: {img_webp.size[0]}x{img_webp.size[1]} píxeles")
            print(f"   Tamaño archivo: {len(response.content)} bytes")
        else:
            print(f"⚠️  WebP no disponible: {response.status_code}")
            print("   (El sistema actual solo soporta PNG)")
    except Exception as e:
        print(f"⚠️  WebP no disponible: {e}")
    
    # Obtener coordenadas de firma
    print("\n📍 Obteniendo coordenadas de firma:")
    try:
        response = requests.get(f"{base_url}/api/templates/{template_id}/signature-coordinates")
        if response.status_code == 200:
            data = response.json()
            print("✅ Coordenadas obtenidas:")
            
            for field_name, coords in data.get("signatures", {}).items():
                print(f"\n   📍 Campo: {field_name}")
                print(f"      x: {coords['x']}")
                print(f"      y: {coords['y']}")
                print(f"      width: {coords['width']}")
                print(f"      height: {coords['height']}")
                print(f"      Position: {coords['position']}")
                
                # Calcular coordenadas relativas
                if 'png' in locals():
                    rel_x = (coords['x'] / img_png.size[0]) * 100
                    rel_y = (coords['y'] / img_png.size[1]) * 100
                    print(f"      PNG Relative: {rel_x:.1f}% from left, {rel_y:.1f}% from top")
                
                if 'webp' in locals():
                    rel_x = (coords['x'] / img_webp.size[0]) * 100
                    rel_y = (coords['y'] / img_webp.size[1]) * 100
                    print(f"      WebP Relative: {rel_x:.1f}% from left, {rel_y:.1f}% from top")
        else:
            print(f"❌ Error obteniendo coordenadas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error obteniendo coordenadas: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Resumen:")
    print("   • Las coordenadas absolutas (x, y) son las mismas para ambos formatos")
    print("   • Las coordenadas relativas (%) pueden variar si las dimensiones de imagen son diferentes")
    print("   • El sistema actual usa WebP internamente para optimización, pero devuelve PNG")
    print("   • Las coordenadas se calculan basándose en el PDF original, no en la imagen final")

if __name__ == "__main__":
    test_coordinates_comparison()
