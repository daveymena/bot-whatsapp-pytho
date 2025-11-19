# 🚀 Referencia Rápida - Sistema Conversacional Avanzado

## 📋 Componentes Implementados

### 1. 🧠 Sistema de Memoria del Cliente
**Archivo:** `ai/customer_memory.py`

```python
from ai.customer_memory import customer_memory

# Obtener perfil del cliente
profile = customer_memory.get_customer_profile(phone_number)

# Actualizar perfil
customer_memory.update_customer_profile(phone_number, {
    'name': 'Juan Pérez',
    'preferences': {'category': 'Cursos'},
    'communication_style': 'casual'
})

# Registrar compra
customer_memory.record_purchase(phone_number, {
    'product': 'Curso Python',
    'amount': 50000
})

# Obtener saludo personalizado
greeting = customer_memory.get_personalized_greeting(phone_number)
```

**Capacidades:**
- ✅ Segmentación automática (nuevo, regular, vip, premium)
- ✅ Historial de compras
- ✅ Preferencias de comunicación
- ✅ Saludos personalizados
- ✅ Recomendaciones basadas en historial

---

### 2. 😊 Análisis de Sentimiento
**Archivo:** `ai/sentiment_analyzer.py`

```python
from ai.sentiment_analyzer import sentiment_analyzer

# Analizar mensaje
analysis = sentiment_analyzer.analyze_message("¡Excelente producto! 😍")

# Resultado:
{
    'sentiment': 'very_positive',  # very_negative, negative, neutral, positive, very_positive
    'score': 4.5,                  # -10 a +10
    'emotion': 'intense',          # calm, moderate, intense
    'urgency': 8,                  # 0-10
    'recommended_tone': 'enthusiastic_matching',
    'should_escalate': False
}
```

**Detecta:**
- ✅ Sentimiento (muy negativo a muy positivo)
- ✅ Emoción (calma, moderada, intensa)
- ✅ Urgencia (0-10)
- ✅ Necesidad de escalamiento
- ✅ Tono recomendado de respuesta

---

### 3. 🚨 Sistema de Escalamiento
**Archivo:** `ai/escalation_manager.py`

```python
from ai.escalation_manager import escalation_manager

# Verificar si debe escalar
should_escalate, reason = escalation_manager.should_escalate(
    phone_number,
    message,
    sentiment_analysis
)

if should_escalate:
    escalation_message = escalation_manager.get_escalation_message(reason)
    # Transferir a humano
```

**Escala automáticamente por:**
- ✅ Solicitud explícita ("quiero hablar con una persona")
- ✅ Quejas graves
- ✅ Confusión repetida (3+ veces)
- ✅ Sentimiento muy negativo
- ✅ Problemas de pago

---

### 4. 🎯 Agente Multi-Dominio
**Archivo:** `ai/multi_domain_agent.py`

```python
from ai.multi_domain_agent import multi_domain_agent

# Detectar dominio
domain = multi_domain_agent.detect_domain(message)
# Resultado: 'product_sales', 'service_booking', 'complaint', etc.

# Procesar según dominio
response = await multi_domain_agent.process_message(phone, message, context)

# Agendar cita
slots = multi_domain_agent.get_available_slots(date, service_type)
booking = multi_domain_agent.book_appointment(phone, slot_id, service_type)
```

**Dominios soportados:**
- ✅ Venta de productos físicos
- ✅ Venta de productos digitales
- ✅ Agendamiento de servicios
- ✅ Consultas generales
- ✅ Quejas y reclamos

---

### 5. 🤖 Agente Avanzado Integrado
**Archivo:** `agents/advanced_sales_agent.py`

```python
from agents.advanced_sales_agent import AdvancedSalesAgent

agent = AdvancedSalesAgent()

# Procesar mensaje con todas las capacidades
response = await agent.process_message(
    phone_number="573001234567",
    message="Hola, quiero comprar un curso",
    context={}
)
```

**Integra:**
- ✅ Memoria del cliente
- ✅ Análisis de sentimiento
- ✅ Escalamiento inteligente
- ✅ Multi-dominio
- ✅ Contexto conversacional

---

## 🎮 Uso Rápido

### Ejemplo Completo

```python
from agents.advanced_sales_agent import AdvancedSalesAgent

agent = AdvancedSalesAgent()

# 1. Cliente nuevo
response = await agent.process_message(
    "573001234567",
    "Hola, quiero información sobre cursos",
    {}
)
# → Saludo genérico + catálogo

# 2. Cliente registra compra
# (se hace automáticamente al confirmar pedido)

# 3. Cliente regresa
response = await agent.process_message(
    "573001234567",
    "Hola de nuevo",
    {}
)
# → Saludo personalizado: "¡Hola Juan! ¿Cómo te fue con tu Curso Python?"

# 4. Cliente molesto
response = await agent.process_message(
    "573001234567",
    "Esto no funciona! Estoy muy molesto 😡",
    {}
)
# → Detecta sentimiento negativo + escala a humano
```

---

## 📊 Flujo de Procesamiento

```
Mensaje entrante
    ↓
1. Análisis de Sentimiento
    ↓
2. Verificar Escalamiento
    ↓ (si no escala)
3. Cargar Perfil del Cliente
    ↓
4. Detectar Dominio
    ↓
5. Procesar según Dominio
    ↓
6. Actualizar Memoria
    ↓
7. Generar Respuesta Personalizada
    ↓
Respuesta final
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Memoria del Cliente
CUSTOMER_MEMORY_ENABLED=true
CUSTOMER_MEMORY_RETENTION_DAYS=365

# Análisis de Sentimiento
SENTIMENT_ANALYSIS_ENABLED=true
SENTIMENT_THRESHOLD_ESCALATE=-5

# Escalamiento
AUTO_ESCALATE_ENABLED=true
ESCALATE_ON_CONFUSION_COUNT=3

# Multi-Dominio
BOOKING_ENABLED=true
BOOKING_SLOT_DURATION=60  # minutos
BOOKING_PRICE=50000
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
python test_advanced_system.py

# Tests individuales
python -c "from ai.customer_memory import customer_memory; print('✅ Memoria OK')"
python -c "from ai.sentiment_analyzer import sentiment_analyzer; print('✅ Sentimiento OK')"
python -c "from ai.escalation_manager import escalation_manager; print('✅ Escalamiento OK')"
python -c "from ai.multi_domain_agent import multi_domain_agent; print('✅ Multi-dominio OK')"
```

---

## 📈 Métricas y Monitoreo

### Memoria del Cliente
```python
# Ver estadísticas
stats = customer_memory.get_statistics()
print(f"Total clientes: {stats['total_customers']}")
print(f"Clientes VIP: {stats['vip_customers']}")
print(f"Valor promedio: ${stats['average_value']}")
```

### Escalamiento
```python
# Ver estadísticas de escalamiento
stats = escalation_manager.get_statistics()
print(f"Total escalamientos: {stats['total_escalations']}")
print(f"Razones: {stats['reasons']}")
```

---

## 🎯 Casos de Uso

### 1. E-commerce
- Venta de productos
- Recomendaciones personalizadas
- Seguimiento post-venta

### 2. Servicios Profesionales
- Agendamiento de citas
- Consultoría
- Servicios a domicilio

### 3. Educación
- Venta de cursos
- Seguimiento de estudiantes
- Recomendaciones de contenido

### 4. Soporte
- Atención al cliente
- Resolución de problemas
- Escalamiento a humanos

---

## 🚀 Próximos Pasos

1. **Integrar con tu sistema actual:**
   ```python
   # En tu message_handler.py
   from agents.advanced_sales_agent import AdvancedSalesAgent
   
   agent = AdvancedSalesAgent()
   response = await agent.process_message(phone, message, context)
   ```

2. **Personalizar respuestas:**
   - Edita los templates en cada módulo
   - Ajusta umbrales de sentimiento
   - Configura reglas de escalamiento

3. **Monitorear y optimizar:**
   - Revisa métricas diariamente
   - Ajusta según feedback
   - Mejora templates de respuesta

---

## 📚 Documentación Completa

- `MEJORAS_SISTEMA_CONVERSACIONAL.md` - Guía detallada
- `RESUMEN_MEJORAS.md` - Resumen ejecutivo
- `IMPLEMENTACION_FINAL_MEJORAS.md` - Guía de implementación

---

## ✅ Checklist de Implementación

- [x] Sistema de memoria del cliente
- [x] Análisis de sentimiento
- [x] Sistema de escalamiento
- [x] Agente multi-dominio
- [x] Agente avanzado integrado
- [x] Tests completos
- [x] Documentación

---

## 💡 Tips

1. **Empieza simple:** Activa una funcionalidad a la vez
2. **Monitorea:** Revisa logs y métricas constantemente
3. **Itera:** Ajusta según el comportamiento real de usuarios
4. **Personaliza:** Adapta los mensajes a tu marca
5. **Escala:** El sistema está diseñado para crecer contigo

---

¡Tu sistema conversacional avanzado está listo! 🎉
