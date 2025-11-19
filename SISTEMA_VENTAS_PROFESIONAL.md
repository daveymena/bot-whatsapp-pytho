# 🎯 Sistema de Ventas Profesional con IA

## Descripción General

Sistema completo de ventas que maneja el ciclo desde el saludo hasta el cierre, con acceso al catálogo real de productos y razonamiento inteligente.

## Componentes Implementados

### 1. Motor de Razonamiento (`ai/sales_reasoning.py`)

**Funcionalidades:**
- Análisis de etapa de venta actual
- Detección de intención del cliente
- Identificación de señales de compra
- Detección de objeciones
- Cálculo de urgencia
- Recomendación de acciones

**Etapas de Venta:**
1. **GREETING** - Saludo inicial profesional
2. **RAPPORT** - Construcción de confianza
3. **DISCOVERY** - Descubrimiento de necesidades
4. **PRESENTATION** - Presentación de productos
5. **HANDLING_OBJECTIONS** - Manejo de objeciones
6. **CLOSING** - Cierre de venta
7. **POST_SALE** - Post-venta

### 2. Agente de Ventas Profesional (`agents/professional_sales_agent.py`)

**Características:**
- Acceso directo al catálogo de productos
- Razonamiento contextual
- Adaptación según etapa de venta
- Manejo profesional de objeciones
- Técnicas de cierre probadas

**Técnicas de Venta Implementadas:**
- Cross-selling (productos complementarios)
- Up-selling (versiones premium)
- Escasez (stock limitado)
- Urgencia (ofertas temporales)
- Prueba social (productos más vendidos)

## Flujo de Conversación

```
Cliente: "Hola"
Bot: "¡Buenos días! Soy tu asesor de Tecnovariedades D&S. ¿En qué puedo ayudarte hoy?" 
[Etapa: GREETING → RAPPORT]

Cliente: "Busco audífonos bluetooth"
Bot: "¡Excelente elección! ¿Qué características son más importantes para ti? ¿Calidad de sonido, duración de batería o precio?"
[Etapa: RAPPORT → DISCOVERY]

Cliente: "Que tengan buena batería"
Bot: "Perfecto! Te recomiendo los Audífonos Bluetooth Pro por $89,900. Tienen 40 horas de batería, cancelación de ruido y son nuestros más vendidos. ¿Te gustaría verlos?"
[Etapa: DISCOVERY → PRESENTATION]

Cliente: "Están un poco caros"
Bot: "Entiendo tu preocupación. Estos audífonos incluyen garantía de 1 año, cancelación de ruido activa y 40 horas de batería. Comparado con otras marcas que cuestan $150,000+, es una excelente inversión. Además, tenemos opciones de pago: Nequi, transferencia o contra entrega."
[Etapa: PRESENTATION → HANDLING_OBJECTIONS]

Cliente: "Ok, me convenciste. ¿Cómo compro?"
Bot: "¡Perfecto! 🎉 ¿Prefieres pago por Nequi o transferencia? El envío es gratis y llega en 24-48 horas."
[Etapa: HANDLING_OBJECTIONS → CLOSING]
```

## Integración con el Sistema

### Paso 1: Actualizar Message Handler

Editar `whatsapp/message_handler.py`:

```python
from agents.professional_sales_agent import professional_sales_agent

class MessageHandler:
    def __init__(self):
        self.agents = {
            "professional_sales": professional_sales_agent,  # NUEVO
            "sales": SalesAgent(),
            "products": ProductsAgent(),
            # ... otros agentes
        }
    
    async def handle_message(self, phone: str, message: str) -> str:
        # Usar el agente profesional por defecto
        agent = self.agents["professional_sales"]
        response = await agent.process_message(phone, message, context)
        return response
```

### Paso 2: Configurar en el Dashboard

Crear nueva pestaña "Ventas IA" en el dashboard para:
- Ver conversaciones en tiempo real
- Monitorear etapas de venta
- Ver productos recomendados
- Estadísticas de conversión
- Configurar respuestas personalizadas

## Configuración

### Variables de Entorno (`.env`)

```env
# IA Configuration
AI_PROVIDER=groq
GROQ_API_KEY=tu_api_key
GROQ_MODEL=llama-3.1-8b-instant

# Sales Configuration
ENABLE_PROFESSIONAL_SALES=true
SALES_AGENT_TONE=consultative  # consultative, aggressive, friendly
AUTO_SEND_CATALOG=true
AUTO_SEND_PHOTOS=true
MAX_PRODUCTS_PER_MESSAGE=3
```

### Personalización del Agente

Editar `agents/professional_sales_agent.py` para ajustar:

1. **Tono de venta:**
   - Consultivo (recomendado)
   - Agresivo
   - Amigable

2. **Estrategias de cierre:**
   - Cierre asumido
   - Cierre alternativo
   - Cierre de urgencia

3. **Manejo de objeciones:**
   - Por precio
   - Por confianza
   - Por timing

## Métricas y Análisis

El sistema rastrea:
- Etapa actual de cada conversación
- Señales de compra detectadas
- Objeciones comunes
- Tasa de conversión por etapa
- Productos más consultados
- Tiempo promedio hasta cierre

## Ventajas del Sistema

✅ **Acceso Real al Catálogo**
- Consulta productos reales de la base de datos
- Precios actualizados
- Stock en tiempo real

✅ **Razonamiento Inteligente**
- Detecta etapa de venta automáticamente
- Adapta respuestas según contexto
- Identifica señales de compra

✅ **Ventas Profesionales**
- Sigue metodología probada
- Maneja objeciones efectivamente
- Cierra ventas naturalmente

✅ **Personalización**
- Se adapta a cada cliente
- Recuerda conversaciones previas
- Aprende de interacciones

## Próximos Pasos

1. ✅ Motor de razonamiento implementado
2. ✅ Agente de ventas profesional creado
3. ⏳ Integrar con message handler
4. ⏳ Crear pestaña en dashboard
5. ⏳ Agregar métricas y reportes
6. ⏳ Entrenar con conversaciones reales

## Uso

### Activar el Sistema

```bash
# 1. Asegurar que las dependencias están instaladas
pip install -r requirements.txt

# 2. Configurar variables de entorno
# Editar .env y agregar ENABLE_PROFESSIONAL_SALES=true

# 3. Reiniciar el servidor Python
python main.py
```

### Probar el Sistema

Envía un mensaje de WhatsApp al bot:
```
"Hola, busco audífonos bluetooth"
```

El bot debería:
1. Saludar profesionalmente
2. Hacer preguntas sobre necesidades
3. Consultar el catálogo real
4. Presentar productos con precios
5. Manejar objeciones
6. Guiar hacia el cierre

## Soporte

Para dudas o problemas:
1. Revisa los logs en la terminal de Python
2. Verifica que GROQ_API_KEY esté configurado
3. Asegúrate de que hay productos en la base de datos
4. Consulta `TROUBLESHOOTING.md`

## Documentación Adicional

- `ai/sales_reasoning.py` - Motor de razonamiento
- `agents/professional_sales_agent.py` - Agente de ventas
- `AGENTS_GUIDE.md` - Guía de agentes
- `API_DOCS.md` - Documentación de API
