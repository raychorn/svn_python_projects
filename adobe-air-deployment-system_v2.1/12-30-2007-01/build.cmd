call reset-build.cmd

buildtime.py > buildtime.txt

call build-server.cmd

if exist installer.spec python -O ..\pyinstaller-1.3\Build.py installer.spec
