@echo off
setlocal enableDelayedExpansion

set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%
set PYTHON=%APP_DIR%\tools\python-3.9.1\python.exe

"%PYTHON%" -m pip install -r "%APP_DIR%\tools\requirements.txt"
if !errorlevel! neq 0 exit /b 1

"%PYTHON%" "%APP_DIR%\tools\update.py"
if !errorlevel! neq 0 exit /b 1
