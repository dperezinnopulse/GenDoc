#!/usr/bin/env python3
"""
Script para analizar el sistema de coordenadas real del template
"""

def analyze_coordinate_system():
    """Analizar el sistema de coordenadas real del template"""
    
    # Coordenadas del template
    template_x = 323
    template_y = 184
    
    # Coordenadas esperadas en la imagen
    expected_x = 446
    expected_y = 1464
    
    # Dimensiones de la imagen
    image_width = 1131
    image_height = 1600
    
    # Dimensiones del PDF (A4)
    pdf_width = 595.32
    pdf_height = 841.92
    
    print("🔍 Analizando sistema de coordenadas del template...")
    print("=" * 70)
    
    print(f"📋 Datos:")
    print(f"   Coordenadas template: ({template_x}, {template_y})")
    print(f"   Coordenadas esperadas: ({expected_x}, {expected_y})")
    print(f"   Dimensiones imagen: {image_width} x {image_height}")
    print(f"   Dimensiones PDF: {pdf_width} x {pdf_height}")
    
    print(f"\n🧪 Probando diferentes interpretaciones:")
    
    # 1. Si las coordenadas están en píxeles de la imagen final
    if template_x <= image_width and template_y <= image_height:
        print(f"   1. Coordenadas en píxeles de imagen: ({template_x}, {template_y})")
        error1 = abs(expected_x - template_x) + abs(expected_y - template_y)
        print(f"      Error: {error1}")
    
    # 2. Si las coordenadas están en porcentajes de la imagen
    rel_x = template_x / 1000  # Asumiendo que están en milésimas
    rel_y = template_y / 1000
    test2_x = int(rel_x * image_width)
    test2_y = int(rel_y * image_height)
    error2 = abs(expected_x - test2_x) + abs(expected_y - test2_y)
    print(f"   2. Coordenadas en milésimas (%): ({test2_x}, {test2_y}) - Error: {error2}")
    
    # 3. Si las coordenadas están en porcentajes directos
    rel3_x = template_x / 100
    rel3_y = template_y / 100
    test3_x = int(rel3_x * image_width)
    test3_y = int(rel3_y * image_height)
    error3 = abs(expected_x - test3_x) + abs(expected_y - test3_y)
    print(f"   3. Coordenadas en porcentajes directos: ({test3_x}, {test3_y}) - Error: {error3}")
    
    # 4. Si las coordenadas están en un sistema personalizado
    # Probar diferentes factores
    factors = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    
    best_factor = None
    best_error = float('inf')
    
    for factor in factors:
        test_x = int(template_x * factor)
        test_y = int(template_y * factor)
        
        if test_x <= image_width and test_y <= image_height:
            error = abs(expected_x - test_x) + abs(expected_y - test_y)
            print(f"   4.{factor}. Factor {factor}: ({test_x}, {test_y}) - Error: {error}")
            
            if error < best_error:
                best_error = error
                best_factor = factor
    
    print(f"\n✅ Mejor factor encontrado: {best_factor} (Error: {best_error})")
    
    # 5. Analizar si hay una relación no lineal
    print(f"\n🔍 Análisis de relación:")
    print(f"   Ratio X esperado/template: {expected_x / template_x:.4f}")
    print(f"   Ratio Y esperado/template: {expected_y / template_y:.4f}")
    
    # 6. Probar si las coordenadas están en un sistema de coordenadas diferente
    # Por ejemplo, si están en puntos (1/72 de pulgada)
    points_to_pixels = 1.33  # Factor aproximado
    test6_x = int(template_x * points_to_pixels)
    test6_y = int(template_y * points_to_pixels)
    error6 = abs(expected_x - test6_x) + abs(expected_y - test6_y)
    print(f"   6. Coordenadas en puntos (1/72\"): ({test6_x}, {test6_y}) - Error: {error6}")
    
    # 7. Probar si están en un sistema de coordenadas de pantalla
    # Por ejemplo, si están en coordenadas de un editor de imágenes
    screen_scale = 1.38  # Factor encontrado anteriormente
    test7_x = int(template_x * screen_scale)
    test7_y = int(template_y * screen_scale)
    error7 = abs(expected_x - test7_x) + abs(expected_y - test7_y)
    print(f"   7. Coordenadas de pantalla (factor 1.38): ({test7_x}, {test7_y}) - Error: {error7}")

if __name__ == "__main__":
    analyze_coordinate_system()
