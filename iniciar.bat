@echo off
echo ========================================
echo Bot VIP Telegram - Iniciando...
echo ========================================
echo.

if not exist .env (
    echo ERRO: Arquivo .env nao encontrado!
    echo.
    echo Copie o arquivo env.example para .env e configure suas credenciais.
    echo Exemplo: copy env.example .env
    echo.
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Iniciando bot...
echo.
python bot.py

pause
