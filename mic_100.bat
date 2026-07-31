@echo off
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%~dp0main.py"
) else (
    echo [ОШИБКА] pythonw.exe не найден в PATH. Установите Python или добавьте его в PATH.
    pause
    exit /b 1
)
