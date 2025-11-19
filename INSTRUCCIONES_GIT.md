# 🚀 INSTRUCCIONES PARA SUBIR A GITHUB

## ⚠️ IMPORTANTE: SEGURIDAD PRIMERO

**NUNCA subas estos archivos a Git:**
- ❌ `.env` - Contiene API keys y contraseñas
- ❌ `.env.local`, `.env.production` - Variables sensibles
- ❌ `data/` - Sesiones de WhatsApp
- ❌ `temp-media/`, `temp-images/` - Archivos temporales

---

## 📋 PASOS PARA SUBIR EL CÓDIGO

### 1. Verificar Seguridad (OBLIGATORIO)
```bash
VERIFICAR_SEGURIDAD.bat
```

**Debe mostrar:**
```
✅ VERIFICACIÓN EXITOSA
Todo está correcto. Es seguro subir a Git.
```

Si muestra errores, NO continúes hasta corregirlos.

---

### 2. Subir a GitHub
```bash
SUBIR_A_GIT.bat
```

**El script hará:**
1. ✅ Verificar que Git esté instalado
2. ✅ Inicializar repositorio (si no existe)
3. ✅ Configurar remote: `https://github.com/daveymena/bot-whatsapp-pytho.git`
4. ✅ Verificar archivos sensibles
5. ✅ Agregar archivos (excluyendo .env y data/)
6. ✅ Crear commit
7. ✅ Subir a GitHub

---

### 3. Autenticación en GitHub

Cuando Git pida credenciales:

**Usuario:** `daveymena`

**Contraseña:** NO uses tu contraseña de GitHub, usa un **Token Personal**

#### Cómo obtener el Token:
1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Nombre: `bot-whatsapp-deployment`
4. Expiration: `No expiration` (o 90 días)
5. Selecciona permisos:
   - ✅ `repo` (todos los sub-permisos)
6. Click "Generate token"
7. **COPIA EL TOKEN** (solo se muestra una vez)
8. Úsalo como contraseña cuando Git lo pida

---

## 🔍 VERIFICAR QUE SE SUBIÓ CORRECTAMENTE

### 1. Ver en GitHub
```
https://github.com/daveymena/bot-whatsapp-pytho
```

### 2. Verificar que NO se subieron archivos sensibles

En GitHub, busca:
- ❌ NO debe aparecer `.env`
- ❌ NO debe aparecer carpeta `data/`
- ✅ SÍ debe aparecer `.env.example`
- ✅ SÍ debe aparecer `.gitignore`

---

## 📁 ARCHIVOS QUE SÍ SE SUBEN

### Código Fuente
- ✅ `*.py` - Archivos Python
- ✅ `*.js` - Archivos JavaScript
- ✅ `*.ts`, `*.tsx` - Archivos TypeScript
- ✅ `*.json` - Configuraciones

### Configuración
- ✅ `Dockerfile`, `Dockerfile.baileys`
- ✅ `docker-compose.prod.yml`
- ✅ `easypanel.yml`
- ✅ `.dockerignore`
- ✅ `.gitignore`
- ✅ `requirements.txt`
- ✅ `package.json`

### Documentación
- ✅ `*.md` - Archivos Markdown
- ✅ `README.md`
- ✅ `DEPLOYMENT_EASYPANEL.md`

---

## 📁 ARCHIVOS QUE NO SE SUBEN

### Sensibles (Protegidos por .gitignore)
- ❌ `.env` - Variables de entorno
- ❌ `.env.local`, `.env.production`
- ❌ `data/` - Sesiones de WhatsApp
- ❌ `temp-media/`, `temp-images/`

### Generados
- ❌ `__pycache__/` - Cache de Python
- ❌ `node_modules/` - Dependencias Node
- ❌ `*.log` - Logs
- ❌ `*.db`, `*.sqlite` - Bases de datos locales

---

## 🔄 ACTUALIZAR CÓDIGO (después del primer push)

### Método 1: Script Automático
```bash
# Crear script de actualización
echo @echo off > ACTUALIZAR_GIT.bat
echo git add . >> ACTUALIZAR_GIT.bat
echo git commit -m "update: cambios realizados" >> ACTUALIZAR_GIT.bat
echo git push origin main >> ACTUALIZAR_GIT.bat

# Ejecutar
ACTUALIZAR_GIT.bat
```

### Método 2: Manual
```bash
git add .
git commit -m "update: descripción de cambios"
git push origin main
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "Permission denied"
**Causa:** No tienes permisos en el repositorio

**Solución:**
1. Verifica que seas colaborador del repo
2. Usa el token personal correcto
3. Verifica que el token tenga permisos `repo`

---

### Problema: "Authentication failed"
**Causa:** Token inválido o contraseña incorrecta

**Solución:**
1. NO uses tu contraseña de GitHub
2. Genera un nuevo token personal
3. Copia el token completo
4. Úsalo como contraseña

---

### Problema: ".env aparece en git status"
**Causa:** .env no está en .gitignore o ya fue agregado antes

**Solución:**
```bash
# Remover .env del tracking de Git
git rm --cached .env

# Verificar que esté en .gitignore
findstr ".env" .gitignore

# Si no está, agregarlo
echo .env >> .gitignore

# Commit y push
git add .gitignore
git commit -m "fix: agregar .env a gitignore"
git push origin main
```

---

### Problema: "data/ se está subiendo"
**Causa:** data/ no está en .gitignore

**Solución:**
```bash
# Remover data/ del tracking
git rm --cached -r data/

# Verificar .gitignore
findstr "data/" .gitignore

# Si no está, agregarlo
echo data/ >> .gitignore

# Commit y push
git add .gitignore
git commit -m "fix: agregar data/ a gitignore"
git push origin main
```

---

### Problema: "Conflictos al hacer push"
**Causa:** Hay cambios en GitHub que no tienes localmente

**Solución:**
```bash
# Descargar cambios de GitHub
git pull origin main

# Resolver conflictos si los hay
# Editar archivos en conflicto

# Agregar archivos resueltos
git add .

# Commit
git commit -m "fix: resolver conflictos"

# Push
git push origin main
```

---

## ✅ CHECKLIST ANTES DE SUBIR

Antes de ejecutar `SUBIR_A_GIT.bat`:

- [ ] ✅ Ejecuté `VERIFICAR_SEGURIDAD.bat`
- [ ] ✅ Verificación pasó sin errores
- [ ] ✅ `.env` está en `.gitignore`
- [ ] ✅ `data/` está en `.gitignore`
- [ ] ✅ Tengo mi token personal de GitHub listo
- [ ] ✅ El código funciona localmente
- [ ] ✅ No hay archivos sensibles sin proteger

---

## 🎯 DESPUÉS DE SUBIR

1. ✅ Verificar en GitHub que el código se subió
2. ✅ Verificar que NO aparezca `.env`
3. ✅ Verificar que NO aparezca `data/`
4. ✅ Continuar con deployment a Easypanel
5. ✅ Seguir `DEPLOYMENT_EASYPANEL.md`

---

## 📞 SOPORTE

Si tienes problemas:
1. Revisa esta guía completa
2. Ejecuta `VERIFICAR_SEGURIDAD.bat`
3. Revisa los mensajes de error
4. Busca la solución en "SOLUCIÓN DE PROBLEMAS"

---

## 🎉 ¡LISTO!

Una vez que el código esté en GitHub:
```
https://github.com/daveymena/bot-whatsapp-pytho
```

Puedes continuar con el deployment a Easypanel siguiendo:
```
DEPLOYMENT_EASYPANEL.md
```

¡Éxito! 🚀
