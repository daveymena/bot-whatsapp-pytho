# Dashboard Next.js - Ventas Bot

Dashboard moderno construido con Next.js 14, React 18 y Tailwind CSS para gestionar el bot de ventas de WhatsApp.

## 🚀 Características

- ✅ Autenticación con JWT
- ✅ Dashboard en tiempo real
- ✅ Gestión de productos
- ✅ Gestión de clientes
- ✅ Estadísticas y métricas
- ✅ Configuración del bot
- ✅ Responsive design
- ✅ Dark mode ready

## 📦 Instalación

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env.local
```

## 🔧 Configuración

Edita el archivo `.env.local`:

```env
BACKEND_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## 🏃 Ejecución

```bash
# Desarrollo
npm run dev

# Producción
npm run build
npm start
```

El dashboard estará disponible en: http://localhost:3001

## 🔐 Credenciales de Prueba

- Email: `admin@ventas.com`
- Password: `admin123`

## 📁 Estructura

```
src/
├── app/                    # App Router de Next.js
│   ├── api/               # API Routes
│   ├── dashboard/         # Página del dashboard
│   └── login/             # Página de login
├── components/
│   ├── dashboard/         # Componentes del dashboard
│   └── ui/                # Componentes UI reutilizables
├── hooks/                 # Custom hooks
└── lib/                   # Utilidades
```

## 🎨 Tecnologías

- **Next.js 14** - Framework React
- **React 18** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos
- **Lucide React** - Iconos
- **Sonner** - Notificaciones

## 🔗 Integración con Backend

El dashboard se conecta al backend Python (FastAPI) en `http://localhost:5000` para:

- Autenticación de usuarios
- Obtener estadísticas
- Gestionar productos y clientes
- Configurar el bot

## 📝 Notas

- El dashboard usa Server Components y Client Components de Next.js 14
- La autenticación se maneja con JWT tokens
- Las estadísticas se actualizan cada 10 segundos
- Responsive design optimizado para móviles y tablets
