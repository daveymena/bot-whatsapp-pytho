@echo off
echo ========================================
echo   INICIANDO SMART SALES BOT COMPLETO
echo ========================================
echo.

echo [1/3] Iniciando Bot de Python...
start "Python Bot" cmd /k "cd /d %~dp0 && python main.py"

timeout /t 3 /nobreak > nul

echo [2/3] Iniciando Servidor Baileys...
start "Baileys Server" cmd /k "cd /d %~dp0\baileys-server && npm start"

timeout /t 3 /nobreak > nul

echo [3/3] Iniciando Dashboard Next.js...
start "Dashboard Next.js" cmd /k "cd /d %~dp0\dashboard-nextjs && npm run dev"

timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo   TODO INICIADO CORRECTAMENTE
echo ========================================
echo.
echo Dashboard Next.js: http://localhost:3001
echo API Backend:       http://localhost:5000
echo API Docs:          http://localhost:5000/docs
echo Baileys Server:    http://localhost:3002/status
echo.
echo Presiona cualquier tecla para abrir el dashboard...
pause > nul

start http://localhost:3001
