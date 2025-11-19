@echo off
title Sistema de Ventas - Reinicio Rapido
color 0E

echo.
echo ========================================
echo   REINICIANDO SISTEMA COMPLETO
echo ========================================
echo.

echo Paso 1: Deteniendo servicios actuales...
call STOP_SYSTEM.bat

echo.
echo Esperando 5 segundos...
timeout /t 5 /nobreak >nul

echo.
echo Paso 2: Iniciando servicios nuevamente...
call START_SYSTEM.bat
