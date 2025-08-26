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
  - `"pdf"` (por defecto): Devuelve PDF
  - `"image"`: Devuelve imagen PNG con coordenadas de firma

---

## 📤 Respuestas

### 1. Formato PDF (`output_format: "pdf"`)

#### Sin campos de firma:
```http
Content-Type: application/pdf
```
Devuelve directamente el archivo PDF.

#### Con campos de firma:
```json
{
  "pdf_base64": "base64_encoded_pdf_content",
  "signatures": {
    "firma_alumno": {
      "x": 351,
      "y": 107,
      "width": 200,
      "height": 100
    },
    "firma_profesor": {
      "x": 500,
      "y": 200,
      "width": 200,
      "height": 100
    }
  }
}
```

### 2. Formato Imagen (`output_format: "image"`)

```json
{
  "image_base64": "base64_encoded_png_content",
  "signatures": {
    "firma_alumno": {
      "x": 351,
      "y": 107,
      "width": 200,
      "height": 100
    }
  }
}
```

---

## 📍 Estructura de Coordenadas de Firma

### Formato de Coordenadas
```json
{
  "nombre_campo": {
    "x": 351,        // Posición X en píxeles
    "y": 107,        // Posición Y en píxeles  
    "width": 200,    // Ancho del área de firma
    "height": 100    // Alto del área de firma
  }
}
```

### Sistema de Coordenadas
- **Origen**: Esquina superior izquierda (0,0)
- **Unidades**: Píxeles
- **X**: Distancia desde el borde izquierdo
- **Y**: Distancia desde el borde superior

---

## 💻 Ejemplos de Uso

### Ejemplo 1: Generar PDF
```javascript
const response = await fetch('https://a83581047e68.ngrok-free.app/api/render', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    template_id: "4beba2ce11614d36bd066809e2f52115",
    data: {
      "Alumno": "Diego Pérez Donoso",
      "Documento": "12345",
      "Fecha": "2025-08-26"
    },
    output_format: "pdf"
  })
});

const result = await response.json();
// result.pdf_base64 contiene el PDF en base64
// result.signatures contiene las coordenadas de firma
```

### Ejemplo 2: Generar Imagen con Coordenadas de Firma
```javascript
const response = await fetch('https://a83581047e68.ngrok-free.app/api/render', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    template_id: "4beba2ce11614d36bd066809e2f52115",
    data: {
      "Alumno": "Diego Pérez Donoso",
      "Documento": "12345",
      "Fecha": "2025-08-26"
    },
    output_format: "image"
  })
});

const result = await response.json();

// Decodificar imagen
const imageData = atob(result.image_base64);
const imageBlob = new Blob([imageData], { type: 'image/png' });

// Usar coordenadas de firma
const signatures = result.signatures;
for (const [fieldName, coords] of Object.entries(signatures)) {
  console.log(`Campo ${fieldName}: x=${coords.x}, y=${coords.y}`);
  // Aquí puedes posicionar elementos de firma en tu UI
}
```

### Ejemplo 3: Python
```python
import requests
import base64

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

response = requests.post(url, json=payload)
result = response.json()

# Decodificar imagen
image_data = base64.b64decode(result['image_base64'])
with open('documento.png', 'wb') as f:
    f.write(image_data)

# Usar coordenadas de firma
signatures = result['signatures']
for field_name, coords in signatures.items():
    print(f"Campo {field_name}: x={coords['x']}, y={coords['y']}")
```

---

## 🔧 Configuración de Campos de Firma

Para que una plantilla incluya coordenadas de firma, debe tener configurados campos de firma en su metadata:

```json
{
  "mapping": {
    "_signatures": {
      "firma_alumno": {
        "x": 351,
        "y": 107,
        "width": 200,
        "height": 100
      },
      "firma_profesor": {
        "x": 500,
        "y": 200,
        "width": 200,
        "height": 100
      }
    }
  }
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | ✅ Éxito |
| 400 | ❌ Error en los datos de entrada |
| 404 | ❌ Plantilla no encontrada |
| 500 | ❌ Error interno del servidor |

---

## 📝 Notas Importantes

1. **Formato de Imagen**: Las imágenes se devuelven en formato PNG
2. **Codificación**: Tanto PDF como imágenes se devuelven en base64
3. **Coordenadas**: Las coordenadas están en píxeles y son relativas al documento
4. **Campos de Firma**: Solo se incluyen si están configurados en la plantilla
5. **Tamaño**: Las imágenes mantienen la resolución original del PDF

---

## 🧪 Plantillas de Prueba

### Template ID: `4beba2ce11614d36bd066809e2f52115`
- **Tipo**: PDF
- **Campos**: Alumno, Documento, Fecha, Logotipo
- **Campos de Firma**: Configurados según metadata

---

## 📞 Soporte

Para dudas o problemas, contactar al equipo de desarrollo de GenDoc.
