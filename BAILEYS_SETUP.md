# 📱 Configuración de Baileys - WhatsApp Real

## 🚀 Instalación Rápida

### Paso 1: Instalar Node.js
Si no tienes Node.js instalado:
1. Descarga desde: https://nodejs.org/
2. Instala la versión LTS (recomendada)
3. Verifica: `node --version`

### Paso 2: Instalar Dependencias de Baileys

```bash
cd baileys-server
npm install
```

### Paso 3: Iniciar Servidor Baileys

**Opción A - Windows:**
```bash
start.bat
```

**Opción B - Manual:**
```bash
npm start
```

### Paso 4: Escanear QR Code

1. El servidor mostrará un QR code en la terminal
2. Abre WhatsApp en tu teléfono
3. Ve a: Configuración > Dispositivos vinculados
4. Toca "Vincular un dispositivo"
5. Escanea el QR code

¡Listo! Tu bot está conectado a WhatsApp.

## 📊 Verificar Conexión

1. Abre: http://localhost:3001/status
2. Deberías ver: `{"status": "CONNECTED"}`

## 🔧 Arquitectura

```
┌─────────────────┐      HTTP      ┌──────────────────┐
│   Python Bot    │ ◄──────────────► │  Baileys Server  │
│  (FastAPI)      │                 │    (Node.js)     │
│  Port: 3000     │                 │   Port: 3001     │
└─────────────────┘                 └──────────────────┘
                                            │
                                            │ WebSocket
                                            ▼
                                    ┌──────────────────┐
                                    │   WhatsApp Web   │
                                    └──────────────────┘
```

## 🔄 Flujo de Mensajes

1. **Cliente envía mensaje** → WhatsApp
2. **Baileys recibe** → Servidor Node.js
3. **Servidor envía** → Python API (`/webhook/message`)
4. **Python procesa** → Agentes IA
5. **Python responde** → Baileys
6. **Baileys envía** → WhatsApp → Cliente

## 📝 Endpoints Baileys

### GET /status
Obtiene el estado de la conexión
```json
{
  "success": true,
  "status": "CONNECTED",
  "connection": {
    "phoneNumber": "573042748687",
    "lastConnectedAt": "2025-11-19T...",
    "isActive": true
  }
}
```

### POST /send-message
Envía un mensaje
```json
{
  "phone": "573001234567",
  "message": "Hola desde el bot!"
}
```

### POST /disconnect
Desconecta WhatsApp

### POST /reconnect
Reconecta WhatsApp

## 🛠️ Troubleshooting

### Error: "Cannot find module '@whiskeysockets/baileys'"
```bash
cd baileys-server
npm install
```

### Error: "EADDRINUSE: address already in use"
El puerto 3001 está ocupado. Cierra el proceso o cambia el puerto en `server.js`

### QR Code no aparece
1. Verifica que el servidor esté corriendo
2. Revisa los logs en la terminal
3. Intenta reiniciar: `npm start`

### WhatsApp se desconecta constantemente
1. Verifica tu conexión a internet
2. Asegúrate de que WhatsApp esté actualizado
3. Revisa los logs del servidor

## 🔐 Seguridad

- Las credenciales se guardan en `auth_info/`
- **NO subas** esta carpeta a Git
- Está incluida en `.gitignore`

## 📦 Dependencias

- `@whiskeysockets/baileys` - Cliente WhatsApp
- `express` - Servidor HTTP
- `cors` - CORS middleware
- `qrcode-terminal` - Mostrar QR en terminal
- `pino` - Logger
- `axios` - HTTP client

## 🚀 Producción

Para producción, considera:
1. Usar PM2 para mantener el proceso activo
2. Configurar variables de entorno
3. Implementar logging robusto
4. Configurar reconexión automática
5. Monitorear el estado de la conexión

```bash
# Instalar PM2
npm install -g pm2

# Iniciar con PM2
pm2 start server.js --name baileys-bot

# Ver logs
pm2 logs baileys-bot

# Reiniciar
pm2 restart baileys-bot
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del servidor
2. Verifica que Python API esté corriendo
3. Comprueba la conexión a internet
4. Consulta la documentación de Baileys

¡Tu bot está listo para recibir y enviar mensajes reales por WhatsApp! 🎉
