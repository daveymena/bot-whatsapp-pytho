@echo off
title Migracion de Base de Datos
color 0E

echo ========================================
echo   MIGRACION DE BASE DE DATOS
echo   Sistema de Pagos y Fotos
echo ========================================
echo.

echo IMPORTANTE:
echo Esta migracion agregara las siguientes columnas:
echo.
echo PRODUCTOS:
echo   - image_url (URL de imagen principal)
echo   - images (Array de imagenes adicionales)
echo   - views (Contador de vistas)
echo.
echo ORDENES:
echo   - order_number (Numero unico de orden)
echo   - payment_proof (Comprobante de pago)
echo.
echo Se recomienda hacer un backup antes de continuar.
echo.

pause

echo.
echo Ejecutando migracion...
python migrate_database.py

echo.
echo ========================================
echo   MIGRACION COMPLETADA
echo ========================================
echo.

pause
