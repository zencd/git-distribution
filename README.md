# Windows Installer Builder

Sources for making the app's Windows build.

- download portable Python from https://winpython.github.io/
- specifically one like `Winpython32-3.9.1.0dot.exe` ~30 MB
- extract an inner folder from there to get a tree like `.\app\tools\python-3.9.1\python.exe`
- make sure `7z` is in the PATH
- run `build.bat`
- asset `app.zip` is ready
- attach it to a release on Github