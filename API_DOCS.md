# 📚 Documentación de API

## Python API (Puerto 3000)

### Endpoints Principales

#### GET /
**Descripción:** Estado general del bot

**Respuesta:**
```json
{
  "status": "online",
  "bot": "Tecnovariedades D&S Bot",
  "business": "Tecnovariedades D&S",
  "connected": true
}
```

#### GET /health
**Descripción:** Health check del sistema

**Respuesta:**
```json
{
  "status": "healthy",
  "whatsapp_connected": true,
  "ai_provider": "groq"
}
```

#### GET /stats
**Descripción:** Estadísticas del bot

**Respuesta:**
```json
{
  "active_conversations": 5,
  "reconnect_attempts": 0,
  "agents": ["sales", "products", "dropshipping", "reservations", "payment"]
}
```

#### POST /send-message
**Descripción:** Enviar mensaje manualmente

**Body:**
```json
{
  "phone": "573001234567",
  "message": "Hola, ¿cómo estás?"
}
```

**Respuesta:**
```json
{
  "status": "sent",
  "phone": "573001234567"
}
```

#### POST /webhook/message
**Descripción:** Webhook para recibir mensajes desde Baileys

**Body:**
```json
{
  "phone": "573001234567",
  "message": "Quiero comprar un producto",
  "timestamp": 1234567890
}
```

**Respuesta:**
```json
{
  "reply": "¡Hola! Claro, con gusto te ayudo..."
}
```

---

## Baileys API (Puerto 3001)

### Endpoints Principales

#### GET /status
**Descripción:** Estado de la conexión WhatsApp

**Respuesta:**
```json
{
  "connected": true,
  "qrCode": null,
  "reconnectAttempts": 0
}
```

#### GET /qr
**Descripción:** Obtener QR code para conectar

**Respuesta (no conectado):**
```json
{
  "qr": "2@abc123def456..."
}
```

**Respuesta (conectado):**
```json
{
  "message": "Already connected"
}
```

#### POST /send-message
**Descripción:** Enviar mensaje de WhatsApp

**Body:**
```json
{
  "phone": "573001234567@s.whatsapp.net",
  "message": "Hola desde el bot",
  "simulateTyping": true
}
```

**Respuesta:**
```json
{
  "success": true
}
```

#### POST /send-image
**Descripción:** Enviar imagen por WhatsApp

**Body:**
```json
{
  "phone": "573001234567@s.whatsapp.net",
  "imageUrl": "https://example.com/image.jpg",
  "caption": "Mira este producto"
}
```

**Respuesta:**
```json
{
  "success": true
}
```

---

## Formato de Números de Teléfono

### Para Python API
```
573001234567
```

### Para Baileys API
```
573001234567@s.whatsapp.net
```

---

## Códigos de Error

### Python API

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Parámetros faltantes |
| 500 | Internal Server Error - Error del servidor |

### Baileys API

| Código | Descripción |
|--------|-------------|
| 400 | Bad Request - Parámetros inválidos |
| 500 | Internal Server Error - WhatsApp no conectado |

---

## Ejemplos de Uso

### cURL

**Enviar mensaje (Python):**
```bash
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{"phone":"573001234567","message":"Hola"}'
```

**Obtener estado:**
```bash
curl http://localhost:3000/health
```

**Ver QR code:**
```bash
curl http://localhost:3001/qr
```

### Python

```python
import requests

# Enviar mensaje
response = requests.post(
    "http://localhost:3000/send-message",
    json={
        "phone": "573001234567",
        "message": "Hola desde Python"
    }
)
print(response.json())
```

### JavaScript

```javascript
// Enviar mensaje
fetch('http://localhost:3000/send-message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '573001234567',
    message: 'Hola desde JS'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Webhooks

### Configurar Webhook Externo

Si quieres recibir mensajes en tu propio servidor:

1. Modifica `baileys-server.js`
2. Cambia `PYTHON_API_URL` a tu URL
3. Asegúrate de que tu servidor responda con:

```json
{
  "reply": "Mensaje de respuesta"
}
```

---

## Rate Limits

### GROQ API
- 30 requests/minuto por API key
- Rotación automática habilitada

### WhatsApp
- Máximo 1 mensaje/segundo por chat
- Simulación de typing habilitada

---

## Monitoreo

### Logs

**Python:**
```bash
tail -f logs/python.log
```

**Baileys:**
```bash
tail -f logs/baileys.log
```

### Métricas

Accede a `/stats` para ver:
- Conversaciones activas
- Intentos de reconexión
- Agentes disponibles
