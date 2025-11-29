@echo off
chcp 65001 >nul
title RutaFix - Sistema de Optimización de Rutas
color 0A

echo ════════════════════════════════════════════════════════
echo          RUTAFIX v2.0 - SISTEMA DE OPTIMIZACIÓN
echo ════════════════════════════════════════════════════════
echo.
echo Iniciando servicios...
echo.

:: Start Backend in a new window
start "RutaFix Backend" cmd /k "cd Back && uvicorn infrastructure.api.main:app --reload"

:: Start Frontend in a new window
start "RutaFix Frontend" cmd /k "cd Front && npm run dev"

echo Servidores iniciados!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause
