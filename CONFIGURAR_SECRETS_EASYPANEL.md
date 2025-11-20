# 🔐 Configurar Secretos en Easypanel

## ⚠️ IMPORTANTE

Los archivos de este repositorio NO contienen las API keys reales por seguridad.

Las API keys reales están en tu archivo `.env` local (que NO se sube a Git).

## 📋 Cómo Configurar en Easypanel

### 1. Copia las Variables de tu .env Local

Abre tu archivo `.env` local y copia las siguientes variables:

```env
# IA - GROQ
GROQ_API_KEY=gsk_...
GROQ_API_KEY_2=gsk_...
GROQ_API_KEY_6=gsk_...

# EMAIL - SMTP
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_password_aplicacion

# PAGOS - MERCADOPAGO
MERCADOPAGO_ACCESS_TOKEN=APP_USR-...
MERCADO_PAGO_PUBLIC_KEY=APP_USR-...

# PAGOS - PAYPAL
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...

# GMAIL API
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...
GMAIL_REFRESH_TOKEN=...

# DROPI
DROPI_AGENT_TOKEN=...
```

### 2. Pegar en Easypanel

1. Ve a https://easypanel.io
2. Selecciona tu proyecto
3. Ve al servicio Python
4. Click en "Environment" o "Variables"
5. Pega las variables con sus valores reales
6. Guarda

### 3. Rebuild

Después de configurar las variables:
1. Fuerza un rebuild del servicio
2. Espera 3-5 minutos
3. Verifica los logs

## 🔒 Seguridad

- ✅ Las API keys reales están en `.env` (ignorado por Git)
- ✅ Las API keys reales están en Easypanel (seguro)
- ❌ Las API keys NO están en el repositorio público
- ❌ Las API keys NO están en archivos de documentación

## 📝 Archivo de Plantilla

El archivo `VARIABLES_EASYPANEL.txt` es una PLANTILLA con valores de ejemplo.

Reemplaza los valores de ejemplo con tus valores reales en Easypanel.

## ✅ Checklist

- [ ] Copié las variables de mi `.env` local
- [ ] Pegué en Easypanel con valores reales
- [ ] Guardé los cambios
- [ ] Forcé un rebuild
- [ ] Verifiqué los logs
- [ ] El sistema funciona correctamente
