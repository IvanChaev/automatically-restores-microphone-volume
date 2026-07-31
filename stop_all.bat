@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"

set "PIDFILE=%~dp0logs\pid.pid"
set "LOGFILE=%~dp0logs\watchdog.log"

title Stop: norm gromkost micro

echo.
echo  ============================================
echo  Остановка: watchdog + скрипт микрофона
echo  ============================================
echo.

REM --- 1. Остановить watchdog (cmd с нашим watchdog.bat) ---
wmic process where "name='cmd.exe' and commandline like '%%watchdog.bat%%' and not commandline like '%%my_voice_project%%'" call terminate >nul 2>nul
echo  [OK] Watchdog остановлен

REM --- 2. Остановить скрипт микрофона по pid-файлу ---
set "PID="
if not exist "!PIDFILE!" goto :cleanup
for /f "usebackq delims=" %%i in ("!PIDFILE!") do set "PID=%%i"
if not defined PID goto :cleanup
taskkill /PID !PID! /F >nul 2>nul
if errorlevel 1 goto :pid_dead
echo  [OK] Скрипт микрофона (pid !PID!) остановлен
goto :cleanup

:pid_dead
echo  [ИНФО] Процесс !PID! уже не работает

REM --- 3. Страховка: pythonw с нашим main.py ---
:cleanup
wmic process where "name='pythonw.exe' and commandline like '%%norm gromkost micro%%' and commandline like '%%main.py%%'" call terminate >nul 2>nul

REM --- 4. Очистить pid-файл ---
if exist "!PIDFILE!" del "!PIDFILE!" 2>nul

set "LOGMSG=[%date% %time%] СТОП: программа и watchdog остановлены пользователем"
powershell -NoProfile -Command "Add-Content -LiteralPath $env:LOGFILE -Encoding UTF8 -Value $env:LOGMSG"

echo.
echo  Готово. Для запуска: двойной клик watchdog.bat
echo.
pause
