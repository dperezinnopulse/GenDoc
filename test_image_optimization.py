#!/usr/bin/env python3
"""
Script para probar la optimización de imagen.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.template_store import TemplateStore
from app.services.renderer import Renderer

def test_image_optimization():
    """Prueba la optimización de imagen."""
    print("🔄 Probando optimización de imagen")
    print("=" * 50)
    
    # Inicializar servicios
    store = TemplateStore(base_path="storage/templates")
    renderer = Renderer(store)
    
    # Datos de prueba
    template_id = "4beba2ce11614d36bd066809e2f52115"
    data = {
        "Alumno": "Diego Pérez Donoso",
        "Documento": "12345",
        "Fecha": "2025-08-26",
        "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
    }
    
    print(f"📄 Template ID: {template_id}")
    print(f"📝 Datos: {data}")
    
    try:
        # 1. Generar PDF
        print("\n🔄 Paso 1: Generando PDF...")
        pdf_bytes = renderer.render_to_pdf(template_id, data)
        print(f"✅ PDF generado: {len(pdf_bytes)} bytes")
        
        # 2. Convertir PDF a imagen optimizada
        print("\n🔄 Paso 2: Convirtiendo PDF a imagen optimizada...")
        image_bytes = renderer.convert_pdf_to_image(pdf_bytes)
        print(f"✅ Imagen optimizada generada: {len(image_bytes)} bytes")
        
        # 3. Calcular reducción de tamaño
        size_kb = len(image_bytes) / 1024
        print(f"📊 Tamaño final: {size_kb:.1f} KB")
        
        if size_kb <= 100:
            print("✅ Optimización exitosa: imagen menor a 100KB")
        elif size_kb <= 200:
            print("⚠️  Optimización moderada: imagen entre 100-200KB")
        else:
            print("❌ Optimización insuficiente: imagen mayor a 200KB")
        
        # 4. Guardar imagen para verificar
        filename = f"test_optimized_image_{template_id}.png"
        with open(filename, 'wb') as f:
            f.write(image_bytes)
        print(f"💾 Imagen guardada como: {filename}")
        
        # 5. Verificar si es PNG válido
        if image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            print("✅ Formato PNG válido")
        else:
            print("⚠️  Formato PNG no válido")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_image_optimization()
