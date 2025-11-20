# 🔍 Diagnóstico - Dashboard Puerto 3000

## 🎯 Situación

Tienes el dashboard Next.js configurado en el puerto 3000 pero no arranca.

## 📋 Necesito Saber

### 1. ¿Tienes un servicio separado para el dashboard en Easypanel?

Ve a Easypanel → Tu proyecto

¿Ves estos servicios?
- [ ] bot-whatsapp-python (Backend)
- [ ] bot-whatsapp-dashboard (Frontend Next.js)
- [ ] bot-whatsapp-db (Base de datos)

O solo ves:
- [ ] bot-whatsapp-python (Backend)
- [ ] bot-whatsapp-db (Base de datos)

### 2. Si tienes el servicio del dashboard, ¿qué dicen los logs?

Easypanel → Servicio Dashboard → Logs

Busca errores como:
- `Error: Cannot find module 'next'`
- `Error: NEXTAUTH_SECRET is missing`
- `Error: Port 3000 is already in use`
- `npm ERR!`

### 3. ¿Qué configuración tiene el servicio del dashboard?

Easypanel → Servicio Dashboard → Settings

- Build Command: ¿Qué dice?
- Start Command: ¿Qué dice?
- Port: ¿Qué dice?
- Build Path: ¿Qué dice?

## 🔧 Soluciones Según el Caso

### CASO A: NO tienes servicio separado para el dashboard

Necesitas crear uno nuevo:

1. Easypanel → Add Service → App
2. Configurar:
   - Name: `bot-whatsapp-dashboard`
   - Source: GitHub (tu repositorio)
   - Branch: main
   - Build Path: `dashboard-nextjs`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`
   - Port: `3000`

3. Variables de entorno:
```env
NEXT_PUBLIC_API_URL=https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host/api
NEXTAUTH_URL=https://bot-whatsapp-dashboard.sqaoeo.easypanel.host
NEXTAUTH_SECRET=genera-un-secret-aleatorio
NODE_ENV=production
PORT=3000
```

### CASO B: SÍ tienes servicio pero no arranca

#### Solución 1: Verificar Build Path

El Build Path debe ser: `dashboard-nextjs`

Si está vacío o incorrecto, el build fallará.

#### Solución 2: Verificar package.json

El dashboard debe tener `package.json` en `dashboard-nextjs/package.json`

Verifica que exista y tenga estos scripts:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

#### Solución 3: Agregar NEXTAUTH_SECRET

El dashboard Next.js REQUIERE esta variable:

```env
NEXTAUTH_SECRET=cualquier-string-aleatorio-de-32-caracteres
```

Genera uno:
```bash
openssl rand -base64 32
```

O usa este:
```
NEXTAUTH_SECRET=tecnovariedades-dashboard-secret-2025-production-key
```

#### Solución 4: Forzar Rebuild

1. Easypanel → Servicio Dashboard
2. Click en "Rebuild" o "Redeploy"
3. Espera 5-10 minutos
4. Verifica los logs

#### Solución 5: Verificar Dependencias

Si el build falla con errores de módulos:

Build Command debe ser:
```
npm install && npm run build
```

NO solo:
```
npm run build
```

## 🎯 Solución Rápida (Mientras arreglas)

Usa el panel admin que SÍ funciona:

```
https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host/admin/dashboard
```

Credenciales:
- Email: `daveymena16@gmail.com`
- Password: `6715320Dvd.`

## 📊 Comparación de Opciones

| Opción | Ventajas | Desventajas |
|--------|----------|-------------|
| Panel Admin (puerto 5000) | ✅ Ya funciona<br>✅ No requiere configuración | ⚠️ Interfaz simple |
| Dashboard Next.js (puerto 3000) | ✅ Interfaz moderna<br>✅ Más funcionalidades | ⚠️ Requiere configuración<br>⚠️ Servicio adicional |

## 🔍 Comandos de Verificación

### Verificar si el dashboard existe en el repo

```bash
cd dashboard-nextjs
ls package.json
```

Debe existir.

### Verificar scripts en package.json

```bash
cat dashboard-nextjs/package.json | grep -A 5 "scripts"
```

Debe tener `build` y `start`.

### Probar build local

```bash
cd dashboard-nextjs
npm install
npm run build
npm start
```

Si funciona local, el problema es la configuración en Easypanel.

## 📋 Checklist

- [ ] Verifiqué si tengo servicio separado para el dashboard
- [ ] Revisé los logs del servicio
- [ ] Verifiqué el Build Path: `dashboard-nextjs`
- [ ] Verifiqué Build Command: `npm install && npm run build`
- [ ] Verifiqué Start Command: `npm start`
- [ ] Verifiqué Port: `3000`
- [ ] Agregué NEXTAUTH_SECRET
- [ ] Agregué NEXT_PUBLIC_API_URL
- [ ] Forcé un rebuild
- [ ] Esperé 5-10 minutos
- [ ] Revisé los logs nuevamente

## 🆘 Información que Necesito

Para ayudarte específicamente, comparte:

1. **¿Tienes servicio separado para el dashboard?** (Sí/No)
2. **Si sí, ¿qué dicen los logs?** (Últimas 20 líneas)
3. **¿Qué configuración tiene?** (Build Command, Start Command, Port)
4. **¿Qué variables de entorno tiene?** (Solo nombres, no valores)

Con esa información puedo darte la solución exacta.

## 🎯 Mientras Tanto

Usa el panel admin que funciona:
```
https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host/admin/dashboard
```

O usa Electron:
```bash
cd dashboard-electron
npm start
```

Ambos están configurados y funcionando.
