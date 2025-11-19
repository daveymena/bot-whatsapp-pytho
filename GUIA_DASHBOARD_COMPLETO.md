# 📖 Guía Completa del Dashboard

## 🚀 Inicio Rápido

### Opción 1: Script Automático
```bash
# Windows
INICIAR_DASHBOARD_COMPLETO.bat

# Linux/Mac
cd dashboard-nextjs && npm run dev
```

### Opción 2: Manual
```bash
cd dashboard-nextjs
npm install
npm run dev
```

El dashboard estará disponible en: **http://localhost:3001**

## 🔐 Acceso

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📱 Secciones del Dashboard

### 1. 📊 Resumen (Overview)
**Ruta:** `/dashboard?tab=overview`

**Funcionalidades:**
- Ver estadísticas en tiempo real
- Conversaciones activas
- Pedidos del día
- Ventas del día
- Tasa de conversión
- Gráficos de actividad

**Cómo usar:**
1. Al iniciar sesión, verás esta pantalla por defecto
2. Las estadísticas se actualizan cada 30 segundos
3. Puedes ver gráficos de conversaciones e intenciones

---

### 2. 💬 WhatsApp
**Ruta:** `/dashboard?tab=whatsapp`

**Funcionalidades:**
- Conectar/Desconectar WhatsApp
- Ver código QR para escanear
- Estado de conexión
- Información del número conectado

**Cómo usar:**
1. Haz clic en "Conectar WhatsApp"
2. Escanea el código QR con tu WhatsApp
3. Espera la confirmación de conexión
4. El bot estará activo automáticamente

**Solución de problemas:**
- Si no aparece el QR, verifica que el servidor Baileys esté corriendo
- Si falla la conexión, usa el botón "Limpiar Sesión"

---

### 3. 💬 Conversaciones
**Ruta:** `/dashboard?tab=conversations`

**Funcionalidades:**
- Ver historial de conversaciones
- Filtrar por intención
- Ver análisis de sentimiento
- Identificar tipo de agente usado
- Ver si fue atendido por humano

**Cómo usar:**
1. Navega a la sección de Conversaciones
2. Verás una lista de todas las interacciones
3. Cada conversación muestra:
   - Número de teléfono del cliente
   - Mensaje enviado
   - Intención detectada (compra, consulta, etc.)
   - Sentimiento (positivo, neutral, negativo)
   - Agente que respondió
4. Usa el botón "Actualizar" para ver nuevas conversaciones

---

### 4. 📦 Productos
**Ruta:** `/dashboard?tab=products`

**Funcionalidades:**
- Ver catálogo completo
- Agregar nuevos productos
- Editar productos existentes
- Eliminar productos
- Gestionar stock
- Subir imágenes
- Categorizar productos
- Marcar como digital o dropshipping

**Cómo agregar un producto:**
1. Haz clic en "Agregar Producto"
2. Completa el formulario:
   - Nombre del producto
   - Descripción
   - Precio
   - Stock
   - Categoría
   - Garantía (opcional)
   - URL de imagen
3. Marca si es digital o dropshipping
4. Haz clic en "Guardar"

**Cómo editar un producto:**
1. Haz clic en el botón de editar (lápiz) en el producto
2. Modifica los campos necesarios
3. Guarda los cambios

**Cómo eliminar un producto:**
1. Haz clic en el botón de eliminar (basura)
2. Confirma la eliminación

---

### 5. 🤖 Agentes IA
**Ruta:** `/dashboard?tab=agents`

**Funcionalidades:**
- Ver todos los agentes especializados
- Conocer las capacidades de cada agente
- Entender cómo funciona el sistema multi-agente

**Agentes disponibles:**

1. **Agente de Ventas Profesional**
   - Técnicas AIDA y SPIN
   - Manejo de objeciones
   - Cierre de ventas
   - Análisis de sentimiento

2. **Agente de Productos**
   - Búsqueda inteligente
   - Comparativas
   - Recomendaciones
   - Gestión de stock

3. **Agente de Dropshipping**
   - Integración con Dropi
   - Cálculo de márgenes
   - Sincronización automática

4. **Agente de Reservas**
   - Agendamiento de citas
   - Recordatorios
   - Confirmaciones
   - Cancelaciones

5. **Agente de Pagos**
   - PayPal
   - MercadoPago
   - Verificación de pagos
   - Generación de recibos

6. **Agente Multi-Dominio**
   - Coordinación de agentes
   - Routing inteligente
   - Escalamiento
   - Gestión de contexto

7. **Sistema Híbrido**
   - Respuestas rápidas locales
   - IA avanzada cuando es necesario
   - Optimización de costos
   - Caché inteligente

---

### 6. 🏪 Mi Tienda
**Ruta:** `/dashboard?tab=store`

**Funcionalidades:**
- Configurar información de la tienda
- Personalizar datos de contacto
- Subir logo
- Vista previa en tiempo real

**Cómo configurar:**
1. Completa el formulario con:
   - Nombre de la tienda
   - Descripción
   - Teléfono
   - Email
   - Dirección
   - Sitio web
2. Sube el logo de tu tienda
3. Verifica la vista previa
4. Guarda los cambios

**Nota:** Esta información se mostrará a los clientes cuando interactúen con el bot.

---

### 7. 🎭 Personalidad del Bot
**Ruta:** `/dashboard?tab=personality`

**Funcionalidades:**
- Definir el nombre del bot
- Configurar tono de comunicación
- Establecer estilo de respuesta
- Personalizar mensajes de bienvenida y despedida
- Seleccionar idioma
- Configurar uso de emojis
- Vista previa de conversación

**Cómo personalizar:**
1. **Nombre del Bot:** Elige un nombre amigable
2. **Tono:** Selecciona entre:
   - Amigable: Cálido y cercano
   - Profesional: Formal pero accesible
   - Casual: Relajado e informal
   - Formal: Muy profesional
3. **Estilo:** Elige cómo responde:
   - Conciso: Respuestas cortas
   - Detallado: Explicaciones completas
   - Profesional: Equilibrado
   - Conversacional: Natural y fluido
4. **Mensajes:** Personaliza saludos y despedidas
5. **Emojis:** Define cuántos usar
6. Guarda los cambios

**Vista Previa:** Verás cómo se comportará el bot con tu configuración.

---

### 8. 🧠 IA & Prompts
**Ruta:** `/dashboard?tab=prompts`

**Funcionalidades:**
- Configurar prompts para cada agente
- Definir comportamiento de IA
- Optimizar respuestas

**Prompts disponibles:**

1. **Prompt de Ventas**
   - Define cómo vende el bot
   - Técnicas de persuasión
   - Manejo de objeciones

2. **Prompt de Productos**
   - Cómo presenta productos
   - Comparativas
   - Recomendaciones

3. **Prompt de Soporte**
   - Resolución de problemas
   - Empatía
   - Pasos claros

4. **Prompt General**
   - Base para todos los agentes
   - Comportamiento general

**Cómo editar prompts:**
1. Selecciona el tipo de prompt
2. Edita el texto en el editor
3. Sé específico sobre el rol y objetivos
4. Incluye ejemplos si es posible
5. Guarda los cambios

**Tips:**
- Sé específico sobre el rol del agente
- Define claramente los objetivos
- Incluye ejemplos de respuestas
- Prueba y ajusta continuamente

---

### 9. ⚡ Entrenamiento del Bot
**Ruta:** `/dashboard?tab=training`

**Funcionalidades:**
- Agregar ejemplos de preguntas y respuestas
- Categorizar ejemplos
- Exportar/Importar datos de entrenamiento
- Ver estadísticas

**Cómo entrenar el bot:**
1. **Agregar Ejemplo:**
   - Escribe una pregunta común de clientes
   - Escribe la respuesta ideal
   - Asigna una categoría
   - Haz clic en "Agregar Ejemplo"

2. **Gestionar Ejemplos:**
   - Revisa la lista de ejemplos
   - Elimina ejemplos obsoletos
   - Agrupa por categorías

3. **Exportar/Importar:**
   - Exporta tus datos en JSON
   - Comparte con otros sistemas
   - Importa ejemplos de otros

4. **Guardar y Entrenar:**
   - Haz clic en "Guardar y Entrenar"
   - El bot aprenderá de los ejemplos

**Mejores prácticas:**
- Usa preguntas reales de clientes
- Sé específico en las respuestas
- Agrupa por categorías similares
- Actualiza regularmente
- Incluye variaciones de la misma pregunta

---

### 10. 👥 Clientes
**Ruta:** `/dashboard?tab=customers`

**Funcionalidades:**
- Ver base de datos de clientes
- Historial de compras
- Total gastado
- Última interacción

**Información mostrada:**
- Nombre del cliente
- Teléfono
- Email
- Número de compras
- Total gastado
- Última interacción

**Cómo usar:**
1. Navega a la sección de Clientes
2. Verás una tabla con todos los clientes
3. Puedes ver su historial de compras
4. Identifica clientes frecuentes
5. Analiza patrones de compra

---

### 11. ⚙️ Configuración
**Ruta:** `/dashboard?tab=settings`

**Funcionalidades:**
- Configurar API Keys
- Gestionar notificaciones
- Configurar seguridad
- Gestionar base de datos

#### 🔑 API Keys
**Claves necesarias:**
1. **OpenAI API Key**
   - Necesaria para funciones de IA
   - Formato: `sk-...`
   - Obtener en: https://platform.openai.com

2. **PayPal**
   - Client ID
   - Secret
   - Obtener en: https://developer.paypal.com

3. **MercadoPago**
   - Access Token
   - Formato: `APP_USR-...`
   - Obtener en: https://www.mercadopago.com/developers

**Cómo configurar:**
1. Ve a la pestaña "API Keys"
2. Pega cada clave en su campo
3. Guarda la configuración

#### 🔔 Notificaciones
**Opciones:**
- Notificaciones por Email
- Notificaciones por WhatsApp
- Alertas de nuevos pedidos

**Cómo configurar:**
1. Ve a la pestaña "Notificaciones"
2. Activa/Desactiva cada tipo
3. Guarda los cambios

#### 🔒 Seguridad
**Opciones:**
- Autenticación de dos factores (2FA)
- Tiempo de sesión

**Cómo configurar:**
1. Ve a la pestaña "Seguridad"
2. Activa 2FA si lo deseas
3. Configura el tiempo de sesión (5-120 minutos)
4. Guarda los cambios

#### 💾 Base de Datos
**Funciones:**
- Respaldo automático
- Respaldo manual
- Restauración

**Cómo usar:**
1. Ve a la pestaña "Base de Datos"
2. Activa respaldos automáticos
3. Usa "Crear Respaldo Manual" cuando necesites
4. Usa "Restaurar" para recuperar datos

---

## 🎨 Características Generales

### Navegación
- **Sidebar:** Menú lateral con todas las secciones
- **Responsive:** Funciona en móvil, tablet y desktop
- **Colapsable:** Puedes colapsar el sidebar para más espacio

### Notificaciones
- **Toasts:** Mensajes emergentes para confirmaciones
- **Colores:**
  - Verde: Éxito
  - Rojo: Error
  - Azul: Información
  - Amarillo: Advertencia

### Estados de Carga
- **Spinners:** Mientras se cargan datos
- **Skeleton:** Placeholders mientras carga

### Actualización Automática
- Las estadísticas se actualizan cada 30 segundos
- Puedes forzar actualización con botones "Actualizar"

---

## 🔧 Solución de Problemas

### El dashboard no carga
1. Verifica que el servidor esté corriendo: `npm run dev`
2. Verifica la URL: `http://localhost:3001`
3. Limpia caché del navegador

### No puedo iniciar sesión
1. Verifica credenciales: `admin` / `admin123`
2. Verifica que el backend esté corriendo
3. Revisa la consola del navegador (F12)

### Los datos no se cargan
1. Verifica que el backend esté corriendo en puerto 5000
2. Revisa la consola del navegador (F12)
3. Verifica la conexión a la base de datos

### WhatsApp no conecta
1. Verifica que el servidor Baileys esté corriendo
2. Limpia la sesión de WhatsApp
3. Escanea el QR nuevamente

### Los productos no se guardan
1. Verifica que todos los campos estén completos
2. Revisa la consola del navegador (F12)
3. Verifica la conexión al backend

---

## 📞 Soporte

Si tienes problemas:
1. Revisa esta guía
2. Consulta los logs del servidor
3. Revisa la consola del navegador (F12)
4. Verifica que todos los servicios estén corriendo

---

## 🎉 ¡Disfruta tu Dashboard!

Ahora tienes un dashboard completo y profesional para gestionar tu bot de ventas de WhatsApp. Todas las funcionalidades están implementadas y listas para usar.

**¡Buenas ventas!** 🚀
