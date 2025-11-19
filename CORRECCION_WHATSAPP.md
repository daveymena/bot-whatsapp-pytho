# ✅ Corrección del Error de WhatsApp

## Problema Identificado

El dashboard mostraba el error: **"Error al conectar WhatsApp"**

## Causa Raíz

La variable de entorno `NEXT_PUBLIC_API_URL` en el archivo `.env.local` del dashboard estaba configurada incorrectamente:

```env
# ❌ INCORRECTO
NEXT_PUBLIC_API_URL=http://localhost:3001
```

Esto hacía que el dashboard intentara conectarse a sí mismo (puerto 3001) en lugar de conectarse al servidor Python (puerto 5000).

## Solución Aplicada

### 1. Corregir variables de entorno

**Archivo:** `dashboard-nextjs/.env.local`

```env
# ✅ CORRECTO
BACKEND_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 2. Mejorar manejo de errores

Se mejoró el componente `WhatsAppTab.tsx` para:
- Mostrar mensajes de error más descriptivos
- Agregar timeout de 5 segundos en las peticiones
- Mostrar alertas visuales cuando hay problemas de conexión
- Indicar claramente qué servidor no está respondiendo

### 3. Agregar botón "Limpiar Sesión"

Se agregó funcionalidad para limpiar la sesión de WhatsApp cuando hay problemas:
- Botón en la interfaz del dashboard
- Nueva ruta `/cleanup` en el servidor Baileys
- Elimina archivos de autenticación corruptos

### 4. Mejorar servidor Baileys

Se mejoró el manejo de reconexiones en `baileys-server/server.js`:
- Evita múltiples conexiones simultáneas
- Mejor manejo de errores
- Logs más descriptivos

### 5. Scripts de diagnóstico

Se crearon nuevos scripts para facilitar el diagnóstico:

**CHECK_SERVERS.bat** - Verifica que todos los servidores estén corriendo
**START_ALL_FIXED.bat** - Inicia todos los servidores correctamente
**SOLUCION_WHATSAPP.md** - Guía completa de solución de problemas

## Cómo Usar Después de la Corrección

### Paso 1: Reiniciar el dashboard Next.js

Si el dashboard ya está corriendo, debes reiniciarlo para que tome los nuevos valores:

1. Ve a la terminal donde corre el dashboard
2. Presiona `Ctrl+C` para detenerlo
3. Vuelve a iniciarlo:
```bash
cd dashboard-nextjs
npm run dev
```

### Paso 2: Verificar servidores

Ejecuta el script de verificación:
```bash
CHECK_SERVERS.bat
```

Debes ver:
- ✅ Servidor Python corriendo (puerto 5000)
- ✅ Servidor Baileys corriendo (puerto 3002)
- ✅ Dashboard Next.js corriendo (puerto 3001)

### Paso 3: Conectar WhatsApp

1. Abre el dashboard en `http://localhost:3001`
2. Ve a la pestaña "WhatsApp"
3. Si está desconectado, haz clic en **"Reconectar"**
4. Espera a que aparezca el código QR (10-15 segundos)
5. Escanea el QR con tu WhatsApp

### Si el problema persiste

1. **Limpia la sesión:**
   - Haz clic en el botón **"Limpiar Sesión"** en el dashboard
   - O manualmente: `cd baileys-server && rmdir /s /q auth_info`

2. **Reinicia el servidor Baileys:**
   - Cierra la terminal (Ctrl+C)
   - Vuelve a iniciar: `cd baileys-server && node server.js`

3. **Reconecta WhatsApp:**
   - En el dashboard, haz clic en **"Reconectar"**
   - Escanea el nuevo QR

## Arquitectura de Puertos

Para entender mejor cómo funciona el sistema:

```
┌─────────────────────────────────────────────────────────┐
│                    ARQUITECTURA                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Dashboard Next.js (Puerto 3001)                        │
│         │                                                │
│         │ HTTP Requests                                 │
│         ↓                                                │
│  Servidor Python FastAPI (Puerto 5000)                  │
│         │                                                │
│         │ HTTP Requests                                 │
│         ↓                                                │
│  Servidor Baileys (Puerto 3002)                         │
│         │                                                │
│         │ WhatsApp Web Protocol                         │
│         ↓                                                │
│  WhatsApp Servers                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Variables de Entorno Importantes

### Dashboard Next.js (.env.local)
```env
BACKEND_URL=http://localhost:5000          # Servidor Python
NEXT_PUBLIC_API_URL=http://localhost:5000  # Servidor Python (para cliente)
```

### Servidor Python (.env)
```env
PORT=3000                                  # Puerto del servidor Python
WHATSAPP_PROVIDER=baileys                  # Proveedor de WhatsApp
```

### Servidor Baileys (hardcoded en server.js)
```javascript
const PORT = 3002                          // Puerto del servidor Baileys
const PYTHON_API = 'http://localhost:5000' // URL del servidor Python
```

## Archivos Modificados

1. ✅ `dashboard-nextjs/.env.local` - Corregida URL de API
2. ✅ `dashboard-nextjs/.env.example` - Actualizado ejemplo
3. ✅ `dashboard-nextjs/src/components/whatsapp/WhatsAppTab.tsx` - Mejorado manejo de errores
4. ✅ `dashboard-nextjs/src/app/api/whatsapp/cleanup/route.ts` - Nueva funcionalidad
5. ✅ `baileys-server/server.js` - Mejorado manejo de reconexiones
6. ✅ `CHECK_SERVERS.bat` - Nuevo script de verificación
7. ✅ `START_ALL_FIXED.bat` - Nuevo script de inicio
8. ✅ `SOLUCION_WHATSAPP.md` - Nueva guía de solución

## Próximos Pasos

1. **Reinicia el dashboard** para aplicar los cambios
2. **Verifica los servidores** con `CHECK_SERVERS.bat`
3. **Conecta WhatsApp** desde el dashboard
4. **Prueba el bot** enviando un mensaje

## Notas Importantes

- ⚠️ Siempre inicia los servidores en este orden:
  1. Servidor Python (puerto 5000)
  2. Servidor Baileys (puerto 3002)
  3. Dashboard Next.js (puerto 3001)

- ⚠️ Si cambias variables de entorno, debes reiniciar el servidor correspondiente

- ⚠️ El código QR expira después de 60 segundos, si no lo escaneas a tiempo, haz clic en "Reconectar" para generar uno nuevo

- ⚠️ No cierres las terminales de los servidores mientras uses el sistema

## Soporte

Si después de aplicar estas correcciones el problema persiste, consulta:
- `SOLUCION_WHATSAPP.md` - Guía detallada de solución de problemas
- `BAILEYS_SETUP.md` - Configuración del servidor Baileys
- `PORTS_CONFIG.md` - Configuración de puertos
