# 🚀 Guía de Instalación y Configuración

## Requisitos Previos

### Software Necesario
- **Python 3.9+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 18+** - [Descargar](https://nodejs.org/)
- **PostgreSQL 14+** - [Descargar](https://www.postgresql.org/download/)
- **Git** - [Descargar](https://git-scm.com/)

### Cuentas y API Keys
- Cuenta GROQ con API keys - [Obtener](https://console.groq.com/)
- Cuenta Dropi (opcional) - [Registrarse](https://dropi.co/)
- MercadoPago (opcional) - [Desarrolladores](https://www.mercadopago.com.co/developers/)

## Instalación Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd whatsapp-sales-bot
```

### 2. Configurar Base de Datos PostgreSQL

**Crear base de datos:**
```sql
CREATE DATABASE botwhatsapp;
CREATE USER botuser WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE botwhatsapp TO botuser;
```

**Actualizar .env:**
```env
DATABASE_URL=postgresql://botuser:tu_password@localhost:5432/botwhatsapp
```

### 3. Instalar Dependencias Python

**Crear entorno virtual:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Instalar paquetes:**
```bash
pip install -r requirements.txt
```

### 4. Instalar Dependencias Node.js
```bash
npm install
```

### 5. Configurar Variables de Entorno

Edita el archivo `.env` con tus credenciales:

```env
# API Keys de GROQ (obligatorio)
GROQ_API_KEY=tu_api_key_aqui
GROQ_API_KEY_2=tu_segunda_key
GROQ_API_KEY_6=tu_tercera_key

# Información del negocio
BUSINESS_NAME=Tu Negocio
BUSINESS_PHONE=+57 300 123 4567
BUSINESS_EMAIL=tu@email.com

# WhatsApp
WHATSAPP_NUMBER=573001234567

# Pagos (opcional)
NEQUI_NUMBER=3001234567
DAVIPLATA_NUMBER=3001234567
MERCADO_PAGO_ACCESS_TOKEN=tu_token
```

### 6. Inicializar Base de Datos
```bash
python -c "from database.connection import init_db; init_db()"
```

### 7. Poblar con Datos de Ejemplo (Opcional)
```bash
python seed_database.py
```

## Iniciar el Bot

### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Opción 2: Manual

**Terminal 1 - Baileys (Node.js):**
```bash
npm start
```

**Terminal 2 - Python API:**
```bash
python main.py
```

## Conectar WhatsApp

1. Ejecuta el bot
2. En la terminal de Node.js aparecerá un QR code
3. Abre WhatsApp en tu teléfono
4. Ve a **Dispositivos vinculados** > **Vincular dispositivo**
5. Escanea el QR code
6. ¡Listo! El bot está conectado

## Verificar Instalación

### Endpoints de Prueba

**Estado del bot:**
```bash
curl http://localhost:3000/
```

**Estado de Baileys:**
```bash
curl http://localhost:3001/status
```

**Ver QR code (JSON):**
```bash
curl http://localhost:3001/qr
```

### Probar Conversación
```bash
python test_conversation.py
```

## Estructura de Carpetas

```
whatsapp-sales-bot/
├── agents/              # Agentes especializados
├── ai/                  # Cliente GROQ y gestión de IA
├── config/              # Configuración
├── database/            # Modelos y conexión DB
├── services/            # Lógica de negocio
├── utils/               # Utilidades
├── whatsapp/            # Cliente WhatsApp
├── baileys-server.js    # Servidor Node.js
├── main.py              # Servidor Python
└── .env                 # Variables de entorno
```

## Solución de Problemas

### Error: "No se puede conectar a PostgreSQL"
- Verifica que PostgreSQL esté corriendo
- Confirma las credenciales en `.env`
- Prueba la conexión: `psql -U botuser -d botwhatsapp`

### Error: "GROQ API key inválida"
- Verifica que las API keys sean correctas
- Asegúrate de tener créditos en GROQ
- Prueba con una sola key primero

### Error: "Baileys no conecta"
- Verifica que Node.js esté instalado
- Ejecuta `npm install` de nuevo
- Revisa que el puerto 3001 esté libre

### WhatsApp se desconecta constantemente
- Verifica tu conexión a internet
- No uses WhatsApp Web en otro navegador
- Revisa los logs en la terminal

## Configuración Avanzada

### Cambiar Puertos
```env
# En .env
PORT=3000  # Python API

# En baileys-server.js
const PORT = 3001;  # Baileys
```

### Ajustar Timeouts
```env
GROQ_TIMEOUT=60000
CONNECTION_TIMEOUT=60000
TYPING_DELAY_MIN=2000
TYPING_DELAY_MAX=4000
```

### Habilitar/Deshabilitar Funciones
```env
ENABLE_TYPING_SIMULATION=true
ENABLE_CONVERSATION_MEMORY=true
DROPI_ENABLED=true
MERCADOPAGO_ENABLED=true
```

## Despliegue en Producción

### Recomendaciones
- Usa un servidor VPS (DigitalOcean, AWS, etc.)
- Configura HTTPS con certificado SSL
- Usa PM2 para mantener procesos activos
- Configura backups automáticos de la DB
- Monitorea logs y errores

### PM2 (Recomendado)
```bash
# Instalar PM2
npm install -g pm2

# Iniciar Baileys
pm2 start baileys-server.js --name baileys

# Iniciar Python
pm2 start "python main.py" --name python-api

# Ver logs
pm2 logs

# Guardar configuración
pm2 save
pm2 startup
```

## Soporte

Si tienes problemas:
1. Revisa los logs en las terminales
2. Verifica que todas las dependencias estén instaladas
3. Confirma que las API keys sean válidas
4. Consulta la documentación de Baileys

## Próximos Pasos

- [ ] Personalizar prompts de agentes
- [ ] Agregar más productos a la DB
- [ ] Configurar métodos de pago
- [ ] Integrar con Dropi
- [ ] Crear dashboard web (opcional)
- [ ] Configurar notificaciones
