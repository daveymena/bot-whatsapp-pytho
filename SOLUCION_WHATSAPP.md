# 🔧 Solución de Problemas de WhatsApp

## Error: "Error al conectar WhatsApp"

Este error ocurre cuando el dashboard no puede comunicarse con los servidores. Sigue estos pasos:

### 1. Verificar que todos los servidores estén corriendo

Ejecuta el script de verificación:
```bash
CHECK_SERVERS.bat
```

Debes ver:
- ✅ Servidor Python corriendo (puerto 5000)
- ✅ Servidor Baileys corriendo (puerto 3002)
- ✅ Dashboard Next.js corriendo (puerto 3001)

### 2. Si algún servidor NO está corriendo

**Opción A: Iniciar todos los servidores automáticamente**
```bash
START_ALL_FIXED.bat
```

**Opción B: Iniciar manualmente cada servidor**

Terminal 1 - Servidor Python:
```bash
python main.py
```

Terminal 2 - Servidor Baileys:
```bash
cd baileys-server
node server.js
```

Terminal 3 - Dashboard Next.js:
```bash
cd dashboard-nextjs
npm run dev
```

### 3. Si los servidores están corriendo pero sigue el error

#### Paso 1: Limpiar la sesión de WhatsApp

En el dashboard, haz clic en el botón **"Limpiar Sesión"**

O manualmente:
```bash
cd baileys-server
rmdir /s /q auth_info
```

#### Paso 2: Reiniciar el servidor Baileys

1. Cierra la terminal del servidor Baileys (Ctrl+C)
2. Vuelve a iniciarlo:
```bash
cd baileys-server
node server.js
```

#### Paso 3: Reconectar WhatsApp

1. En el dashboard, haz clic en **"Reconectar"**
2. Espera a que aparezca el código QR
3. Escanea el QR con tu WhatsApp

### 4. Verificar puertos en uso

Si hay conflictos de puertos, verifica qué está usando cada puerto:

```bash
netstat -ano | findstr :5000
netstat -ano | findstr :3002
netstat -ano | findstr :3001
```

### 5. Errores comunes y soluciones

#### Error: "EADDRINUSE" (Puerto en uso)

**Solución:** Mata el proceso que está usando el puerto

```bash
# Para puerto 5000
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F

# Para puerto 3002
netstat -ano | findstr :3002
taskkill /PID [PID_NUMBER] /F
```

#### Error: "Cannot find module"

**Solución:** Reinstala las dependencias

Para Baileys:
```bash
cd baileys-server
npm install
```

Para Dashboard:
```bash
cd dashboard-nextjs
npm install
```

#### Error: "QR Code no aparece"

**Solución:**
1. Limpia la sesión (botón "Limpiar Sesión")
2. Espera 5 segundos
3. Haz clic en "Reconectar"
4. El QR debería aparecer en 10-15 segundos

#### Error: "Connection timeout"

**Solución:**
1. Verifica tu conexión a internet
2. Desactiva temporalmente el firewall/antivirus
3. Reinicia todos los servidores

### 6. Logs para diagnóstico

**Ver logs del servidor Baileys:**
- Abre la terminal donde corre `node server.js`
- Busca mensajes de error en rojo

**Ver logs del servidor Python:**
- Abre la terminal donde corre `python main.py`
- Busca mensajes de error

**Ver logs del navegador:**
- Abre DevTools (F12)
- Ve a la pestaña "Console"
- Busca errores en rojo

### 7. Última opción: Reinstalación completa

Si nada funciona, reinstala todo:

```bash
# 1. Detener todos los servidores (Ctrl+C en cada terminal)

# 2. Limpiar sesión de WhatsApp
cd baileys-server
rmdir /s /q auth_info

# 3. Reinstalar dependencias de Baileys
npm install

# 4. Volver al directorio principal
cd ..

# 5. Reinstalar dependencias de Python
pip install -r requirements.txt

# 6. Reinstalar dependencias del dashboard
cd dashboard-nextjs
npm install

# 7. Volver al directorio principal
cd ..

# 8. Iniciar todo de nuevo
START_ALL_FIXED.bat
```

## ✅ Checklist de verificación

Antes de reportar un problema, verifica:

- [ ] Todos los servidores están corriendo
- [ ] No hay conflictos de puertos
- [ ] La conexión a internet funciona
- [ ] El firewall no está bloqueando los puertos
- [ ] Las dependencias están instaladas
- [ ] La sesión de WhatsApp está limpia
- [ ] Has esperado al menos 15 segundos después de reconectar

## 📞 Soporte

Si después de seguir todos estos pasos el problema persiste:

1. Toma capturas de pantalla de:
   - El error en el dashboard
   - Los logs de la terminal de Baileys
   - Los logs de la terminal de Python
   - La consola del navegador (F12)

2. Anota:
   - Sistema operativo
   - Versión de Node.js (`node --version`)
   - Versión de Python (`python --version`)
   - Qué pasos has intentado

3. Revisa los archivos de documentación:
   - `BAILEYS_SETUP.md`
   - `PORTS_CONFIG.md`
   - `TROUBLESHOOTING.md`
