# 🚀 Guía de Despliegue - GenDoc Preproducción

Esta guía te ayudará a desplegar la aplicación GenDoc en un servidor de preproducción.

## 📋 Prerrequisitos

### En el servidor de preproducción:
- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)
- **Git** (para clonar el repositorio)
- **curl** (para health checks)

### Verificar instalación:
```bash
docker --version
docker-compose --version
git --version
curl --version
```

## 🛠️ Pasos de Despliegue

### 1. Clonar el repositorio
```bash
git clone https://github.com/dperezinnopulse/GenDoc.git
cd GenDoc
```

### 2. Configurar variables de entorno
```bash
# Copiar archivo de configuración
cp config.preprod.env .env

# Editar configuración si es necesario
nano .env
```

### 3. Desplegar con Docker Compose
```bash
# Opción A: Usar script automático
chmod +x deploy.sh
./deploy.sh

# Opción B: Comandos manuales
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 4. Verificar el despliegue
```bash
# Verificar estado de los contenedores
docker-compose ps

# Verificar health check
curl http://localhost:8080/health

# Ver logs
docker-compose logs -f
```

## 🌐 URLs de Acceso

Una vez desplegado, la aplicación estará disponible en:

- **Aplicación principal**: http://localhost:8080
- **Documentación API**: http://localhost:8080/docs
- **Interfaz de administración**: http://localhost:8080/admin
- **Health check**: http://localhost:8080/health

## 📊 Comandos de Gestión

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Reiniciar el servicio
```bash
docker-compose restart
```

### Parar el servicio
```bash
docker-compose down
```

### Ver estadísticas del contenedor
```bash
docker stats
```

### Acceder al contenedor (debug)
```bash
docker-compose exec gendoc bash
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

### Configurar variables de entorno
```yaml
environment:
  - DEBUG=false
  - LOG_LEVEL=INFO
  - SECRET_KEY=your-secret-key
```

## 🚨 Troubleshooting

### Problema: Contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs

# Verificar recursos del sistema
docker system df
docker system prune
```

### Problema: Puerto ocupado
```bash
# Verificar qué usa el puerto
netstat -tulpn | grep 8080

# Cambiar puerto en docker-compose.yml
```

### Problema: Permisos de archivos
```bash
# Dar permisos al directorio storage
chmod -R 755 storage/
```

## 📈 Monitoreo

### Health Check
```bash
curl -f http://localhost:8080/health
```

### Métricas del contenedor
```bash
docker stats gendoc
```

### Logs estructurados
```bash
docker-compose logs --tail=100 | grep ERROR
```

## 🔒 Seguridad

### Cambiar secret key
```bash
# Generar nueva secret key
openssl rand -hex 32

# Actualizar en .env
SECRET_KEY=tu-nueva-secret-key
```

### Configurar firewall
```bash
# Permitir solo puerto 8080
ufw allow 8080/tcp
```

## 📝 Notas Importantes

1. **Backup**: Los templates se almacenan en `./storage/templates/`
2. **Logs**: Se guardan en el contenedor, configurar volumen si es necesario
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
