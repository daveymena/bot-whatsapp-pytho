# 🚀 Inicio Completo del Sistema

## Estado Actual

✅ Dashboard Next.js está corriendo en puerto 3001
❌ Servidor Python NO está corriendo (puerto 5000)
❌ Servidor Baileys NO está corriendo (puerto 3002)

## Pasos para Iniciar Todo

### Opción 1: Scripts Individuales (Recomendado)

Abre **3 terminales diferentes** y ejecuta en cada una:

**Terminal 1 - Servidor Python:**
```bash
INICIAR_PYTHON.bat
```

**Terminal 2 - Servidor Baileys:**
```bash
INICIAR_BAILEYS.bat
```

**Terminal 3 - Dashboard (ya está corriendo):**
```bash
# Ya lo tienes corriendo, no hagas nada aquí
```

### Opción 2: Inicio Manual

**Terminal 1 - Servidor Python:**
```bash
python main.py
```

**Terminal 2 - Servidor Baileys:**
```bash
cd baileys-server
node server.js
```

**Terminal 3 - Dashboard:**
```bash
cd dashboard-nextjs
npm run dev
```

## Verificar que Todo Esté Corriendo

Después de iniciar los 3 servidores, verifica:

**1. Servidor Python (Puerto 5000):**
```bash
curl http://localhost:5000/admin/whatsapp/status
```

Deberías ver algo como:
```json
{
  "success": true,
  "status": "DISCONNECTED",
  ...
}
```

**2. Servidor Baileys (Puerto 3002):**
```bash
curl http://localhost:3002/status
```

Deberías ver algo como:
```json
{
  "success": true,
  "status": "DISCONNECTED",
  ...
}
```

**3. Dashboard (Puerto 3001):**
Abre tu navegador en: `http://localhost:3001`

## Conectar WhatsApp

Una vez que los 3 servidores estén corriendo:

1. Abre `http://localhost:3001` en tu navegador
2. Inicia sesión si es necesario
3. Ve a la pestaña **"WhatsApp"**
4. Haz clic en **"Reconectar"**
5. Espera 10-15 segundos
6. El código QR aparecerá
7. Escanéalo con tu WhatsApp

## Orden de Inicio Recomendado

Es importante iniciar los servidores en este orden:

1. **Primero:** Servidor Python (puerto 5000)
2. **Segundo:** Servidor Baileys (puerto 3002)
3. **Tercero:** Dashboard Next.js (puerto 3001)

## Logs que Deberías Ver

### Servidor Python (Terminal 1):
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000
```

### Servidor Baileys (Terminal 2):
```
============================================================
🚀 SERVIDOR BAILEYS INICIADO
============================================================
📡 Puerto: 3002
🔗 API: http://localhost:3002
🐍 Python API: http://localhost:5000
============================================================
🔄 Iniciando conexión a WhatsApp...
```

### Dashboard Next.js (Terminal 3):
```
▲ Next.js 14.2.33
- Local:        http://localhost:3001
✓ Ready in 2.4s
```

## Troubleshooting

### Error: "ECONNREFUSED" en el Dashboard

**Causa:** El servidor Python o Baileys no está corriendo

**Solución:**
1. Verifica que ambos servidores estén corriendo
2. Revisa las terminales para ver si hay errores
3. Reinicia los servidores si es necesario

### Error: "EADDRINUSE" (Puerto en uso)

**Causa:** Ya hay un proceso usando ese puerto

**Solución para puerto 5000:**
```bash
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

**Solución para puerto 3002:**
```bash
netstat -ano | findstr :3002
taskkill /PID [PID_NUMBER] /F
```

**Solución para puerto 3001:**
```bash
netstat -ano | findstr :3001
taskkill /PID [PID_NUMBER] /F
```

### El QR no aparece

**Posibles causas:**
1. El servidor Baileys no está corriendo
2. El servidor Python no está corriendo
3. Hay un error en la conexión

**Solución:**
1. Verifica que los 3 servidores estén corriendo
2. Revisa los logs de cada terminal
3. Limpia la sesión y reconecta

## Comandos Útiles

**Ver todos los puertos en uso:**
```bash
netstat -ano | findstr :5000
netstat -ano | findstr :3002
netstat -ano | findstr :3001
```

**Matar todos los procesos de Node.js:**
```bash
taskkill /F /IM node.exe
```

**Matar todos los procesos de Python:**
```bash
taskkill /F /IM python.exe
```

## Resumen Visual

```
┌─────────────────────────────────────────────────────────┐
│                    ARQUITECTURA                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Terminal 3] Dashboard Next.js (Puerto 3001) ✅        │
│         │                                                │
│         │ HTTP Requests                                 │
│         ↓                                                │
│  [Terminal 1] Servidor Python (Puerto 5000) ❌          │
│         │                                                │
│         │ HTTP Requests                                 │
│         ↓                                                │
│  [Terminal 2] Servidor Baileys (Puerto 3002) ❌         │
│         │                                                │
│         │ WhatsApp Web Protocol                         │
│         ↓                                                │
│  WhatsApp Servers                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Próximos Pasos

1. ✅ Dashboard está corriendo
2. ⏳ Inicia el servidor Python: `INICIAR_PYTHON.bat`
3. ⏳ Inicia el servidor Baileys: `INICIAR_BAILEYS.bat`
4. ⏳ Abre el dashboard y conecta WhatsApp

## Notas Importantes

- ⚠️ No cierres ninguna de las 3 terminales mientras uses el sistema
- ⚠️ Si reinicias un servidor, espera 5 segundos antes de usar el dashboard
- ⚠️ El código QR expira después de 60 segundos
- ⚠️ Solo puedes tener una sesión activa de WhatsApp Web

## Archivos de Ayuda

- `INICIAR_PYTHON.bat` - Inicia servidor Python
- `INICIAR_BAILEYS.bat` - Inicia servidor Baileys
- `REINICIAR_DASHBOARD.bat` - Reinicia dashboard
- `CHECK_SERVERS.bat` - Verifica estado de servidores
- `START_ALL_FIXED.bat` - Inicia todo automáticamente
