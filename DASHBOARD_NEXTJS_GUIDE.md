# 🎨 Guía del Dashboard Next.js

## 📋 Descripción

Dashboard moderno y profesional construido con Next.js 14, React 18 y Tailwind CSS para gestionar tu bot de ventas de WhatsApp.

## ✨ Características Principales

### 🔐 Autenticación
- Login seguro con JWT
- Sesión persistente
- Protección de rutas
- Auto-refresh de tokens

### 📊 Dashboard Principal
- Estadísticas en tiempo real
- Métricas de conversaciones
- Estado de conexión WhatsApp
- Gráficos y visualizaciones

### 📦 Gestión de Productos
- Crear, editar y eliminar productos
- Categorización
- Control de inventario
- Imágenes de productos
- Productos digitales y dropshipping

### 👥 Gestión de Clientes
- Base de datos de clientes
- Historial de compras
- Segmentación
- Análisis de comportamiento

### 🤖 Configuración del Bot
- Personalidad del bot
- Prompts de IA
- Entrenamiento
- Respuestas automáticas

### 💬 WhatsApp
- Estado de conexión
- QR Code para vincular
- Gestión de sesiones
- Logs de mensajes

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- Node.js 18+ instalado
- Backend Python corriendo en puerto 5000
- Servidor Baileys en puerto 3002

### 2. Instalación

```bash
cd dashboard-nextjs
npm install
```

### 3. Configuración

Crea el archivo `.env.local`:

```env
BACKEND_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### 4. Iniciar Dashboard

```bash
# Desarrollo
npm run dev

# Producción
npm run build
npm start
```

## 🔑 Acceso

### URL
http://localhost:3001

### Credenciales de Prueba
- **Email**: admin@ventas.com
- **Password**: admin123

## 📁 Estructura del Proyecto

```
dashboard-nextjs/
├── src/
│   ├── app/                      # App Router de Next.js
│   │   ├── api/                  # API Routes
│   │   │   ├── auth/            # Autenticación
│   │   │   └── stats/           # Estadísticas
│   │   ├── dashboard/           # Página principal
│   │   ├── login/               # Página de login
│   │   ├── layout.tsx           # Layout principal
│   │   └── page.tsx             # Página de inicio
│   │
│   ├── components/
│   │   ├── dashboard/           # Componentes del dashboard
│   │   │   └── main-dashboard.tsx
│   │   └── ui/                  # Componentes UI
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── tabs.tsx
│   │       ├── badge.tsx
│   │       └── avatar.tsx
│   │
│   ├── hooks/                   # Custom Hooks
│   │   ├── use-auth.tsx        # Hook de autenticación
│   │   └── useSessionPersistence.tsx
│   │
│   └── lib/                     # Utilidades
│       └── utils.ts
│
├── public/                      # Archivos estáticos
├── .env.local                   # Variables de entorno
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## 🎯 Funcionalidades por Sección

### 📊 Resumen (Overview)
- Total de conversaciones
- Conversaciones activas
- Productos en catálogo
- Clientes registrados
- Mensajes enviados
- Estado de conexión WhatsApp

### 💬 WhatsApp
- Ver estado de conexión
- Escanear QR Code
- Desconectar/Reconectar
- Ver número vinculado
- Logs de mensajes

### 📦 Productos
- Lista de productos
- Agregar nuevo producto
- Editar producto existente
- Eliminar producto
- Importar productos masivamente
- Filtrar por categoría
- Buscar productos

### 🏪 Mi Tienda
- Configuración de tienda
- Información del negocio
- Horarios de atención
- Métodos de pago
- Políticas de envío

### 🤖 Personalidad del Bot
- Definir tono de voz
- Estilo de comunicación
- Saludos personalizados
- Despedidas
- Manejo de objeciones

### 🧠 IA & Prompts
- Configurar prompts del sistema
- Prompts por agente
- Ejemplos de conversación
- Fine-tuning de respuestas

### ⚡ Entrenamiento del Bot
- Subir documentos de entrenamiento
- Base de conocimiento
- FAQs
- Casos de uso

### 👥 Clientes
- Lista de clientes
- Detalles del cliente
- Historial de compras
- Conversaciones
- Segmentación

### ⚙️ Configuración
- Configuración general
- API Keys
- Integraciones
- Notificaciones
- Usuarios y permisos

## 🔄 Integración con Backend

El dashboard se comunica con el backend Python a través de:

### API Routes de Next.js
- `/api/auth/login` - Autenticación
- `/api/auth/logout` - Cerrar sesión
- `/api/auth/ping` - Mantener sesión activa
- `/api/stats/overview` - Estadísticas generales

### Backend Python (FastAPI)
- `POST /api/auth/login` - Login
- `GET /api/stats/overview` - Estadísticas
- `GET /api/stats/dashboard` - Dashboard stats
- `GET /admin/products` - Productos
- `GET /admin/customers` - Clientes
- `GET /admin/whatsapp/status` - Estado WhatsApp

## 🎨 Personalización

### Colores
Los colores principales están en `tailwind.config.ts`:
- Verde WhatsApp: `#25d366`
- Verde oscuro: `#075e54`
- Verde medio: `#128c7e`

### Componentes UI
Los componentes están en `src/components/ui/` y usan:
- Tailwind CSS para estilos
- class-variance-authority para variantes
- clsx y tailwind-merge para clases dinámicas

## 📱 Responsive Design

El dashboard es completamente responsive:
- **Desktop**: Sidebar expandido, todas las funciones
- **Tablet**: Sidebar colapsable
- **Mobile**: Sidebar overlay, navegación optimizada

## 🔒 Seguridad

- Autenticación JWT
- Tokens con expiración
- Refresh automático de sesión
- Protección de rutas
- Validación de permisos

## 🚀 Despliegue

### Desarrollo
```bash
npm run dev
```

### Producción
```bash
npm run build
npm start
```

### Docker (Próximamente)
```bash
docker build -t ventas-bot-dashboard .
docker run -p 3001:3001 ventas-bot-dashboard
```

## 🐛 Troubleshooting

### El dashboard no carga
1. Verifica que el backend esté corriendo en puerto 5000
2. Revisa las variables de entorno en `.env.local`
3. Verifica la consola del navegador para errores

### No puedo hacer login
1. Verifica las credenciales: admin@ventas.com / admin123
2. Asegúrate de que el backend esté respondiendo
3. Revisa los logs del backend Python

### Las estadísticas no se actualizan
1. Verifica la conexión con el backend
2. Revisa la consola del navegador
3. Asegúrate de que la base de datos tenga datos

### Error de CORS
1. Verifica que el backend tenga CORS habilitado
2. Revisa la configuración en `main.py`
3. Asegúrate de que las URLs coincidan

## 📚 Recursos

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Lucide Icons](https://lucide.dev)

## 🤝 Soporte

Si tienes problemas o preguntas:
1. Revisa esta guía
2. Consulta los logs del servidor
3. Verifica la configuración del backend
4. Revisa la documentación de Next.js

## 📝 Notas Importantes

- El dashboard usa Server Components y Client Components de Next.js 14
- Las estadísticas se actualizan cada 10 segundos automáticamente
- La sesión se mantiene activa con pings cada 5 minutos
- El diseño está optimizado para WhatsApp Business
- Todos los componentes son reutilizables y personalizables

## 🎯 Próximas Funcionalidades

- [ ] Gráficos avanzados con Chart.js
- [ ] Exportación de reportes
- [ ] Notificaciones en tiempo real
- [ ] Chat en vivo con clientes
- [ ] Análisis de sentimiento
- [ ] Integración con Google Analytics
- [ ] Multi-idioma
- [ ] Modo oscuro completo
- [ ] PWA (Progressive Web App)
- [ ] Webhooks configurables
