#!/usr/bin/env python3
"""
Script para probar diferentes interpretaciones del sistema de coordenadas
"""

def test_coordinate_systems():
    """Probar diferentes interpretaciones del sistema de coordenadas"""
    
    # Coordenadas del template
    template_x = 351
    template_y = 107
    
    # Coordenadas esperadas en la imagen
    expected_x = 446
    expected_y = 1464
    
    # Dimensiones
    image_width = 1131
    image_height = 1600
    pdf_width = 595.32
    pdf_height = 841.92
    
    # Factores de escala
    scale_x = image_width / pdf_width
    scale_y = image_height / pdf_height
    
    print("🔍 Probando diferentes sistemas de coordenadas...")
    print("=" * 60)
    
    print(f"📋 Datos:")
    print(f"   Coordenadas template: ({template_x}, {template_y})")
    print(f"   Coordenadas esperadas: ({expected_x}, {expected_y})")
    print(f"   Factores escala: ({scale_x:.4f}, {scale_y:.4f})")
    
    print(f"\n🧪 Probando diferentes interpretaciones:")
    
    # 1. Sistema actual: PDF bottom-left, convertir Y
    current_x = int(template_x * scale_x)
    current_y = int((pdf_height - template_y) * scale_y)
    error_current = abs(expected_x - current_x) + abs(expected_y - current_y)
    print(f"   1. Actual (PDF bottom-left, convertir Y): ({current_x}, {current_y}) - Error: {error_current}")
    
    # 2. PDF top-left, sin conversión Y
    test1_x = int(template_x * scale_x)
    test1_y = int(template_y * scale_y)
    error1 = abs(expected_x - test1_x) + abs(expected_y - test1_y)
    print(f"   2. PDF top-left, sin conversión Y: ({test1_x}, {test1_y}) - Error: {error1}")
    
    # 3. PDF bottom-left, sin conversión Y
    test2_x = int(template_x * scale_x)
    test2_y = int(template_y * scale_y)
    error2 = abs(expected_x - test2_x) + abs(expected_y - test2_y)
    print(f"   3. PDF bottom-left, sin conversión Y: ({test2_x}, {test2_y}) - Error: {error2}")
    
    # 4. Coordenadas relativas (porcentajes)
    rel_x = template_x / pdf_width
    rel_y = template_y / pdf_height
    test3_x = int(rel_x * image_width)
    test3_y = int(rel_y * image_height)
    error3 = abs(expected_x - test3_x) + abs(expected_y - test3_y)
    print(f"   4. Coordenadas relativas (%): ({test3_x}, {test3_y}) - Error: {error3}")
    
    # 5. Coordenadas relativas con Y invertido
    rel_x_inv = template_x / pdf_width
    rel_y_inv = (pdf_height - template_y) / pdf_height
    test4_x = int(rel_x_inv * image_width)
    test4_y = int(rel_y_inv * image_height)
    error4 = abs(expected_x - test4_x) + abs(expected_y - test4_y)
    print(f"   5. Coordenadas relativas con Y invertido: ({test4_x}, {test4_y}) - Error: {error4}")
    
    # 6. Probar si las coordenadas están en píxeles ya
    test5_x = template_x
    test5_y = template_y
    error5 = abs(expected_x - test5_x) + abs(expected_y - test5_y)
    print(f"   6. Coordenadas ya en píxeles: ({test5_x}, {test5_y}) - Error: {error5}")
    
    # 7. Probar con offset
    offset_x = 100
    offset_y = 50
    test6_x = int(template_x * scale_x) + offset_x
    test6_y = int((pdf_height - template_y) * scale_y) + offset_y
    error6 = abs(expected_x - test6_x) + abs(expected_y - test6_y)
    print(f"   7. Con offset ({offset_x}, {offset_y}): ({test6_x}, {test6_y}) - Error: {error6}")
    
    # Encontrar el mejor método
    methods = [
        ("Actual", current_x, current_y, error_current),
        ("Top-left sin conversión", test1_x, test1_y, error1),
        ("Bottom-left sin conversión", test2_x, test2_y, error2),
        ("Coordenadas relativas", test3_x, test3_y, error3),
        ("Relativas con Y invertido", test4_x, test4_y, error4),
        ("Ya en píxeles", test5_x, test5_y, error5),
        (f"Con offset ({offset_x}, {offset_y})", test6_x, test6_y, error6)
    ]
    
    best_method = min(methods, key=lambda x: x[3])
    
    print(f"\n✅ Mejor método encontrado:")
    print(f"   Método: {best_method[0]}")
    print(f"   Coordenadas: ({best_method[1]}, {best_method[2]})")
    print(f"   Error: {best_method[3]}")
    
    # Análisis adicional
    print(f"\n🔍 Análisis adicional:")
    print(f"   • Coordenadas template como % del PDF: ({template_x/pdf_width*100:.1f}%, {template_y/pdf_height*100:.1f}%)")
    print(f"   • Coordenadas esperadas como % de la imagen: ({expected_x/image_width*100:.1f}%, {expected_y/image_height*100:.1f}%)")
    
    # Verificar si hay una relación directa
    ratio_x = expected_x / template_x
    ratio_y = expected_y / template_y
    print(f"   • Ratios directos: X={ratio_x:.2f}, Y={ratio_y:.2f}")
    
    # Probar con estos ratios
    test7_x = int(template_x * ratio_x)
    test7_y = int(template_y * ratio_y)
    error7 = abs(expected_x - test7_x) + abs(expected_y - test7_y)
    print(f"   8. Con ratios directos: ({test7_x}, {test7_y}) - Error: {error7}")

if __name__ == "__main__":
    test_coordinate_systems()
