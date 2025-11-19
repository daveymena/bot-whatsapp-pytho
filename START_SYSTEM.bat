@echo off
title Sistema de Ventas - Inicio Unificado
color 0A

echo.
echo ========================================
echo   SISTEMA DE VENTAS CON IA
echo   Inicio Unificado
echo ========================================
echo.
echo Iniciando todos los servicios...
echo.

REM Verificar Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado
    echo Descarga desde: https://nodejs.org
    pause
    exit /b 1
)

REM Verificar Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo Descarga desde: https://python.org
    pause
    exit /b 1
)

echo [1/3] Iniciando Servidor Python (Puerto 5000)...
start "Python API Server" cmd /k "color 0B && title Python API - Puerto 5000 && python main.py"
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Servidor Baileys (Puerto 3002)...
start "Baileys WhatsApp Server" cmd /k "color 0A && title Baileys Server - Puerto 3002 && cd baileys-server && node server.js"
timeout /t 3 /nobreak >nul

echo [3/3] Iniciando Dashboard Next.js (Puerto 3001)...
start "Next.js Dashboard" cmd /k "color 0E && title Dashboard - Puerto 3001 && cd dashboard-nextjs && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   SISTEMA INICIADO CORRECTAMENTE
echo ========================================
echo.
echo Servicios corriendo:
echo   [Python]    http://localhost:5000
echo   [Baileys]   http://localhost:3002
echo   [Dashboard] http://localhost:3001
echo.
echo Abre tu navegador en: http://localhost:3001
echo.
echo Presiona cualquier tecla para verificar estado...
pause >nul

REM Verificar que los servicios esten corriendo
echo.
echo Verificando servicios...
echo.

curl -s http://localhost:5000/admin/whatsapp/status >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python API corriendo
) else (
    echo [!] Python API no responde
)

curl -s http://localhost:3002/status >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Baileys Server corriendo
) else (
    echo [!] Baileys Server no responde
)

curl -s http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Dashboard corriendo
) else (
    echo [!] Dashboard no responde
)

echo.
echo ========================================
echo   SISTEMA LISTO PARA USAR
echo ========================================
echo.
echo Proximos pasos:
echo 1. Abre http://localhost:3001 en tu navegador
echo 2. Inicia sesion en el dashboard
echo 3. Ve a la pestana WhatsApp y conecta
echo 4. Empieza a vender!
echo.
echo Para detener todo: Ejecuta STOP_SYSTEM.bat
echo.
pause
