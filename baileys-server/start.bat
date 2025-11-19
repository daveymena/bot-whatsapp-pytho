@echo off
echo ========================================
echo   INICIANDO SERVIDOR BAILEYS
echo ========================================
echo.

cd /d "%~dp0"

if not exist "node_modules" (
    echo Instalando dependencias...
    call npm install
    echo.
)

echo Iniciando servidor...
call npm start
