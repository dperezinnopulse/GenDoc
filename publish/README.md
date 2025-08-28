# 📦 Archivos de Despliegue - GenDoc Ubuntu

Esta carpeta contiene todos los archivos necesarios para desplegar la aplicación GenDoc en un servidor Ubuntu.

## 📁 Archivos Incluidos

### 🐳 **Docker**
- **`Dockerfile`** - Configuración del contenedor Docker
- **`docker-compose.yml`** - Orquestación de servicios

### ⚙️ **Aplicación**
- **`app/`** - Código fuente de la aplicación
- **`requirements.txt`** - Dependencias de Python

### 🚀 **Despliegue**
- **`deploy.sh`** - Script automático de despliegue

## 🛠️ Instrucciones de Despliegue

### 1. Instalar Docker (si no está instalado)
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Cerrar sesión y volver a iniciar, o ejecutar: newgrp docker
```

### 2. Copiar archivos al servidor
```bash
# Copiar esta carpeta al servidor Ubuntu
scp -r publish/ usuario@servidor:/ruta/destino/
```

### 3. Desplegar automáticamente
```bash
cd /ruta/destino/publish
chmod +x deploy.sh
./deploy.sh
```

## 🌐 URLs de Acceso

Una vez desplegado:
- **Aplicación principal**: http://localhost:8080
- **Documentación API**: http://localhost:8080/docs
- **Interfaz de administración**: http://localhost:8080/admin
- **Health check**: http://localhost:8080/health

## 📊 Comandos de Gestión

```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down

# Ver estado
docker-compose ps
```

## 📋 Prerrequisitos

- Ubuntu 18.04 o superior
- Docker (v20.10+)
- Docker Compose (v2.0+)
- 2GB RAM mínimo
- 2GB espacio libre

## 🔗 Enlaces Útiles

- **Repositorio**: https://github.com/dperezinnopulse/GenDoc
- **API Docs**: http://localhost:8080/docs (después del despliegue)
