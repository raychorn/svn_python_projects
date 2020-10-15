call reset-build.cmd

buildtime.py > buildtime.txt

call build-server.cmd

if exist installer.spec python -O C:\Python25\Lib\site-packages\pyinstaller13\Build.py installer.spec
