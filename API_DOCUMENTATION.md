# 📋 Documentación de la API GenDoc

## 🚀 Información General

**URL Base:** `https://a83581047e68.ngrok-free.app/api`

## 📄 Endpoint Principal: Generación de Documentos

### POST `/render`

Genera documentos en formato PDF o imagen con coordenadas de campos de firma.

---

## 📋 Parámetros de Entrada

### Headers
```
Content-Type: application/json
```

### Payload (JSON)
```json
{
  "template_id": "string",
  "data": {
    "campo1": "valor1",
    "campo2": "valor2"
  },
  "output_format": "pdf" | "image"
}
```

#### Parámetros:
- **`template_id`** (string, requerido): ID único de la plantilla
- **`data`** (object, requerido): Datos a insertar en la plantilla
- **`output_format`** (string, opcional): 
  - `"pdf"` (por defecto): Devuelve documento PDF
  - `"image"`: Devuelve imagen optimizada con coordenadas de firma

---

## 📤 Respuestas

### Para `output_format: "pdf"`

**Content-Type:** `application/pdf` o `application/json`

```json
{
  "pdf_base64": "JVBERi0xLjQKJcOkw7zDtsO...",
  "signatures": {
    "firma1": {
      "x": 100,
      "y": 200,
      "width": 150,
      "height": 50
    }
  }
}
```

### Para `output_format: "image"`

**Content-Type:** `application/json`

```json
{
  "image_base64": "UklGRiQAAABXRUJQVlA4IBgAAAAwAQCgASgBAAAD...",
  "signatures": {
    "firma1": {
      "x": 100,
      "y": 200,
      "width": 150,
      "height": 50
    }
  }
}
```

---

## 🖼️ Optimización de Imágenes

### ✨ Características de la Optimización Avanzada

La API utiliza un **algoritmo de optimización avanzado** que incluye:

1. **Formato WebP**: Mejor compresión que PNG/JPEG
2. **Modo Documento**: Escala de grises + nitidez para texto nítido
3. **Búsqueda Binaria**: Encuentra la calidad óptima automáticamente
4. **Limpieza de Metadatos**: Elimina EXIF/ICC para reducir peso
5. **Redimensionado Inteligente**: Máximo 1600px manteniendo proporción

### 📊 Especificaciones Técnicas

- **Tamaño objetivo**: ~260KB (20% más calidad)
- **Formato**: WebP (con fallback a JPEG)
- **Calidad**: Optimizada automáticamente
- **Resolución máxima**: 1600x1600 píxeles
- **Color**: Mantenido (no escala de grises)
- **Modo documento**: Desactivado para preservar colores

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Generar PDF
```bash
curl -X POST "https://a83581047e68.ngrok-free.app/api/render" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "4beba2ce11614d36bd066809e2f52115",
    "data": {
      "Alumno": "Diego Pérez Donoso",
      "Documento": "12345",
      "Fecha": "2025-08-26"
    },
    "output_format": "pdf"
  }'
```

### Ejemplo 2: Generar Imagen Optimizada
```bash
curl -X POST "https://a83581047e68.ngrok-free.app/api/render" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "4beba2ce11614d36bd066809e2f52115",
    "data": {
      "Alumno": "Diego Pérez Donoso",
      "Documento": "12345",
      "Fecha": "2025-08-26"
    },
    "output_format": "image"
  }'
```

### Ejemplo 3: Python
```python
import requests
import base64

# Configuración
url = "https://a83581047e68.ngrok-free.app/api/render"
payload = {
    "template_id": "4beba2ce11614d36bd066809e2f52115",
    "data": {
        "Alumno": "Diego Pérez Donoso",
        "Documento": "12345",
        "Fecha": "2025-08-26"
    },
    "output_format": "image"
}

# Llamada a la API
response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    
    # Guardar imagen
    image_data = base64.b64decode(result["image_base64"])
    with open("documento.png", "wb") as f:
        f.write(image_data)
    
    # Procesar coordenadas de firma
    signatures = result["signatures"]
    for key, coords in signatures.items():
        print(f"Campo {key}: x={coords['x']}, y={coords['y']}")
else:
    print(f"Error: {response.status_code}")
```

---

## 🔧 Códigos de Estado HTTP

- **200 OK**: Operación exitosa
- **400 Bad Request**: Datos de entrada inválidos
- **404 Not Found**: Plantilla no encontrada
- **500 Internal Server Error**: Error interno del servidor

---

## 📋 Campos de Firma

### Estructura de Coordenadas
```json
{
  "signatures": {
    "nombre_campo": {
      "x": 100,        // Posición X en píxeles
      "y": 200,        // Posición Y en píxeles
      "width": 150,    // Ancho del campo en píxeles
      "height": 50     // Alto del campo en píxeles
    }
  }
}
```

### Configuración en Plantillas
Los campos de firma se configuran en el archivo `meta.json` de cada plantilla:

```json
{
  "mapping": {
    "_signatures": {
      "firma_alumno": {
        "x": 351,
        "y": 107,
        "width": 200,
        "height": 100
      }
    }
  }
}
```

---

## 🚀 Mejoras Recientes (v2.1.0)

### ✅ Optimización de Imágenes Avanzada
- **Algoritmo inteligente**: Búsqueda binaria de calidad óptima
- **Formato WebP**: Mejor compresión y calidad
- **Color preservado**: No se convierte a escala de grises
- **Calidad aumentada**: 20% más calidad que la versión anterior
- **Tamaño optimizado**: ~260KB con excelente calidad visual

### ✅ Rendimiento Mejorado
- **Conversión más rápida**: Algoritmos optimizados
- **Menor uso de memoria**: Procesamiento eficiente
- **Mejor calidad visual**: Texto más nítido y legible

---

## 📞 Soporte

Para soporte técnico o consultas sobre la API, contacta al equipo de desarrollo.

**Versión actual:** 2.1.0  
**Última actualización:** Agosto 2025
