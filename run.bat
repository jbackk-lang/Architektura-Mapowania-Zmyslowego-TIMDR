@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ===============================================
echo   PC_TIMDR Sensory Engine API - uruchamianie
echo ===============================================
echo.

REM --- 0. Czy komenda "python" w ogole istnieje w PATH? ---
where python >nul 2>nul
if errorlevel 1 (
    echo BLAD: nie znaleziono komendy "python" w PATH.
    echo Zainstaluj Pythona z https://www.python.org/downloads/
    echo i podczas instalacji zaznacz "Add python.exe to PATH".
    goto END
)

python --version
echo.

REM --- 1. Utworz venv, jesli nie istnieje LUB jest niekompletny ---
if not exist venv\Scripts\activate.bat (
    echo [1/3] Tworze srodowisko wirtualne...
    python -m venv venv

    if not exist venv\Scripts\activate.bat (
        echo.
        echo BLAD: tworzenie venv nie powiodlo sie ^(brak pliku venv\Scripts\activate.bat^).
        echo.
        echo Najczestsza przyczyna na Windows 10/11: komenda "python" wskazuje na
        echo alias Microsoft Store zamiast prawdziwej instalacji Pythona ^(wyglada
        echo na dzialajaca, ale nic realnie nie robi^). Sprawdz:
        echo   Ustawienia - Aplikacje - Zaawansowane opcje aplikacji
        echo   - Aliasy wykonywania aplikacji - wylacz alias dla "python.exe" i "python3.exe"
        echo a nastepnie zainstaluj Pythona z https://www.python.org/downloads/
        goto END
    )
) else (
    echo [1/3] Srodowisko wirtualne juz istnieje, pomijam tworzenie.
)

call venv\Scripts\activate.bat
if not defined VIRTUAL_ENV (
    echo BLAD: aktywacja venv nie powiodla sie ^(call venv\Scripts\activate.bat^).
    goto END
)

REM --- 2. Zaleznosci (BEZ --quiet, zeby bledy byly widoczne) ---
echo [2/3] Instaluje zaleznosci z requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo BLAD: instalacja zaleznosci nie powiodla sie - patrz komunikaty pip powyzej.
    goto END
)

REM --- 3. Start API ---
echo.
echo [3/3] Uruchamiam PC_TIMDR Sensory Engine API...
echo.
echo    http://127.0.0.1:5000
echo.
echo Nacisnij Ctrl+C w tym oknie, zeby zatrzymac serwer.
echo.

python api.py

if errorlevel 1 (
    echo.
    echo BLAD: api.py zakonczyl sie bledem - patrz komunikaty powyzej.
)

:END
echo.
echo ===============================================
echo Nacisnij dowolny klawisz, zeby zamknac to okno...
pause >nul