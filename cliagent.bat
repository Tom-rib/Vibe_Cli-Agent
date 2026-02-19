@echo off
REM Script batch pour lancer l'Agent IA CLI en mode interactif
REM Permet de taper simplement "copilot" depuis le terminal

setlocal enabledelayedexpansion

REM Déterminer le répertoire du script
set SCRIPT_DIR=%~dp0

REM Chercher et activer venv Python
set VENV_PATH=%SCRIPT_DIR%venv\Scripts\activate.bat

if exist "!VENV_PATH!" (
    call "!VENV_PATH!"
) else (
    echo.
    echo ❌ Erreur: virtualenv non trouvé
    echo   Veuillez exécuter: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Vérifier .env
if not exist "%SCRIPT_DIR%.env" (
    echo.
    echo ❌ Erreur: fichier .env non trouvé
    echo   Veuillez copier .env.example vers .env et configurer votre clé API
    echo.
    pause
    exit /b 1
)

REM Lancer le CLI en mode interactif
python "%SCRIPT_DIR%cli.py" interactive %*

endlocal
