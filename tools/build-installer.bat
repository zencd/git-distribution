if not exist appname\work\python-3.9.1 exit /b 1
del /s "*.pyc"
del "appname.zip"
copy install.bat appname
"C:\Program Files\7-Zip\7z.exe" a "appname.zip" -mmt -mx5 appname
