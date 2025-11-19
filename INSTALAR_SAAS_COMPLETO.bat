@echo off
echo ========================================
echo INSTALACION COMPLETA - BOT WHATSAPP SAAS
echo ========================================
echo.

echo [1/5] Instalando dependencias de Python...
pip install openai gtts pytesseract pillow
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)
echo ✓ Dependencias de Python instaladas
echo.

echo [2/5] Verificando Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠ Tesseract OCR no está instalado
    echo.
    echo Por favor instala Tesseract OCR desde:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Después de instalar, agrega Tesseract al PATH del sistema
    echo Ubicación típica: C:\Program Files\Tesseract-OCR
    echo.
    pause
) else (
    echo ✓ Tesseract OCR encontrado
)
echo.

echo [3/5] Ejecutando migración de base de datos...
python migrate_saas_complete.py
if %errorlevel% neq 0 (
    echo ERROR: La migración de base de datos falló
    pause
    exit /b 1
)
echo ✓ Base de datos migrada correctamente
echo.

echo [4/5] Verificando configuración .env...
if not exist .env (
    echo ⚠ Archivo .env no encontrado
    echo Copiando .env.example a .env...
    copy .env.example .env
    echo.
    echo ⚠ IMPORTANTE: Edita el archivo .env y configura:
    echo   - OPENAI_API_KEY
    echo   - SMTP_USER y SMTP_PASSWORD
    echo   - Otras configuraciones necesarias
    echo.
    pause
) else (
    echo ✓ Archivo .env encontrado
)
echo.

echo [5/5] Instalando dependencias de Node.js...
cd baileys-server
call npm install
cd ..
echo ✓ Dependencias de Node.js instaladas
echo.

echo ========================================
echo ✓ INSTALACION COMPLETADA
echo ========================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Edita el archivo .env y configura:
echo    - OPENAI_API_KEY (para audio e imágenes)
echo    - SMTP_USER y SMTP_PASSWORD (para emails)
echo    - Otras configuraciones según necesites
echo.
echo 2. Si no instalaste Tesseract OCR, descárgalo de:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 3. Inicia el sistema con:
echo    START_SYSTEM.bat
echo.
echo 4. Accede al dashboard en:
echo    http://localhost:3000
echo.
echo ========================================
pause
