@echo off
title Sistema de Ventas - Iniciando Todos los Servicios
color 0A

echo ========================================
echo   SISTEMA DE VENTAS CON WHATSAPP
echo ========================================
echo.
echo Iniciando todos los servicios...
echo.

REM Verificar que Node.js esta instalado
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado
    echo Por favor instala Node.js desde https://nodejs.org
    pause
    exit /b 1
)

REM Verificar que Python esta instalado
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo [1/3] Iniciando servidor Python (Puerto 5000)...
start "Python API Server" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando servidor Baileys (Puerto 3002)...
start "Baileys WhatsApp Server" cmd /k "cd baileys-server && node server.js"
timeout /t 3 /nobreak >nul

echo [3/3] Iniciando Dashboard Next.js (Puerto 3001)...
start "Next.js Dashboard" cmd /k "cd dashboard-nextjs && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   TODOS LOS SERVICIOS INICIADOS
echo ========================================
echo.
echo Servicios corriendo:
echo   - Python API:     http://localhost:5000
echo   - Baileys Server: http://localhost:3002
echo   - Dashboard:      http://localhost:3001
echo.
echo Abre tu navegador en: http://localhost:3001
echo.
echo Presiona cualquier tecla para verificar el estado...
pause >nul

REM Verificar servidores
call CHECK_SERVERS.bat
