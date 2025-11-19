# 🚀 Integración de Pagos y Fotos - Bot de Ventas

## ✅ Funcionalidades Implementadas

### 💳 Sistema de Pagos Dinámicos

#### 1. Mercado Pago
- ✅ Generación automática de links de pago
- ✅ Soporte para tarjetas crédito/débito
- ✅ PSE (Pagos Seguros en Línea)
- ✅ Hasta 12 cuotas sin interés
- ✅ Webhooks para confirmación automática
- ✅ Notificaciones por WhatsApp

**Uso:**
```
Cliente: "Quiero pagar con Mercado Pago"
Bot: [Genera link automático]
```

#### 2. PayPal
- ✅ Links de pago internacionales
- ✅ Conversión automática COP a USD
- ✅ Protección al comprador
- ✅ Confirmación automática de pagos
- ✅ Notificaciones por WhatsApp

**Uso:**
```
Cliente: "PayPal"
Bot: [Genera link de pago internacional]
```

#### 3. Pagos Manuales
- ✅ Nequi
- ✅ Daviplata
- ✅ Transferencia Bancaria
- ✅ Solicitud automática de comprobantes
- ✅ Confirmación manual de pagos

**Uso:**
```
Cliente: "Nequi"
Bot: [Envía datos de Nequi + instrucciones]
Cliente: [Envía comprobante]
Bot: "confirmar pago"
```

#### 4. Contra Entrega
- ✅ Pago en efectivo al recibir
- ✅ Confirmación de dirección
- ✅ Coordinación de envío

**Uso:**
```
Cliente: "Contra entrega"
Bot: [Confirma pedido para pago al recibir]
```

### 📸 Sistema de Envío de Fotos

#### 1. Envío Automático de Fotos de Productos
- ✅ Fotos desde base de datos
- ✅ Optimización automática de imágenes
- ✅ Múltiples fotos por producto
- ✅ Captions con información del producto
- ✅ Contador de vistas

**Uso:**
```
Cliente: "Quiero ver el iPhone 13"
Bot: [Envía fotos + descripción + precio]
```

#### 2. Catálogo con Fotos
- ✅ Envío de catálogo completo
- ✅ Filtrado por categoría
- ✅ Primeros 3 productos con fotos
- ✅ Lista completa de productos

**Uso:**
```
Cliente: "Catálogo"
Bot: [Envía lista + fotos de productos destacados]
```

#### 3. Búsqueda Inteligente
- ✅ Búsqueda por nombre
- ✅ Búsqueda por palabras clave
- ✅ Búsqueda por categoría
- ✅ Envío automático de fotos

**Uso:**
```
Cliente: "Buscar audífonos bluetooth"
Bot: [Busca + envía fotos de audífonos]
```

## 🔧 Configuración

### 1. Variables de Entorno (.env)

```env
# Mercado Pago
MERCADOPAGO_ENABLED=true
MERCADOPAGO_ACCESS_TOKEN=tu_access_token_aqui

# PayPal
PAYPAL_ENABLED=true
PAYPAL_MODE=live  # o sandbox para pruebas
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_client_secret
USD_TO_COP_RATE=4000

# Pagos Manuales
NEQUI_NUMBER=3136174267
DAVIPLATA_NUMBER=3136174267
BANK_NAME=Bancolombia
BANK_ACCOUNT_TYPE=Ahorros
BANK_ACCOUNT_NUMBER=12345678901
BANK_ACCOUNT_HOLDER=Tecnovariedades D&S

# Fotos
PHOTOS_ENABLED=true

# Base URL (para webhooks)
BASE_URL=http://localhost:5000
```

### 2. Instalación de Dependencias

```bash
pip install mercadopago paypalrestsdk pillow aiohttp
```

### 3. Configuración de Webhooks

#### Mercado Pago:
1. Ir a: https://www.mercadopago.com.co/developers/panel/webhooks
2. Agregar URL: `https://tu-dominio.com/payment/webhook/mercadopago`
3. Seleccionar eventos: `payment`

#### PayPal:
1. Ir a: https://developer.paypal.com/dashboard/
2. Configurar Return URL: `https://tu-dominio.com/payment/paypal/success`
3. Configurar Cancel URL: `https://tu-dominio.com/payment/paypal/cancel`

## 📊 Base de Datos

### Modelo de Productos (actualizado)

```python
class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(String)  # Imagen principal
    images = Column(JSON)  # Array de URLs adicionales
    category = Column(String)
    views = Column(Integer, default=0)  # Contador de vistas
    sales_count = Column(Integer, default=0)
```

### Modelo de Órdenes (actualizado)

```python
class Order(Base):
    id = Column(Integer, primary_key=True)
    order_number = Column(String, unique=True)
    user_phone = Column(String, nullable=False)
    products = Column(JSON)
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")
    payment_method = Column(String)  # mercadopago, paypal, nequi, etc.
    payment_proof = Column(String)  # URL del comprobante
```

## 🎯 Flujo de Compra Completo

### Ejemplo 1: Compra con Mercado Pago

```
Cliente: "Hola"
Bot: "¡Hola! ¿En qué puedo ayudarte?"

Cliente: "Quiero ver productos"
Bot: [Envía catálogo con fotos]

Cliente: "El número 2"
Bot: [Envía fotos detalladas del producto 2]

Cliente: "Lo quiero"
Bot: "¿Cómo deseas pagar?"

Cliente: "Mercado Pago"
Bot: [Genera link de pago]
     "✅ Link de pago generado: https://mpago.la/xxx"

[Cliente paga]

Bot: "✅ ¡Pago confirmado! Tu pedido será enviado pronto."
```

### Ejemplo 2: Compra con Nequi

```
Cliente: "Quiero comprar"
Bot: "¿Qué producto te interesa?"

Cliente: "iPhone 13"
Bot: [Envía fotos del iPhone 13]

Cliente: "Lo quiero, Nequi"
Bot: "💜 PAGO POR NEQUI
     Número: 3136174267
     Total: $2,500,000 COP
     
     Envía el comprobante después de pagar"

[Cliente transfiere y envía foto del comprobante]

Cliente: "Ya pagué"
Bot: "✅ ¡Pago confirmado! Gracias por tu compra."
```

## 🔌 Endpoints API

### Pagos

```
POST /payment/webhook/mercadopago
GET  /payment/success
GET  /payment/failure
GET  /payment/paypal/success
GET  /payment/paypal/cancel
POST /payment/confirm-manual
GET  /payment/status/{order_number}
```

## 🧪 Testing

### Probar Mercado Pago (Sandbox)

```python
# En .env
MERCADOPAGO_ACCESS_TOKEN=TEST-xxx
```

Tarjetas de prueba:
- Aprobada: 5031 7557 3453 0604
- Rechazada: 5031 4332 1540 6351

### Probar PayPal (Sandbox)

```python
# En .env
PAYPAL_MODE=sandbox
```

Usar cuentas de prueba de PayPal Developer

## 📱 Comandos del Bot

### Productos y Fotos

```
"catálogo" → Muestra catálogo con fotos
"buscar [producto]" → Busca producto específico
"fotos" → Envía fotos del producto actual
"más fotos" → Envía fotos adicionales
"categoría [nombre]" → Filtra por categoría
```

### Pagos

```
"mercadopago" o "mp" → Link de Mercado Pago
"paypal" → Link de PayPal
"nequi" → Datos de Nequi
"daviplata" → Datos de Daviplata
"banco" → Datos bancarios
"contraentrega" → Pago al recibir
"confirmar pago" → Confirma pago manual
```

## 🎨 Características Avanzadas

### 1. Optimización de Imágenes
- Redimensionamiento automático (máx 1280x1280)
- Compresión con calidad 85%
- Formato optimizado para WhatsApp

### 2. Contador de Vistas
- Tracking automático de productos vistos
- Analytics de productos más populares

### 3. Notificaciones Automáticas
- Confirmación de pago por WhatsApp
- Envío de factura digital
- Actualizaciones de estado del pedido

### 4. Búsqueda Inteligente
- Búsqueda por nombre
- Búsqueda por palabras clave
- Búsqueda por descripción
- Sugerencias automáticas

## 🚀 Próximas Mejoras

- [ ] Generación de QR codes para pagos
- [ ] Integración con más pasarelas de pago
- [ ] Carrusel de imágenes en WhatsApp
- [ ] Videos de productos
- [ ] Realidad aumentada (AR)
- [ ] Chatbot de voz

## 📞 Soporte

Para dudas o problemas:
- Email: daveymena16@gmail.com
- WhatsApp: +57 300 556 0186

---

**Desarrollado con ❤️ para Tecnovariedades D&S**
