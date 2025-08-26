#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de salida de imagen.
"""

import requests
import json
import time
import os

# Configuración
BASE_URL = "http://localhost:8080"
TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115"

# Datos de prueba
TEST_DATA = {
    "nombre": "Ana",
    "apellido": "Pérez",
    "documento": "12345678A",
    "fecha": "2025-01-15",
    "curso": "Matemáticas"
}

def test_pdf_output():
    """Prueba la salida en formato PDF (comportamiento por defecto)."""
    print("🔄 Probando salida PDF...")
    
    payload = {
        "template_id": TEMPLATE_ID,
        "data": TEST_DATA,
        "output_format": "pdf"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print("✅ PDF generado correctamente")
                print(f"   📄 Tamaño: {len(response.content)} bytes")
                print(f"   📋 Content-Type: {content_type}")
                
                # Guardar PDF para verificación
                with open('test_output.pdf', 'wb') as f:
                    f.write(response.content)
                print("   💾 PDF guardado como 'test_output.pdf'")
                return True
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def test_image_output():
    """Prueba la salida en formato imagen."""
    print("\n🔄 Probando salida imagen...")
    
    payload = {
        "template_id": TEMPLATE_ID,
        "data": TEST_DATA,
        "output_format": "image"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image/png' in content_type:
                print("✅ Imagen generada correctamente")
                print(f"   🖼️  Tamaño: {len(response.content)} bytes")
                print(f"   📋 Content-Type: {content_type}")
                
                # Guardar imagen para verificación
                with open('test_output.png', 'wb') as f:
                    f.write(response.content)
                print("   💾 Imagen guardada como 'test_output.png'")
                return True
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def test_default_output():
    """Prueba la salida por defecto (sin especificar output_format)."""
    print("\n🔄 Probando salida por defecto...")
    
    payload = {
        "template_id": TEMPLATE_ID,
        "data": TEST_DATA
        # Sin output_format - debería ser PDF por defecto
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print("✅ Salida por defecto es PDF (correcto)")
                print(f"   📄 Tamaño: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ Content-Type inesperado para salida por defecto: {content_type}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def main():
    """Función principal de prueba."""
    print("🚀 INICIANDO PRUEBAS DE SALIDA DE IMAGEN")
    print("=" * 50)
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"📋 Template ID: {TEMPLATE_ID}")
    print()
    
    # Verificar que el servidor esté funcionando
    try:
        health_check = requests.get(f"{BASE_URL}/api/templates", timeout=5)
        if health_check.status_code != 200:
            print("❌ El servidor no está respondiendo correctamente")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        return
    
    print("✅ Servidor funcionando correctamente")
    print()
    
    # Ejecutar pruebas
    results = []
    
    # Prueba 1: Salida por defecto (PDF)
    results.append(("Salida por defecto", test_default_output()))
    
    # Prueba 2: Salida PDF explícita
    results.append(("Salida PDF", test_pdf_output()))
    
    # Prueba 3: Salida imagen
    results.append(("Salida imagen", test_image_output()))
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La funcionalidad está funcionando correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar los errores anteriores.")
    
    # Limpiar archivos de prueba
    print("\n🧹 Limpiando archivos de prueba...")
    for filename in ['test_output.pdf', 'test_output.png']:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"   🗑️  {filename} eliminado")
        except:
            pass

if __name__ == "__main__":
    main()
