@echo off
echo ========================================
echo INSTALANDO INTEGRACIONES DE PAGO
echo ========================================
echo.

echo [1/3] Instalando Mercado Pago SDK...
pip install mercadopago==2.2.1

echo.
echo [2/3] Instalando PayPal SDK...
pip install paypalrestsdk==1.13.1

echo.
echo [3/3] Verificando instalacion...
pip list | findstr "mercadopago paypalrestsdk"

echo.
echo ========================================
echo INSTALACION COMPLETADA
echo ========================================
echo.
echo Ahora configura tus credenciales en el archivo .env:
echo - MERCADOPAGO_ACCESS_TOKEN
echo - PAYPAL_CLIENT_ID
echo - PAYPAL_CLIENT_SECRET
echo.
pause
