@echo off
echo ========================================
echo   INICIANDO DASHBOARD NEXT.JS
echo ========================================
echo.

cd dashboard-nextjs

echo [1/2] Verificando dependencias...
if not exist "node_modules" (
    echo Instalando dependencias de Node.js...
    call npm install
)

echo.
echo [2/2] Iniciando servidor Next.js...
echo Dashboard disponible en: http://localhost:3001
echo.

call npm run dev

pause
