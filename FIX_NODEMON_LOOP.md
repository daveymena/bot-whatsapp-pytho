# 🔧 Solución: Loop Infinito de Nodemon

## Problema

El servidor Baileys se está reiniciando constantemente:
```
[nodemon] restarting due to changes...
[nodemon] starting `node baileys-server.js`
🚀 Baileys server running on port 3001
[nodemon] restarting due to changes...
```

## Causas

1. **Nodemon detecta cambios** en la carpeta `auth_info/` cada vez que se conecta
2. **Puerto incorrecto** - Está usando 3001 en lugar de 3002
3. **Archivo incorrecto** - Está ejecutando `baileys-server.js` en lugar de `server.js`

## Solución

### 1. Detener el proceso actual

En la terminal donde está corriendo, presiona:
```
Ctrl + C
```

Si no responde, cierra la terminal completamente.

### 2. Matar cualquier proceso en el puerto 3002

```bash
netstat -ano | findstr :3002
taskkill /PID [PID_NUMBER] /F
```

### 3. Iniciar correctamente (SIN nodemon)

**Opción A: Usar el script correcto**
```bash
cd C:\ventas-2
INICIAR_BAILEYS.bat
```

**Opción B: Manual**
```bash
cd C:\ventas-2\baileys-server
node server.js
```

**❌ NO USES:**
```bash
npm run dev          # Esto usa nodemon
nodemon server.js    # Esto causa el loop
```

**✅ USA:**
```bash
npm start            # Esto usa node directamente
node server.js       # Esto es lo correcto
```

## Verificar que Funciona

Después de iniciar correctamente, deberías ver:

```
============================================================
🚀 SERVIDOR BAILEYS INICIADO
============================================================
📡 Puerto: 3002
🔗 API: http://localhost:3002
🐍 Python API: http://localhost:5000
============================================================
🔄 Iniciando conexión a WhatsApp...
```

Y **NO** deberías ver:
```
[nodemon] restarting due to changes...
```

## Por Qué Pasa Esto

Nodemon está diseñado para desarrollo y reinicia el servidor cada vez que detecta cambios en archivos. El problema es que:

1. Baileys crea/modifica archivos en `auth_info/` cuando se conecta
2. Nodemon detecta estos cambios
3. Nodemon reinicia el servidor
4. El servidor se vuelve a conectar
5. Baileys modifica archivos en `auth_info/`
6. Vuelve al paso 2 (loop infinito)

## Solución Permanente

Se creó un archivo `.nodemonignore` que le dice a nodemon que ignore la carpeta `auth_info/`, pero **es mejor usar `node` directamente** para producción.

## Diferencia entre los Comandos

| Comando | Usa | Cuándo Usar |
|---------|-----|-------------|
| `npm run dev` | nodemon | Solo para desarrollo, cuando estás editando código |
| `npm start` | node | Para producción o cuando ya no vas a editar |
| `node server.js` | node | Siempre funciona, recomendado |

## Verificar Puerto Correcto

El servidor Baileys debe correr en el puerto **3002**, NO en 3001.

Para verificar:
```bash
netstat -ano | findstr :3002
```

Deberías ver algo como:
```
TCP    0.0.0.0:3002    0.0.0.0:0    LISTENING    [PID]
```

## Si el Problema Persiste

1. **Cierra todas las terminales**
2. **Mata todos los procesos de Node:**
   ```bash
   taskkill /F /IM node.exe
   ```
3. **Espera 5 segundos**
4. **Inicia de nuevo:**
   ```bash
   cd C:\ventas-2\baileys-server
   node server.js
   ```

## Resumen

✅ **CORRECTO:**
```bash
cd baileys-server
node server.js
```

❌ **INCORRECTO:**
```bash
cd baileys-server
npm run dev          # Causa loop infinito
nodemon server.js    # Causa loop infinito
```

## Próximos Pasos

Una vez que el servidor esté corriendo correctamente (sin reinicios):

1. Abre `http://localhost:3001` (dashboard)
2. Ve a la pestaña "WhatsApp"
3. El QR debería aparecer
4. Escanéalo con tu WhatsApp
