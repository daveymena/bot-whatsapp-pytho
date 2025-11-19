# 🚀 Sistema de Inicio Unificado

## ¡Todo desde un Solo Lugar!

Ya no necesitas abrir 3 terminales diferentes. Ahora puedes controlar todo el sistema desde un solo lugar.

## 📋 Scripts Disponibles

### 1. **MENU.bat** - Menú Principal Interactivo
El centro de control del sistema. Desde aquí puedes hacer todo:

```bash
MENU.bat
```

**Opciones disponibles:**
- [1] Iniciar Sistema Completo
- [2] Detener Sistema Completo
- [3] Reiniciar Sistema
- [4] Ver Estado del Sistema
- [5] Verificar Instalación
- [6] Limpiar Sesión WhatsApp
- [7] Ejecutar Pruebas
- [8] Abrir Dashboard en Navegador
- [9] Ver Documentación
- [0] Salir

### 2. **START_SYSTEM.bat** - Inicio Rápido
Inicia todos los servicios automáticamente:

```bash
START_SYSTEM.bat
```

**Qué hace:**
- ✅ Inicia Python API (Puerto 5000)
- ✅ Inicia Baileys Server (Puerto 3002)
- ✅ Inicia Dashboard Next.js (Puerto 3001)
- ✅ Verifica que todo esté corriendo
- ✅ Abre 3 terminales con colores diferentes

### 3. **STOP_SYSTEM.bat** - Detener Todo
Detiene todos los servicios de una vez:

```bash
STOP_SYSTEM.bat
```

**Qué hace:**
- ⛔ Detiene todos los procesos Node.js
- ⛔ Detiene todos los procesos Python
- ⛔ Limpia los puertos

### 4. **RESTART_SYSTEM.bat** - Reinicio Rápido
Reinicia todo el sistema:

```bash
RESTART_SYSTEM.bat
```

**Qué hace:**
- 🔄 Detiene todos los servicios
- ⏳ Espera 5 segundos
- ✅ Inicia todo de nuevo

### 5. **STATUS_SYSTEM.bat** - Monitor en Tiempo Real
Monitorea el estado de todos los servicios:

```bash
STATUS_SYSTEM.bat
```

**Qué muestra:**
- 🟢 Estado de Python API
- 🟢 Estado de Baileys Server
- 🟢 Estado de Dashboard
- 🔄 Se actualiza automáticamente

## 🎯 Uso Recomendado

### Primera Vez

1. **Ejecuta el menú principal:**
   ```bash
   MENU.bat
   ```

2. **Selecciona opción [5]** para verificar instalación

3. **Selecciona opción [1]** para iniciar el sistema

4. **Selecciona opción [8]** para abrir el dashboard

### Uso Diario

**Opción A: Menú Interactivo (Recomendado)**
```bash
MENU.bat
```
Luego selecciona la opción que necesites.

**Opción B: Inicio Directo**
```bash
START_SYSTEM.bat
```
Inicia todo directamente sin menú.

### Detener al Final del Día

```bash
STOP_SYSTEM.bat
```
O usa el menú: `MENU.bat` → Opción [2]

## 📊 Ventanas que se Abren

Cuando inicias el sistema, se abren 3 ventanas con colores diferentes:

1. **Ventana Azul** - Python API (Puerto 5000)
   - Logs del servidor Python
   - Procesamiento de mensajes
   - IA y agentes

2. **Ventana Verde** - Baileys Server (Puerto 3002)
   - Conexión de WhatsApp
   - Código QR
   - Mensajes entrantes/salientes

3. **Ventana Amarilla** - Dashboard (Puerto 3001)
   - Servidor Next.js
   - Compilación de páginas
   - Hot reload

## 🔍 Verificar que Todo Funciona

### Método 1: Usar el Monitor
```bash
STATUS_SYSTEM.bat
```

Deberías ver:
```
[Python API - Puerto 5000]
Estado: [ONLINE] Corriendo correctamente
Puerto: [OK] 5000 en uso

[Baileys Server - Puerto 3002]
Estado: [ONLINE] Corriendo correctamente
Puerto: [OK] 3002 en uso

[Dashboard Next.js - Puerto 3001]
Estado: [ONLINE] Corriendo correctamente
Puerto: [OK] 3001 en uso
```

### Método 2: Abrir URLs
- Python API: http://localhost:5000/admin/whatsapp/status
- Baileys: http://localhost:3002/status
- Dashboard: http://localhost:3001

## 🛠️ Solución de Problemas

### Problema: "Puerto en uso"

**Solución:**
```bash
STOP_SYSTEM.bat
```
Espera 5 segundos y luego:
```bash
START_SYSTEM.bat
```

### Problema: Un servicio no inicia

**Solución:**
1. Ejecuta `STATUS_SYSTEM.bat` para ver cuál falla
2. Revisa la ventana de ese servicio para ver el error
3. Corrige el error
4. Ejecuta `RESTART_SYSTEM.bat`

### Problema: WhatsApp no conecta

**Solución:**
1. Ejecuta `MENU.bat`
2. Selecciona opción [6] (Limpiar Sesión WhatsApp)
3. Selecciona opción [3] (Reiniciar Sistema)
4. Escanea el nuevo QR

## 📁 Estructura de Scripts

```
ventas-2/
├── MENU.bat                    # ⭐ Menú principal (USAR ESTE)
├── START_SYSTEM.bat            # Iniciar todo
├── STOP_SYSTEM.bat             # Detener todo
├── RESTART_SYSTEM.bat          # Reiniciar todo
├── STATUS_SYSTEM.bat           # Monitor de estado
├── VERIFICAR_INSTALACION.bat   # Verificar dependencias
└── test_professional_sales.py  # Pruebas del sistema
```

## 🎨 Personalización

### Cambiar Puertos

Edita `.env`:
```env
PORT=5000  # Puerto de Python
```

Para Baileys, edita `baileys-server/server.js`:
```javascript
const PORT = 3002;
```

Para Dashboard, edita `dashboard-nextjs/package.json`:
```json
"dev": "next dev -p 3001"
```

### Cambiar Colores de Ventanas

Edita `START_SYSTEM.bat`:
```batch
color 0B  # Azul claro
color 0A  # Verde
color 0E  # Amarillo
```

## 📝 Comandos Rápidos

| Acción | Comando |
|--------|---------|
| Iniciar todo | `START_SYSTEM.bat` |
| Detener todo | `STOP_SYSTEM.bat` |
| Reiniciar | `RESTART_SYSTEM.bat` |
| Ver estado | `STATUS_SYSTEM.bat` |
| Menú completo | `MENU.bat` |

## 🚀 Flujo de Trabajo Típico

### Mañana (Iniciar)
```bash
1. Doble clic en MENU.bat
2. Presiona [1] para iniciar
3. Presiona [8] para abrir dashboard
4. ¡Listo para trabajar!
```

### Durante el Día (Monitorear)
```bash
1. Doble clic en STATUS_SYSTEM.bat
2. Deja la ventana abierta
3. Se actualiza automáticamente
```

### Noche (Detener)
```bash
1. Doble clic en MENU.bat
2. Presiona [2] para detener
3. Cierra todas las ventanas
```

## ✅ Ventajas del Sistema Unificado

✅ **Un Solo Comando** - No más 3 terminales
✅ **Colores Diferentes** - Identifica cada servicio fácilmente
✅ **Verificación Automática** - Sabe si todo está corriendo
✅ **Reinicio Rápido** - Un comando para reiniciar todo
✅ **Monitor en Tiempo Real** - Ve el estado siempre
✅ **Menú Interactivo** - Todas las opciones en un lugar

## 🎉 ¡Mucho Más Fácil!

Antes:
```
Terminal 1: python main.py
Terminal 2: cd baileys-server && node server.js
Terminal 3: cd dashboard-nextjs && npm run dev
```

Ahora:
```
MENU.bat → [1]
```

¡Eso es todo! 🚀

## 📞 Soporte

Si tienes problemas:
1. Ejecuta `STATUS_SYSTEM.bat` para diagnóstico
2. Revisa las ventanas de cada servicio
3. Consulta `SOLUCION_WHATSAPP.md`
4. Usa `RESTART_SYSTEM.bat` para reiniciar

## 🎯 Próximos Pasos

1. ✅ Ejecuta `MENU.bat`
2. ✅ Inicia el sistema (opción 1)
3. ✅ Abre el dashboard (opción 8)
4. ✅ Conecta WhatsApp
5. ✅ ¡Empieza a vender!
