# ✅ Pasos Finales para Ver el QR Code

## Estado Actual

✅ La librería `qrcode.react@4.2.0` está instalada correctamente
✅ El código del componente WhatsApp está actualizado
✅ Los archivos de configuración están corregidos

## Próximos Pasos

### 1. Reiniciar el Dashboard Next.js

**Opción A: Usar el script automático**
```bash
REINICIAR_DASHBOARD.bat
```

**Opción B: Manual**

Si tienes el dashboard corriendo en otra terminal:
1. Ve a esa terminal
2. Presiona `Ctrl+C` para detenerlo
3. Ejecuta:
```bash
cd dashboard-nextjs
npm run dev
```

Si NO tienes el dashboard corriendo:
```bash
cd dashboard-nextjs
npm run dev
```

### 2. Verificar que todos los servidores estén corriendo

Necesitas tener 3 servidores corriendo:

**Terminal 1 - Servidor Python (Puerto 5000)**
```bash
python main.py
```

**Terminal 2 - Servidor Baileys (Puerto 3002)**
```bash
cd baileys-server
node server.js
```

**Terminal 3 - Dashboard Next.js (Puerto 3001)**
```bash
cd dashboard-nextjs
npm run dev
```

### 3. Abrir el Dashboard

1. Abre tu navegador
2. Ve a: `http://localhost:3001`
3. Inicia sesión si es necesario
4. Ve a la pestaña **"WhatsApp"**

### 4. Conectar WhatsApp

1. Si está desconectado, haz clic en **"Reconectar"**
2. Espera 10-15 segundos
3. El código QR debería aparecer (ahora como SVG, no como imagen)
4. Escanea el QR con tu WhatsApp:
   - Abre WhatsApp en tu teléfono
   - Ve a Configuración → Dispositivos vinculados
   - Toca "Vincular un dispositivo"
   - Escanea el código QR

## Qué Cambió

### Antes
- El QR se generaba usando un servicio externo (`api.qrserver.com`)
- Aparecía como imagen PNG
- Podía fallar si el servicio externo no respondía

### Ahora
- El QR se genera directamente en el navegador
- Aparece como SVG (mejor calidad)
- No depende de servicios externos
- Más rápido y confiable

## Verificación Visual

Cuando el QR aparezca correctamente, deberías ver:

```
┌─────────────────────────────────────────┐
│  Escanea el Código QR                   │
│  Abre WhatsApp en tu teléfono y         │
│  escanea este código para conectar      │
│                                         │
│  ┌───────────────────────────────┐     │
│  │                               │     │
│  │   [Código QR en SVG]          │     │
│  │   (Cuadrado negro con         │     │
│  │    patrones QR)               │     │
│  │                               │     │
│  └───────────────────────────────┘     │
│                                         │
│  Instrucciones paso a paso...           │
└─────────────────────────────────────────┘
```

## Troubleshooting

### El QR sigue sin aparecer

1. **Verifica la consola del navegador:**
   - Presiona F12
   - Ve a la pestaña "Console"
   - Busca errores en rojo

2. **Verifica que el servidor Baileys esté corriendo:**
   ```bash
   curl http://localhost:3002/status
   ```
   
   Deberías ver algo como:
   ```json
   {
     "success": true,
     "status": "QR_PENDING",
     "qrCode": "2@..."
   }
   ```

3. **Verifica que el servidor Python esté corriendo:**
   ```bash
   curl http://localhost:5000/admin/whatsapp/status
   ```

### Error: "Module not found: Can't resolve 'qrcode.react'"

**Solución:** Reinstala la librería
```bash
cd dashboard-nextjs
npm install qrcode.react
npm run dev
```

### El QR aparece pero está en blanco

**Causa:** El servidor Baileys no está generando el QR correctamente

**Solución:**
1. Limpia la sesión de WhatsApp:
   ```bash
   cd baileys-server
   rmdir /s /q auth_info
   ```

2. Reinicia el servidor Baileys:
   - Presiona Ctrl+C en la terminal de Baileys
   - Vuelve a ejecutar: `node server.js`

3. En el dashboard, haz clic en "Reconectar"

### El QR aparece pero no se puede escanear

**Posibles causas:**
1. El QR expiró (expira después de 60 segundos)
2. Ya tienes una sesión activa de WhatsApp Web

**Solución:**
1. Cierra todas las sesiones de WhatsApp Web
2. En el dashboard, haz clic en "Limpiar Sesión"
3. Espera 5 segundos
4. Haz clic en "Reconectar"
5. Escanea el nuevo QR rápidamente

## Comandos Útiles

**Ver si el dashboard está corriendo:**
```bash
netstat -ano | findstr :3001
```

**Ver si Baileys está corriendo:**
```bash
netstat -ano | findstr :3002
```

**Ver si Python está corriendo:**
```bash
netstat -ano | findstr :5000
```

**Matar proceso en puerto específico:**
```bash
# Para puerto 3001
netstat -ano | findstr :3001
taskkill /PID [PID_NUMBER] /F
```

## Resumen de Archivos Modificados

1. ✅ `dashboard-nextjs/package.json` - Agregada `qrcode.react`
2. ✅ `dashboard-nextjs/src/components/whatsapp/WhatsAppTab.tsx` - Usa QRCodeSVG
3. ✅ `dashboard-nextjs/.env.local` - Corregida URL de API
4. ✅ `baileys-server/server.js` - Mejorado manejo de reconexiones

## Siguiente Paso

**Reinicia el dashboard y prueba la conexión:**

```bash
# Si el dashboard está corriendo, detenlo (Ctrl+C)
# Luego ejecuta:
cd dashboard-nextjs
npm run dev
```

O simplemente ejecuta:
```bash
REINICIAR_DASHBOARD.bat
```

Luego abre `http://localhost:3001` y ve a la pestaña WhatsApp.

## ¿Necesitas Ayuda?

Si después de seguir todos estos pasos el QR sigue sin aparecer:

1. Toma capturas de pantalla de:
   - El dashboard (pestaña WhatsApp)
   - La consola del navegador (F12)
   - La terminal del servidor Baileys
   - La terminal del servidor Python

2. Revisa los archivos de documentación:
   - `FIX_QR_CODE.md` - Solución del QR
   - `SOLUCION_WHATSAPP.md` - Solución general de WhatsApp
   - `CORRECCION_WHATSAPP.md` - Corrección de URLs
