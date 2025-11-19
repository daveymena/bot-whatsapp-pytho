@echo off
title Verificacion de Instalacion - Bot de Ventas
color 0B

echo ========================================
echo   VERIFICACION DE INSTALACION
echo   Bot de Ventas con Pagos y Fotos
echo ========================================
echo.

echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python NO instalado
    echo    Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python instalado
)

echo.
echo [2/8] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js NO instalado
    echo    Descarga desde: https://nodejs.org/
    pause
    exit /b 1
) else (
    node --version
    echo ✅ Node.js instalado
)

echo.
echo [3/8] Verificando dependencias Python...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo ❌ FastAPI no instalado
    echo    Ejecuta: pip install -r requirements.txt
) else (
    echo ✅ FastAPI instalado
)

pip show mercadopago >nul 2>&1
if errorlevel 1 (
    echo ❌ Mercado Pago SDK no instalado
    echo    Ejecuta: pip install mercadopago
) else (
    echo ✅ Mercado Pago SDK instalado
)

pip show paypalrestsdk >nul 2>&1
if errorlevel 1 (
    echo ❌ PayPal SDK no instalado
    echo    Ejecuta: pip install paypalrestsdk
) else (
    echo ✅ PayPal SDK instalado
)

pip show pillow >nul 2>&1
if errorlevel 1 (
    echo ❌ Pillow no instalado
    echo    Ejecuta: pip install pillow
) else (
    echo ✅ Pillow instalado
)

echo.
echo [4/8] Verificando archivo .env...
if exist .env (
    echo ✅ Archivo .env existe
    
    findstr /C:"MERCADOPAGO_ACCESS_TOKEN" .env >nul
    if errorlevel 1 (
        echo ⚠️  MERCADOPAGO_ACCESS_TOKEN no configurado
    ) else (
        echo ✅ Mercado Pago configurado
    )
    
    findstr /C:"PAYPAL_CLIENT_ID" .env >nul
    if errorlevel 1 (
        echo ⚠️  PAYPAL_CLIENT_ID no configurado
    ) else (
        echo ✅ PayPal configurado
    )
    
    findstr /C:"NEQUI_NUMBER" .env >nul
    if errorlevel 1 (
        echo ⚠️  NEQUI_NUMBER no configurado
    ) else (
        echo ✅ Nequi configurado
    )
    
    findstr /C:"DATABASE_URL" .env >nul
    if errorlevel 1 (
        echo ❌ DATABASE_URL no configurado
    ) else (
        echo ✅ Base de datos configurada
    )
) else (
    echo ❌ Archivo .env NO existe
    echo    Copia .env.example a .env y configura las variables
)

echo.
echo [5/8] Verificando estructura de archivos...
if exist services\payment_service.py (
    echo ✅ payment_service.py
) else (
    echo ❌ payment_service.py NO encontrado
)

if exist integrations\mercadopago_integration.py (
    echo ✅ mercadopago_integration.py
) else (
    echo ❌ mercadopago_integration.py NO encontrado
)

if exist integrations\paypal_integration.py (
    echo ✅ paypal_integration.py
) else (
    echo ❌ paypal_integration.py NO encontrado
)

if exist admin\payment_routes.py (
    echo ✅ payment_routes.py
) else (
    echo ❌ payment_routes.py NO encontrado
)

if exist whatsapp\multimedia_handler.py (
    echo ✅ multimedia_handler.py
) else (
    echo ❌ multimedia_handler.py NO encontrado
)

echo.
echo [6/8] Verificando Baileys Server...
if exist baileys-server\server.js (
    echo ✅ Baileys server encontrado
) else (
    echo ❌ Baileys server NO encontrado
)

if exist baileys-server\node_modules (
    echo ✅ Dependencias de Baileys instaladas
) else (
    echo ⚠️  Dependencias de Baileys no instaladas
    echo    Ejecuta: cd baileys-server ^&^& npm install
)

echo.
echo [7/8] Verificando Dashboard Next.js...
if exist dashboard-nextjs\package.json (
    echo ✅ Dashboard Next.js encontrado
) else (
    echo ❌ Dashboard Next.js NO encontrado
)

if exist dashboard-nextjs\node_modules (
    echo ✅ Dependencias del dashboard instaladas
) else (
    echo ⚠️  Dependencias del dashboard no instaladas
    echo    Ejecuta: cd dashboard-nextjs ^&^& npm install
)

echo.
echo [8/8] Probando conexion a base de datos...
python -c "from database.connection import SessionLocal; db = SessionLocal(); print('✅ Conexion exitosa'); db.close()" 2>nul
if errorlevel 1 (
    echo ❌ Error conectando a base de datos
    echo    Verifica DATABASE_URL en .env
) else (
    echo ✅ Base de datos conectada
)

echo.
echo ========================================
echo   RESUMEN DE VERIFICACION
echo ========================================
echo.

python -c "import sys; from database.connection import SessionLocal; from config.settings import settings; errors = []; errors.append('Python') if sys.version_info < (3, 8) else None; errors.append('Mercado Pago') if not settings.MERCADOPAGO_ACCESS_TOKEN else None; errors.append('PayPal') if not settings.PAYPAL_CLIENT_ID else None; errors.append('Base de datos') if not settings.DATABASE_URL else None; print('✅ TODO LISTO PARA INICIAR' if not errors else f'⚠️  Faltan configurar: {chr(44).join(errors)}')" 2>nul

echo.
echo Documentacion disponible:
echo   - INTEGRACION_PAGOS_FOTOS.md (Completa)
echo   - GUIA_RAPIDA_PAGOS.md (Rapida)
echo   - CONFIGURAR_WEBHOOKS.md (Webhooks)
echo   - RESUMEN_INTEGRACION.md (Resumen)
echo.

echo Para iniciar el sistema:
echo   1. START_WITH_PAYMENTS.bat (Completo)
echo   2. START_ALL.bat (Basico)
echo.

echo Para probar la integracion:
echo   python test_payment_integration.py
echo.

pause
