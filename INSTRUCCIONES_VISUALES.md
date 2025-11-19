# 🎯 Instrucciones Visuales - Dashboard Next.js

## 📋 Guía Paso a Paso con Comandos Exactos

### 🔧 PASO 1: Instalar Dependencias

#### 1.1 Dashboard Next.js
```bash
# Abre una terminal en la carpeta del proyecto
cd ventas-2

# Entra a la carpeta del dashboard
cd dashboard-nextjs

# Instala las dependencias
npm install

# Espera a que termine (puede tomar 1-2 minutos)
# Verás algo como: "added 390 packages"

# Regresa a la carpeta principal
cd ..
```

#### 1.2 Backend Python
```bash
# Asegúrate de estar en la carpeta ventas-2
# Instala las nuevas dependencias
pip install pyjwt passlib[bcrypt]

# Verás algo como: "Successfully installed pyjwt-2.8.0 passlib-1.7.4"
```

### 🚀 PASO 2: Iniciar el Sistema

#### Opción A: Iniciar Todo Automáticamente (RECOMENDADO)
```bash
# Simplemente ejecuta:
START_ALL.bat

# Se abrirán 3 ventanas:
# 1. Backend Python (puerto 5000)
# 2. Baileys Server (puerto 3002)
# 3. Dashboard Next.js (puerto 3001)
```

#### Opción B: Iniciar Manualmente (Si prefieres control)

**Terminal 1 - Backend Python:**
```bash
cd ventas-2
python main.py
```
Verás:
```
🚀 INICIANDO BOT DE VENTAS WHATSAPP PRO
🏢 Negocio: Tu Negocio
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**Terminal 2 - Baileys Server:**
```bash
cd ventas-2\baileys-server
npm start
```
Verás:
```
🚀 Baileys Server iniciado en puerto 3002
```

**Terminal 3 - Dashboard Next.js:**
```bash
cd ventas-2\dashboard-nextjs
npm run dev
```
Verás:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3001
- Ready in 2.5s
```

### 🌐 PASO 3: Acceder al Dashboard

1. **Abre tu navegador** (Chrome, Firefox, Edge)

2. **Ve a:** http://localhost:3001

3. **Verás la pantalla de login:**
   ```
   ┌─────────────────────────────┐
   │                             │
   │    🤖 VENTAS BOT            │
   │                             │
   │    Email:                   │
   │    [________________]       │
   │                             │
   │    Password:                │
   │    [________________]       │
   │                             │
   │    [  INICIAR SESIÓN  ]     │
   │                             │
   └─────────────────────────────┘
   ```

4. **Ingresa las credenciales:**
   - Email: `admin@ventas.com`
   - Password: `admin123`

5. **Presiona "Iniciar Sesión"**

6. **¡Listo!** Verás el dashboard principal

### 📊 PASO 4: Explorar el Dashboard

Una vez dentro, verás:

```
┌─────────────────────────────────────────────────────────┐
│  ☰  VB    [Notificaciones]  [Usuario] [Logout]         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Resumen                                             │
│  💬 WhatsApp                                            │
│  📦 Productos                                           │
│  🏪 Mi Tienda                                           │
│  🤖 Personalidad Bot                                    │
│  🧠 IA & Prompts                                        │
│  ⚡ Entrenamiento Bot                                   │
│  👥 Clientes                                            │
│  ⚙️ Configuración                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🎯 PASO 5: Verificar que Todo Funciona

#### 5.1 Verificar Backend
```bash
# Abre una nueva terminal
curl http://localhost:5000/docs

# O abre en el navegador:
# http://localhost:5000/docs
```

Deberías ver la documentación de la API (Swagger UI)

#### 5.2 Verificar Baileys
```bash
# En el navegador:
# http://localhost:3002/status
```

Verás algo como:
```json
{
  "success": true,
  "status": "DISCONNECTED",
  "connection": {
    "phoneNumber": null,
    "isActive": false
  }
}
```

#### 5.3 Verificar Dashboard
```bash
# Ya deberías estar viendo el dashboard en:
# http://localhost:3001
```

### 🧪 PASO 6: Probar con el Script de Pruebas

```bash
# En una nueva terminal
cd ventas-2
python test_dashboard.py
```

Verás:
```
============================================================
🧪 PRUEBAS DEL DASHBOARD Y APIs
============================================================

🔐 Probando autenticación...
✅ Login exitoso
   Usuario: Administrador
   Email: admin@ventas.com

📊 Probando estadísticas...
✅ Estadísticas obtenidas
   Conversaciones: 0
   Productos: 0
   Clientes: 0

...

🎯 Resultado: 5/5 pruebas exitosas
🎉 ¡Todas las pruebas pasaron! El dashboard está listo.
```

## 🎨 Navegación en el Dashboard

### Sección: Resumen
- Ver estadísticas generales
- Conversaciones activas
- Productos en catálogo
- Estado de WhatsApp

### Sección: WhatsApp
- Ver estado de conexión
- Escanear QR Code
- Desconectar/Reconectar

### Sección: Productos
- Ver lista de productos
- Agregar nuevo producto
- Editar productos
- Eliminar productos

### Sección: Clientes
- Ver lista de clientes
- Historial de compras
- Información de contacto

## 🔄 Flujo de Trabajo Típico

1. **Iniciar el sistema** con `START_ALL.bat`
2. **Abrir dashboard** en http://localhost:3001
3. **Login** con las credenciales
4. **Conectar WhatsApp** (si es necesario)
5. **Configurar productos** en la sección Productos
6. **Personalizar bot** en Personalidad Bot
7. **Monitorear** conversaciones en Resumen

## 🛑 Cómo Detener el Sistema

### Si usaste START_ALL.bat:
- Cierra las 3 ventanas de terminal que se abrieron

### Si iniciaste manualmente:
- En cada terminal, presiona `Ctrl + C`

## 🔧 Solución de Problemas Comunes

### Problema 1: "npm no se reconoce"
**Solución:**
```bash
# Instala Node.js desde:
# https://nodejs.org/
# Versión recomendada: LTS (18.x o superior)
```

### Problema 2: "Puerto 3001 ya está en uso"
**Solución:**
```bash
# Windows
netstat -ano | findstr :3001
taskkill /PID <número> /F

# Luego reinicia el dashboard
cd dashboard-nextjs
npm run dev
```

### Problema 3: "Error al conectar con el backend"
**Solución:**
```bash
# Verifica que el backend esté corriendo
# Abre http://localhost:5000/docs
# Si no carga, inicia el backend:
python main.py
```

### Problema 4: "No puedo hacer login"
**Solución:**
- Verifica las credenciales:
  - Email: `admin@ventas.com`
  - Password: `admin123`
- Asegúrate de que el backend esté corriendo
- Revisa la consola del navegador (F12)

### Problema 5: "Las estadísticas muestran 0"
**Solución:**
```bash
# Es normal si es la primera vez
# Necesitas:
1. Conectar WhatsApp
2. Agregar productos
3. Tener conversaciones

# O puedes poblar la base de datos:
python seed_database.py
```

## 📱 Acceso desde Móvil

Para acceder desde tu teléfono en la misma red:

1. **Encuentra tu IP local:**
```bash
# Windows
ipconfig
# Busca "Dirección IPv4": 192.168.X.X
```

2. **Actualiza .env.local:**
```env
BACKEND_URL=http://192.168.X.X:5000
NEXT_PUBLIC_API_URL=http://192.168.X.X:3001
```

3. **Reinicia el dashboard**

4. **En tu móvil, abre:**
```
http://192.168.X.X:3001
```

## 🎓 Próximos Pasos

1. ✅ **Conectar WhatsApp**
   - Ve a la sección WhatsApp
   - Escanea el QR Code

2. ✅ **Agregar Productos**
   - Ve a Productos
   - Click en "Agregar Producto"
   - Llena la información

3. ✅ **Personalizar Bot**
   - Ve a Personalidad Bot
   - Define el tono de voz
   - Configura saludos

4. ✅ **Configurar IA**
   - Ve a IA & Prompts
   - Ajusta los prompts
   - Prueba respuestas

5. ✅ **Entrenar Bot**
   - Ve a Entrenamiento
   - Sube documentos
   - Agrega FAQs

## 📞 Ayuda Adicional

Si necesitas más ayuda, revisa:
- `DASHBOARD_NEXTJS_GUIDE.md` - Guía completa
- `PORTS_CONFIG.md` - Configuración de puertos
- `RESUMEN_DASHBOARD.md` - Resumen general
- http://localhost:5000/docs - Documentación API

## ✅ Checklist Final

Antes de empezar a usar en producción:

- [ ] Dependencias instaladas (`npm install`)
- [ ] Backend corriendo (puerto 5000)
- [ ] Baileys corriendo (puerto 3002)
- [ ] Dashboard corriendo (puerto 3001)
- [ ] Login funciona
- [ ] Estadísticas se cargan
- [ ] WhatsApp conectado
- [ ] Productos agregados
- [ ] Bot personalizado

## 🎉 ¡Felicidades!

Si llegaste hasta aquí y todo funciona, ¡tienes un sistema completo de bot de ventas con dashboard profesional!

**Disfruta tu nuevo dashboard** 🚀
