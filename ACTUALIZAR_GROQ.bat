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
git add FIX_GROQ_ERROR.md
git add ACTUALIZAR_GROQ.bat

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
