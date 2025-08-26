#!/usr/bin/env python3
"""
Script para probar la generación de imagen con la aplicación funcionando.
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://localhost:8080"

def test_image_generation():
    """Prueba la generación de imagen."""
    print("🖼️  PROBANDO GENERACIÓN DE IMAGEN")
    print("=" * 50)
    
    # Datos de prueba
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "nombre": "Ana",
            "apellido": "Pérez",
            "documento": "12345678A",
            "fecha": "2025-01-15",
            "curso": "Matemáticas"
        },
        "output_format": "image"
    }
    
    print(f"📤 Enviando petición a: {BASE_URL}/api/render")
    print(f"📋 Template ID: {payload['template_id']}")
    print(f"🖼️  Output Format: {payload['output_format']}")
    print(f"📝 Datos: {json.dumps(payload['data'], indent=2)}")
    print()
    
    try:
        # Medir tiempo de respuesta
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=60
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'image/png' in content_type:
                print("✅ ¡ÉXITO! Imagen generada correctamente")
                print(f"   🖼️  Tamaño: {len(response.content)} bytes")
                print(f"   📋 Content-Type: {content_type}")
                
                # Guardar imagen para verificación
                filename = f"test_image_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 Imagen guardada como '{filename}'")
                
                # Verificar que es una imagen PNG válida
                if response.content.startswith(b'\x89PNG\r\n\x1a\n'):
                    print("   ✅ Formato PNG válido")
                else:
                    print("   ⚠️  Formato PNG no válido")
                
                return True
                
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                print(f"   📝 Primeros 100 bytes: {response.content[:100]}")
                return False
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_pdf_comparison():
    """Prueba la generación de PDF para comparar."""
    print("\n📄 PROBANDO GENERACIÓN DE PDF (COMPARACIÓN)")
    print("=" * 50)
    
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "nombre": "Ana",
            "apellido": "Pérez",
            "documento": "12345678A",
            "fecha": "2025-01-15",
            "curso": "Matemáticas"
        },
        "output_format": "pdf"
    }
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/render",
            json=payload,
            timeout=60
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Tiempo de respuesta: {response_time:.2f} segundos")
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                print("✅ PDF generado correctamente")
                print(f"   📄 Tamaño: {len(response.content)} bytes")
                
                # Guardar PDF para verificación
                filename = f"test_pdf_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 PDF guardado como '{filename}'")
                
                return True
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 INICIANDO PRUEBAS DE GENERACIÓN DE IMAGEN")
    print("=" * 60)
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"🕐 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar que el servidor esté funcionando
    try:
        health_check = requests.get(f"{BASE_URL}/api/templates", timeout=5)
        if health_check.status_code == 200:
            print("✅ Servidor funcionando correctamente")
        else:
            print("❌ Servidor no responde correctamente")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        return
    
    print()
    
    # Prueba 1: Generación de imagen
    image_success = test_image_generation()
    
    # Prueba 2: Generación de PDF (comparación)
    pdf_success = test_pdf_comparison()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    print(f"🖼️  Generación de imagen: {'✅ EXITOSA' if image_success else '❌ FALLIDA'}")
    print(f"📄 Generación de PDF: {'✅ EXITOSA' if pdf_success else '❌ FALLIDA'}")
    
    if image_success and pdf_success:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("✅ La funcionalidad de imagen está funcionando correctamente")
        print("✅ La funcionalidad de PDF sigue funcionando")
        print("✅ La nueva funcionalidad es compatible con la existente")
    elif image_success:
        print("\n⚠️  Solo la generación de imagen funcionó")
        print("❌ Hay un problema con la generación de PDF")
    elif pdf_success:
        print("\n⚠️  Solo la generación de PDF funcionó")
        print("❌ Hay un problema con la generación de imagen")
    else:
        print("\n❌ Ambas pruebas fallaron")
        print("❌ Hay un problema general con el servidor")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
