# 🔗 Configuración de Webhooks - Guía Paso a Paso

## 📋 Requisitos Previos

Antes de configurar webhooks, necesitas:

1. ✅ Servidor accesible públicamente (no localhost)
2. ✅ Certificado SSL (HTTPS)
3. ✅ Dominio configurado
4. ✅ Bot funcionando correctamente

## 🌐 Opción 1: Usar Ngrok (Para Testing)

### Paso 1: Instalar Ngrok

```bash
# Descargar de https://ngrok.com/download
# O con chocolatey:
choco install ngrok
```

### Paso 2: Iniciar Túnel

```bash
ngrok http 5000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

### Paso 3: Actualizar .env

```env
BASE_URL=https://abc123.ngrok.io
```

### Paso 4: Reiniciar Bot

```bash
python main.py
```

## 💳 Configurar Mercado Pago

### Paso 1: Acceder al Panel

1. Ir a: https://www.mercadopago.com.co/developers/panel/webhooks
2. Iniciar sesión con tu cuenta

### Paso 2: Crear Webhook

1. Click en "Crear webhook"
2. Seleccionar aplicación
3. Configurar:

```
URL de producción: https://tu-dominio.com/payment/webhook/mercadopago
Eventos: payment
```

### Paso 3: Obtener Credenciales

1. Ir a: https://www.mercadopago.com.co/developers/panel/credentials
2. Copiar "Access Token"
3. Agregar en `.env`:

```env
MERCADOPAGO_ACCESS_TOKEN=APP_USR-xxxxxxxxxx
```

### Paso 4: Probar Webhook

```bash
# Hacer una compra de prueba
python test_payment_integration.py
```

### Verificar en Panel

1. Ir a "Webhooks" en el panel
2. Ver "Notificaciones enviadas"
3. Verificar que el estado sea "200 OK"

## 🌎 Configurar PayPal

### Paso 1: Acceder al Dashboard

1. Ir a: https://developer.paypal.com/dashboard/
2. Iniciar sesión

### Paso 2: Crear Aplicación

1. Click en "My Apps & Credentials"
2. Click en "Create App"
3. Nombre: "Bot Ventas WhatsApp"
4. Tipo: "Merchant"

### Paso 3: Configurar URLs

En la configuración de la app:

```
Return URL: https://tu-dominio.com/payment/paypal/success
Cancel URL: https://tu-dominio.com/payment/paypal/cancel
```

### Paso 4: Obtener Credenciales

1. Copiar "Client ID"
2. Copiar "Secret"
3. Agregar en `.env`:

```env
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_secret
PAYPAL_MODE=live  # o sandbox para pruebas
```

### Paso 5: Activar Webhooks (Opcional)

1. En la app, ir a "Webhooks"
2. Click en "Add Webhook"
3. URL: `https://tu-dominio.com/payment/webhook/paypal`
4. Eventos:
   - PAYMENT.SALE.COMPLETED
   - PAYMENT.SALE.DENIED
   - PAYMENT.SALE.REFUNDED

## 🧪 Testing con Sandbox

### Mercado Pago Sandbox

```env
# Usar token de prueba
MERCADOPAGO_ACCESS_TOKEN=TEST-xxxxxxxxxx
```

**Tarjetas de prueba:**

| Tarjeta | Resultado |
|---------|-----------|
| 5031 7557 3453 0604 | Aprobada |
| 5031 4332 1540 6351 | Rechazada |
| 5031 4332 1540 6351 | Pendiente |

### PayPal Sandbox

```env
PAYPAL_MODE=sandbox
```

**Cuentas de prueba:**

1. Ir a: https://developer.paypal.com/dashboard/accounts
2. Crear cuenta de comprador
3. Crear cuenta de vendedor
4. Usar para pruebas

## 🔍 Verificar Webhooks

### Script de Verificación

```python
# test_webhooks.py
import requests

def test_mercadopago_webhook():
    url = "http://localhost:5000/payment/webhook/mercadopago"
    data = {
        "type": "payment",
        "data": {
            "id": "123456789"
        }
    }
    response = requests.post(url, json=data)
    print(f"Mercado Pago: {response.status_code}")

def test_paypal_webhook():
    url = "http://localhost:5000/payment/webhook/paypal"
    data = {
        "event_type": "PAYMENT.SALE.COMPLETED",
        "resource": {
            "id": "PAY-123456789"
        }
    }
    response = requests.post(url, json=data)
    print(f"PayPal: {response.status_code}")

if __name__ == "__main__":
    test_mercadopago_webhook()
    test_paypal_webhook()
```

### Ejecutar Prueba

```bash
python test_webhooks.py
```

## 🚀 Despliegue en Producción

### Opción 1: VPS (Recomendado)

#### Proveedores Sugeridos

- **DigitalOcean:** $5/mes
- **Linode:** $5/mes
- **AWS Lightsail:** $3.50/mes
- **Vultr:** $5/mes

#### Configuración

```bash
# 1. Conectar al servidor
ssh root@tu-servidor

# 2. Instalar dependencias
apt update
apt install python3 python3-pip nginx certbot

# 3. Clonar repositorio
git clone tu-repositorio.git
cd tu-repositorio

# 4. Instalar dependencias Python
pip3 install -r requirements.txt

# 5. Configurar Nginx
nano /etc/nginx/sites-available/bot

# Contenido:
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 6. Activar sitio
ln -s /etc/nginx/sites-available/bot /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 7. Obtener SSL
certbot --nginx -d tu-dominio.com

# 8. Iniciar bot
python3 main.py
```

### Opción 2: Heroku

```bash
# 1. Instalar Heroku CLI
# Descargar de: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Crear app
heroku create tu-app-bot

# 4. Configurar variables
heroku config:set MERCADOPAGO_ACCESS_TOKEN=xxx
heroku config:set PAYPAL_CLIENT_ID=xxx
heroku config:set PAYPAL_CLIENT_SECRET=xxx

# 5. Desplegar
git push heroku main

# 6. Obtener URL
heroku info
# URL: https://tu-app-bot.herokuapp.com
```

### Opción 3: Railway

1. Ir a: https://railway.app
2. Conectar repositorio de GitHub
3. Configurar variables de entorno
4. Desplegar automáticamente

## 🔐 Seguridad de Webhooks

### Validar Firma de Mercado Pago

```python
import hmac
import hashlib

def validate_mercadopago_signature(request):
    x_signature = request.headers.get('x-signature')
    x_request_id = request.headers.get('x-request-id')
    
    # Obtener secret de Mercado Pago
    secret = settings.MERCADOPAGO_WEBHOOK_SECRET
    
    # Calcular firma
    data = f"{x_request_id}{request.body}"
    expected_signature = hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(x_signature, expected_signature)
```

### Validar Webhook de PayPal

```python
from paypalrestsdk import WebhookEvent

def validate_paypal_webhook(request):
    webhook_id = settings.PAYPAL_WEBHOOK_ID
    
    transmission_id = request.headers.get('PAYPAL-TRANSMISSION-ID')
    transmission_time = request.headers.get('PAYPAL-TRANSMISSION-TIME')
    cert_url = request.headers.get('PAYPAL-CERT-URL')
    auth_algo = request.headers.get('PAYPAL-AUTH-ALGO')
    transmission_sig = request.headers.get('PAYPAL-TRANSMISSION-SIG')
    
    return WebhookEvent.verify(
        transmission_id,
        transmission_time,
        webhook_id,
        request.body,
        cert_url,
        auth_algo,
        transmission_sig
    )
```

## 📊 Monitoreo de Webhooks

### Logs

```python
# Agregar en payment_routes.py
import logging

logger = logging.getLogger(__name__)

@router.post("/webhook/mercadopago")
async def mercadopago_webhook(request: Request):
    logger.info(f"Webhook recibido: {await request.json()}")
    # ... resto del código
```

### Dashboard de Webhooks

Crear endpoint para ver webhooks recibidos:

```python
@router.get("/webhooks/history")
async def webhook_history():
    db = SessionLocal()
    webhooks = db.query(WebhookLog).order_by(
        WebhookLog.created_at.desc()
    ).limit(100).all()
    db.close()
    
    return {
        "total": len(webhooks),
        "webhooks": [
            {
                "id": w.id,
                "type": w.type,
                "status": w.status,
                "created_at": w.created_at
            }
            for w in webhooks
        ]
    }
```

## 🆘 Solución de Problemas

### Webhook no se recibe

**Verificar:**

1. ✅ URL correcta en panel de Mercado Pago/PayPal
2. ✅ Servidor accesible públicamente
3. ✅ Puerto 5000 abierto
4. ✅ SSL configurado correctamente
5. ✅ Firewall no bloquea conexiones

**Probar manualmente:**

```bash
curl -X POST https://tu-dominio.com/payment/webhook/mercadopago \
  -H "Content-Type: application/json" \
  -d '{"type":"payment","data":{"id":"123"}}'
```

### Error 401 Unauthorized

**Solución:**

1. Verificar Access Token en `.env`
2. Regenerar token en panel de Mercado Pago
3. Verificar que no haya espacios en el token

### Error 500 Internal Server Error

**Solución:**

1. Ver logs del servidor: `tail -f logs/bot.log`
2. Verificar base de datos conectada
3. Verificar todas las dependencias instaladas

## 📞 Soporte

Si tienes problemas:

1. **Revisar logs:** `logs/bot.log`
2. **Ejecutar pruebas:** `python test_payment_integration.py`
3. **Contactar soporte:**
   - Email: daveymena16@gmail.com
   - WhatsApp: +57 300 556 0186

---

**¡Webhooks configurados correctamente! 🎉**

Tu bot ahora puede recibir notificaciones automáticas de pagos y confirmar órdenes sin intervención manual.
