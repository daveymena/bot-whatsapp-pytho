# 🚀 Bot de Ventas WhatsApp - Con Pagos Dinámicos y Fotos

## 🎯 Características Principales

### 💳 Sistema de Pagos Completo (6 Métodos)

| Método | Tipo | Características |
|--------|------|-----------------|
| 💳 **Mercado Pago** | Automático | Links dinámicos, tarjetas, PSE, 12 cuotas |
| 🌎 **PayPal** | Automático | Internacional, conversión USD/COP |
| 💜 **Nequi** | Manual | Transferencia instantánea |
| ❤️ **Daviplata** | Manual | Transferencia rápida |
| 🏦 **Banco** | Manual | Transferencia bancaria |
| 💵 **Contra Entrega** | Manual | Pago en efectivo |

### 📸 Sistema de Fotos Inteligente

- ✅ Envío automático de fotos de productos
- ✅ Catálogo visual con imágenes
- ✅ Búsqueda inteligente con fotos
- ✅ Múltiples fotos por producto (hasta 4)
- ✅ Optimización automática de imágenes
- ✅ Contador de vistas y analytics

## ⚡ Inicio Rápido (5 minutos)

### 1. Verificar Instalación

```bash
VERIFICAR_INSTALACION.bat
```

### 2. Instalar Dependencias de Pago

```bash
INSTALL_PAYMENTS.bat
```

### 3. Configurar Credenciales

Edita `.env`:

```env
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=tu_token_aqui

# PayPal
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_secret

# Pagos Manuales
NEQUI_NUMBER=3136174267
DAVIPLATA_NUMBER=3136174267
BANK_ACCOUNT_NUMBER=12345678901
```

### 4. Iniciar Sistema

```bash
START_WITH_PAYMENTS.bat
```

### 5. Probar Integración

```bash
python test_payment_integration.py
```

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| **INTEGRACION_PAGOS_FOTOS.md** | Documentación completa y detallada |
| **GUIA_RAPIDA_PAGOS.md** | Guía rápida de uso |
| **CONFIGURAR_WEBHOOKS.md** | Configuración de webhooks paso a paso |
| **RESUMEN_INTEGRACION.md** | Resumen técnico de la integración |

## 💬 Ejemplos de Uso

### Compra con Mercado Pago

```
Cliente: "Hola"
Bot: "¡Hola! ¿En qué puedo ayudarte?"

Cliente: "Quiero ver productos"
Bot: [Envía catálogo con fotos]

Cliente: "El iPhone 13"
Bot: [Envía fotos del iPhone 13]
     "📦 iPhone 13
      💰 $2,500,000 COP"

Cliente: "Lo quiero con Mercado Pago"
Bot: [Genera link de pago]
     "✅ https://mpago.la/xxx"

[Cliente paga]

Bot: "✅ ¡Pago confirmado! #ORD-123"
```

### Búsqueda con Fotos

```
Cliente: "Buscar audífonos bluetooth"
Bot: [Busca y envía fotos]
     "Encontré 3 audífonos bluetooth"

Cliente: "Los Sony"
Bot: [Envía todas las fotos de Sony]
     "📦 Sony WH-1000XM4
      💰 $850,000 COP"
```

## 🎯 Comandos del Bot

### Productos

```
"catálogo" → Catálogo con fotos
"buscar [producto]" → Buscar producto
"fotos" → Ver fotos del producto
"más fotos" → Fotos adicionales
```

### Pagos

```
"mercadopago" → Link de Mercado Pago
"paypal" → Link de PayPal
"nequi" → Datos de Nequi
"daviplata" → Datos de Daviplata
"banco" → Datos bancarios
"contraentrega" → Pago al recibir
"confirmar pago" → Confirmar pago manual
```

## 🔧 Configuración Avanzada

### Webhooks

Para recibir confirmaciones automáticas de pago:

1. **Mercado Pago:**
   - Panel: https://www.mercadopago.com.co/developers/panel/webhooks
   - URL: `https://tu-dominio.com/payment/webhook/mercadopago`

2. **PayPal:**
   - Dashboard: https://developer.paypal.com/dashboard/
   - Return URL: `https://tu-dominio.com/payment/paypal/success`

Ver guía completa: `CONFIGURAR_WEBHOOKS.md`

### Base de Datos

Agregar productos con fotos:

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

product = Product(
    name="iPhone 13",
    description="Smartphone Apple",
    price=2500000,
    stock=5,
    image_url="https://ejemplo.com/iphone13.jpg",
    images=[
        "https://ejemplo.com/iphone13-1.jpg",
        "https://ejemplo.com/iphone13-2.jpg",
        "https://ejemplo.com/iphone13-3.jpg"
    ],
    category="Electrónica"
)

db.add(product)
db.commit()
```

## 📊 Estructura del Proyecto

```
ventas-2/
├── services/
│   └── payment_service.py          # Servicio de pagos
├── integrations/
│   ├── mercadopago_integration.py  # Mercado Pago
│   └── paypal_integration.py       # PayPal
├── agents/
│   ├── payment_agent.py            # Agente de pagos
│   └── products_agent.py           # Agente de productos
├── whatsapp/
│   └── multimedia_handler.py       # Manejo de fotos
├── admin/
│   └── payment_routes.py           # Rutas y webhooks
└── database/
    └── models.py                   # Modelos de BD
```

## 🧪 Testing

### Probar Integración Completa

```bash
python test_payment_integration.py
```

### Probar Mercado Pago (Sandbox)

```env
MERCADOPAGO_ACCESS_TOKEN=TEST-xxx
```

Tarjeta de prueba: `5031 7557 3453 0604`

### Probar PayPal (Sandbox)

```env
PAYPAL_MODE=sandbox
```

Usar cuentas de prueba de PayPal Developer

## 🚀 Despliegue

### Opción 1: VPS

```bash
# Conectar al servidor
ssh root@tu-servidor

# Clonar repositorio
git clone tu-repo.git
cd tu-repo

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
nano .env

# Iniciar
python main.py
```

### Opción 2: Heroku

```bash
heroku create tu-app
heroku config:set MERCADOPAGO_ACCESS_TOKEN=xxx
git push heroku main
```

### Opción 3: Railway

1. Conectar repositorio en https://railway.app
2. Configurar variables de entorno
3. Desplegar automáticamente

## 📈 Métricas y Analytics

El sistema registra automáticamente:

- ✅ Vistas de productos
- ✅ Conversiones de ventas
- ✅ Métodos de pago más usados
- ✅ Productos más vendidos
- ✅ Tasa de abandono

Ver en: http://localhost:3000/admin/dashboard

## 🔐 Seguridad

- ✅ Tokens en variables de entorno
- ✅ Validación de webhooks
- ✅ Confirmación de pagos
- ✅ Registro de transacciones
- ✅ Encriptación de datos sensibles

## 🆘 Solución de Problemas

### Error: "Mercado Pago no configurado"

```bash
# Verificar token en .env
cat .env | grep MERCADOPAGO

# Obtener nuevo token
# https://www.mercadopago.com.co/developers/panel/credentials
```

### Las fotos no se envían

```bash
# Verificar configuración
python -c "from config.settings import settings; print(settings.PHOTOS_ENABLED)"

# Verificar productos con fotos
python -c "from database.connection import SessionLocal; from database.models import Product; db = SessionLocal(); print(db.query(Product).filter(Product.image_url.isnot(None)).count())"
```

### Webhook no funciona

1. Verificar URL pública
2. Verificar SSL configurado
3. Ver logs: `tail -f logs/bot.log`

## 📞 Soporte

- **Email:** daveymena16@gmail.com
- **WhatsApp:** +57 300 556 0186
- **Documentación:** Ver archivos `.md` en el proyecto

## 🎉 Características Destacadas

### 🤖 Automatización Total

- Links de pago generados automáticamente
- Fotos enviadas sin intervención manual
- Confirmaciones automáticas por webhook
- Facturas digitales automáticas

### 🧠 Inteligencia Artificial

- Detección de intención de compra
- Búsqueda inteligente de productos
- Recomendaciones personalizadas
- Análisis de sentimiento

### 📱 Experiencia de Usuario

- Respuestas instantáneas
- Fotos de alta calidad
- Proceso de compra simple
- Múltiples opciones de pago

## 🔄 Actualizaciones

### Versión 2.0 (Actual)

- ✅ Sistema de pagos dinámicos (6 métodos)
- ✅ Envío automático de fotos
- ✅ Webhooks para confirmación automática
- ✅ Analytics de productos y ventas
- ✅ Optimización de imágenes
- ✅ Integración completa con BD

### Próximas Mejoras

- [ ] QR codes para pagos
- [ ] Carrusel de imágenes
- [ ] Videos de productos
- [ ] Realidad aumentada
- [ ] Chatbot de voz

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🙏 Créditos

Desarrollado con ❤️ para **Tecnovariedades D&S**

---

**¡Listo para vender! 🚀**

*Sistema completo de ventas por WhatsApp con pagos dinámicos y fotos automáticas*
