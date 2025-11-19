# 🚀 Guía Rápida - Sistema de Pagos y Fotos

## ⚡ Inicio Rápido

### 1. Instalar Dependencias

```bash
# Opción 1: Automático
INSTALL_PAYMENTS.bat

# Opción 2: Manual
pip install mercadopago==2.2.1 paypalrestsdk==1.13.1
```

### 2. Configurar Credenciales

Edita el archivo `.env`:

```env
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=tu_token_aqui

# PayPal
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_secret
PAYPAL_MODE=live  # o sandbox para pruebas

# Pagos Manuales
NEQUI_NUMBER=3136174267
DAVIPLATA_NUMBER=3136174267
BANK_ACCOUNT_NUMBER=12345678901
```

### 3. Iniciar Sistema

```bash
START_WITH_PAYMENTS.bat
```

## 💬 Ejemplos de Conversación

### Compra con Mercado Pago

```
👤 Cliente: Hola
🤖 Bot: ¡Hola! ¿En qué puedo ayudarte?

👤 Cliente: Quiero ver productos
🤖 Bot: [Envía catálogo con fotos]

👤 Cliente: El iPhone 13
🤖 Bot: [Envía fotos del iPhone 13]
     📦 iPhone 13
     💰 $2,500,000 COP
     📊 Stock: 5 unidades

👤 Cliente: Lo quiero
🤖 Bot: ¿Cómo deseas pagar?

👤 Cliente: Mercado Pago
🤖 Bot: ✅ Link de pago generado
     💳 https://mpago.la/xxx
     
     Puedes pagar con:
     • Tarjetas crédito/débito
     • PSE
     • Hasta 12 cuotas

[Cliente paga en el link]

🤖 Bot: ✅ ¡Pago confirmado!
     Pedido: #ORD-20250119-ABC123
     Tu pedido será enviado en 24-48h
```

### Compra con Nequi

```
👤 Cliente: Buscar audífonos
🤖 Bot: [Envía fotos de audífonos]

👤 Cliente: Los Sony
🤖 Bot: [Envía fotos detalladas]

👤 Cliente: Comprar con Nequi
🤖 Bot: 💜 PAGO POR NEQUI
     Número: 3136174267
     Total: $150,000 COP
     
     Envía el comprobante después de pagar

[Cliente transfiere]

👤 Cliente: [Envía foto del comprobante]
🤖 Bot: Recibido! Verificando...

👤 Cliente: Confirmar pago
🤖 Bot: ✅ ¡Pago confirmado!
     Gracias por tu compra 🎉
```

## 🎯 Comandos Principales

### Productos y Fotos

| Comando | Acción |
|---------|--------|
| `catálogo` | Muestra catálogo con fotos |
| `buscar [producto]` | Busca producto específico |
| `fotos` | Envía fotos del producto actual |
| `más fotos` | Envía fotos adicionales |
| `categoría [nombre]` | Filtra por categoría |

### Pagos

| Comando | Acción |
|---------|--------|
| `mercadopago` o `mp` | Genera link de Mercado Pago |
| `paypal` | Genera link de PayPal |
| `nequi` | Muestra datos de Nequi |
| `daviplata` | Muestra datos de Daviplata |
| `banco` | Muestra datos bancarios |
| `contraentrega` | Pago al recibir |
| `confirmar pago` | Confirma pago manual |

## 🔧 Solución de Problemas

### Error: "Mercado Pago no configurado"

**Solución:**
1. Obtén tu Access Token en: https://www.mercadopago.com.co/developers/panel/credentials
2. Agrégalo en `.env`: `MERCADOPAGO_ACCESS_TOKEN=tu_token`
3. Reinicia el bot

### Error: "PayPal authentication failed"

**Solución:**
1. Verifica tus credenciales en: https://developer.paypal.com/dashboard/
2. Asegúrate de usar el modo correcto (`sandbox` o `live`)
3. Verifica que `PAYPAL_CLIENT_ID` y `PAYPAL_CLIENT_SECRET` estén correctos

### Las fotos no se envían

**Solución:**
1. Verifica que `PHOTOS_ENABLED=true` en `.env`
2. Asegúrate de que los productos tengan `image_url` en la base de datos
3. Verifica la conexión a internet para descargar imágenes

### Webhook no funciona

**Solución:**
1. Asegúrate de que tu servidor sea accesible públicamente
2. Configura `BASE_URL` correctamente en `.env`
3. Verifica que los webhooks estén configurados en Mercado Pago/PayPal

## 📊 Monitoreo

### Ver órdenes recientes

```python
from database.connection import SessionLocal
from database.models import Order

db = SessionLocal()
orders = db.query(Order).order_by(Order.created_at.desc()).limit(10).all()

for order in orders:
    print(f"{order.order_number}: {order.status} - ${order.total}")
```

### Ver productos más vistos

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()
products = db.query(Product).order_by(Product.views.desc()).limit(10).all()

for product in products:
    print(f"{product.name}: {product.views} vistas")
```

## 🎨 Personalización

### Cambiar mensaje de pago

Edita `ventas-2/services/payment_service.py`:

```python
message = f"""✅ *TU MENSAJE PERSONALIZADO*

Pedido: #{order_data['order_number']}
Total: ${order_data['total']:,.0f} COP

💳 Link de pago: {result['init_point']}
"""
```

### Agregar nuevo método de pago

1. Crea integración en `ventas-2/integrations/`
2. Agrega método en `payment_service.py`
3. Actualiza `payment_agent.py` con el nuevo comando

## 📈 Estadísticas

El sistema registra automáticamente:
- ✅ Vistas de productos
- ✅ Conversiones de ventas
- ✅ Métodos de pago más usados
- ✅ Productos más vendidos
- ✅ Tasa de abandono de carrito

Ver en el dashboard: http://localhost:3000/admin/dashboard

## 🆘 Soporte

**Documentación completa:** `INTEGRACION_PAGOS_FOTOS.md`

**Contacto:**
- Email: daveymena16@gmail.com
- WhatsApp: +57 300 556 0186

---

**¡Listo para vender! 🚀**
