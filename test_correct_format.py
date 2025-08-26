#!/usr/bin/env python3
"""
Script para probar la llamada con el formato correcto.
"""

import requests
import json
import time

def test_correct_format():
    """Prueba la llamada con el formato correcto."""
    print("🖼️  PROBANDO FORMATO CORRECTO")
    print("=" * 50)
    
    # Datos de prueba (con el formato correcto)
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "output_format": "image"  # Formato correcto
    }
    
    print(f"📤 Enviando petición a: http://localhost:8080/api/render")
    print(f"📋 Template ID: {payload['template_id']}")
    print(f"🖼️  Output Format: {payload['output_format']}")
    print(f"📝 Datos: {json.dumps(payload['data'], indent=2)}")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8080/api/render",
            json=payload,
            timeout=60
        )
        
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
                filename = f"test_correct_format_{int(time.time())}.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 Imagen guardada como '{filename}'")
                
                # Verificar que es una imagen PNG válida
                if response.content.startswith(b'\x89PNG\r\n\x1a\n'):
                    print("   ✅ Formato PNG válido")
                else:
                    print("   ⚠️  Formato PNG no válido")
                
                return True
                
            elif 'application/pdf' in content_type:
                print("❌ Se devolvió PDF en lugar de imagen")
                print(f"   📄 Tamaño: {len(response.content)} bytes")
                
                # Guardar PDF para verificación
                filename = f"test_incorrect_pdf_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 PDF guardado como '{filename}'")
                
                return False
                
            else:
                print(f"❌ Content-Type inesperado: {content_type}")
                print(f"   📝 Primeros 100 bytes: {response.content[:100]}")
                return False
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_wrong_format():
    """Prueba la llamada con el formato incorrecto (como lo estás enviando)."""
    print("\n❌ PROBANDO FORMATO INCORRECTO (como lo envías)")
    print("=" * 50)
    
    # Datos de prueba (con el formato incorrecto)
    payload = {
        "template_id": "4beba2ce11614d36bd066809e2f52115",
        "data": {
            "Alumno": "Diego Pérez Donoso",
            "Documento": "12345",
            "Fecha": "2025-08-26",
            "Logotipo": "http://localhost:8080/img/logos/COITT.jpg"
        },
        "format": "png"  # Formato incorrecto
    }
    
    print(f"📤 Enviando petición con formato incorrecto")
    print(f"🖼️  Format: {payload['format']}")
    
    try:
        response = requests.post(
            "http://localhost:8080/api/render",
            json=payload,
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                print("❌ Se devolvió PDF (comportamiento por defecto)")
                print("   Esto confirma que el parámetro 'format' no funciona")
                
                # Guardar PDF para verificación
                filename = f"test_wrong_format_{int(time.time())}.pdf"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"   💾 PDF guardado como '{filename}'")
                
                return False
                
            else:
                print(f"⚠️  Content-Type inesperado: {content_type}")
                return False
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal."""
    print("🚀 INICIANDO PRUEBAS DE FORMATO")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    try:
        health_check = requests.get("http://localhost:8080/api/templates", timeout=5)
        if health_check.status_code == 200:
            print("✅ Servidor funcionando correctamente")
        else:
            print("❌ Servidor no responde correctamente")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        return
    
    print()
    
    # Prueba 1: Formato incorrecto (como lo envías)
    wrong_format_result = test_wrong_format()
    
    # Prueba 2: Formato correcto
    correct_format_result = test_correct_format()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    print(f"❌ Formato incorrecto ('format'): {'❌ FALLÓ' if not wrong_format_result else '⚠️  Inesperado'}")
    print(f"✅ Formato correcto ('output_format'): {'✅ EXITOSO' if correct_format_result else '❌ FALLÓ'}")
    
    print("\n🔧 SOLUCIÓN:")
    print("Cambia en tu aplicación:")
    print('   ❌ "format": "png"')
    print('   ✅ "output_format": "image"')
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
