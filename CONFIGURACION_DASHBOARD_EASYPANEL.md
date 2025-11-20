# ⚙️ Configuración Correcta del Dashboard en Easypanel

## 🎯 Problema Resuelto

El dashboard estaba configurado para el puerto 3001, ahora está en 3000.

## 📋 Configuración para Easypanel

### Crear Servicio del Dashboard

1. **Ve a Easypanel** → Tu proyecto
2. **Click en "Add Service"** → "App"
3. **Configura así:**

#### General
```
Name: bot-whatsapp-dashboard
Source: GitHub
Repository: tu-repositorio
Branch: main
```

#### Build
```
Build Path: dashboard-nextjs
Build Command: npm install && npm run build
Start Command: npm start
```

#### Networking
```
Port: 3000
Domain: (Easypanel generará uno automático)
```

Ejemplo de dominio:
```
bot-whatsapp-dashboard.sqaoeo.easypanel.host
```

### Variables de Entorno

Agrega estas variables en el servicio del dashboard:

```env
# API del Backend
NEXT_PUBLIC_API_URL=https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host/api

# Auth (OBLIGATORIO)
NEXTAUTH_URL=https://bot-whatsapp-dashboard.sqaoeo.easypanel.host
NEXTAUTH_SECRET=tecnovariedades-dashboard-secret-2025-production-key

# Sistema
NODE_ENV=production
PORT=3000
```

**IMPORTANTE:** Reemplaza `bot-whatsapp-dashboard.sqaoeo.easypanel.host` con el dominio que Easypanel te asigne.

## 🚀 Pasos para Desplegar

### 1. Subir Cambios a Git

```bash
git add dashboard-nextjs/package.json
git commit -m "fix: cambiar puerto del dashboard de 3001 a 3000"
git push
```

### 2. Crear Servicio en Easypanel

Sigue la configuración de arriba.

### 3. Esperar el Build

El primer build tarda 5-10 minutos.

### 4. Verificar Logs

Easypanel → Servicio Dashboard → Logs

Busca:
```
✓ Ready in X ms
✓ Local: http://localhost:3000
```

### 5. Acceder

Una vez desplegado:
```
https://bot-whatsapp-dashboard.sqaoeo.easypanel.host
```

## 🔧 Solución de Problemas

### Error: NEXTAUTH_SECRET is missing

Agrega la variable:
```env
NEXTAUTH_SECRET=tecnovariedades-dashboard-secret-2025-production-key
```

### Error: Cannot find module 'next'

Build Command debe incluir `npm install`:
```
npm install && npm run build
```

### Error: Port 3000 is already in use

Verifica que el Port en Easypanel sea `3000`.

### Build falla

Revisa los logs del build en Easypanel.

Errores comunes:
- Falta `package.json`
- Build Path incorrecto
- Dependencias faltantes

## 📊 Arquitectura Final

```
┌─────────────────────────────────────────┐
│         EASYPANEL                       │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Backend Python (Puerto 5000)    │  │
│  │  bot-whatsapp-bot-inteligente    │  │
│  │  - API: /api/*                   │  │
│  │  - Panel Admin: /admin/dashboard │  │
│  │  - Health: /health               │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Dashboard Next.js (Puerto 3000) │  │
│  │  bot-whatsapp-dashboard          │  │
│  │  - Interfaz moderna              │  │
│  │  - Conecta con API del backend   │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  PostgreSQL                      │  │
│  │  bot-whatsapp-db                 │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

## ✅ Checklist de Despliegue

- [ ] Cambié el puerto en package.json (3001 → 3000)
- [ ] Subí los cambios a Git
- [ ] Creé el servicio en Easypanel
- [ ] Configuré Build Path: `dashboard-nextjs`
- [ ] Configuré Build Command: `npm install && npm run build`
- [ ] Configuré Start Command: `npm start`
- [ ] Configuré Port: `3000`
- [ ] Agregué NEXTAUTH_SECRET
- [ ] Agregué NEXT_PUBLIC_API_URL
- [ ] Agregué NEXTAUTH_URL
- [ ] Hice deploy
- [ ] Esperé 5-10 minutos
- [ ] Verifiqué los logs
- [ ] Accedí al dashboard

## 🎯 URLs Finales

### Backend (Ya funciona)
```
https://bot-whatsapp-bot-inteligente.sqaoeo.easypanel.host
```

Rutas:
- API: `/api/*`
- Panel Admin: `/admin/dashboard`
- Health: `/health`

### Dashboard (Después de desplegar)
```
https://bot-whatsapp-dashboard.sqaoeo.easypanel.host
```

## 🔄 Actualizar Electron

Una vez que el dashboard esté funcionando, actualiza Electron:

Edita `dashboard-electron/main.js`:

```javascript
// Cambiar de panel admin a dashboard Next.js
mainWindow.loadURL('https://bot-whatsapp-dashboard.sqaoeo.easypanel.host');
```

## 📞 Siguiente Paso

1. **Sube los cambios a Git:**
   ```bash
   git add dashboard-nextjs/package.json
   git commit -m "fix: cambiar puerto del dashboard de 3001 a 3000"
   git push
   ```

2. **Crea el servicio en Easypanel** con la configuración de arriba

3. **Espera el build** (5-10 min)

4. **Accede al dashboard**

## 🆘 Si Necesitas Ayuda

Comparte:
1. Los logs del build en Easypanel
2. Los logs del servicio en Easypanel
3. Las variables de entorno configuradas

Y te ayudo a resolver el problema específico.
