@echo off
chcp 65001 >nul
echo ========================================
echo   SUBIR CÓDIGO A GITHUB
echo ========================================
echo.
echo Repositorio: https://github.com/daveymena/bot-whatsapp-pytho.git
echo.

echo [1/6] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git no está instalado
    echo    Descarga Git desde: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git instalado

echo.
echo [2/6] Inicializando repositorio (si no existe)...
if not exist ".git" (
    git init
    echo ✅ Repositorio inicializado
) else (
    echo ✅ Repositorio ya existe
)

echo.
echo [3/6] Configurando remote...
git remote remove origin 2>nul
git remote add origin https://github.com/daveymena/bot-whatsapp-pytho.git
echo ✅ Remote configurado

echo.
echo [4/6] Verificando archivos sensibles...
if exist ".env" (
    echo ⚠️  ADVERTENCIA: Archivo .env encontrado
    echo    Verificando que esté en .gitignore...
    findstr /C:".env" .gitignore >nul
    if errorlevel 1 (
        echo ❌ ERROR: .env NO está en .gitignore
        echo    Agregando .env a .gitignore...
        echo .env >> .gitignore
    )
    echo ✅ .env está protegido (no se subirá)
)

if exist "data\" (
    echo ⚠️  Carpeta data/ encontrada
    findstr /C:"data/" .gitignore >nul
    if errorlevel 1 (
        echo    Agregando data/ a .gitignore...
        echo data/ >> .gitignore
    )
    echo ✅ data/ está protegido (no se subirá)
)

echo.
echo [5/6] Agregando archivos...
git add .
echo ✅ Archivos agregados (excluyendo .env y data/)

echo.
echo [6/6] Creando commit...
git commit -m "feat: Sistema completo de ventas con IA - Deployment ready"
if errorlevel 1 (
    echo ⚠️  No hay cambios para commitear o ya existe el commit
) else (
    echo ✅ Commit creado
)

echo.
echo [7/7] Subiendo a GitHub...
echo.
echo ⚠️  IMPORTANTE: Necesitarás autenticarte con GitHub
echo    Si es la primera vez, usa tu token personal (no la contraseña)
echo.
echo    Cómo obtener token:
echo    1. Ve a: https://github.com/settings/tokens
echo    2. Generate new token (classic)
echo    3. Selecciona: repo (todos los permisos)
echo    4. Copia el token
echo    5. Úsalo como contraseña cuando Git lo pida
echo.
pause

git branch -M main
git push -u origin main --force

if errorlevel 1 (
    echo.
    echo ❌ Error al subir a GitHub
    echo.
    echo Posibles causas:
    echo 1. No tienes permisos en el repositorio
    echo 2. Token de autenticación inválido
    echo 3. Problemas de conexión
    echo.
    echo Solución:
    echo 1. Verifica que tengas acceso al repo
    echo 2. Usa un token personal en lugar de contraseña
    echo 3. Intenta de nuevo
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ CÓDIGO SUBIDO EXITOSAMENTE
echo ========================================
echo.
echo Repositorio: https://github.com/daveymena/bot-whatsapp-pytho
echo.
echo PRÓXIMOS PASOS:
echo.
echo 1. Verifica el código en GitHub:
echo    https://github.com/daveymena/bot-whatsapp-pytho
echo.
echo 2. Configura Easypanel:
echo    - Abre DEPLOYMENT_EASYPANEL.md
echo    - Sigue los pasos desde "PASO 2: CONFIGURAR EASYPANEL"
echo.
echo 3. Variables de entorno:
echo    - Prepara tu archivo .env.production
echo    - Configúralas en Easypanel
echo.
pause
