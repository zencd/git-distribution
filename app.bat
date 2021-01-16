@echo off
setlocal enableDelayedExpansion

set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%
set WORK_DIR=%APP_DIR%\work
set PY_VER=python-3.9.1
set PY_EXE=%APP_DIR%\work\%PY_VER%\python.exe
set PY_URL=https://github.com/zencd/git-distribution/releases/download/python-3.9.1/python-3.9.1.exe
set PY_SFX=%APP_DIR%\work\%PY_VER%.exe
set VER_DIR=%APP_DIR%
set APP_VER_FILE=%WORK_DIR%\app-version
set VERSIONS_DIR=%WORK_DIR%\versions
set APP_VER=

if not exist "%WORK_DIR%" mkdir "%WORK_DIR%"
if not exist "%VERSIONS_DIR%" mkdir "%VERSIONS_DIR%"

if exist "%APP_VER_FILE%" set /p APP_VER=<"%APP_VER_FILE%"
if not "%APP_VER%" == "" set VER_DIR=%VERSIONS_DIR%\%APP_VER%
set MAIN_PY=%VER_DIR%\main.py
::exit 1

if not exist "%PY_EXE%" (
    echo Downloading python from %PY_URL%
    cscript //nologo "%APP_DIR%\tools\dl.vbs" "%PY_URL%" "%PY_SFX%"
    if !errorlevel! neq 0 exit /b 1
    if not exist "%PY_SFX%" exit /b 1

    echo Extracting python sfx
    "%PY_SFX%" -y "-o%WORK_DIR%"
    if !errorlevel! neq 0 exit /b 1

    del /f "%PY_SFX%"

    echo Installing python requirements
    "%PY_EXE%" -m pip install -r "%APP_DIR%\requirements.txt"
    if !errorlevel! neq 0 exit /b 1
)

if "%1" == "--update" (
    set PYTHONPATH=%APP_DIR%\tools
    :: todo use VER_DIR
    :: todo use VER_DIR
    :: todo use VER_DIR
    "%PY_EXE%" "%APP_DIR%\tools\update.py"
    ::"%PY_EXE%" "%VER_DIR%\tools\update.py"
    goto end
)

echo MAIN_PY: %MAIN_PY%
"%PY_EXE%" "%MAIN_PY%" %*

:end