@echo off
chcp 65001 >nul
echo ========================================
echo   INSTALACIÓN SISTEMA SAAS COMPLETO
echo ========================================
echo.

echo [1/3] Instalando dependencias Python...
pip install openai gtts SpeechRecognition pytesseract pillow

echo.
echo [2/3] Ejecutando migración de base de datos...
python recreate_subscription_tables.py

echo.
echo [3/3] Verificando instalación...
echo.
echo ✅ INSTALACIÓN COMPLETADA
echo.
echo ========================================
echo   CONFIGURACIÓN REQUERIDA
echo ========================================
echo.
echo 1. Instala Tesseract OCR:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo    Después de instalar, agrega Tesseract al PATH del sistema
echo    Ubicación típica: C:\Program Files\Tesseract-OCR
echo.
echo 2. Configura tu archivo .env:
echo    - OPENAI_API_KEY=tu_key_aqui
echo    - SMTP_USER=tu_email@gmail.com
echo    - SMTP_PASSWORD=tu_app_password
echo    - TTS_ENABLED=true
echo    - VISION_AI_ENABLED=true
echo    - OCR_ENABLED=true
echo.
echo 3. Inicia el sistema:
echo    START_SYSTEM.bat
echo.
pause
