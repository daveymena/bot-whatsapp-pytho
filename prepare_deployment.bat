@echo off
chcp 65001 >nul
echo ========================================
echo   PREPARAR DEPLOYMENT A EASYPANEL
echo ========================================
echo.

echo [1/5] Verificando archivos necesarios...
if not exist "Dockerfile" (
    echo ❌ Falta Dockerfile
    pause
    exit /b 1
)
if not exist "Dockerfile.baileys" (
    echo ❌ Falta Dockerfile.baileys
    pause
    exit /b 1
)
if not exist "docker-compose.prod.yml" (
    echo ❌ Falta docker-compose.prod.yml
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo ❌ Falta requirements.txt
    pause
    exit /b 1
)
if not exist "package.json" (
    echo ❌ Falta package.json
    pause
    exit /b 1
)
echo ✅ Todos los archivos necesarios están presentes

echo.
echo [2/5] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado
    echo    Descarga Git desde: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git instalado

echo.
echo [3/5] Verificando repositorio Git...
if not exist ".git" (
    echo ⚠️  Repositorio Git no inicializado
    echo    Inicializando...
    git init
    echo ✅ Repositorio Git inicializado
) else (
    echo ✅ Repositorio Git ya existe
)

echo.
echo [4/5] Creando .gitignore si no existe...
if not exist ".gitignore" (
    echo # Python > .gitignore
    echo __pycache__/ >> .gitignore
    echo *.py[cod] >> .gitignore
    echo .env >> .gitignore
    echo .env.local >> .gitignore
    echo .env.production >> .gitignore
    echo venv/ >> .gitignore
    echo # Node >> .gitignore
    echo node_modules/ >> .gitignore
    echo # Data >> .gitignore
    echo data/ >> .gitignore
    echo temp-media/ >> .gitignore
    echo temp-images/ >> .gitignore
    echo *.log >> .gitignore
    echo ✅ .gitignore creado
) else (
    echo ✅ .gitignore ya existe
)

echo.
echo [5/5] Verificando archivos sensibles...
if exist ".env" (
    echo ⚠️  ADVERTENCIA: Archivo .env encontrado
    echo    Asegúrate de que .env esté en .gitignore
    echo    NO subas este archivo a Git
)

echo.
echo ========================================
echo   PREPARACIÓN COMPLETADA
echo ========================================
echo.
echo ✅ El proyecto está listo para deployment
echo.
echo PRÓXIMOS PASOS:
echo.
echo 1. Crear repositorio en GitHub:
echo    https://github.com/new
echo.
echo 2. Subir código:
echo    git add .
echo    git commit -m "feat: Sistema completo de ventas"
echo    git remote add origin https://github.com/TU-USUARIO/bot-whatsapp-ventas.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Seguir la guía:
echo    DEPLOYMENT_EASYPANEL.md
echo.
pause
