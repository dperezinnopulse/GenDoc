# 🪟 Guía de Despliegue - Windows

Esta guía te ayudará a desplegar la aplicación GenDoc en un servidor Windows.

## 📋 Prerrequisitos

### Instalar Docker Desktop
1. **Descargar** Docker Desktop desde: https://www.docker.com/products/docker-desktop
2. **Instalar** siguiendo el asistente
3. **Reiniciar** el equipo si es necesario
4. **Verificar** que Docker esté funcionando:
   ```cmd
   docker --version
   docker-compose --version
   ```

### Instalar Git (si no está instalado)
1. **Descargar** Git desde: https://git-scm.com/download/win
2. **Instalar** con opciones por defecto
3. **Verificar** instalación:
   ```cmd
   git --version
   ```

## 🛠️ Pasos de Despliegue

### 1. Clonar el repositorio
```cmd
git clone https://github.com/dperezinnopulse/GenDoc.git
cd GenDoc
```

### 2. Copiar archivos de despliegue
```cmd
xcopy publish\* C:\ruta\del\servidor\ /E /I
cd C:\ruta\del\servidor\
```

### 3. Configurar variables de entorno
```cmd
copy config.preprod.env .env
REM Editar si es necesario con notepad
notepad .env
```

### 4. Desplegar automáticamente
```cmd
deploy.bat
```

## 🌐 URLs de Acceso

Una vez desplegado:
- **Aplicación principal**: http://localhost:8080
- **Documentación API**: http://localhost:8080/docs
- **Interfaz de administración**: http://localhost:8080/admin
- **Health check**: http://localhost:8080/health

## 📊 Comandos de Gestión

### Ver logs en tiempo real
```cmd
docker-compose logs -f
```

### Reiniciar el servicio
```cmd
docker-compose restart
```

### Parar el servicio
```cmd
docker-compose down
```

### Ver estado
```cmd
docker-compose ps
```

## 🔧 Configuración Avanzada

### Cambiar puerto
Editar `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Cambiar 8081 por el puerto deseado
```

### Configurar volúmenes persistentes
```yaml
volumes:
  - ./storage:/app/storage
  - ./logs:/app/logs
```

## 🚨 Troubleshooting

### Problema: Docker no inicia
1. **Verificar** que Docker Desktop esté ejecutándose
2. **Reiniciar** Docker Desktop
3. **Verificar** que WSL2 esté habilitado (Windows 10/11)

### Problema: Puerto ocupado
```cmd
netstat -ano | findstr :8080
taskkill /PID [PID] /F
```

### Problema: Permisos de archivos
```cmd
icacls storage /grant Everyone:F /T
```

## 📈 Monitoreo

### Health Check
```cmd
curl http://localhost:8080/health
```

### Métricas del contenedor
```cmd
docker stats gendoc
```

## 🔒 Seguridad

### Cambiar secret key
```cmd
REM Generar nueva secret key
powershell -Command "[System.Web.Security.Membership]::GeneratePassword(32,0)"

REM Actualizar en .env
notepad .env
```

### Configurar firewall
```cmd
netsh advfirewall firewall add rule name="GenDoc" dir=in action=allow protocol=TCP localport=8080
```

## 📝 Notas Importantes

1. **Backup**: Los templates se almacenan en `.\storage\templates\`
2. **Logs**: Se guardan en el contenedor
3. **Memoria**: La aplicación requiere mínimo 1GB de RAM
4. **Disco**: Mínimo 2GB de espacio libre
5. **CPU**: Recomendado 2 cores mínimo

## 🆘 Soporte

Si encuentras problemas:

1. Revisar logs: `docker-compose logs -f`
2. Verificar configuración: `docker-compose config`
3. Reiniciar servicio: `docker-compose restart`
4. Reconstruir imagen: `docker-compose build --no-cache`

## 📞 Contacto

Para soporte técnico, contacta al equipo de desarrollo.
