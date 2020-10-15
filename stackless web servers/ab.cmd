@echo off

REM "C:\Apache\bin\ab" -n 20000 -c 100 -v 1 -w -k http://localhost:8000/ > ab-ThreadedWebserver.html
 "C:\Apache\bin\ab" -n 20000 -c 100 -v 1 -w -k http://localhost:8000/ > ab-Webserver.html
