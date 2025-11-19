# 📊 Guía de Dashboards - Smart Sales Bot

Hemos creado **DOS versiones** del dashboard para tu bot de WhatsApp:

## 1. 🌐 Dashboard Web (HTML/CSS/JS)

### Ubicación
```
ventas-2/admin/templates/dashboard.html
```

### Características
- ✅ HTML puro con Tailwind CSS
- ✅ Sin dependencias de Node.js
- ✅ Se sirve directamente desde FastAPI
- ✅ Actualización en tiempo real cada 30 segundos
- ✅ Diseño responsive
- ✅ Tema verde WhatsApp profesional

### Cómo Usar
1. El bot de Python ya está configurado para servir el dashboard
2. Inicia el bot: `python main.py`
3. Abre en tu navegador: `http://localhost:3000/admin/dashboard`

### Endpoints API Disponibles
- `GET /admin/dashboard` - Dashboard principal
- `GET /admin/stats` - Estadísticas en tiempo real
- `GET /admin/conversations/recent` - Conversaciones recientes
- `GET /admin/orders/recent` - Pedidos recientes

---

## 2. 🖥️ Dashboard Electron (React + Electron)

### Ubicación
```
ventas-2/dashboard-electron/
```

### Características
- ✅ Aplicación de escritorio nativa
- ✅ React 18 + Vite
- ✅ Tailwind CSS
- ✅ Barra de título personalizada
- ✅ Ventana sin bordes (frameless)
- ✅ Iconos con Lucide React
- ✅ Gráficos con Recharts
- ✅ Empaquetado para Windows, Mac y Linux

### Instalación

```bash
cd ventas-2/dashboard-electron

# Instalar dependencias
npm install

# Desarrollo
npm run dev

# Build para producción
npm run build

# Crear ejecutable
npm run build:electron
```

### Estructura del Proyecto

```
dashboard-electron/
├── src/
│   ├── components/
│   │   ├── TitleBar.jsx      # Barra de título personalizada
│   │   ├── Sidebar.jsx        # Menú lateral
│   │   ├── Overview.jsx       # Vista de resumen
│   │   ├── Conversations.jsx  # Lista de conversaciones
│   │   └── Agents.jsx         # Agentes IA
│   ├── App.jsx                # Componente principal
│   ├── main.jsx               # Entry point React
│   └── index.css              # Estilos globales
├── main.js                    # Proceso principal Electron
├── preload.js                 # Script de preload
├── package.json               # Dependencias
├── vite.config.js             # Configuración Vite
└── tailwind.config.js         # Configuración Tailwind
```

### Componentes Principales

#### TitleBar
- Barra de título personalizada con botones de minimizar, maximizar y cerrar
- Estilo verde WhatsApp
- Draggable

#### Sidebar
- Menú lateral con navegación
- Iconos de Lucide React
- Animaciones suaves
- Estado activo visual

#### Overview
- 4 tarjetas de estadísticas principales
- Gráficos de conversaciones e intenciones
- Actividad reciente

#### Conversations
- Lista de conversaciones recientes
- Badges de intención y sentimiento
- Timestamps
- Scroll infinito

#### Agents
- Tarjetas de los 5 agentes especializados
- Descripción y capacidades
- Iconos coloridos

### Configuración de Build

El proyecto está configurado para generar ejecutables para:
- **Windows**: `.exe` con instalador NSIS
- **Mac**: `.dmg`
- **Linux**: `.AppImage`

Los ejecutables se generan en `dist-electron/`

### Personalización

#### Cambiar colores
Edita `tailwind.config.js`:
```javascript
colors: {
  whatsapp: {
    light: '#25d366',
    DEFAULT: '#128c7e',
    dark: '#075e54'
  }
}
```

#### Cambiar puerto API
Edita `src/App.jsx`:
```javascript
const API_URL = 'http://localhost:3000';
```

#### Agregar nuevo componente
1. Crear archivo en `src/components/`
2. Importar en `App.jsx`
3. Agregar al switch de tabs

---

## 🎨 Diseño

Ambas versiones comparten:
- ✅ Paleta de colores verde WhatsApp
- ✅ Diseño moderno y profesional
- ✅ Animaciones suaves
- ✅ Responsive design
- ✅ Iconos consistentes
- ✅ Tipografía clara

### Paleta de Colores

```css
Verde WhatsApp Claro: #25d366
Verde WhatsApp: #128c7e
Verde WhatsApp Oscuro: #075e54
Gris Claro: #f8fafc
Gris: #64748b
Gris Oscuro: #1e293b
```

---

## 📊 Funcionalidades Implementadas

### Dashboard Web
- ✅ Estadísticas en tiempo real
- ✅ Conversaciones activas
- ✅ Pedidos del día
- ✅ Ventas del día
- ✅ Tasa de conversión
- ✅ Actividad reciente
- ✅ Auto-refresh cada 30s

### Dashboard Electron
- ✅ Todo lo del dashboard web
- ✅ Ventana nativa de escritorio
- ✅ Barra de título personalizada
- ✅ Navegación entre secciones
- ✅ Vista de agentes IA
- ✅ Gráficos interactivos (preparado)
- ✅ Notificaciones de escritorio (preparado)

---

## 🚀 Próximos Pasos

### Para Dashboard Web
1. Agregar gráficos con Chart.js
2. Implementar filtros de fecha
3. Exportar reportes PDF
4. Modo oscuro

### Para Dashboard Electron
1. Agregar gráficos con Recharts
2. Notificaciones de escritorio
3. Atajos de teclado
4. Modo offline
5. Auto-actualización

---

## 🔧 Troubleshooting

### Dashboard Web no carga
```bash
# Verificar que el bot esté corriendo
python main.py

# Verificar en navegador
http://localhost:3000/health
```

### Dashboard Electron no inicia
```bash
cd dashboard-electron

# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install

# Verificar versión de Node
node --version  # Debe ser 16+
```

### Error de CORS
El dashboard web ya tiene CORS configurado en FastAPI. Si tienes problemas:
```python
# En main.py, verifica:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 Notas

- El dashboard web es más ligero y fácil de desplegar
- El dashboard Electron es mejor para uso local y tiene más funcionalidades
- Ambos se conectan a la misma API de Python
- Puedes usar ambos simultáneamente

¡Disfruta de tus dashboards profesionales! 🎉
