@echo off
setlocal

REM PC_TIMDR Sensory Engine API -- uruchomienie na Windows
REM Tworzy (jesli trzeba) lokalne srodowisko wirtualne, instaluje
REM zaleznosci z requirements.txt i uruchamia lokalny serwer API
REM na http://127.0.0.1:5000

cd /d "%~dp0"

if not exist venv (
    echo [1/3] Tworze srodowisko wirtualne (venv)...
    python -m venv venv
    if errorlevel 1 (
        echo BLAD: nie udalo sie utworzyc srodowiska wirtualnego. Sprawdz, czy Python jest zainstalowany i dostepny w PATH.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Srodowisko wirtualne juz istnieje, pomijam tworzenie.
)

call venv\Scripts\activate.bat

echo [2/3] Instaluje zaleznosci z requirements.txt...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo BLAD: instalacja zaleznosci nie powiodla sie.
    pause
    exit /b 1
)

echo [3/3] Uruchamiam PC_TIMDR Sensory Engine API...
echo.
echo    http://127.0.0.1:5000
echo.
echo Nacisnij Ctrl+C w tym oknie, zeby zatrzymac serwer.
echo.

python api.py

pause
