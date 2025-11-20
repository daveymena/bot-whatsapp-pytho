# 🔧 CONFIGURAR VARIABLES EN EASYPANEL

## 📋 ARCHIVO DE VARIABLES

Todas las variables están en: **`VARIABLES_EASYPANEL.txt`**

---

## 🎯 PASOS PARA CONFIGURAR

### 1. Abrir Easypanel
1. Ve a tu panel de Easypanel
2. Selecciona el proyecto `bot-whatsapp`
3. Click en el servicio `bot-whatsapp-python`

### 2. Ir a Variables de Entorno
1. En el menú lateral, click en **"Environment"** o **"Variables"**
2. Verás un editor de texto

### 3. Copiar Variables
1. Abre el archivo `VARIABLES_EASYPANEL.txt`
2. **Copia TODO el contenido**
3. Pégalo en el editor de Easypanel

### 4. Ajustar Variables Críticas

#### A. DATABASE_URL (IMPORTANTE)
```env
# Cambiar esto:
DATABASE_URL=postgresql://postgres:TU_PASSWORD_AQUI@bot-whatsapp-db:5432/botwhatsapp

# Por esto (usa el password que configuraste en PostgreSQL):
DATABASE_URL=postgresql://postgres:tu_password_real@bot-whatsapp-db:5432/botwhatsapp
```

#### B. URLs de Easypanel
Actualiza estas URLs con las que te da Easypanel:
```env
NEXT_PUBLIC_APP_URL=https://tu-app.sqaoeo.easypanel.host
NEXTAUTH_URL=https://tu-app.sqaoeo.easypanel.host
FRONTEND_URL=https://tu-app.sqaoeo.easypanel.host
```

#### C. Secrets (Opcional pero recomendado)
Genera nuevos secrets para producción:
```env
NEXTAUTH_SECRET=genera_un_secret_aleatorio_aqui
JWT_SECRET=genera_otro_secret_aleatorio_aqui
PAYMENT_LINK_TOKEN_SECRET=genera_otro_secret_aleatorio_aqui
```

Para generar secrets aleatorios:
```bash
# En tu terminal local:
openssl rand -base64 32
```

### 5. Guardar y Deploy
1. Click en **"Save"** o **"Update"**
2. Easypanel redesplegará automáticamente
3. Espera 2-3 minutos

---

## ✅ VARIABLES CRÍTICAS (VERIFICAR)

Estas variables son OBLIGATORIAS:

### Base de Datos
```env
DATABASE_URL=postgresql://postgres:PASSWORD@bot-whatsapp-db:5432/botwhatsapp
```

### IA (GROQ)
```env
GROQ_API_KEY=tu_groq_api_key_aqui
GROQ_API_KEY_2=tu_segunda_groq_key_aqui
GROQ_API_KEY_6=tu_tercera_groq_key_aqui
```

### Negocio
```env
BUSINESS_NAME=Tecnovariedades D&S
BUSINESS_PHONE=+57 300 556 0186
BUSINESS_EMAIL=deinermena25@gmail.com
```

### Pagos
```env
NEQUI_NUMBER=3136174267
DAVIPLATA_NUMBER=3136174267
MERCADOPAGO_ACCESS_TOKEN=APP_USR-8419296773492182-072623-ec7505166228860ec8b43957c948e7da-2021591453
PAYPAL_CLIENT_ID=BAAtdQwVN8LvIoRstmHZWlo2ndcJBP8dFZdXLc8HJGdYUXstriO6mO0GJMZimkBCdZHotBkulELqeFm_R4
PAYPAL_CLIENT_SECRET=EP5jZdzbUuHva4I8ERnbNYSHQ_BNe0niXQe91Bvf33Kl88nRKY-ivRx0_PGERS72JbjQSiMr63y9lEEL
```

### Email
```env
SMTP_USER=deinermena25@gmail.com
SMTP_PASSWORD=uccj yqpq vqlt vcie
```

---

## 📝 FORMATO EN EASYPANEL

Easypanel acepta dos formatos:

### Formato 1: Texto Plano (Recomendado)
```
VARIABLE1=valor1
VARIABLE2=valor2
VARIABLE3=valor3
```

### Formato 2: JSON (Alternativo)
```json
{
  "VARIABLE1": "valor1",
  "VARIABLE2": "valor2",
  "VARIABLE3": "valor3"
}
```

**Usa el Formato 1** (texto plano) que está en `VARIABLES_EASYPANEL.txt`

---

## 🔍 VERIFICAR CONFIGURACIÓN

Después de guardar, verifica:

### 1. Ver Logs
```bash
# En Easypanel, ve a "Logs" del servicio bot-whatsapp-python
# Busca errores como:
- "DATABASE_URL not found" ❌
- "GROQ_API_KEY not found" ❌
- "Application startup complete" ✅
```

### 2. Health Check
```bash
# Accede a:
https://tu-app.sqaoeo.easypanel.host/health

# Debe responder:
{
  "status": "healthy",
  "database": "connected"
}
```

### 3. Variables Cargadas
En los logs, al inicio debe mostrar:
```
INFO: Loading environment variables...
INFO: Database URL configured
INFO: GROQ API configured
INFO: Email SMTP configured
```

---

## ⚠️ PROBLEMAS COMUNES

### Problema 0: "TypeError: Client.__init__() got an unexpected keyword argument 'proxies'"
**Causa:** Versión antigua de la librería `groq`

**Solución:**
1. Ya se actualizó `requirements.txt` con `groq>=0.11.0`
2. Ejecuta `ACTUALIZAR_GROQ.bat` para subir los cambios
3. En Easypanel, fuerza un rebuild del servicio
4. O espera a que Easypanel detecte el cambio y reconstruya automáticamente

**Ver documentación completa:** `FIX_GROQ_ERROR.md`

### Problema 1: "Database connection failed"
**Causa:** DATABASE_URL incorrecta

**Solución:**
```env
# Verifica que sea:
DATABASE_URL=postgresql://postgres:PASSWORD@bot-whatsapp-db:5432/botwhatsapp

# NO uses localhost o 127.0.0.1
# USA el nombre del servicio: bot-whatsapp-db
```

### Problema 2: "GROQ API key not found"
**Causa:** Variable no configurada

**Solución:**
```env
# Verifica que estén las 3 keys:
GROQ_API_KEY=gsk_...
GROQ_API_KEY_2=gsk_...
GROQ_API_KEY_6=gsk_...
```

### Problema 3: "SMTP authentication failed"
**Causa:** Contraseña incorrecta

**Solución:**
```env
# Usa la contraseña de aplicación de Gmail:
SMTP_PASSWORD=uccj yqpq vqlt vcie

# NO uses tu contraseña normal de Gmail
```

### Problema 4: Variables no se cargan
**Causa:** Formato incorrecto

**Solución:**
- No uses comillas en los valores
- No uses espacios alrededor del `=`
- Una variable por línea
- Sin comas al final

**Correcto:**
```env
VARIABLE=valor
```

**Incorrecto:**
```env
VARIABLE = "valor",
```

---

## 🔄 ACTUALIZAR VARIABLES

Si necesitas cambiar variables después:

1. Ve a Easypanel → Servicio → Environment
2. Edita las variables
3. Click "Save"
4. El servicio se redesplegará automáticamente

---

## 📊 RESUMEN

### Archivo a Usar
```
VARIABLES_EASYPANEL.txt
```

### Dónde Configurar
```
Easypanel → bot-whatsapp → bot-whatsapp-python → Environment
```

### Variables Críticas
- ✅ DATABASE_URL
- ✅ GROQ_API_KEY (3 keys)
- ✅ BUSINESS_* (info del negocio)
- ✅ SMTP_* (email)
- ✅ Métodos de pago

### Verificar
```
Logs → "Application startup complete"
Health → https://tu-app/health
```

---

## 🎯 CHECKLIST

Antes de continuar:
- [ ] Copié todas las variables de `VARIABLES_EASYPANEL.txt`
- [ ] Pegué en Easypanel → Environment
- [ ] Actualicé `DATABASE_URL` con el password correcto
- [ ] Actualicé las URLs con mi dominio de Easypanel
- [ ] Guardé los cambios
- [ ] Esperé el redeploy (2-3 min)
- [ ] Verifiqué los logs (sin errores)
- [ ] Probé el health check (responde OK)

---

## ✅ LISTO

Una vez configuradas las variables, el bot estará listo para:
- Conectarse a la base de datos
- Usar IA (GROQ)
- Procesar pagos
- Enviar emails
- Responder mensajes de WhatsApp

**Siguiente paso:** Conectar WhatsApp escaneando el QR code 📱
