#!/usr/bin/env python3
import json
import os
from pathlib import Path

def check_template_config():
    print("🔍 Verificando configuración del template...")
    
    template_id = "4beba2ce11614d36bd066809e2f52115"
    meta_path = f"storage/templates/{template_id}/meta.json"
    
    if not os.path.exists(meta_path):
        print(f"❌ No se encontró el archivo meta.json en {meta_path}")
        return
    
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        print(f"✅ Template encontrado: {meta.get('name', 'Sin nombre')}")
        print(f"📄 Tipo: {meta.get('kind', 'Desconocido')}")
        
        # Verificar mapping
        mapping = meta.get('mapping', {})
        print(f"\n📋 Mapping configurado:")
        print(json.dumps(mapping, indent=2, ensure_ascii=False))
        
        # Verificar campos de imagen
        images = mapping.get('_images', {})
        if images:
            print(f"\n🖼️ Campos de imagen configurados:")
            for key, config in images.items():
                print(f"  - {key}: {config}")
        else:
            print(f"\n❌ No hay campos de imagen configurados")
            print(f"💡 Necesitas crear un campo de imagen llamado 'Logotipo' en el editor visual")
        
        # Verificar posiciones
        positions = mapping.get('_positions', {})
        if positions:
            print(f"\n📍 Campos de texto configurados:")
            for key, pos in positions.items():
                print(f"  - {key}: {pos}")
        
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")

if __name__ == "__main__":
    check_template_config()
