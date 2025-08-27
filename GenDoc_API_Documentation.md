# GenDoc API - Documentación para Integración

## 📋 Descripción General

GenDoc es un servicio de generación de PDFs basado en plantillas que permite renderizar documentos personalizados usando datos JSON. El servicio soporta plantillas PDF, DOCX y XLSX con campos dinámicos, incluyendo imágenes desde URLs.

## 🌐 Configuración del Servicio

### URL del Servicio
- **Demo/Desarrollo**: `https://1aca264c0a2c.ngrok-free.app/`
- **Producción**: `https://tu-servidor-gendoc.com` (cambiar según tu despliegue)

## 🔌 Endpoints Principales

### 1. Renderizado de PDF
```http
POST /api/render/{template_id}
Content-Type: application/json
```

**Parámetros:**
- `template_id`: ID único de la plantilla (ej: `4beba2ce11614d36bd066809e2f52115`)

**Body (JSON):**
```json
{
  "Alumno": "Diego Pérez",
  "Documento": "12345678",
  "Fecha": "2025-01-15",
  "Logotipo": "https://ejemplo.com/logo.png"
}
```

**Respuesta:**
- **200 OK**: Archivo PDF en el body de la respuesta
- **400 Bad Request**: Error en los datos o plantilla
- **404 Not Found**: Plantilla no encontrada

### 2. Listar Plantillas Disponibles
```http
GET /api/templates
```

**Respuesta:**
```json
[
  {
    "id": "4beba2ce11614d36bd066809e2f52115",
    "name": "DR",
    "kind": "pdf",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

### 3. Obtener Información de Plantilla
```http
GET /api/templates/{template_id}
```

### 4. Obtener Schema de Plantilla
```http
GET /api/templates/{template_id}/schema
```

## 🎯 Ejemplo con Plantilla "DR"

### Plantilla Actual: DR
- **ID**: `4beba2ce11614d36bd066809e2f52115`
- **Tipo**: PDF con overlay
- **Campos configurados**: Alumno, Documento, Fecha, Logotipo

### Datos de Ejemplo para DR

#### Ejemplo Básico
```json
{
  "Alumno": "Diego Pérez",
  "Documento": "12345678",
  "Fecha": "2025-01-15",
  "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
}
```

#### Ejemplo con Placeholder
```json
{
  "Alumno": "Ana García",
  "Documento": "87654321",
  "Fecha": "2025-01-20",
  "Logotipo": "https://via.placeholder.com/200x80/0066cc/ffffff?text=Logo"
}
```

#### Ejemplo con Imagen Base64
```json
{
  "Alumno": "Carlos López",
  "Documento": "11223344",
  "Fecha": "2025-01-25",
  "Logotipo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
}
```

## 💻 Ejemplos de Integración

### Python
```python
import requests
import json

# CONFIGURACIÓN - CAMBIAR URL SEGÚN DESPLIEGUE
GENDOC_URL = "http://localhost:8080"  # Cambiar por URL de producción
TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115"  # Plantilla DR

# Datos para el renderizado
data = {
    "Alumno": "Diego Pérez",
    "Documento": "12345678",
    "Fecha": "2025-01-15",
    "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
}

# Llamada al API
response = requests.post(
    f"{GENDOC_URL}/api/render/{TEMPLATE_ID}",
    json=data,
    headers={"Content-Type": "application/json"},
    timeout=30
)

if response.status_code == 200:
    # Guardar el PDF generado
    with open("documento_generado.pdf", "wb") as f:
        f.write(response.content)
    print("�?PDF generado exitosamente")
else:
    print(f"�?Error: {response.status_code}")
    print(response.text)
```

### JavaScript/Node.js
```javascript
const axios = require('axios');
const fs = require('fs');

async function generarPDF() {
    // CONFIGURACIÓN - CAMBIAR URL SEGÚN DESPLIEGUE
    const GENDOC_URL = "http://localhost:8080";  // Cambiar por URL de producción
    const TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115";  // Plantilla DR
    
    const data = {
        "Alumno": "Diego Pérez",
        "Documento": "12345678",
        "Fecha": "2025-01-15",
        "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
    };
    
    try {
        const response = await axios.post(
            `${GENDOC_URL}/api/render/${TEMPLATE_ID}`,
            data,
            {
                responseType: 'arraybuffer',
                headers: { 'Content-Type': 'application/json' },
                timeout: 30000
            }
        );
        
        fs.writeFileSync('documento_generado.pdf', response.data);
        console.log('�?PDF generado exitosamente');
    } catch (error) {
        console.error('�?Error:', error.response?.data || error.message);
    }
}

generarPDF();
```

### cURL
```bash
# CONFIGURACIÓN - CAMBIAR URL SEGÚN DESPLIEGUE
GENDOC_URL="http://localhost:8080"  # Cambiar por URL de producción
TEMPLATE_ID="4beba2ce11614d36bd066809e2f52115"  # Plantilla DR

curl -X POST \
  ${GENDOC_URL}/api/render/${TEMPLATE_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "Alumno": "Diego Pérez",
    "Documento": "12345678",
    "Fecha": "2025-01-15",
    "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
  }' \
  --output documento_generado.pdf \
  --max-time 30
```

### PHP
```php
<?php
// CONFIGURACIÓN - CAMBIAR URL SEGÚN DESPLIEGUE
$GENDOC_URL = "http://localhost:8080";  // Cambiar por URL de producción
$TEMPLATE_ID = "4beba2ce11614d36bd066809e2f52115";  // Plantilla DR

$data = [
    "Alumno" => "Diego Pérez",
    "Documento" => "12345678",
    "Fecha" => "2025-01-15",
    "Logotipo" => "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "{$GENDOC_URL}/api/render/{$TEMPLATE_ID}");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 30);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    file_put_contents('documento_generado.pdf', $response);
    echo "�?PDF generado exitosamente\n";
} else {
    echo "�?Error: HTTP {$httpCode}\n";
    echo $response . "\n";
}
?>
```

## 🔧 Cliente Python Completo

```python
import requests
import json
from typing import Dict, Any, Optional

class GenDocClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Inicializar cliente GenDoc
        
        Args:
            base_url: URL del servicio GenDoc (cambiar para producción)
        """
        self.base_url = base_url.rstrip('/')
    
    def list_templates(self) -> Dict[str, Any]:
        """Listar todas las plantillas disponibles"""
        response = requests.get(f"{self.base_url}/api/templates")
        response.raise_for_status()
        return response.json()
    
    def get_template_info(self, template_id: str) -> Dict[str, Any]:
        """Obtener información de una plantilla específica"""
        response = requests.get(f"{self.base_url}/api/templates/{template_id}")
        response.raise_for_status()
        return response.json()
    
    def render_pdf(self, template_id: str, data: Dict[str, Any]) -> bytes:
        """
        Renderizar PDF con una plantilla y datos
        
        Args:
            template_id: ID de la plantilla
            data: Datos para el renderizado
            
        Returns:
            bytes: Contenido del PDF
        """
        response = requests.post(
            f"{self.base_url}/api/render/{template_id}",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.content
    
    def save_pdf(self, template_id: str, data: Dict[str, Any], filename: str) -> str:
        """
        Renderizar y guardar PDF
        
        Args:
            template_id: ID de la plantilla
            data: Datos para el renderizado
            filename: Nombre del archivo de salida
            
        Returns:
            str: Nombre del archivo guardado
        """
        pdf_content = self.render_pdf(template_id, data)
        with open(filename, "wb") as f:
            f.write(pdf_content)
        return filename

# Ejemplo de uso
if __name__ == "__main__":
    # CONFIGURACIÓN - CAMBIAR URL SEGÚN DESPLIEGUE
    client = GenDocClient("http://localhost:8080")  # Cambiar para producción
    
    # Listar plantillas disponibles
    try:
        templates = client.list_templates()
        print("📋 Plantillas disponibles:")
        for template in templates:
            print(f"  - {template['name']} (ID: {template['id']})")
    except Exception as e:
        print(f"�?Error al listar plantillas: {e}")
    
    # Datos para la plantilla DR
    data = {
        "Alumno": "Diego Pérez",
        "Documento": "12345678",
        "Fecha": "2025-01-15",
        "Logotipo": "https://idlogisticsgestor.iformalia.es/assets/css/custom/idlogistics/logo-portada.png"
    }
    
    # Renderizar PDF con plantilla DR
    try:
        filename = client.save_pdf("4beba2ce11614d36bd066809e2f52115", data, "mi_documento.pdf")
        print(f"�?PDF guardado como: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"�?Error al generar PDF: {e}")
```

## 📝 Tipos de Datos Soportados

### Campos de Texto
- **String**: Texto simple
- **Number**: Números
- **Date**: Fechas en formato ISO (YYYY-MM-DD)

### Campos de Imagen
- **URL HTTP/HTTPS**: `https://ejemplo.com/imagen.png`
- **Base64**: `data:image/png;base64,iVBORw0KGgo...`
- **Placeholder**: `https://via.placeholder.com/200x100/color/texto`

## ⚠️ Consideraciones Importantes

### URLs de Imagen
- **Soporte**: PNG, JPG, SVG (conversión automática)
- **Timeout**: 10 segundos por imagen
- **User-Agent**: Mozilla/5.0 para compatibilidad

### Límites
- **Tamaño de imagen**: Hasta 10MB por imagen
- **Timeout total**: 30 segundos por request
- **Formato de salida**: PDF

### Errores Comunes
- **404**: Plantilla no encontrada
- **400**: Datos inválidos o campos faltantes
- **500**: Error interno del servidor
- **Timeout**: Imagen no accesible o servidor lento

## 🔒 Seguridad

- **CORS**: Configurado para permitir requests desde cualquier origen
- **Autenticación**: No requerida en la versión actual
- **Validación**: Los datos se validan contra el schema de la plantilla

## 📞 Soporte

Para problemas o consultas sobre la integración:
- **Repositorio**: https://github.com/dperezinnopulse/GenDoc
- **Issues**: Crear issue en GitHub con detalles del problema

---

**Nota**: Recuerda cambiar `http://localhost:8080` por la URL real de tu servicio GenDoc en producción.



