#!/usr/bin/env python3
"""
Script para probar diferentes factores de escalado
"""

def test_scaling_factors():
    """Probar diferentes factores de escalado"""
    
    # Coordenadas originales del template
    template_x = 351
    template_y = 107
    
    # Coordenadas esperadas en la imagen
    expected_x = 446
    expected_y = 1464
    
    # Dimensiones de la imagen final
    image_width = 1131
    image_height = 1600
    
    # Dimensiones del PDF original (A4)
    pdf_width = 595.32
    pdf_height = 841.92
    
    print("🔍 Probando diferentes factores de escalado...")
    print("=" * 60)
    
    print(f"📋 Datos de entrada:")
    print(f"   Coordenadas template: ({template_x}, {template_y})")
    print(f"   Coordenadas esperadas: ({expected_x}, {expected_y})")
    print(f"   Dimensiones imagen: {image_width} x {image_height}")
    print(f"   Dimensiones PDF: {pdf_width} x {pdf_height}")
    
    print(f"\n🧮 Cálculos actuales:")
    scale_x = image_width / pdf_width
    scale_y = image_height / pdf_height
    print(f"   Factor escala X: {scale_x:.4f}")
    print(f"   Factor escala Y: {scale_y:.4f}")
    
    # Coordenadas calculadas actualmente
    current_x = int(template_x * scale_x)
    current_y = int((pdf_height - template_y) * scale_y)  # Convertir Y de bottom-left a top-left
    print(f"   Coordenadas calculadas: ({current_x}, {current_y})")
    
    print(f"\n🔍 Análisis de diferencias:")
    x_diff = expected_x - current_x
    y_diff = expected_y - current_y
    print(f"   Diferencia X: {x_diff}")
    print(f"   Diferencia Y: {y_diff}")
    
    print(f"\n🧪 Probando diferentes factores:")
    
    # Probar diferentes factores de escala
    test_factors = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
    
    best_factor_x = scale_x
    best_factor_y = scale_y
    best_error = abs(x_diff) + abs(y_diff)
    
    for factor in test_factors:
        test_scale_x = scale_x * factor
        test_scale_y = scale_y * factor
        
        test_x = int(template_x * test_scale_x)
        test_y = int((pdf_height - template_y) * test_scale_y)
        
        error_x = abs(expected_x - test_x)
        error_y = abs(expected_y - test_y)
        total_error = error_x + error_y
        
        print(f"   Factor {factor:.2f}: ({test_x}, {test_y}) - Error: {total_error}")
        
        if total_error < best_error:
            best_error = total_error
            best_factor_x = test_scale_x
            best_factor_y = test_scale_y
    
    print(f"\n✅ Mejor factor encontrado:")
    print(f"   Factor X: {best_factor_x:.4f}")
    print(f"   Factor Y: {best_factor_y:.4f}")
    print(f"   Error total: {best_error}")
    
    # Calcular coordenadas con el mejor factor
    best_x = int(template_x * best_factor_x)
    best_y = int((pdf_height - template_y) * best_factor_y)
    print(f"   Coordenadas resultantes: ({best_x}, {best_y})")
    
    print(f"\n💡 Análisis:")
    print(f"   • El factor actual es: {scale_x:.4f}")
    print(f"   • El mejor factor sería: {best_factor_x:.4f}")
    print(f"   • Diferencia en factor: {best_factor_x - scale_x:.4f}")
    
    # Verificar si el problema está en el sistema de coordenadas Y
    print(f"\n🔍 Verificando sistema de coordenadas Y:")
    print(f"   Coordenada Y original: {template_y}")
    print(f"   PDF height: {pdf_height}")
    print(f"   Y convertida (bottom-left a top-left): {pdf_height - template_y}")
    print(f"   Y esperada en imagen: {expected_y}")
    
    # Probar sin convertir Y
    test_y_no_convert = int(template_y * best_factor_y)
    print(f"   Y sin conversión: {test_y_no_convert}")
    print(f"   Error Y sin conversión: {abs(expected_y - test_y_no_convert)}")

if __name__ == "__main__":
    test_scaling_factors()
