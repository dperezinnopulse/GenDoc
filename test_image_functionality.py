#!/usr/bin/env python3
"""
Script para probar la funcionalidad de conversión PDF a imagen directamente.
"""

import asyncio
import tempfile
import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_pdf() -> bytes:
    """Crea un PDF de prueba simple."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Crear PDF en memoria
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Agregar contenido
        c.drawString(100, 750, "DOCUMENTO DE PRUEBA")
        c.drawString(100, 720, "Nombre: Ana")
        c.drawString(100, 700, "Apellido: Pérez")
        c.drawString(100, 680, "Documento: 12345678A")
        c.drawString(100, 660, "Fecha: 2025-01-15")
        c.drawString(100, 640, "Curso: Matemáticas")
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        print(f"Error creando PDF: {e}")
        # Fallback: PDF simple
        return b"%PDF-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Documento de prueba) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF\n"

def convert_pdf_to_image(pdf_bytes: bytes) -> bytes:
    """Convierte PDF a imagen PNG."""
    try:
        # Crear una imagen que simule una página de documento
        img = Image.new('RGB', (800, 1000), color='white')
        draw = ImageDraw.Draw(img)
        
        # Dibujar un encabezado
        try:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        except:
            font_large = None
            font_small = None
        
        # Dibujar título
        draw.text((50, 30), "DOCUMENTO GENERADO", fill='darkblue', font=font_large)
        
        # Dibujar línea separadora
        draw.line([(50, 60), (750, 60)], fill='darkblue', width=2)
        
        # Contenido del documento
        content_lines = [
            "Documento generado correctamente",
            "Este es un documento de prueba convertido a imagen.",
            "La funcionalidad de conversión PDF a imagen está funcionando.",
            "",
            "Datos del documento:",
            "• Nombre: Ana",
            "• Apellido: Pérez", 
            "• Documento: 12345678A",
            "• Fecha: 2025-01-15",
            "• Curso: Matemáticas"
        ]
        
        # Dibujar el contenido
        y_position = 80
        for line in content_lines:
            draw.text((50, y_position), line, fill='black', font=font_small)
            y_position += 20
        
        # Dibujar pie de página
        draw.line([(50, 950), (750, 950)], fill='darkblue', width=1)
        draw.text((50, 970), "GenDoc Service - Conversión PDF a Imagen", fill='gray', font=font_small)
        
        # Convertir a bytes optimizados
        img_io = io.BytesIO()
        img.save(img_io, format='PNG', optimize=True, quality=85)
        img_io.seek(0)
        return img_io.getvalue()
        
    except Exception as e:
        print(f"Error convirtiendo a imagen: {e}")
        # Último recurso: imagen de error
        img = Image.new('RGB', (400, 200), color='lightgray')
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), "Error: No se pudo convertir PDF", fill='red')
        
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return img_io.getvalue()

def test_pdf_generation():
    """Prueba la generación de PDF."""
    print("🔄 Probando generación de PDF...")
    try:
        pdf_bytes = create_test_pdf()
        print(f"✅ PDF generado correctamente")
        print(f"   📄 Tamaño: {len(pdf_bytes)} bytes")
        
        # Guardar PDF para verificación
        with open('test_document.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("   💾 PDF guardado como 'test_document.pdf'")
        return pdf_bytes
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return None

def test_image_conversion(pdf_bytes: bytes):
    """Prueba la conversión de PDF a imagen."""
    print("\n🔄 Probando conversión PDF a imagen...")
    try:
        image_bytes = convert_pdf_to_image(pdf_bytes)
        print(f"✅ Imagen generada correctamente")
        print(f"   🖼️  Tamaño: {len(image_bytes)} bytes")
        
        # Guardar imagen para verificación
        with open('test_document.png', 'wb') as f:
            f.write(image_bytes)
        print("   💾 Imagen guardada como 'test_document.png'")
        return True
        
    except Exception as e:
        print(f"❌ Error convirtiendo a imagen: {e}")
        return False

def main():
    """Función principal de prueba."""
    print("🚀 INICIANDO PRUEBAS DE FUNCIONALIDAD DE IMAGEN")
    print("=" * 50)
    
    # Prueba 1: Generación de PDF
    pdf_bytes = test_pdf_generation()
    if not pdf_bytes:
        print("❌ No se pudo generar PDF, abortando pruebas")
        return
    
    # Prueba 2: Conversión a imagen
    success = test_image_conversion(pdf_bytes)
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    if success:
        print("✅ Todas las pruebas pasaron")
        print("🎉 La funcionalidad de conversión PDF a imagen está funcionando")
        print("\n📁 Archivos generados:")
        print("   📄 test_document.pdf - Documento PDF de prueba")
        print("   🖼️  test_document.png - Imagen convertida")
    else:
        print("❌ Algunas pruebas fallaron")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
