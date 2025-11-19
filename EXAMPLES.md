# 💡 Ejemplos de Uso

## Conversaciones de Ejemplo

### 1. Venta de Producto Físico

**Cliente:** Hola, busco un celular

**Bot (Agente de Ventas):** ¡Hola! 👋 Bienvenido a Tecnovariedades D&S. Perfecto, te puedo ayudar con eso. ¿Qué características buscas en tu celular? ¿Tienes algún presupuesto en mente?

**Cliente:** Algo bueno pero no muy caro, máximo 4 millones

**Bot (Agente de Productos):** Excelente, tengo opciones perfectas para ti en ese rango:

📱 **Samsung Galaxy S24**
- Precio: $3,800,000 COP
- IA integrada, pantalla AMOLED
- Cámara profesional
- Stock disponible ✅

📱 **iPhone 15 Pro**
- Precio: $4,500,000 COP (un poco más)
- Chip A17 Pro, cámara 48MP
- Lo último de Apple
- Stock limitado ⚡

¿Cuál te llama más la atención?

**Cliente:** El Samsung se ve bien, pero está muy caro

**Bot (Agente de Ventas - Manejo de Objeción):** Entiendo tu preocupación por el precio 😊 Déjame mostrarte el valor real:

✅ **Inversión a largo plazo**: Este equipo te durará 3-4 años
✅ **Tecnología actual**: IA que mejora tus fotos y rendimiento
✅ **Garantía incluida**: 1 año de respaldo
✅ **Financiación**: Puedes pagar con MercadoPago en cuotas

Además, si decides hoy, te incluyo:
🎁 Funda protectora premium
🎁 Vidrio templado

¿Te parece si lo separamos?

**Cliente:** Ok, me convenciste. ¿Cómo pago?

**Bot (Agente de Pagos):** ¡Excelente decisión! 🎉

**Total a pagar: $3,800,000 COP**

Métodos de pago disponibles:

1️⃣ **Nequi** - Instantáneo
2️⃣ **Daviplata** - Rápido
3️⃣ **Transferencia Bancaria**
4️⃣ **MercadoPago** - Cuotas disponibles
5️⃣ **Contra entrega** - Pagas al recibir

¿Cuál prefieres?

---

### 2. Reserva de Servicio

**Cliente:** Necesito una cita para corte de cabello

**Bot (Agente de Reservas):** ¡Claro! Con gusto te agendo 💇‍♂️

Para tu cita de peluquería necesito:
- ¿Qué día prefieres?
- ¿Horario de preferencia?

Horarios disponibles:
📅 Lunes a Viernes: 8:00 AM - 6:00 PM
📅 Sábados: 9:00 AM - 2:00 PM

**Cliente:** Mañana a las 3 pm

**Bot:** Perfecto, verificando disponibilidad...

✅ **Reserva Confirmada**

📅 Fecha: Mañana 20 de Enero
🕒 Hora: 3:00 PM
💇 Servicio: Corte de cabello
📍 Dirección: [Tu dirección]

Te enviaré un recordatorio 1 hora antes.
¿Necesitas algo más?

---

### 3. Producto Digital

**Cliente:** Venden cursos?

**Bot (Agente de Productos):** ¡Sí! Tenemos cursos digitales excelentes 📚

**Curso de Marketing Digital**
💰 Precio: $150,000 COP
📖 Contenido:
- SEO y SEM
- Redes sociales
- Email marketing
- Analítica web
- Certificación incluida

**Megapack de Diseño Gráfico**
💰 Precio: $80,000 COP
🎨 Incluye:
- 500+ plantillas
- Fuentes premium
- Recursos vectoriales
- Actualizaciones gratis

Entrega inmediata por email ⚡

¿Cuál te interesa?

---

### 4. Dropshipping

**Cliente:** Tienen smartwatch?

**Bot (Agente de Dropshipping):** ¡Sí! Tengo un smartwatch deportivo increíble 🏃‍♂️

⌚ **Smartwatch Deportivo**
💰 Precio: $250,000 COP
✨ Características:
- Monitor de frecuencia cardíaca
- Contador de pasos
- Notificaciones del celular
- Resistente al agua
- Batería 7 días

📦 Envío: 5-7 días hábiles
🚚 Envío incluido a tu ciudad

¿Te gustaría ordenarlo?

**Cliente:** Sí, pero cuánto demora?

**Bot:** El tiempo de entrega es de 5-7 días hábiles 📦

El producto viene directamente del proveedor a tu puerta, por eso el precio es tan competitivo. Incluye:
✅ Envío gratis
✅ Garantía de 30 días
✅ Seguimiento en tiempo real

¿Confirmo tu pedido?

---

## Ejemplos de API

### Enviar Mensaje Manual

```python
import requests

response = requests.post(
    "http://localhost:3000/send-message",
    json={
        "phone": "573001234567",
        "message": "¡Hola! Tenemos una oferta especial para ti"
    }
)
print(response.json())
```

### Consultar Estadísticas

```python
import requests

stats = requests.get("http://localhost:3000/stats").json()
print(f"Conversaciones activas: {stats['active_conversations']}")
print(f"Agentes: {', '.join(stats['agents'])}")
```

### Verificar Estado

```bash
curl http://localhost:3000/health
```

---

## Personalización de Agentes

### Modificar Prompt del Agente de Ventas

Edita `agents/sales_agent.py`:

```python
def get_system_prompt(self) -> str:
    return f"""Eres {self.name} de {settings.BUSINESS_NAME}.

TU PERSONALIDAD:
- Amigable y profesional
- Usa emojis moderadamente
- Enfócate en beneficios, no características
- Crea urgencia sin presionar

TU OBJETIVO:
Convertir cada conversación en una venta.

TÉCNICAS:
1. Escucha activa
2. Identifica necesidades
3. Presenta soluciones
4. Maneja objeciones
5. Cierra la venta

Responde en español de forma natural."""
```

---

## Integración con Dropi

### Obtener Productos

```python
from agents.dropshipping_agent import DropshippingAgent

agent = DropshippingAgent()
products = await agent.get_dropi_products(search="smartwatch")

for product in products:
    print(f"{product['name']}: ${product['price']}")
```

---

## Base de Datos

### Agregar Producto

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

producto = Product(
    name="Nuevo Producto",
    description="Descripción detallada",
    price=100000,
    category="Tecnología",
    stock=50,
    is_digital=False,
    is_dropshipping=False
)

db.add(producto)
db.commit()
```

### Consultar Órdenes

```python
from database.models import Order

orders = db.query(Order).filter(
    Order.status == "pending"
).all()

for order in orders:
    print(f"Orden #{order.id}: ${order.total}")
```

---

## Webhooks Personalizados

### Notificar a Slack cuando hay venta

Edita `main.py`:

```python
import requests

async def notify_sale(order):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    message = {
        "text": f"🎉 Nueva venta: ${order.total} COP"
    }
    
    requests.post(webhook_url, json=message)
```

---

## Testing

### Probar Agente Específico

```python
from agents.sales_agent import SalesAgent

agent = SalesAgent()
response = await agent.process_message(
    "573001234567",
    "Hola, quiero comprar"
)
print(response)
```

### Simular Conversación Completa

```bash
python test_conversation.py
```

---

## Monitoreo

### Ver Logs en Tiempo Real

```bash
# Python
tail -f logs/python.log

# Baileys
tail -f logs/baileys.log

# PM2
pm2 logs
```

### Métricas Personalizadas

```python
from whatsapp.message_handler import message_handler

# Conversaciones activas
active = len(message_handler.user_contexts)

# Por agente
for phone, context in message_handler.user_contexts.items():
    print(f"{phone}: {context['current_agent']}")
```

---

## Casos de Uso Avanzados

### 1. Envío Masivo (Broadcast)

```python
phones = ["573001234567", "573007654321"]
message = "¡Oferta especial hoy!"

for phone in phones:
    await baileys_client.send_message(phone, message)
    await asyncio.sleep(2)  # Evitar spam
```

### 2. Respuestas Automáticas Fuera de Horario

```python
from datetime import datetime

def is_business_hours():
    now = datetime.now()
    return 8 <= now.hour < 18

if not is_business_hours():
    return "Gracias por escribir. Nuestro horario es 8 AM - 6 PM. Te responderemos pronto."
```

### 3. Seguimiento Automático

```python
# Después de 24h sin respuesta
if last_message_time > 24_hours:
    await send_message(
        phone,
        "Hola! Vi que estabas interesado en [producto]. ¿Tienes alguna duda?"
    )
```

---

## Tips y Trucos

### 1. Mejorar Conversión
- Usa urgencia: "Solo quedan 3 unidades"
- Ofrece garantías: "30 días de garantía"
- Facilita el pago: "Acepto Nequi, Daviplata..."

### 2. Personalización
- Guarda nombre del cliente
- Recuerda conversaciones previas
- Recomienda basado en historial

### 3. Optimización
- Respuestas cortas y directas
- Usa emojis relevantes
- Pregunta una cosa a la vez

---

## Recursos Adicionales

- [Documentación Baileys](https://github.com/WhiskeySockets/Baileys)
- [GROQ API Docs](https://console.groq.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
