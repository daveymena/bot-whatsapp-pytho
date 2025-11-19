@echo off
title Sistema de Ventas - Menu Principal
color 0A

:MENU
cls
echo.
echo ========================================
echo   SISTEMA DE VENTAS CON IA
echo   Menu Principal
echo ========================================
echo.
echo [1] Iniciar Sistema Completo
echo [2] Detener Sistema Completo
echo [3] Reiniciar Sistema
echo [4] Ver Estado del Sistema
echo [5] Verificar Instalacion
echo [6] Limpiar Sesion WhatsApp
echo [7] Ejecutar Pruebas
echo [8] Abrir Dashboard en Navegador
echo [9] Ver Documentacion
echo [0] Salir
echo.
echo ========================================
echo.
set /p option="Selecciona una opcion (0-9): "

if "%option%"=="1" goto START
if "%option%"=="2" goto STOP
if "%option%"=="3" goto RESTART
if "%option%"=="4" goto STATUS
if "%option%"=="5" goto VERIFY
if "%option%"=="6" goto CLEANUP
if "%option%"=="7" goto TEST
if "%option%"=="8" goto BROWSER
if "%option%"=="9" goto DOCS
if "%option%"=="0" goto EXIT

echo Opcion invalida. Presiona cualquier tecla...
pause >nul
goto MENU

:START
cls
echo Iniciando sistema...
call START_SYSTEM.bat
goto MENU

:STOP
cls
echo Deteniendo sistema...
call STOP_SYSTEM.bat
goto MENU

:RESTART
cls
echo Reiniciando sistema...
call RESTART_SYSTEM.bat
goto MENU

:STATUS
cls
call STATUS_SYSTEM.bat
goto MENU

:VERIFY
cls
echo.
echo Verificando instalacion...
echo.
call VERIFICAR_INSTALACION.bat
pause
goto MENU

:CLEANUP
cls
echo.
echo Limpiando sesion de WhatsApp...
echo.
cd baileys-server
rmdir /s /q auth_info 2>nul
echo [OK] Sesion limpiada
echo.
echo Reinicia el servidor Baileys para generar nuevo QR
pause
goto MENU

:TEST
cls
echo.
echo Ejecutando pruebas del sistema...
echo.
python test_professional_sales.py
pause
goto MENU

:BROWSER
cls
echo.
echo Abriendo dashboard en navegador...
start http://localhost:3001
echo.
echo Si el dashboard no abre, verifica que este corriendo.
timeout /t 3 /nobreak >nul
goto MENU

:DOCS
cls
echo.
echo ========================================
echo   DOCUMENTACION DISPONIBLE
echo ========================================
echo.
echo [1] SISTEMA_VENTAS_PROFESIONAL.md
echo [2] INTEGRACION_COMPLETADA_IA.md
echo [3] INICIO_COMPLETO.md
echo [4] SOLUCION_WHATSAPP.md
echo [5] README.md
echo.
echo Abre estos archivos con tu editor de texto
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Gracias por usar el Sistema de Ventas con IA
echo.
timeout /t 2 /nobreak >nul
exit
