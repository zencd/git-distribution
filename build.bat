@echo off
setlocal enableDelayedExpansion

set zip=app.zip

if not exist "app/tools/python-*" (
    echo Error: copy a portable python into the project
    exit /b 1
)

if exist "%zip%" del "%zip%"
if exist "app/repo" rmdir /S /Q "app/repo"
if exist "app/repo_" rmdir /S /Q "app/repo_"

del /s *.pyc

7z a "%zip%" app
