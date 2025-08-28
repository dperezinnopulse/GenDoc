#!/bin/bash

# Script de despliegue para GenDoc en Ubuntu

set -e

echo "🚀 Iniciando despliegue de GenDoc en Ubuntu..."

# Variables
IMAGE_NAME="gendoc-preprod"
CONTAINER_NAME="gendoc-preprod"
PORT="8080"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instala Docker primero."
    print_status "Comando para instalar Docker: sudo apt update && sudo apt install docker.io docker-compose"
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor, instala Docker Compose primero."
    print_status "Comando para instalar Docker Compose: sudo apt install docker-compose"
    exit 1
fi

# Verificar que el usuario esté en el grupo docker
if ! groups $USER | grep -q docker; then
    print_warning "El usuario no está en el grupo docker. Agregando..."
    sudo usermod -aG docker $USER
    print_status "Por favor, cierra sesión y vuelve a iniciar sesión, o ejecuta: newgrp docker"
    exit 1
fi

print_status "✅ Docker y Docker Compose verificados"

# Crear directorios necesarios
print_status "📁 Creando directorios necesarios..."
mkdir -p storage/templates logs

# Parar y eliminar contenedor existente si existe
print_status "📋 Deteniendo contenedor existente..."
docker-compose down 2>/dev/null || true

# Eliminar imagen existente
print_status "🗑️ Eliminando imagen existente..."
docker rmi $IMAGE_NAME 2>/dev/null || true

# Construir nueva imagen
print_status "🔨 Construyendo nueva imagen Docker..."
docker-compose build --no-cache

# Iniciar servicios
print_status "🚀 Iniciando servicios..."
docker-compose up -d

# Esperar a que el servicio esté listo
print_status "⏳ Esperando a que el servicio esté listo..."
sleep 15

# Verificar que el servicio esté funcionando
print_status "🔍 Verificando estado del servicio..."
if curl -f http://localhost:$PORT/health 2>/dev/null; then
    print_status "✅ Servicio desplegado correctamente en http://localhost:$PORT"
else
    print_warning "⚠️ El servicio puede estar aún iniciando. Verificando logs..."
    docker-compose logs --tail=20
fi

# Mostrar información del despliegue
echo ""
print_status "📋 Información del despliegue:"
echo "   • URL: http://localhost:$PORT"
echo "   • API Docs: http://localhost:$PORT/docs"
echo "   • Admin: http://localhost:$PORT/admin"
echo "   • Health Check: http://localhost:$PORT/health"
echo ""
print_status "📊 Comandos útiles:"
echo "   • Ver logs: docker-compose logs -f"
echo "   • Parar servicio: docker-compose down"
echo "   • Reiniciar: docker-compose restart"
echo "   • Ver estado: docker-compose ps"
echo "   • Ver estadísticas: docker stats"

echo ""
print_status "🎉 ¡Despliegue completado!"
