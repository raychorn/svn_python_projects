REM if exist installer.spec del installer.spec
REM ..\..\pyinstaller-1.3\Makespec.py -F -K -a -c -X --name=installer_tk installer.py
REM ..\..\pyinstaller-1.3\Makespec.py -D -a -c -X --name=server-folder ../XMLSocketServer.py

REM ..\pyinstaller-1.3\Makespec.py -F -a -c -X --name=demo theBall.py

 ..\pyinstaller-1.3\Makespec.py -D -a -c -X --name=demo theBall.py
