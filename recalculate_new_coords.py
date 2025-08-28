#!/usr/bin/env python3
"""
Script para recalcular los factores de escalado con las nuevas coordenadas de ChatGPT
"""

def recalculate_new_coordinates():
    """Recalcular factores de escalado con las coordenadas de ChatGPT"""
    
    # Coordenadas del template
    template_x = 323
    template_y = 184
    
    # Coordenadas reales según ChatGPT
    real_x = 407
    real_y = 1375
    
    # Dimensiones de la imagen
    image_width = 1131
    image_height = 1600
    
    print("🔍 Recalculando con coordenadas reales de ChatGPT...")
    print("=" * 60)
    
    print(f"📋 Datos:")
    print(f"   Coordenadas template: ({template_x}, {template_y})")
    print(f"   Coordenadas reales (ChatGPT): ({real_x}, {real_y})")
    print(f"   Imagen: {image_width} x {image_height}")
    
    # Calcular nuevos factores de escalado
    new_scale_x = real_x / template_x
    new_scale_y = real_y / template_y
    
    print(f"\n🧮 Nuevos factores de escalado:")
    print(f"   Factor X: {new_scale_x:.4f}")
    print(f"   Factor Y: {new_scale_y:.4f}")
    
    # Verificar el cálculo
    calculated_x = int(template_x * new_scale_x)
    calculated_y = int(template_y * new_scale_y)
    
    print(f"\n✅ Verificación:")
    print(f"   Calculado: ({calculated_x}, {calculated_y})")
    print(f"   Real: ({real_x}, {real_y})")
    print(f"   Diferencia: ({real_x - calculated_x}, {real_y - calculated_y})")
    
    # Comparar con los factores anteriores
    old_scale_x = 1.3808
    old_scale_y = 7.9565
    
    old_calculated_x = int(template_x * old_scale_x)
    old_calculated_y = int(template_y * old_scale_y)
    
    print(f"\n📊 Comparación con factores anteriores:")
    print(f"   Factores anteriores: X={old_scale_x:.4f}, Y={old_scale_y:.4f}")
    print(f"   Calculado con factores anteriores: ({old_calculated_x}, {old_calculated_y})")
    print(f"   Diferencia con reales: ({real_x - old_calculated_x}, {real_y - old_calculated_y})")
    
    print(f"\n💡 Conclusión:")
    print(f"   Los nuevos factores son: X={new_scale_x:.4f}, Y={new_scale_y:.4f}")
    print(f"   Estos factores deberían dar coordenadas más precisas")

if __name__ == "__main__":
    recalculate_new_coordinates()
