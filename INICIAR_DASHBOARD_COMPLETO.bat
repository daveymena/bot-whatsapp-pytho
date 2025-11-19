@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🚀 INICIANDO DASHBOARD COMPLETO - NEXTJS              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/3] 📦 Verificando dependencias...
cd dashboard-nextjs
if not exist "node_modules" (
    echo ⚠️  Instalando dependencias...
    call npm install
)

echo.
echo [2/3] 🔧 Configurando entorno...
if not exist ".env.local" (
    echo NEXT_PUBLIC_API_URL=http://localhost:5000 > .env.local
    echo ✅ Archivo .env.local creado
)

echo.
echo [3/3] 🌐 Iniciando servidor de desarrollo...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  Dashboard disponible en: http://localhost:3001            ║
echo ║                                                            ║
echo ║  Credenciales por defecto:                                 ║
echo ║  Usuario: admin                                            ║
echo ║  Contraseña: admin123                                      ║
echo ║                                                            ║
echo ║  Presiona Ctrl+C para detener el servidor                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

call npm run dev

pause
