@echo off
REM Script de despliegue para GenDoc en Windows

echo 🚀 Iniciando despliegue de GenDoc en Windows...

REM Variables
set IMAGE_NAME=gendoc-preprod
set CONTAINER_NAME=gendoc-preprod
set PORT=8080

REM Verificar que Docker esté instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker no está instalado. Por favor, instala Docker Desktop primero.
    pause
    exit /b 1
)

REM Verificar que Docker Compose esté instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose no está instalado. Por favor, instala Docker Compose primero.
    pause
    exit /b 1
)

echo ✅ Docker y Docker Compose verificados

REM Parar y eliminar contenedor existente si existe
echo 📋 Deteniendo contenedor existente...
docker-compose down 2>nul

REM Eliminar imagen existente
echo 🗑️ Eliminando imagen existente...
docker rmi %IMAGE_NAME% 2>nul

REM Construir nueva imagen
echo 🔨 Construyendo nueva imagen Docker...
docker-compose build --no-cache

REM Iniciar servicios
echo 🚀 Iniciando servicios...
docker-compose up -d

REM Esperar a que el servicio esté listo
echo ⏳ Esperando a que el servicio esté listo...
timeout /t 10 /nobreak >nul

REM Verificar que el servicio esté funcionando
echo 🔍 Verificando estado del servicio...
curl -f http://localhost:%PORT%/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️ El servicio puede estar aún iniciando. Verificando logs...
    docker-compose logs --tail=20
) else (
    echo ✅ Servicio desplegado correctamente en http://localhost:%PORT%
)

REM Mostrar información del despliegue
echo.
echo 📋 Información del despliegue:
echo    • URL: http://localhost:%PORT%
echo    • API Docs: http://localhost:%PORT%/docs
echo    • Admin: http://localhost:%PORT%/admin
echo.
echo 📊 Comandos útiles:
echo    • Ver logs: docker-compose logs -f
echo    • Parar servicio: docker-compose down
echo    • Reiniciar: docker-compose restart
echo    • Ver estado: docker-compose ps

echo.
echo 🎉 ¡Despliegue completado!
pause
