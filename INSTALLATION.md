# 🚀 Guía de Instalación Completa

## Requisitos Previos

- Python 3.9 o superior
- PostgreSQL 12 o superior
- Node.js 16+ (para Baileys)
- Git

## Paso 1: Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd whatsapp-sales-bot
```

## Paso 2: Crear Entorno Virtual

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

## Paso 3: Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

## Paso 4: Configurar Base de Datos PostgreSQL

1. Crear base de datos:
```sql
CREATE DATABASE botwhatsapp;
CREATE USER botuser WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE botwhatsapp TO botuser;
```

2. Actualizar `.env` con tu conexión:
```env
DATABASE_URL=postgresql://botuser:tu_password@localhost:5432/botwhatsapp
```

## Paso 5: Configurar Variables de Entorno

Edita el archivo `.env` con tus credenciales:

```env
# API Keys de GROQ (obtener en https://console.groq.com)
GROQ_API_KEY=tu_api_key_aqui
GROQ_API_KEY_2=tu_segunda_api_key
GROQ_API_KEY_6=tu_tercera_api_key

# WhatsApp
WHATSAPP_NUMBER=57300123456

# Negocio
BUSINESS_NAME=Tu Negocio
BUSINESS_PHONE=+57 300 123 4567
BUSINESS_EMAIL=tu@email.com

# Pagos
NEQUI_NUMBER=3001234567
DAVIPLATA_NUMBER=3001234567
BANK_ACCOUNT_NUMBER=12345678901

# Dropi (si usas dropshipping)
DROPI_AGENT_TOKEN=tu_token_dropi
```

## Paso 6: Inicializar Base de Datos

```bash
python -c "from database.connection import init_db; init_db()"
```

## Paso 7: Instalar Baileys (Node.js)

Crea un proyecto Node.js separado para Baileys:

```bash
mkdir baileys-server
cd baileys-server
npm init -y
npm install @whiskeysockets/baileys qrcode-terminal
```

Crea `server.js`:
```javascript
const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });
    
    sock.ev.on('creds.update', saveCreds);
    
    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.key.fromMe && msg.message) {
            const phone = msg.key.remoteJid;
            const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
            
            // Enviar a Python API
            const response = await fetch('http://localhost:3000/webhook/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone, message: text })
            });
            
            const data = await response.json();
            
            // Enviar respuesta
            if (data.reply) {
                await sock.sendMessage(phone, { text: data.reply });
            }
        }
    });
}

connectToWhatsApp();
```

## Paso 8: Iniciar el Bot

### Terminal 1 - Python API
```bash
python main.py
```

### Terminal 2 - Baileys Server
```bash
cd baileys-server
node server.js
```

Escanea el código QR con WhatsApp.

## Paso 9: Verificar Instalación

1. Abre: http://localhost:3000/health
2. Deberías ver: `{"status": "healthy"}`
3. Panel Admin: http://localhost:3000/admin/dashboard

## Paso 10: Poblar Base de Datos (Opcional)

Crea productos de ejemplo:

```python
from database.connection import SessionLocal
from database.models import Product

db = SessionLocal()

productos = [
    Product(
        name="iPhone 15 Pro",
        description="Último modelo de Apple",
        price=4500000,
        category="Electrónica",
        stock=10,
        warranty="1 año"
    ),
    Product(
        name="Curso Python Completo",
        description="Aprende Python desde cero",
        price=150000,
        category="Cursos",
        is_digital=True,
        stock=999
    )
]

for p in productos:
    db.add(p)

db.commit()
print("✅ Productos creados")
```

## Integración con Google Sheets (Opcional)

1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear credenciales de servicio
4. Descargar `credentials.json`
5. Colocar en la raíz del proyecto

```python
from integrations.google_sheets import sheets_integration

sheets_integration.connect("Nombre de tu Spreadsheet")
```

## Solución de Problemas

### Error de conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql  # Linux
# o
pg_ctl status  # Windows
```

### Error con GROQ API
- Verifica que tus API keys sean válidas
- Revisa límites de rate en https://console.groq.com

### Baileys no conecta
- Asegúrate de tener Node.js 16+
- Elimina carpeta `auth_info` y vuelve a escanear QR
- Verifica que WhatsApp Web esté disponible

## Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f logs/bot.log

# Reiniciar base de datos
python -c "from database.connection import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"

# Verificar dependencias
pip list

# Actualizar dependencias
pip install --upgrade -r requirements.txt
```

## Próximos Pasos

1. Personaliza los prompts de los agentes en `agents/`
2. Agrega tus productos a la base de datos
3. Configura métodos de pago
4. Prueba el bot enviando mensajes
5. Monitorea en el panel admin

## Soporte

Si tienes problemas, revisa:
- Logs en consola
- Panel admin: http://localhost:3000/admin/dashboard
- API docs: http://localhost:3000/docs

¡Listo! Tu bot está operativo 🎉
