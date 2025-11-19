@echo off
title Reiniciar Dashboard Next.js
color 0A

echo ========================================
echo   REINICIANDO DASHBOARD NEXT.JS
echo ========================================
echo.
echo IMPORTANTE: Este script reiniciara el dashboard
echo Si tienes el dashboard corriendo en otra terminal,
echo cierralo primero (Ctrl+C)
echo.
pause

echo.
echo Iniciando dashboard en puerto 3001...
echo.

cd dashboard-nextjs
start "Dashboard Next.js" cmd /k "npm run dev"

echo.
echo ========================================
echo   DASHBOARD INICIADO
echo ========================================
echo.
echo El dashboard esta corriendo en:
echo http://localhost:3001
echo.
echo Abre tu navegador y ve a la pestana WhatsApp
echo para ver el codigo QR.
echo.
pause
