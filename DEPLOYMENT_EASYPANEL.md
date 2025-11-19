# 🚀 GUÍA DE DEPLOYMENT A EASYPANEL

## 📋 PREPARACIÓN

### 1. Archivos Necesarios
✅ `Dockerfile` - Imagen principal Python
✅ `Dockerfile.baileys` - Imagen Baileys (WhatsApp)
✅ `docker-compose.prod.yml` - Configuración producción
✅ `easypanel.yml` - Configuración Easypanel
✅ `.dockerignore` - Optimización build
✅ `requirements.txt` - Dependencias Python
✅ `package.json` - Dependencias Node

### 2. Variables de Entorno Requeridas
Crea un archivo `.env.production` con:

```env
# Base de Datos
DB_PASSWORD=tu_password_seguro_aqui

# IA - GROQ (Requerido)
GROQ_API_KEY=gsk_xxxxx
GROQ_API_KEY_2=gsk_xxxxx
GROQ_API_KEY_6=gsk_xxxxx

# IA - OpenAI (Opcional)
OPENAI_API_KEY=sk-xxxxx

# Negocio
BUSINESS_NAME=Tecnovariedades D&S
BUSINESS_PHONE=+57 300 556 0186
BUSINESS_EMAIL=deinermena25@gmail.com
BOT_NAME=Tecnovariedades D&S Bot

# Pagos
NEQUI_NUMBER=3136174267
DAVIPLATA_NUMBER=3136174267
BANK_NAME=Bancolombia
BANK_ACCOUNT_NUMBER=12345678901
MERCADOPAGO_ACCESS_TOKEN=APP_USR-xxxxx
PAYPAL_CLIENT_ID=xxxxx
PAYPAL_CLIENT_SECRET=xxxxx

# Email
SMTP_USER=deinermena25@gmail.com
SMTP_PASSWORD=uccj yqpq vqlt vcie

# Dropshipping
DROPI_AGENT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# GitHub
GITHUB_REPO=tu-usuario/tu-repo
```

---

## 🔧 PASO 1: PREPARAR REPOSITORIO GIT

### 1.1 Inicializar Git (si no existe)
```bash
cd ventas-2
git init
```

### 1.2 Crear .gitignore
```bash
# Ya existe, pero verifica que incluya:
.env
.env.local
.env.production
__pycache__/
node_modules/
data/
temp-media/
temp-images/
*.log
```

### 1.3 Commit inicial
```bash
git add .
git commit -m "feat: Sistema completo de ventas con IA"
```

### 1.4 Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `bot-whatsapp-ventas`
3. Descripción: "Bot de WhatsApp con IA para ventas"
4. Privado o Público (recomendado: Privado)
5. Crear repositorio

### 1.5 Subir código
```bash
git remote add origin https://github.com/TU-USUARIO/bot-whatsapp-ventas.git
git branch -M main
git push -u origin main
```

---

## 🌐 PASO 2: CONFIGURAR EASYPANEL

### 2.1 Acceder a Easypanel
1. Ve a tu panel de Easypanel
2. Inicia sesión

### 2.2 Crear Nuevo Proyecto
1. Click en "New Project"
2. Nombre: `bot-whatsapp`
3. Descripción: "Sistema de ventas con WhatsApp"

### 2.3 Agregar Base de Datos PostgreSQL
1. Click en "Add Service"
2. Selecciona "PostgreSQL"
3. Configuración:
   - Name: `bot-whatsapp-db`
   - Version: `14`
   - Database: `botwhatsapp`
   - Username: `postgres`
   - Password: (genera uno seguro)
   - Storage: `5GB`
4. Click "Create"

### 2.4 Agregar Servidor Baileys (WhatsApp)
1. Click en "Add Service"
2. Selecciona "App from GitHub"
3. Configuración:
   - Name: `bot-whatsapp-baileys`
   - Repository: `tu-usuario/bot-whatsapp-ventas`
   - Branch: `main`
   - Dockerfile: `Dockerfile.baileys`
   - Port: `3001`
   - Health Check: `/health`
4. Variables de entorno:
   ```
   NODE_ENV=production
   PORT=3001
   SESSION_PATH=/data/whatsapp-sessions
   ```
5. Volumes:
   - `/data/whatsapp-sessions` → `2GB`
6. Click "Deploy"

### 2.5 Agregar Backend Python
1. Click en "Add Service"
2. Selecciona "App from GitHub"
3. Configuración:
   - Name: `bot-whatsapp-python`
   - Repository: `tu-usuario/bot-whatsapp-ventas`
   - Branch: `main`
   - Dockerfile: `Dockerfile`
   - Port: `5000`
   - Health Check: `/health`
   - Public: ✅ (activar)
4. Variables de entorno (copiar todas del `.env.production`)
5. Volumes:
   - `/data/whatsapp-sessions` → `2GB` (mismo que Baileys)
   - `/app/temp-media` → `1GB`
6. Dependencies:
   - Depends on: `bot-whatsapp-db`, `bot-whatsapp-baileys`
7. Click "Deploy"

---

## 🔗 PASO 3: CONFIGURAR DOMINIOS

### 3.1 Dominio Principal (API)
1. En el servicio `bot-whatsapp-python`
2. Click en "Domains"
3. Agregar dominio:
   - `bot-whatsapp.tu-dominio.com`
   - O usar el dominio de Easypanel: `bot-whatsapp-python.sqaoeo.easypanel.host`

### 3.2 Configurar DNS (si usas dominio propio)
Agregar registro CNAME:
```
bot-whatsapp.tu-dominio.com → bot-whatsapp-python.sqaoeo.easypanel.host
```

---

## 🔐 PASO 4: CONFIGURAR VARIABLES DE ENTORNO

### 4.1 En Easypanel
1. Ve al servicio `bot-whatsapp-python`
2. Click en "Environment"
3. Agregar todas las variables del `.env.production`

### 4.2 Variables Críticas
Asegúrate de configurar:
```env
# Base de datos (usar la URL interna de Easypanel)
DATABASE_URL=postgresql://postgres:PASSWORD@bot-whatsapp-db:5432/botwhatsapp

# GROQ API (obligatorio)
GROQ_API_KEY=gsk_xxxxx
GROQ_API_KEY_2=gsk_xxxxx
GROQ_API_KEY_6=gsk_xxxxx

# Negocio
BUSINESS_NAME=Tu Negocio
BUSINESS_PHONE=+57 XXX XXX XXXX
BUSINESS_EMAIL=tu@email.com

# Pagos
NEQUI_NUMBER=XXXXXXXXXX
DAVIPLATA_NUMBER=XXXXXXXXXX
MERCADOPAGO_ACCESS_TOKEN=APP_USR-xxxxx
PAYPAL_CLIENT_ID=xxxxx
PAYPAL_CLIENT_SECRET=xxxxx

# Email
SMTP_USER=tu@gmail.com
SMTP_PASSWORD=tu_app_password
```

---

## 🚀 PASO 5: DEPLOY

### 5.1 Orden de Deploy
1. ✅ Base de datos (ya está corriendo)
2. ✅ Baileys (WhatsApp)
3. ✅ Python API

### 5.2 Verificar Logs
```bash
# En Easypanel, ve a cada servicio y revisa los logs:

# Baileys
- "Server running on port 3001"
- "WhatsApp connected"

# Python API
- "Application startup complete"
- "Uvicorn running on http://0.0.0.0:5000"
```

### 5.3 Verificar Health Checks
```bash
# Baileys
curl https://bot-whatsapp-baileys.sqaoeo.easypanel.host/health

# Python API
curl https://bot-whatsapp-python.sqaoeo.easypanel.host/health
```

---

## 📱 PASO 6: CONECTAR WHATSAPP

### 6.1 Obtener QR Code
1. Ve a los logs de `bot-whatsapp-baileys`
2. Busca el QR code en los logs
3. O accede a: `https://bot-whatsapp-baileys.sqaoeo.easypanel.host/qr`

### 6.2 Escanear QR
1. Abre WhatsApp en tu teléfono
2. Ve a Configuración → Dispositivos vinculados
3. Escanea el QR code

### 6.3 Verificar Conexión
```bash
# Revisa los logs, deberías ver:
"WhatsApp connected successfully"
"Session saved"
```

---

## 🗄️ PASO 7: INICIALIZAR BASE DE DATOS

### 7.1 Ejecutar Migraciones
En Easypanel, abre una terminal en `bot-whatsapp-python`:
```bash
python recreate_subscription_tables.py
python add_sample_products.py
```

### 7.2 Crear Usuario Admin
```bash
python -c "
from database.connection import SessionLocal
from database.models import AdminUser
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db = SessionLocal()

admin = AdminUser(
    email='admin@tudominio.com',
    password=pwd_context.hash('tu_password_seguro'),
    name='Admin',
    role='admin',
    is_active=True,
    email_verified=True
)
db.add(admin)
db.commit()
print('✅ Usuario admin creado')
"
```

---

## ✅ PASO 8: VERIFICACIÓN

### 8.1 Verificar Servicios
```bash
# Health checks
curl https://tu-dominio.com/health

# Respuesta esperada:
{
  "status": "healthy",
  "database": "connected",
  "whatsapp": "connected"
}
```

### 8.2 Probar Bot
1. Envía un mensaje de WhatsApp al número conectado
2. El bot debe responder automáticamente
3. Verifica en los logs que todo funciona

### 8.3 Acceder al Dashboard
```bash
https://tu-dominio.com/admin/login
```

---

## 🔄 PASO 9: ACTUALIZACIONES

### 9.1 Actualizar Código
```bash
# Local
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main

# Easypanel detectará el cambio y redesplegará automáticamente
```

### 9.2 Rollback (si algo falla)
En Easypanel:
1. Ve al servicio
2. Click en "Deployments"
3. Selecciona un deployment anterior
4. Click "Rollback"

---

## 🐛 TROUBLESHOOTING

### Problema: Base de datos no conecta
```bash
# Verificar URL de conexión
echo $DATABASE_URL

# Debe ser:
postgresql://postgres:PASSWORD@bot-whatsapp-db:5432/botwhatsapp
```

### Problema: WhatsApp no conecta
```bash
# Revisar logs de Baileys
# Verificar que el volumen /data/whatsapp-sessions esté montado
# Eliminar sesión y reconectar:
rm -rf /data/whatsapp-sessions/*
```

### Problema: Bot no responde
```bash
# Verificar variables de entorno
env | grep GROQ_API_KEY

# Verificar logs
tail -f /var/log/app.log
```

### Problema: Fotos no se envían
```bash
# Verificar que los productos tengan image_url
# Verificar variable AUTO_SEND_PHOTOS=true
```

---

## 📊 MONITOREO

### Métricas a Vigilar
- CPU usage < 80%
- Memory usage < 80%
- Response time < 2s
- Error rate < 1%

### Logs Importantes
```bash
# Ver logs en tiempo real
# En Easypanel, cada servicio tiene su sección de logs

# Filtrar errores
grep "ERROR" logs.txt

# Filtrar mensajes de WhatsApp
grep "Message received" logs.txt
```

---

## 🔒 SEGURIDAD

### Checklist de Seguridad
- ✅ Variables de entorno en Easypanel (no en código)
- ✅ Base de datos con password fuerte
- ✅ HTTPS habilitado
- ✅ Firewall configurado
- ✅ Backups automáticos activados
- ✅ Logs monitoreados

### Backups
En Easypanel:
1. Ve a "Backups"
2. Configura backup automático diario
3. Retención: 7 días

---

## 📝 CHECKLIST FINAL

Antes de considerar el deployment completo:

- [ ] ✅ Código subido a GitHub
- [ ] ✅ Base de datos PostgreSQL creada
- [ ] ✅ Servidor Baileys desplegado
- [ ] ✅ Backend Python desplegado
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Dominios configurados
- [ ] ✅ WhatsApp conectado (QR escaneado)
- [ ] ✅ Base de datos inicializada
- [ ] ✅ Usuario admin creado
- [ ] ✅ Health checks pasando
- [ ] ✅ Bot respondiendo mensajes
- [ ] ✅ Dashboard accesible
- [ ] ✅ Fotos enviándose automáticamente
- [ ] ✅ Métodos de pago configurados
- [ ] ✅ Backups configurados
- [ ] ✅ Monitoreo activo

---

## 🎉 ¡LISTO!

Tu bot de WhatsApp está desplegado y funcionando en producción.

**URLs importantes:**
- API: `https://bot-whatsapp-python.sqaoeo.easypanel.host`
- Dashboard: `https://bot-whatsapp-python.sqaoeo.easypanel.host/admin`
- Health: `https://bot-whatsapp-python.sqaoeo.easypanel.host/health`

**Próximos pasos:**
1. Monitorear logs las primeras 24 horas
2. Probar todas las funcionalidades
3. Configurar alertas
4. Documentar procesos internos

¿Necesitas ayuda? Revisa los logs o contacta soporte. 🚀
