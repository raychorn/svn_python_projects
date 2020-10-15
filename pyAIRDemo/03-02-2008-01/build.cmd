call reset-build.cmd

if exist server.spec python -O C:\Python25\Lib\site-packages\pyinstaller13\Build.py server.spec
