# ⚡ Inicio Rápido - 5 Minutos

## 🎯 Objetivo
Tener el bot funcionando en menos de 5 minutos.

## 📋 Pre-requisitos
- Python 3.9+ instalado
- Node.js 18+ instalado
- PostgreSQL instalado y corriendo

## 🚀 Pasos

### 1. Clonar e Instalar (2 min)
```bash
git clone <tu-repo>
cd whatsapp-sales-bot
pip install -r requirements.txt
npm install
```

### 2. Configurar (1 min)
```bash
# Copiar .env
cp .env.example .env

# Editar solo estas líneas esenciales:
nano .env
```

**Mínimo requerido:**
```env
GROQ_API_KEY=tu_api_key_de_groq
DATABASE_URL=postgresql://postgres:password@localhost:5432/botwhatsapp
BUSINESS_NAME=Tu Negocio
WHATSAPP_NUMBER=573001234567
```

### 3. Inicializar DB (30 seg)
```bash
python -c "from database.connection import init_db; init_db()"
python seed_database.py
```

### 4. Iniciar Bot (30 seg)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 5. Conectar WhatsApp (1 min)
1. Verás un QR code en la terminal
2. Abre WhatsApp en tu teléfono
3. Ve a **Dispositivos vinculados**
4. Escanea el QR
5. ¡Listo! 🎉

## ✅ Verificar

Abre en tu navegador:
- http://localhost:3000 - API Python
- http://localhost:3001/status - Baileys
- dashboard.html - Dashboard visual

## 🧪 Probar

Envía un mensaje de WhatsApp al número conectado:
```
Hola
```

El bot debería responder automáticamente.

## 🆘 Problemas Comunes

**Error: GROQ API key inválida**
- Obtén tu key en: https://console.groq.com/

**Error: No se puede conectar a PostgreSQL**
```bash
# Crear base de datos
createdb botwhatsapp
```

**Error: Puerto en uso**
```bash
# Cambiar puerto en .env
PORT=3002
```

## 📚 Siguiente Paso

Lee la documentación completa:
- [SETUP.md](SETUP.md) - Instalación detallada
- [API_DOCS.md](API_DOCS.md) - Documentación API
- [DEPLOYMENT.md](DEPLOYMENT.md) - Despliegue producción

## 💡 Tips

1. **Obtener GROQ API Key gratis:**
   - Visita https://console.groq.com/
   - Regístrate
   - Crea una API key
   - Copia y pega en .env

2. **Probar sin WhatsApp:**
   ```bash
   python test_conversation.py
   ```

3. **Ver dashboard:**
   - Abre `dashboard.html` en tu navegador
   - Verás estadísticas en tiempo real

4. **Personalizar agentes:**
   - Edita archivos en `agents/`
   - Modifica los prompts según tu negocio

## 🎓 Recursos

- [Video Tutorial](#) (próximamente)
- [Comunidad Discord](#) (próximamente)
- [Ejemplos](#) (próximamente)

---

**¿Funcionó?** ⭐ Dale una estrella al repo!

**¿Problemas?** 🐛 Abre un issue en GitHub
