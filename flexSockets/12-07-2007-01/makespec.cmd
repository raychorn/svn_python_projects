if exist server.spec del server.spec
..\pyinstaller-1.3\Makespec.py -F -a -c -X --name=server server.py
