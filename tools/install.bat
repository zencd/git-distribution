@echo off
setlocal enableDelayedExpansion

set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%
set WORK_DIR=%APP_DIR%\work
set PY_VER=python-3.9.1
set PY_EXE=%APP_DIR%\work\%PY_VER%\python.exe

if exist "repo_tmp" rmdir /S /Q "repo_tmp"
if exist ".git" rmdir /S /Q ".git"

:: install deps for the installer
"%PY_EXE%" -m pip install pygit2==1.4.0 > nul

:: copy the app into the current folder
"%PY_EXE%" -c "import pygit2; pygit2.clone_repository('https://github.com/zencd/git-distribution', 'repo_tmp', checkout_branch='installer')"
:: batch can't move hidden files so copy+delete
xcopy /K /I /E /H /Q /Y repo_tmp\* .
rmdir /S /Q repo_tmp

:: install deps for the app
"%PY_EXE%" -m pip install -r requirements.txt > nul

:: todo check exit codes