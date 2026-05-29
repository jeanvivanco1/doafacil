@echo off
echo ==================================================
echo       TESTANDO INSTALACAO DO PYTHON...
echo ==================================================

:: Tenta rodar o python para ver se funciona
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] O comando 'python' nao foi encontrado.
    echo Tentando comando 'py'...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERRO CRITICO] Python nao esta instalado ou nao esta no PATH.
        echo Por favor, instale o Python e marque "Add Python to PATH".
        pause
        exit
    ) else (
        set PY_CMD=py
    )
) else (
    set PY_CMD=python
)

echo [OK] Python encontrado: %PY_CMD%

echo [INFO] Instalando bibliotecas necessarias...
%PY_CMD% -m pip install flask flask-sqlalchemy flask-login pillow

echo [INFO] Iniciando o site...
start "" "http://127.0.0.1:5000"
%PY_CMD% app.py

echo.
echo ==================================================
echo Se o site nao abriu, verifique as mensagens acima.
echo ==================================================
pause
