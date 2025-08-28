# 📦 Archivos de Despliegue - GenDoc

Esta carpeta contiene todos los archivos necesarios para desplegar la aplicación GenDoc en un servidor de preproducción.

## 📁 Archivos Incluidos

### 🐳 **Docker**
- **`Dockerfile`** - Configuración del contenedor Docker
- **`docker-compose.yml`** - Orquestación de servicios
- **`.dockerignore`** - Archivos a ignorar en el build

### ⚙️ **Configuración**
- **`config.preprod.env`** - Variables de entorno para preproducción
- **`deploy.sh`** - Script automático de despliegue

### 📚 **Documentación**
- **`DEPLOYMENT.md`** - Guía completa de despliegue

## 🚀 Instrucciones de Uso

### Para Windows:
1. **Copiar estos archivos** al servidor de preproducción
2. **Instalar Docker Desktop** para Windows
3. **Ejecutar** `deploy.bat` (doble clic o desde cmd)

### Para Linux/Mac:
1. **Copiar estos archivos** al servidor de preproducción
2. **Seguir la guía** en `DEPLOYMENT.md`
3. **Ejecutar** `./deploy.sh` para desplegar automáticamente

## 📋 Prerrequisitos

### Para Windows:
- **Docker Desktop** para Windows (incluye Docker Compose)
- **Git** para Windows
- **curl** (incluido en Windows 10/11)

### Para Linux/Mac:
- Docker (v20.10+)
- Docker Compose (v2.0+)
- Git
- curl

## 🔗 Enlaces Útiles

- **Repositorio**: https://github.com/dperezinnopulse/GenDoc
- **Documentación**: Ver `DEPLOYMENT.md`
- **API Docs**: http://localhost:8080/docs (después del despliegue)
