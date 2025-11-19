@echo off
title Servidor Baileys - Puerto 3002
color 0A

echo ========================================
echo   INICIANDO SERVIDOR BAILEYS
echo ========================================
echo.
echo Puerto: 3002
echo IMPORTANTE: NO uses nodemon, usa node directamente
echo.

cd baileys-server
node server.js

pause
