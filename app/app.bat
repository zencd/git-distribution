@echo off
setlocal enableDelayedExpansion

set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%
set REPO_DIR=%APP_DIR%\repo
set PYTHON=%APP_DIR%\tools\python-3.9.1\python.exe
set MAIN_PY=%REPO_DIR%\main.py

if not exist "%MAIN_PY%" (
	call "%APP_DIR%\update.bat"
    if !errorlevel! neq 0 exit /b 1
)

set PYTHONPATH=%REPO_DIR%
"%PYTHON%" "%MAIN_PY%" %*
