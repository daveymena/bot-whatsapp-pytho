# 🚀 CÓMO USAR EL SISTEMA

## ✅ Sistema Completamente Funcional

### 📋 Servicios Necesarios

Asegúrate de que estos 3 servicios estén corriendo:

1. **Backend Python** (Puerto 5000)
2. **Servidor Baileys WhatsApp** (Puerto 3002)  
3. **Dashboard Next.js** (Puerto 3001)

### 🎯 Iniciar Todo

```bash
cd ventas-2
START_ALL.bat
```

O manualmente:
```bash
# Terminal 1 - Backend Python
cd ventas-2
python main.py

# Terminal 2 - Baileys
cd ventas-2/baileys-server
node server.js

# Terminal 3 - Dashboard
cd ventas-2/dashboard-nextjs
npm run dev
```

### 🔐 Acceder al Sistema

1. **Abrir navegador**: http://localhost:3001

2. **Login con credenciales de prueba**:
   - Email: `admin@ventas.com`
   - Password: `admin123`

3. **O Registrarse**:
   - Click en "Empezar Gratis" o "Registrarse"
   - Completar formulario
   - Automáticamente inicia sesión

### 📱 Conectar WhatsApp

1. En el dashboard, click en "WhatsApp" en el menú lateral
2. Click en "Conectar WhatsApp"
3. Escanea el QR con tu teléfono
4. ¡Listo! El bot está activo

### 📦 Gestionar Productos

1. Click en "Productos" en el menú lateral
2. Click en "Nuevo Producto" para agregar
3. Completa el formulario
4. Los productos aparecen en el catálogo

### 🔧 Solución de Problemas

**Si el login no funciona:**
1. Verifica que el backend Python esté corriendo (puerto 5000)
2. Abre la consola del navegador (F12) y busca errores
3. Verifica que puedas acceder a: http://localhost:5000/api/auth/login

**Si el dashboard no carga:**
1. Limpia el caché del navegador (Ctrl+Shift+Delete)
2. Recarga la página (Ctrl+F5)
3. Verifica que Next.js esté corriendo (puerto 3001)

**Si WhatsApp no conecta:**
1. Verifica que Baileys esté corriendo (puerto 3002)
2. Prueba acceder a: http://localhost:3002/status
3. Si hay sesión antigua, usa "Limpiar y Generar Nuevo QR"

### 📊 Estructura del Sistema

```
ventas-2/
├── main.py                    # Backend Python (FastAPI)
├── baileys-server/            # Servidor WhatsApp
│   └── server.js
├── dashboard-nextjs/          # Frontend (Next.js)
│   ├── src/app/
│   │   ├── landing/          # Landing page
│   │   ├── login/            # Login
│   │   ├── register/         # Registro
│   │   └── dashboard/        # Dashboard principal
│   └── src/components/
│       ├── products/         # Gestión de productos
│       └── dashboard/        # Componentes del dashboard
└── database/
    └── ventas.db             # Base de datos SQLite
```

### 🎉 Funcionalidades Disponibles

- ✅ Landing page profesional
- ✅ Sistema de registro y login
- ✅ Dashboard completo
- ✅ Conexión WhatsApp con QR
- ✅ Gestión de productos (CRUD completo)
- ✅ Importar/Exportar productos
- ✅ Búsqueda y filtros
- ✅ Visualización de imágenes
- ✅ Estadísticas en tiempo real
- ✅ Gestión de clientes
- ✅ Auto-reconexión de WhatsApp

### 📞 Soporte

Si tienes problemas:
1. Revisa los logs de cada servicio
2. Verifica que todos los puertos estén disponibles
3. Asegúrate de tener todas las dependencias instaladas

**¡El sistema está listo para usar!** 🎊
