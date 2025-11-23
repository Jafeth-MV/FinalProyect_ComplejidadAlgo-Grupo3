@echo off
chcp 65001 >nul
title RutaFix - Sistema de Optimización de Rutas
color 0A

echo ════════════════════════════════════════════════════════
echo          RUTAFIX - SISTEMA DE OPTIMIZACIÓN
echo ════════════════════════════════════════════════════════
echo.
echo Iniciando servidor...
echo.

cd /d "%~dp0Front"
start http://localhost:5000
python app.py

pause

