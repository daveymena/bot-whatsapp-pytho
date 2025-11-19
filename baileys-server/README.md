# 📱 Servidor Baileys para WhatsApp

Este servidor maneja la conexión real con WhatsApp usando Baileys.

## 🚀 Instalación

```bash
cd baileys-server
npm install
```

## ▶️ Iniciar

```bash
npm start
```

## 📋 Endpoints

- `GET /status` - Estado de la conexión
- `POST /send-message` - Enviar mensaje
- `POST /disconnect` - Desconectar
- `POST /reconnect` - Reconectar

## 🔧 Configuración

El servidor se conecta automáticamente al iniciar.
Escanea el QR code que aparece en la terminal con WhatsApp.

## 🔗 Integración

El servidor se comunica con la API de Python en `http://localhost:3000`
