# 🤖 Bot de Ventas WhatsApp con Python + Baileys

Bot inteligente de ventas para WhatsApp con múltiples agentes especializados, integración con IA (GROQ), base de datos PostgreSQL y sistema de dropshipping.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

---

## 🎯 ¿Qué hace este bot?

Un asistente de ventas profesional que:
- 💬 Conversa naturalmente con clientes en WhatsApp
- 🤖 Usa IA avanzada (GROQ/Llama 3.1) para respuestas inteligentes
- 🎭 Tiene 5 agentes especializados trabajando en equipo
- 💰 Maneja todo el proceso de venta: desde saludo hasta cierre
- 📦 Gestiona productos físicos, digitales y dropshipping
- 💳 Procesa pagos por múltiples métodos
- 📅 Agenda citas y reservas
- 🔄 Se reconecta automáticamente (anti-baneo)

---

## 🌟 Características

### 🎨 Dashboard Moderno (NUEVO)
- **Next.js 14** con React 18 y Tailwind CSS
- Dashboard en tiempo real con estadísticas
- Gestión completa de productos y clientes
- Configuración del bot y personalidad IA
- Responsive design (móvil, tablet, desktop)
- Autenticación segura con JWT

### Agentes Especializados
- **Agente de Ventas**: Maneja todo el proceso de venta (AIDA, SPIN, manejo de objeciones)
- **Agente de Productos**: Experto en catálogo (físicos, digitales, dropshipping)
- **Agente de Dropshipping**: Gestiona productos Dropi
- **Agente de Reservas**: Agenda servicios (peluquería, odontología, mantenimiento)
- **Agente de Pagos**: Procesa pagos (Nequi, Daviplata, MercadoPago, PayPal)

### Tecnologías
- **Backend**: Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **WhatsApp**: Baileys (WhatsApp Web API)
- **IA**: GROQ AI (Llama 3.1)
- **Base de Datos**: PostgreSQL

### Funcionalidades
- ✅ Dashboard moderno con Next.js
- ✅ Conversaciones inteligentes con IA
- ✅ Memoria de conversación (24h)
- ✅ Rotación de API keys
- ✅ Simulación de escritura humana
- ✅ Reconexión automática
- ✅ Sistema anti-baneo
- ✅ Múltiples métodos de pago
- ✅ Integración con Dropi
- ✅ Base de datos completa
- ✅ Panel de administración profesional

## ⚡ Inicio Rápido

**¿Quieres empezar YA?** Lee [QUICK_START.md](QUICK_START.md) - 5 minutos

### Instalación Completa

1. **Clonar repositorio**
```bash
git clone <repo>
cd whatsapp-sales-bot
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
npm install
```

3. **Configurar .env**
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

4. **Inicializar base de datos**
```bash
python -c "from database.connection import init_db; init_db()"
```

5. **Instalar Dashboard Next.js**
```bash
cd dashboard-nextjs
npm install
cd ..
```

6. **Iniciar todo**
```bash
# Windows
START_ALL.bat

# Linux/Mac
./start.sh
```

### URLs Importantes
- 🎨 **Dashboard Next.js**: http://localhost:3001 (Recomendado)
- 🔧 **API Backend**: http://localhost:5000
- 📚 **API Docs**: http://localhost:5000/docs
- 💬 **Baileys Server**: http://localhost:3002/status

### Credenciales Dashboard
- **Email**: admin@ventas.com
- **Password**: admin123
python seed_database.py
```

5. **Iniciar bot**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

6. **Escanear QR de WhatsApp**
- Aparecerá en la terminal
- Escanea con tu WhatsApp
- ¡Listo! 🎉

## 🎯 Uso

### Iniciar el bot
```bash
python main.py
```

El bot estará disponible en `http://localhost:3000`

### Endpoints API

- `GET /` - Estado del bot
- `GET /health` - Health check
- `GET /stats` - Estadísticas
- `POST /send-message` - Enviar mensaje manual

## 📋 Configuración

### Variables de Entorno Principales

```env
# IA
GROQ_API_KEY=tu_api_key
GROQ_MODEL=llama-3.1-8b-instant

# WhatsApp
WHATSAPP_NUMBER=573005560186
SESSION_PATH=./data/whatsapp-sessions

# Base de Datos
DATABASE_URL=postgresql://user:pass@host:5432/db

# Negocio
BUSINESS_NAME=Tu Negocio
BUSINESS_PHONE=+57 300 123 4567
```

## 🤝 Agentes

### Agente de Ventas
- Saludo profesional
- Descubrimiento de necesidades
- Presentación de soluciones
- Manejo de objeciones
- Cierre de ventas

### Agente de Productos
- Búsqueda en catálogo
- Especificaciones técnicas
- Comparativas
- Recomendaciones
- Cross-selling y up-selling

### Agente de Dropshipping
- Integración con Dropi
- Cálculo de márgenes
- Gestión de pedidos
- Seguimiento de envíos

### Agente de Reservas
- Agendamiento de citas
- Verificación de disponibilidad
- Confirmaciones
- Recordatorios

### Agente de Pagos
- Múltiples métodos
- Verificación de pagos
- Generación de recibos
- Seguimiento de transacciones

## 📊 Base de Datos

Modelos incluidos:
- `Product` - Productos
- `User` - Usuarios
- `Conversation` - Conversaciones
- `Order` - Pedidos
- `Reservation` - Reservas

## 🔧 Próximos Pasos

Para conectar con Baileys real:
1. Crear proceso Node.js con Baileys
2. Implementar comunicación IPC o WebSocket
3. Manejar QR code para autenticación
4. Implementar manejo de eventos de Baileys

## 📚 Documentación

- 📖 [Guía de Instalación Completa](SETUP.md)
- 🚀 [Guía de Despliegue](DEPLOYMENT.md)
- 📡 [Documentación de API](API_DOCS.md)
- ⚡ [Inicio Rápido (5 min)](QUICK_START.md)
- 📝 [Changelog](CHANGELOG.md)

## 🎨 Dashboard

Abre `dashboard.html` en tu navegador para ver:
- Estado del bot en tiempo real
- Estadísticas de conversaciones
- Agentes activos
- QR code de WhatsApp
- Métricas del sistema

## 🐳 Docker

```bash
docker-compose up -d
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea tu feature branch
3. Commit tus cambios
4. Push al branch
5. Abre un Pull Request

## 📝 Notas Importantes

- ✅ Usa GROQ con rotación automática de API keys
- ✅ Memoria conversacional de 24 horas
- ✅ Simulación de escritura humana
- ✅ Reconexión inteligente automática
- ✅ Sistema anti-baneo integrado
- ⚠️ Respeta los límites de WhatsApp
- ⚠️ No uses para spam

## 🛠️ Desarrollo

### Agregar un nuevo agente:
1. Crear clase en `agents/nuevo_agent.py`
2. Heredar de `BaseAgent`
3. Implementar `get_system_prompt()`
4. Registrar en `message_handler.py`

### Estructura del proyecto:
```
agents/         → Agentes especializados
ai/             → Cliente IA y gestión
database/       → Modelos y conexión
services/       → Lógica de negocio
whatsapp/       → Cliente WhatsApp
```

## 🐛 Troubleshooting

**Bot no responde:**
- Verifica que ambos servidores estén corriendo
- Revisa los logs en las terminales
- Confirma que WhatsApp esté conectado

**Error de base de datos:**
- Verifica PostgreSQL esté corriendo
- Confirma credenciales en .env

**GROQ API error:**
- Verifica tu API key
- Confirma que tengas créditos

## 📊 Estadísticas

- 🤖 5 agentes especializados
- 💬 Conversaciones ilimitadas
- 🔄 Reconexión automática
- 📦 Soporte multi-producto
- 💳 6 métodos de pago
- 🌐 API REST completa

## 🌟 Características Destacadas

- **IA Conversacional**: Respuestas naturales y contextuales
- **Multi-Agente**: Especialistas trabajando en equipo
- **Anti-Baneo**: Sistema de reconexión inteligente
- **Escalable**: Arquitectura modular y extensible
- **Production Ready**: Listo para desplegar

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

## 💬 Soporte

- 📧 Email: tu@email.com
- 💬 Discord: [Próximamente]
- 🐛 Issues: GitHub Issues

## ⭐ Agradecimientos

- [Baileys](https://github.com/WhiskeySockets/Baileys) - Cliente WhatsApp
- [GROQ](https://groq.com/) - IA ultrarrápida
- [FastAPI](https://fastapi.tiangolo.com/) - Framework Python

---

**Hecho con ❤️ para vendedores que quieren automatizar sin perder el toque humano**

⭐ Si te gusta el proyecto, dale una estrella!
