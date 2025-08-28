#!/usr/bin/env python3
"""
Script para recalcular los factores de escalado con las nuevas coordenadas
"""

def recalculate_scaling():
    """Recalcular factores de escalado con las nuevas coordenadas"""
    
    # Nuevas coordenadas del template (después de mover el marcador)
    template_x = 323
    template_y = 184
    
    # Coordenadas esperadas en la imagen (donde realmente aparece la firma)
    expected_x = 446
    expected_y = 1464
    
    # Dimensiones de la imagen
    image_width = 1131
    image_height = 1600
    
    print("🔍 Recalculando factores de escalado...")
    print("=" * 60)
    
    print(f"📋 Nuevas coordenadas del template:")
    print(f"   Template: ({template_x}, {template_y})")
    print(f"   Esperadas: ({expected_x}, {expected_y})")
    print(f"   Imagen: {image_width} x {image_height}")
    
    # Calcular nuevos factores de escalado
    new_scale_x = expected_x / template_x
    new_scale_y = expected_y / template_y
    
    print(f"\n🧮 Nuevos factores de escalado:")
    print(f"   Factor X: {new_scale_x:.4f}")
    print(f"   Factor Y: {new_scale_y:.4f}")
    
    # Verificar el cálculo
    calculated_x = int(template_x * new_scale_x)
    calculated_y = int(template_y * new_scale_y)
    
    print(f"\n✅ Verificación:")
    print(f"   Calculado: ({calculated_x}, {calculated_y})")
    print(f"   Esperado: ({expected_x}, {expected_y})")
    print(f"   Diferencia: ({expected_x - calculated_x}, {expected_y - calculated_y})")
    
    # Probar con diferentes coordenadas para verificar que funciona
    print(f"\n🧪 Prueba con coordenadas anteriores:")
    old_template_x = 351
    old_template_y = 107
    
    old_calculated_x = int(old_template_x * new_scale_x)
    old_calculated_y = int(old_template_y * new_scale_y)
    
    print(f"   Template anterior: ({old_template_x}, {old_template_y})")
    print(f"   Calculado con nuevos factores: ({old_calculated_x}, {old_calculated_y})")
    print(f"   Esperado anterior: (446, 1464)")
    print(f"   Diferencia: ({446 - old_calculated_x}, {1464 - old_calculated_y})")
    
    print(f"\n💡 Conclusión:")
    print(f"   Los nuevos factores son específicos para las nuevas coordenadas")
    print(f"   No funcionan bien con las coordenadas anteriores")
    print(f"   Necesitamos un método más genérico")

if __name__ == "__main__":
    recalculate_scaling()
