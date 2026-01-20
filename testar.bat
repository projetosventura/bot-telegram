@echo off
echo ========================================
echo Bot VIP Telegram - Teste
echo ========================================
echo.

if not exist .env (
    echo ERRO: Arquivo .env nao encontrado!
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Testando configuracoes...
echo.
python utils.py test

pause
