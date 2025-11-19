@echo off
title Detener Todos los Servidores
color 0C

echo ========================================
echo   DETENIENDO TODOS LOS SERVIDORES
echo ========================================
echo.

echo Matando todos los procesos de Node.js...
taskkill /F /IM node.exe 2>nul
if %errorlevel% equ 0 (
    echo [OK] Procesos de Node.js detenidos
) else (
    echo [INFO] No habia procesos de Node.js corriendo
)

echo.
echo Matando todos los procesos de Python...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo [OK] Procesos de Python detenidos
) else (
    echo [INFO] No habia procesos de Python corriendo
)

echo.
echo Esperando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   TODOS LOS SERVIDORES DETENIDOS
echo ========================================
echo.
echo Ahora puedes iniciar los servidores correctamente:
echo.
echo 1. INICIAR_PYTHON.bat
echo 2. INICIAR_BAILEYS.bat  (usa node, NO nodemon)
echo 3. Dashboard ya deberia estar en otra terminal
echo.
pause
