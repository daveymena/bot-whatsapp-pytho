# 🔧 Reiniciar Servidor Baileys

## Problema Corregido

Se corrigió el error: `ReferenceError: saveCreds is not defined`

El problema era que la variable `saveCreds` estaba fuera del scope donde se usaba.

## Cómo Reiniciar

### 1. Detener el servidor actual

En la terminal donde está corriendo Baileys, presiona:
```
Ctrl + C
```

### 2. Volver a iniciar

```bash
cd C:\ventas-2
INICIAR_BAILEYS.bat
```

O manualmente:
```bash
cd C:\ventas-2\baileys-server
node server.js
```

## Qué Deberías Ver

Después de reiniciar, deberías ver:

```
============================================================
🚀 SERVIDOR BAILEYS INICIADO
============================================================
📡 Puerto: 3002
🔗 API: http://localhost:3002
🐍 Python API: http://localhost:5000
============================================================
🔄 Iniciando conexión a WhatsApp...
📱 QR Code generado
```

Y el QR debería aparecer en la terminal (en formato ASCII).

## Próximos Pasos

Una vez que el servidor Baileys esté corriendo correctamente:

1. Abre el dashboard en `http://localhost:3001`
2. Ve a la pestaña "WhatsApp"
3. El QR debería aparecer automáticamente
4. Si no aparece, haz clic en "Reconectar"
5. Escanea el QR con tu WhatsApp

## Verificar que Funciona

Puedes verificar que el servidor está corriendo correctamente con:

```bash
curl http://localhost:3002/status
```

Deberías ver algo como:
```json
{
  "success": true,
  "status": "QR_PENDING",
  "qrCode": "2@...",
  "connection": {
    "phoneNumber": null,
    "lastConnectedAt": null,
    "isActive": false
  }
}
```
