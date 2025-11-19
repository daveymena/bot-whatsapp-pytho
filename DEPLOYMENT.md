# 🚀 Guía de Despliegue en Producción

## Opciones de Despliegue

### 1. VPS (Recomendado)
- DigitalOcean
- AWS EC2
- Google Cloud
- Linode
- Vultr

### 2. Docker (Más Fácil)
- Docker Compose incluido
- Fácil de escalar
- Aislamiento de servicios

### 3. Serverless (Avanzado)
- AWS Lambda + RDS
- Google Cloud Functions
- Requiere adaptaciones

---

## Despliegue con Docker

### Requisitos
- Docker 20+
- Docker Compose 2+

### Pasos

1. **Clonar repositorio en servidor**
```bash
git clone <tu-repo>
cd whatsapp-sales-bot
```

2. **Configurar .env**
```bash
cp .env.example .env
nano .env
```

3. **Construir y ejecutar**
```bash
docker-compose up -d
```

4. **Ver logs**
```bash
docker-compose logs -f
```

5. **Conectar WhatsApp**
```bash
# Ver QR en logs de Baileys
docker-compose logs baileys
```

---

## Despliegue en VPS (Ubuntu 22.04)

### 1. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip nodejs npm postgresql git

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Configurar PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE botwhatsapp;
CREATE USER botuser WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE botwhatsapp TO botuser;
\q
```

### 3. Clonar y Configurar

```bash
cd /opt
sudo git clone <tu-repo> whatsapp-bot
cd whatsapp-bot
sudo chown -R $USER:$USER .

# Configurar .env
nano .env
```

### 4. Instalar Dependencias

```bash
# Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node.js
npm install
```

### 5. Inicializar Base de Datos

```bash
python3 -c "from database.connection import init_db; init_db()"
python3 seed_database.py
```

### 6. Configurar PM2

```bash
# Instalar PM2
sudo npm install -g pm2

# Iniciar servicios
pm2 start baileys-server.js --name baileys
pm2 start "python3 main.py" --name python-api

# Guardar configuración
pm2 save
pm2 startup
```

### 7. Configurar Nginx (Opcional)

```bash
sudo apt install nginx

# Crear configuración
sudo nano /etc/nginx/sites-available/whatsapp-bot
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/whatsapp-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## Configuración de Firewall

```bash
# UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## Monitoreo y Logs

### PM2 Logs
```bash
pm2 logs
pm2 logs baileys
pm2 logs python-api
```

### Monitoreo en Tiempo Real
```bash
pm2 monit
```

### Logs del Sistema
```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## Backups Automáticos

### Script de Backup

```bash
nano /opt/backup-bot.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio
mkdir -p $BACKUP_DIR

# Backup de base de datos
pg_dump -U botuser botwhatsapp > $BACKUP_DIR/db_$DATE.sql

# Backup de sesiones WhatsApp
tar -czf $BACKUP_DIR/sessions_$DATE.tar.gz /opt/whatsapp-bot/data

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completado: $DATE"
```

```bash
chmod +x /opt/backup-bot.sh

# Agregar a crontab (diario a las 2 AM)
crontab -e
0 2 * * * /opt/backup-bot.sh
```

---

## Actualizaciones

```bash
cd /opt/whatsapp-bot

# Detener servicios
pm2 stop all

# Actualizar código
git pull

# Actualizar dependencias
pip install -r requirements.txt
npm install

# Reiniciar servicios
pm2 restart all
```

---

## Seguridad

### 1. Variables de Entorno
- Nunca subas .env al repositorio
- Usa contraseñas fuertes
- Rota API keys regularmente

### 2. Base de Datos
- Usa contraseñas complejas
- Limita acceso por IP
- Backups encriptados

### 3. Servidor
- Mantén el sistema actualizado
- Usa SSH con llaves
- Deshabilita root login
- Configura fail2ban

### 4. WhatsApp
- No compartas sesiones
- Monitorea actividad sospechosa
- Respeta límites de mensajes

---

## Troubleshooting en Producción

### Bot se desconecta
```bash
pm2 restart all
pm2 logs
```

### Error de base de datos
```bash
sudo systemctl status postgresql
sudo systemctl restart postgresql
```

### Alto uso de CPU
```bash
pm2 monit
htop
```

### Memoria llena
```bash
df -h
du -sh /opt/whatsapp-bot/*
```

---

## Escalabilidad

### Múltiples Instancias
```bash
pm2 start baileys-server.js -i 2
pm2 start main.py -i 4
```

### Load Balancer
- Nginx upstream
- HAProxy
- AWS ELB

### Base de Datos
- PostgreSQL replication
- Connection pooling
- Índices optimizados

---

## Costos Estimados

### VPS Básico
- DigitalOcean: $12/mes (2GB RAM)
- AWS EC2 t3.small: ~$15/mes
- Linode: $10/mes (2GB RAM)

### Servicios
- Dominio: $10-15/año
- SSL: Gratis (Let's Encrypt)
- GROQ API: Gratis (con límites)

### Total Estimado
**$15-20/mes** para operación básica

---

## Checklist de Despliegue

- [ ] Servidor configurado
- [ ] PostgreSQL instalado y configurado
- [ ] Código clonado
- [ ] .env configurado con credenciales
- [ ] Dependencias instaladas
- [ ] Base de datos inicializada
- [ ] PM2 configurado
- [ ] Nginx configurado (opcional)
- [ ] SSL configurado (opcional)
- [ ] Firewall configurado
- [ ] Backups automáticos configurados
- [ ] WhatsApp conectado
- [ ] Pruebas realizadas
- [ ] Monitoreo activo

---

## Soporte Post-Despliegue

### Monitoreo Recomendado
- UptimeRobot (gratis)
- New Relic
- Datadog
- Sentry (errores)

### Alertas
- Email en caídas
- Slack/Telegram notifications
- SMS para críticos

---

## Mantenimiento

### Diario
- Revisar logs
- Verificar conexión WhatsApp

### Semanal
- Revisar métricas
- Limpiar logs antiguos
- Verificar backups

### Mensual
- Actualizar dependencias
- Revisar seguridad
- Optimizar base de datos
