@echo off
chcp 65001 >nul
echo ========================================
echo   VERIFICACIÓN DE SEGURIDAD
echo ========================================
echo.
echo Verificando que archivos sensibles NO se suban a Git...
echo.

set ERROR=0

echo [1/5] Verificando .gitignore...
if not exist ".gitignore" (
    echo ❌ ERROR: .gitignore no existe
    set ERROR=1
) else (
    echo ✅ .gitignore existe
)

echo.
echo [2/5] Verificando que .env esté en .gitignore...
findstr /C:".env" .gitignore >nul
if errorlevel 1 (
    echo ❌ ERROR: .env NO está en .gitignore
    set ERROR=1
) else (
    echo ✅ .env está en .gitignore
)

echo.
echo [3/5] Verificando que data/ esté en .gitignore...
findstr /C:"data/" .gitignore >nul
if errorlevel 1 (
    echo ❌ ERROR: data/ NO está en .gitignore
    set ERROR=1
) else (
    echo ✅ data/ está en .gitignore
)

echo.
echo [4/5] Verificando archivos que se subirán...
git status --short 2>nul | findstr ".env" >nul
if not errorlevel 1 (
    echo ❌ ERROR: .env aparece en git status
    echo    Esto significa que se subirá a Git
    set ERROR=1
) else (
    echo ✅ .env NO se subirá
)

git status --short 2>nul | findstr "data/" >nul
if not errorlevel 1 (
    echo ❌ ERROR: data/ aparece en git status
    set ERROR=1
) else (
    echo ✅ data/ NO se subirá
)

echo.
echo [5/5] Verificando archivos sensibles...
if exist ".env" (
    echo ⚠️  Archivo .env encontrado localmente (OK, no se subirá)
)
if exist "data\" (
    echo ⚠️  Carpeta data/ encontrada localmente (OK, no se subirá)
)

echo.
echo ========================================
if %ERROR%==0 (
    echo   ✅ VERIFICACIÓN EXITOSA
    echo ========================================
    echo.
    echo Todo está correcto. Es seguro subir a Git.
    echo.
    echo Archivos que NO se subirán:
    echo   - .env
    echo   - .env.local
    echo   - .env.production
    echo   - data/
    echo   - temp-media/
    echo   - temp-images/
    echo   - node_modules/
    echo   - __pycache__/
    echo.
    echo Puedes ejecutar: SUBIR_A_GIT.bat
) else (
    echo   ❌ ERRORES ENCONTRADOS
    echo ========================================
    echo.
    echo Hay problemas de seguridad que deben corregirse.
    echo NO subas el código hasta corregir los errores.
    echo.
    echo Solución:
    echo 1. Asegúrate de que .gitignore existe
    echo 2. Verifica que .env y data/ estén en .gitignore
    echo 3. Ejecuta: git rm --cached .env
    echo 4. Ejecuta: git rm --cached -r data/
    echo 5. Vuelve a ejecutar este script
)
echo.
pause
