@echo off
echo 🚀 Iniciando Bot de Ventas WhatsApp
echo ==================================

REM Instalar dependencias Python
echo 📦 Instalando dependencias Python...
pip install -r requirements.txt

REM Instalar dependencias Node.js
echo 📦 Instalando dependencias Node.js...
call npm install

REM Inicializar base de datos
echo 🗄️ Inicializando base de datos...
python -c "from database.connection import init_db; init_db()"

REM Iniciar servidor Baileys
echo 📱 Iniciando servidor Baileys...
start "Baileys Server" cmd /k npm start

REM Esperar 3 segundos
timeout /t 3 /nobreak

REM Iniciar servidor Python
echo 🐍 Iniciando servidor Python...
start "Python API" cmd /k python main.py

echo.
echo ✅ Bot iniciado correctamente
echo ==================================
echo 📱 Baileys: http://localhost:3001
echo 🐍 Python API: http://localhost:3000
echo 📊 QR Code: http://localhost:3001/qr
echo.
pause
