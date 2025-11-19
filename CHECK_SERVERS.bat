@echo off
echo ========================================
echo VERIFICANDO SERVIDORES
echo ========================================
echo.

echo [1/3] Verificando servidor Python (puerto 5000)...
curl -s http://localhost:5000/admin/whatsapp/status >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servidor Python esta corriendo
) else (
    echo [ERROR] Servidor Python NO esta corriendo
    echo        Ejecuta: python main.py
)
echo.

echo [2/3] Verificando servidor Baileys (puerto 3002)...
curl -s http://localhost:3002/status >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servidor Baileys esta corriendo
) else (
    echo [ERROR] Servidor Baileys NO esta corriendo
    echo        Ejecuta: cd baileys-server ^&^& node server.js
)
echo.

echo [3/3] Verificando dashboard Next.js (puerto 3001)...
curl -s http://localhost:3001 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Dashboard Next.js esta corriendo
) else (
    echo [ERROR] Dashboard Next.js NO esta corriendo
    echo        Ejecuta: cd dashboard-nextjs ^&^& npm run dev
)
echo.

echo ========================================
echo VERIFICACION COMPLETADA
echo ========================================
pause
