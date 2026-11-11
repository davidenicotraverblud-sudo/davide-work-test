@echo off
setlocal
cd /d "%~dp0"

echo Installazione dipendenze...
py -m pip install -r requirements.txt
if errorlevel 1 goto errore

echo Creazione eseguibile...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name "SST Manager" main.py
if errorlevel 1 goto errore

echo.
echo Eseguibile creato in: %~dp0dist\SST Manager.exe
pause
exit /b 0

:errore
echo.
echo ERRORE durante la preparazione dell'eseguibile.
pause
exit /b 1
