#!/bin/bash

echo "🚀 Iniciando Bot de Ventas WhatsApp"
echo "=================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado"
    exit 1
fi

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt

# Instalar dependencias Node.js
echo "📦 Instalando dependencias Node.js..."
npm install

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python3 -c "from database.connection import init_db; init_db()"

# Iniciar servidor Baileys en background
echo "📱 Iniciando servidor Baileys..."
npm start &
BAILEYS_PID=$!

# Esperar a que Baileys inicie
sleep 3

# Iniciar servidor Python
echo "🐍 Iniciando servidor Python..."
python3 main.py &
PYTHON_PID=$!

echo ""
echo "✅ Bot iniciado correctamente"
echo "=================================="
echo "📱 Baileys: http://localhost:3001"
echo "🐍 Python API: http://localhost:3000"
echo "📊 QR Code: http://localhost:3001/qr"
echo ""
echo "Para detener: kill $BAILEYS_PID $PYTHON_PID"
echo ""

# Mantener el script corriendo
wait
