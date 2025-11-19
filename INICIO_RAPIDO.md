# 🚀 Inicio Rápido - Smart Sales Bot

## ✅ Lo que ya está listo:

1. ✅ Bot de Python con FastAPI
2. ✅ Dashboard web profesional
3. ✅ Base de datos PostgreSQL conectada
4. ✅ 5 Agentes IA especializados
5. ✅ Sistema de detección de intención (NLP)
6. ✅ Embudo de ventas AIDA
7. ✅ Anti-spam
8. ✅ Panel de administración

## 📋 Pasos para Conectar WhatsApp Real

### 1️⃣ Instalar Node.js (si no lo tienes)
Descarga desde: https://nodejs.org/
Versión recomendada: LTS

### 2️⃣ Instalar Baileys
```bash
cd baileys-server
npm install
```

### 3️⃣ Iniciar el Bot de Python
```bash
# En una terminal
python main.py
```

### 4️⃣ Iniciar Baileys
```bash
# En OTRA terminal
cd baileys-server
npm start
```

### 5️⃣ Escanear QR Code
1. Verás un QR code en la terminal de Baileys
2. Abre WhatsApp en tu teléfono
3. Ve a: **Configuración → Dispositivos vinculados**
4. Toca **"Vincular un dispositivo"**
5. Escanea el QR code

¡Listo! Tu bot está conectado a WhatsApp.

## 🌐 URLs Importantes

- **Dashboard Next.js**: http://localhost:3001 (Nuevo - Recomendado)
- **Dashboard Legacy**: http://localhost:5000/admin/dashboard
- **API Docs**: http://localhost:5000/docs
- **Baileys Status**: http://localhost:3001/status

## 🎨 Nuevo Dashboard Next.js

Ahora incluye un dashboard moderno construido con Next.js:

### Iniciar Dashboard Next.js
```bash
# Opción 1: Iniciar todo junto
START_ALL.bat

# Opción 2: Solo el dashboard
START_DASHBOARD.bat

# Opción 3: Manual
cd dashboard-nextjs
npm install
npm run dev
```

### Credenciales de Acceso
- **Email**: admin@ventas.com
- **Password**: admin123

### Características del Dashboard
- ✅ Interfaz moderna y responsive
- ✅ Estadísticas en tiempo real
- ✅ Gestión de productos
- ✅ Gestión de clientes
- ✅ Configuración del bot
- ✅ Personalidad IA
- ✅ Entrenamiento del bot
- **API Docs**: http://localhost:3000/docs
- **Health Check**: http://localhost:3000/health
- **Baileys Status**: http://localhost:3001/status

## 🎯 Probar el Bot

1. Envía un mensaje a tu número de WhatsApp
2. El bot responderá automáticamente
3. Verás la conversación en el dashboard

## 📊 Dashboard

El dashboard muestra:
- ✅ Estado de WhatsApp (conectado/desconectado)
- ✅ Estadísticas en tiempo real
- ✅ Conversaciones recientes
- ✅ Productos
- ✅ Clientes
- ✅ Pedidos

## 🔧 Troubleshooting

### Bot de Python no inicia
```bash
# Verificar dependencias
pip install -r requirements.txt

# Verificar base de datos
python init_database.py
```

### Baileys no conecta
```bash
cd baileys-server

# Reinstalar dependencias
rm -rf node_modules
npm install

# Iniciar de nuevo
npm start
```

### Dashboard no carga
1. Verifica que Python esté corriendo
2. Abre: http://localhost:3000/health
3. Deberías ver: `{"status": "healthy"}`

## 📝 Comandos Útiles

```bash
# Ver logs del bot
# Los logs aparecen en la terminal donde ejecutaste python main.py

# Reiniciar bot
# Ctrl+C y luego: python main.py

# Ver estado de Baileys
curl http://localhost:3001/status

# Enviar mensaje de prueba
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{"phone":"573001234567","message":"Hola!"}'
```

## 🎉 ¡Todo Listo!

Tu bot ahora puede:
- ✅ Recibir mensajes de WhatsApp
- ✅ Procesar con IA (GROQ)
- ✅ Detectar intenciones
- ✅ Responder inteligentemente
- ✅ Manejar ventas completas
- ✅ Gestionar productos
- ✅ Agendar reservas
- ✅ Procesar pagos

## 📚 Documentación Adicional

- `BAILEYS_SETUP.md` - Configuración detallada de Baileys
- `FEATURES.md` - Lista completa de funcionalidades
- `INSTALLATION.md` - Guía de instalación completa
- `DASHBOARD_GUIDE.md` - Guía del dashboard

¿Necesitas ayuda? Revisa los logs en las terminales! 🚀
