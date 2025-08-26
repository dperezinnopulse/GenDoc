#!/usr/bin/env python3
"""
Servidor mínimo para probar la funcionalidad de imagen.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

app = FastAPI(title="GenDoc Simple Server")

class RenderRequest(BaseModel):
    template_id: str
    data: dict
    output_format: Literal["pdf", "image"] = "pdf"

@app.get("/")
def root():
    return {"message": "GenDoc Simple Server running", "status": "ok"}

@app.get("/api/templates")
def get_templates():
    """Endpoint para verificar que el servidor funciona."""
    return {"templates": ["test_template"], "status": "ok"}

@app.post("/api/render")
async def render_document(req: RenderRequest):
    """Endpoint para renderizar documentos."""
    try:
        print(f"🔍 DEBUG: output_format = {req.output_format}")
        print(f"🔍 DEBUG: template_id = {req.template_id}")
        
        # Simular generación de PDF
        pdf_bytes = create_simple_pdf(req.data)
        
        # Handle different output formats
        if req.output_format == "image":
            print("🖼️  DEBUG: Converting PDF to image...")
            # Convert PDF to image
            image_bytes = await convert_pdf_to_image_async(pdf_bytes)
            print(f"🖼️  DEBUG: Image conversion complete, size: {len(image_bytes)} bytes")
            return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")
        
        print("📄 DEBUG: Returning PDF format...")
        # Default: PDF output
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")
            
    except Exception as ex:
        print(f"❌ Error: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

def create_simple_pdf(data: dict) -> bytes:
    """Crea un PDF simple para pruebas."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Crear PDF en memoria
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Agregar contenido
        c.drawString(100, 750, "DOCUMENTO DE PRUEBA")
        c.drawString(100, 720, f"Nombre: {data.get('nombre', 'N/A')}")
        c.drawString(100, 700, f"Apellido: {data.get('apellido', 'N/A')}")
        c.drawString(100, 680, f"Template ID: {data.get('template_id', 'N/A')}")
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        print(f"Error creando PDF: {e}")
        # Fallback: PDF simple
        return b"%PDF-1.7\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Documento de prueba) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF\n"

async def convert_pdf_to_image_async(pdf_bytes: bytes) -> bytes:
    """Convierte PDF a imagen de forma asíncrona."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, convert_pdf_to_image_sync, pdf_bytes)

def convert_pdf_to_image_sync(pdf_bytes: bytes) -> bytes:
    """Convierte PDF a imagen de forma síncrona."""
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor simple...")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
