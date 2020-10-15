call reset-build.cmd

if exist demo.spec python -O C:\Python25\Lib\site-packages\pyinstaller13\Build.py demo.spec
