@echo off
echo ========================================
echo LIMPIANDO SESION DE WHATSAPP
echo ========================================
echo.

echo Deteniendo servidor Baileys...
taskkill /F /IM node.exe 2>nul

echo.
echo Eliminando carpeta auth_info...
cd baileys-server
rmdir /S /Q auth_info 2>nul

echo.
echo Limpieza completada!
echo.
echo Ahora puedes iniciar de nuevo:
echo 1. Ejecuta START_ALL.bat
echo 2. Ve al dashboard
echo 3. Click en WhatsApp
echo 4. Click en "Conectar WhatsApp"
echo 5. Escanea el QR
echo.
pause
