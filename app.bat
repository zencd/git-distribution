@echo off
setlocal enableDelayedExpansion

set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%
set WORK_DIR=%APP_DIR%\work
set PY_VER=python-3.8.7
set PY_EXE=%APP_DIR%\work\%PY_VER%\python.exe
set PY_URL=https://github.com/zencd/git-distribution/releases/download/python-3.9.1/python-3.9.1.exe
set PY_SFX=%APP_DIR%\work\%PY_VER%.exe
set MAIN_PY=%APP_DIR%\main.py

if not exist "%WORK_DIR%" mkdir "%WORK_DIR%"

:: Install python if not yet
if not exist "%PY_EXE%" (
:: Update the app. Called from update.bat
if "%1" == "--update" (
    set PYTHONPATH=%APP_DIR%\tools
    set DO_HARD_RESET=1
    "%PY_EXE%" "%APP_DIR%\tools\update.py"
    if !errorlevel! neq 0 exit /b 1

    "%PY_EXE%" -m pip install -r "%APP_DIR%\requirements.txt" > nul
    if !errorlevel! neq 0 exit /b 1

    goto end
)

:: Start the app
"%PY_EXE%" "%MAIN_PY%" %*

:end