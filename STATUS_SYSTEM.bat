@echo off
title Sistema de Ventas - Estado del Sistema
color 0B

:CHECK
cls
echo.
echo ========================================
echo   ESTADO DEL SISTEMA
echo   %date% %time%
echo ========================================
echo.

REM Verificar Python
echo [Python API - Puerto 5000]
curl -s http://localhost:5000/admin/whatsapp/status >nul 2>&1
if %errorlevel% equ 0 (
    echo Estado: [ONLINE] Corriendo correctamente
    netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1
    if %errorlevel% equ 0 (
        echo Puerto: [OK] 5000 en uso
    )
) else (
    echo Estado: [OFFLINE] No responde
    echo Puerto: [!] 5000 no esta en uso
)

echo.
echo [Baileys Server - Puerto 3002]
curl -s http://localhost:3002/status >nul 2>&1
if %errorlevel% equ 0 (
    echo Estado: [ONLINE] Corriendo correctamente
    netstat -ano | findstr :3002 | findstr LISTENING >nul 2>&1
    if %errorlevel% equ 0 (
        echo Puerto: [OK] 3002 en uso
    )
) else (
    echo Estado: [OFFLINE] No responde
    echo Puerto: [!] 3002 no esta en uso
)

echo.
echo [Dashboard Next.js - Puerto 3001]
curl -s http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo Estado: [ONLINE] Corriendo correctamente
    netstat -ano | findstr :3001 | findstr LISTENING >nul 2>&1
    if %errorlevel% equ 0 (
        echo Puerto: [OK] 3001 en uso
    )
) else (
    echo Estado: [OFFLINE] No responde
    echo Puerto: [!] 3001 no esta en uso
)

echo.
echo ========================================
echo   ACCIONES DISPONIBLES
echo ========================================
echo.
echo [1] Actualizar estado (F5)
echo [2] Iniciar sistema (START_SYSTEM.bat)
echo [3] Detener sistema (STOP_SYSTEM.bat)
echo [4] Reiniciar sistema (RESTART_SYSTEM.bat)
echo [5] Salir
echo.
echo Presiona cualquier tecla para actualizar...
echo O cierra esta ventana para salir.
pause >nul

goto CHECK
