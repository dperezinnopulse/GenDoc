#!/usr/bin/env python3
"""
Script para comparar la calidad de diferentes optimizaciones de imagen.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.template_store import TemplateStore
from app.services.renderer import Renderer

def test_quality_comparison():
    """Compara diferentes métodos de optimización."""
    print("🔄 Comparando calidad de optimizaciones")
    print("=" * 60)
    
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
        
        # 2. Convertir PDF a imagen con nueva optimización
        print("\n🔄 Paso 2: Convirtiendo con optimización avanzada...")
        image_bytes = renderer.convert_pdf_to_image(pdf_bytes)
        size_kb = len(image_bytes) / 1024
        print(f"✅ Imagen optimizada: {size_kb:.1f} KB")
        
        # 3. Guardar imagen para verificar
        filename = f"test_advanced_optimization_{template_id}.webp"
        with open(filename, 'wb') as f:
            f.write(image_bytes)
        print(f"💾 Imagen guardada como: {filename}")
        
        # 4. Verificar formato
        if image_bytes.startswith(b'RIFF') and b'WEBP' in image_bytes[:20]:
            print("✅ Formato WebP válido")
        elif image_bytes.startswith(b'\xff\xd8\xff'):
            print("✅ Formato JPEG válido")
        elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
            print("✅ Formato PNG válido")
        else:
            print("⚠️  Formato no reconocido")
        
        # 5. Análisis de calidad
        print(f"\n📊 Análisis de Calidad:")
        print(f"   - Tamaño original PDF: {len(pdf_bytes)} bytes")
        print(f"   - Tamaño imagen optimizada: {len(image_bytes)} bytes")
        print(f"   - Reducción: {((len(pdf_bytes) - len(image_bytes)) / len(pdf_bytes) * 100):.1f}%")
        print(f"   - Tamaño en KB: {size_kb:.1f} KB")
        
        if size_kb <= 100:
            print("   - Estado: ✅ Excelente optimización")
        elif size_kb <= 200:
            print("   - Estado: ✅ Buena optimización")
        elif size_kb <= 300:
            print("   - Estado: ⚠️  Optimización moderada")
        else:
            print("   - Estado: ❌ Optimización insuficiente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_quality_comparison()
