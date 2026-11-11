@echo off
setlocal

REM Aggiorna il repository usando la cartella in cui si trova questo script.
git -C "%~dp0" fetch
if errorlevel 1 (
    echo.
    echo ERRORE: git fetch non riuscito.
    pause
    exit /b 1
)

git -C "%~dp0" pull
if errorlevel 1 (
    echo.
    echo ERRORE: git pull non riuscito.
    pause
    exit /b 1
)

echo.
echo Repository aggiornato correttamente.
pause
