@echo off
title Sistema de Ventas - Detener Todo
color 0C

echo.
echo ========================================
echo   DETENIENDO SISTEMA COMPLETO
echo ========================================
echo.

echo Cerrando todos los servicios...
echo.

echo [1/3] Deteniendo Node.js (Dashboard + Baileys)...
taskkill /F /IM node.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servicios Node.js detenidos
) else (
    echo [INFO] No habia servicios Node.js corriendo
)

echo [2/3] Deteniendo Python...
taskkill /F /IM python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servidor Python detenido
) else (
    echo [INFO] No habia servidor Python corriendo
)

echo [3/3] Limpiando puertos...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   SISTEMA DETENIDO COMPLETAMENTE
echo ========================================
echo.
echo Todos los servicios han sido cerrados.
echo.
echo Para iniciar de nuevo: Ejecuta START_SYSTEM.bat
echo.
pause
