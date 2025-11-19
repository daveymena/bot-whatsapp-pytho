@echo off
echo ========================================
echo INSTALANDO LIBRERIA DE QR CODE
echo ========================================
echo.

cd dashboard-nextjs

echo Instalando qrcode.react...
call npm install qrcode.react

echo.
echo ========================================
echo INSTALACION COMPLETADA
echo ========================================
echo.
echo Ahora reinicia el servidor del dashboard:
echo 1. Presiona Ctrl+C en la terminal del dashboard
echo 2. Ejecuta: npm run dev
echo.
pause
