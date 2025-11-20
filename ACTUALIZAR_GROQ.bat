@echo off
echo ========================================
echo ACTUALIZACION DE GROQ - FIX ERROR
echo ========================================
echo.

echo [1/4] Verificando cambios...
git status

echo.
echo [2/4] Agregando archivos actualizados...
git add requirements.txt
git add VARIABLES_EASYPANEL.txt
git add FIX_GROQ_ERROR.md
git add SOLUCION_ERROR_GROQ_EASYPANEL.md
git add RESUMEN_FIX_GROQ.md
git add PASOS_SIMPLES_FIX_GROQ.md
git add INDEX_FIX_GROQ.md
git add START_HERE.txt
git add LEEME_PRIMERO_FIX_GROQ.txt
git add EJECUTAR_AHORA.txt
git add RESUMEN_COMPLETO_FIX.md
git add ACTUALIZAR_GROQ.bat
git add CONFIGURAR_VARIABLES_EASYPANEL.md

echo.
echo [3/4] Creando commit...
git commit -m "fix: actualizar groq a version compatible (>=0.11.0) para resolver error de proxies"

echo.
echo [4/4] Subiendo a repositorio...
git push

echo.
echo ========================================
echo COMPLETADO
echo ========================================
echo.
echo Ahora ve a Easypanel y:
echo 1. Espera a que se reconstruya automaticamente
echo 2. O fuerza un rebuild manual
echo 3. Reinicia el servicio
echo 4. Verifica los logs
echo.
echo Documentacion completa en: FIX_GROQ_ERROR.md
echo.
pause
