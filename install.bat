@echo off
echo ========================================
echo Bot VIP Telegram - Instalacao
echo ========================================
echo.

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/4] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ERRO ao criar ambiente virtual!
    pause
    exit /b 1
)

echo.
echo [3/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [4/4] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacao concluida com sucesso!
echo ========================================
echo.
echo Proximos passos:
echo 1. Copie o arquivo env.example para .env
echo 2. Edite o arquivo .env com suas credenciais
echo 3. Execute iniciar.bat para rodar o bot
echo.
pause
