call reset-build.cmd

if exist Googlize.spec python -O C:\Python25\Lib\site-packages\pyinstaller13\Build.py Googlize.spec
