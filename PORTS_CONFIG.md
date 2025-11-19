# 🔌 Configuración de Puertos y URLs

## 📋 Resumen de Puertos

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| Dashboard Next.js | 3001 | http://localhost:3001 | Dashboard moderno (Frontend) |
| Baileys Server | 3002 | http://localhost:3002 | Servidor WhatsApp Web |
| Backend Python | 5000 | http://localhost:5000 | API FastAPI (Backend) |

## 🎨 Dashboard Next.js (Puerto 3001)

### URLs Principales
- **Dashboard**: http://localhost:3001
- **Login**: http://localhost:3001/login
- **Dashboard Principal**: http://localhost:3001/dashboard

### API Routes Internas
- `POST /api/auth/login` - Autenticación
- `POST /api/auth/logout` - Cerrar sesión
- `POST /api/auth/ping` - Mantener sesión
- `GET /api/stats/overview` - Estadísticas

### Configuración
```env
# .env.local
BACKEND_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## 💬 Baileys Server (Puerto 3002)

### Endpoints
- `GET /status` - Estado de conexión WhatsApp
- `POST /disconnect` - Desconectar WhatsApp
- `POST /reconnect` - Reconectar WhatsApp
- `POST /send-message` - Enviar mensaje

### Configuración
```javascript
// server.js
const PORT = 3002;
const PYTHON_API = 'http://localhost:5000';
```

## 🐍 Backend Python (Puerto 5000)

### Endpoints Principales

#### Autenticación
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Usuario actual

#### Estadísticas
- `GET /api/stats/overview` - Estadísticas generales
- `GET /api/stats/dashboard` - Stats del dashboard
- `GET /api/stats/sales` - Estadísticas de ventas
- `GET /api/stats/products/top` - Productos más vendidos
- `GET /api/stats/customers/top` - Mejores clientes

#### Admin Panel
- `GET /admin/dashboard` - Dashboard HTML legacy
- `GET /admin/stats` - Estadísticas
- `GET /admin/products` - Productos
- `POST /admin/products` - Crear producto
- `PUT /admin/products/{id}` - Actualizar producto
- `DELETE /admin/products/{id}` - Eliminar producto
- `GET /admin/customers` - Clientes
- `GET /admin/conversations/recent` - Conversaciones recientes
- `GET /admin/orders/recent` - Pedidos recientes

#### WhatsApp
- `GET /admin/whatsapp/status` - Estado WhatsApp
- `POST /admin/whatsapp/disconnect` - Desconectar
- `POST /admin/whatsapp/reconnect` - Reconectar

#### Documentación
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

### Configuración
```python
# main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

## 🔄 Flujo de Comunicación

```
Cliente (Navegador)
    ↓
Dashboard Next.js (3001)
    ↓
Backend Python (5000)
    ↓
Baileys Server (3002)
    ↓
WhatsApp Web API
```

## 🚀 Scripts de Inicio

### Windows

#### Iniciar Todo
```batch
START_ALL.bat
```
Inicia:
1. Backend Python (puerto 5000)
2. Baileys Server (puerto 3002)
3. Dashboard Next.js (puerto 3001)

#### Solo Dashboard
```batch
START_DASHBOARD.bat
```

#### Solo Backend
```batch
python main.py
```

#### Solo Baileys
```batch
cd baileys-server
npm start
```

### Linux/Mac

```bash
# Todo
./start.sh

# Solo Backend
python main.py

# Solo Baileys
cd baileys-server && npm start

# Solo Dashboard
cd dashboard-nextjs && npm run dev
```

## 🔧 Cambiar Puertos

### Dashboard Next.js
```json
// package.json
"scripts": {
  "dev": "next dev -p 3001",  // Cambiar aquí
  "start": "next start -p 3001"
}
```

### Baileys Server
```javascript
// server.js
const PORT = 3002;  // Cambiar aquí
```

### Backend Python
```python
# main.py
uvicorn.run(app, host="0.0.0.0", port=5000)  # Cambiar aquí
```

## ⚠️ Conflictos de Puertos

Si un puerto está ocupado:

### Windows
```batch
# Ver qué usa el puerto
netstat -ano | findstr :3001

# Matar proceso
taskkill /PID <PID> /F
```

### Linux/Mac
```bash
# Ver qué usa el puerto
lsof -i :3001

# Matar proceso
kill -9 <PID>
```

## 🔒 Firewall

Si tienes problemas de conexión, asegúrate de permitir estos puertos:
- 3001 (Dashboard)
- 3002 (Baileys)
- 5000 (Backend)

### Windows Firewall
```batch
netsh advfirewall firewall add rule name="Dashboard" dir=in action=allow protocol=TCP localport=3001
netsh advfirewall firewall add rule name="Baileys" dir=in action=allow protocol=TCP localport=3002
netsh advfirewall firewall add rule name="Backend" dir=in action=allow protocol=TCP localport=5000
```

## 🌐 Acceso Remoto

Para acceder desde otra computadora en la red:

1. Encuentra tu IP local:
```batch
# Windows
ipconfig

# Linux/Mac
ifconfig
```

2. Usa la IP en lugar de localhost:
```
http://192.168.1.X:3001  # Dashboard
http://192.168.1.X:5000  # Backend
http://192.168.1.X:3002  # Baileys
```

3. Actualiza las variables de entorno:
```env
BACKEND_URL=http://192.168.1.X:5000
NEXT_PUBLIC_API_URL=http://192.168.1.X:3001
```

## 📝 Notas

- El Dashboard Next.js actúa como proxy para algunas peticiones al backend
- Baileys Server se comunica directamente con el Backend Python
- El Backend Python es el único que accede a la base de datos
- Todos los servicios deben estar corriendo para funcionalidad completa
- El Dashboard puede funcionar sin Baileys, pero no mostrará estado de WhatsApp
