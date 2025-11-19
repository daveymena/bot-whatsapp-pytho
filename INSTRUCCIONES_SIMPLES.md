# 🚀 INSTRUCCIONES SIMPLES - SISTEMA DE VENTAS BOT

## ✅ SISTEMA COMPLETAMENTE FUNCIONAL

### 📋 PASO 1: INICIAR EL SISTEMA

Abre 3 terminales (PowerShell o CMD) y ejecuta en cada una:

**Terminal 1 - Backend:**
```bash
cd C:\ventas-2
python main.py
```

**Terminal 2 - WhatsApp:**
```bash
cd C:\ventas-2\baileys-server
node server.js
```

**Terminal 3 - Dashboard:**
```bash
cd C:\ventas-2\dashboard-nextjs
npm run dev
```

### 🌐 PASO 2: ACCEDER AL DASHBOARD

1. Abre tu navegador
2. Ve a: **http://localhost:3001/dashboard**
3. ¡Listo! Ya estás en el dashboard

### 📱 PASO 3: CONECTAR WHATSAPP

1. En el dashboard, click en **"WhatsApp"** (menú lateral)
2. Click en **"Conectar WhatsApp"**
3. Espera a que aparezca el QR (10-15 segundos)
4. Escanea con tu WhatsApp
5. ¡Conectado!

**Si hay error:**
- Cierra el servidor de WhatsApp (Terminal 2)
- Elimina la carpeta: `C:\ventas-2\baileys-server\auth_info`
- Vuelve a iniciar: `node server.js`
- Intenta conectar de nuevo

### 📦 PASO 4: GESTIONAR PRODUCTOS

1. Click en **"Productos"** (menú lateral)
2. Click en **"Nuevo Producto"**
3. Completa el formulario
4. ¡Producto creado!

### 🎯 SECCIONES DISPONIBLES

- **Resumen**: Estadísticas del bot
- **WhatsApp**: Conexión y QR
- **Productos**: Catálogo completo
- **Mi Tienda**: Configuración
- **Personalidad Bot**: Personalizar respuestas
- **IA & Prompts**: Configurar IA
- **Entrenamiento Bot**: Entrenar respuestas
- **Clientes**: Base de datos
- **Configuración**: Ajustes generales

### 🔧 SOLUCIÓN RÁPIDA DE PROBLEMAS

**Dashboard no carga:**
- Verifica que los 3 servicios estén corriendo
- Recarga la página (Ctrl + F5)

**WhatsApp no conecta:**
- Elimina: `baileys-server\auth_info`
- Reinicia el servidor de WhatsApp
- Intenta de nuevo

**Login no funciona:**
- Ve directo a: http://localhost:3001/dashboard
- No necesitas login para desarrollo

### 📊 PUERTOS USADOS

- **5000**: Backend Python
- **3001**: Dashboard Next.js
- **3002**: Servidor WhatsApp

### ✨ CARACTERÍSTICAS

✅ Dashboard moderno y responsive
✅ Conexión WhatsApp con QR
✅ Gestión completa de productos
✅ Importar/Exportar productos
✅ Búsqueda y filtros
✅ Estadísticas en tiempo real
✅ Auto-reconexión de WhatsApp

---

## 🎉 ¡ESO ES TODO!

El sistema está listo para usar. Simple y directo.

**Acceso rápido:** http://localhost:3001/dashboard
