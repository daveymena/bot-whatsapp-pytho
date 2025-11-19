@echo off
title Bot de Ventas con Pagos y Fotos
color 0A

echo ========================================
echo   BOT DE VENTAS INTELIGENTE
echo   Con Pagos Dinamicos y Fotos
echo ========================================
echo.

echo [1/5] Verificando dependencias...
pip show mercadopago >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Mercado Pago no instalado. Instalando...
    pip install mercadopago==2.2.1
)

pip show paypalrestsdk >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PayPal no instalado. Instalando...
    pip install paypalrestsdk==1.13.1
)

echo ✅ Dependencias verificadas
echo.

echo [2/5] Iniciando servidor Baileys (WhatsApp)...
cd baileys-server
start "Baileys Server" cmd /k "node server.js"
cd ..
timeout /t 5 /nobreak >nul

echo.
echo [3/5] Iniciando bot principal (Python)...
start "Bot Principal" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo.
echo [4/5] Iniciando dashboard Next.js...
cd dashboard-nextjs
start "Dashboard" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul

echo.
echo [5/5] Ejecutando pruebas de integracion...
timeout /t 5 /nobreak >nul
python test_payment_integration.py

echo.
echo ========================================
echo   SISTEMA COMPLETAMENTE OPERATIVO
echo ========================================
echo.
echo 📱 WhatsApp: Escanea el QR en la ventana de Baileys
echo 🤖 Bot: http://localhost:5000
echo 📊 Dashboard: http://localhost:3000
echo.
echo 💳 METODOS DE PAGO ACTIVOS:
echo   - Mercado Pago (links dinamicos)
echo   - PayPal (internacional)
echo   - Nequi / Daviplata
echo   - Transferencia Bancaria
echo   - Contra Entrega
echo.
echo 📸 FOTOS:
echo   - Envio automatico de fotos de productos
echo   - Catalogo con imagenes
echo   - Busqueda inteligente con fotos
echo.
echo Presiona cualquier tecla para ver los logs...
pause >nul

echo.
echo Abriendo logs del sistema...
start "Logs Bot" cmd /k "python -c \"import time; from database.connection import SessionLocal; from database.models import ChatLog; db = SessionLocal(); while True: logs = db.query(ChatLog).order_by(ChatLog.created_at.desc()).limit(10).all(); print('\n'.join([f'{l.user_phone}: {l.content}' for l in logs])); time.sleep(5)\""

echo.
echo Sistema en ejecucion. No cierres esta ventana.
echo Para detener, cierra todas las ventanas de comandos.
pause
