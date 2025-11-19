# 🔧 Solución: QR Code no se muestra

## Problema

El código QR no se muestra correctamente, solo aparece el texto "QR Code" o una imagen rota.

## Causa

El componente estaba usando un servicio externo (`api.qrserver.com`) para generar el QR, pero este servicio puede estar bloqueado o no responder correctamente.

## Solución

Se cambió la implementación para generar el QR directamente en el navegador usando la librería `qrcode.react`.

## Pasos para aplicar la solución

### 1. Instalar la nueva dependencia

**Opción A: Usar el script automático**
```bash
INSTALAR_QR.bat
```

**Opción B: Instalación manual**
```bash
cd dashboard-nextjs
npm install qrcode.react
```

### 2. Reiniciar el dashboard

1. Ve a la terminal donde corre el dashboard Next.js
2. Presiona `Ctrl+C` para detenerlo
3. Vuelve a iniciarlo:
```bash
npm run dev
```

### 3. Verificar que funcione

1. Abre el dashboard en `http://localhost:3001`
2. Ve a la pestaña "WhatsApp"
3. Si está desconectado, haz clic en "Reconectar"
4. Espera 10-15 segundos
5. El código QR debería aparecer correctamente

## Qué se cambió

### Antes (usando API externa):
```typescript
// ❌ Dependía de un servicio externo
const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(status.qrCode)}`
<img src={qrUrl} alt="QR Code" />
```

### Después (generación local):
```typescript
// ✅ Genera el QR directamente en el navegador
import { QRCodeSVG } from 'qrcode.react'

<QRCodeSVG
  value={status.qrCode}
  size={288}
  level="H"
  includeMargin={true}
/>
```

## Ventajas de la nueva implementación

1. ✅ **Más rápido**: No depende de servicios externos
2. ✅ **Más confiable**: Funciona sin conexión a internet (después de cargar la página)
3. ✅ **Mejor calidad**: Genera SVG en lugar de imagen PNG
4. ✅ **Sin límites**: No hay límites de uso de API externa
5. ✅ **Más seguro**: El código QR no se envía a servidores externos

## Verificación

Para verificar que la librería se instaló correctamente:

```bash
cd dashboard-nextjs
npm list qrcode.react
```

Deberías ver algo como:
```
ventas-bot-dashboard@1.0.0
└── qrcode.react@4.1.0
```

## Troubleshooting

### El QR sigue sin aparecer

1. **Verifica que el servidor Baileys esté corriendo:**
   ```bash
   curl http://localhost:3002/status
   ```

2. **Verifica que el servidor Python esté corriendo:**
   ```bash
   curl http://localhost:5000/admin/whatsapp/status
   ```

3. **Limpia la sesión y reconecta:**
   - Haz clic en "Limpiar Sesión"
   - Espera 5 segundos
   - Haz clic en "Reconectar"

### Error: "Cannot find module 'qrcode.react'"

**Solución:** La librería no se instaló correctamente

```bash
cd dashboard-nextjs
npm install qrcode.react --save
npm run dev
```

### El QR aparece pero no se puede escanear

**Posibles causas:**
1. El código QR expiró (expira después de 60 segundos)
2. Ya hay una sesión activa en WhatsApp

**Solución:**
1. Limpia la sesión: Botón "Limpiar Sesión"
2. Reconecta: Botón "Reconectar"
3. Escanea el nuevo QR rápidamente (dentro de 60 segundos)

### El QR aparece muy pequeño o muy grande

El tamaño está configurado en 288px (72 * 4). Si quieres cambiarlo, edita el archivo:

`dashboard-nextjs/src/components/whatsapp/WhatsAppTab.tsx`

```typescript
<QRCodeSVG
  value={status.qrCode}
  size={288}  // Cambia este valor (ej: 256, 320, 384)
  level="H"
  includeMargin={true}
/>
```

## Archivos modificados

1. ✅ `dashboard-nextjs/package.json` - Agregada dependencia `qrcode.react`
2. ✅ `dashboard-nextjs/src/components/whatsapp/WhatsAppTab.tsx` - Cambiado a QRCodeSVG
3. ✅ `INSTALAR_QR.bat` - Script de instalación
4. ✅ `FIX_QR_CODE.md` - Esta guía

## Próximos pasos

1. Ejecuta `INSTALAR_QR.bat` o instala manualmente
2. Reinicia el dashboard
3. Prueba la conexión de WhatsApp
4. Escanea el QR con tu teléfono

## Notas importantes

- ⚠️ El código QR expira después de 60 segundos
- ⚠️ Solo puedes tener una sesión activa de WhatsApp Web a la vez
- ⚠️ Si ya tienes WhatsApp Web abierto en otro navegador, ciérralo primero
- ⚠️ Asegúrate de tener buena conexión a internet en tu teléfono al escanear

## Soporte adicional

Si después de seguir estos pasos el problema persiste:

1. Revisa los logs del servidor Baileys (terminal donde corre `node server.js`)
2. Revisa la consola del navegador (F12 → Console)
3. Consulta `SOLUCION_WHATSAPP.md` para más opciones de diagnóstico
