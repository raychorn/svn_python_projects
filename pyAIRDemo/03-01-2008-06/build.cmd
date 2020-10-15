call reset-build.cmd

if exist server.spec python -O ..\pyinstaller-1.3\Build.py server.spec
