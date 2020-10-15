@echo off

if %1. == . goto error

set SDKPATH=C:\Program Files\Google\google_appengine
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%
set PYTHONPATH=Z:\python projects\@lib;%SDKPATH%\lib;z:\python25\lib;

python "%SDKPATH%\dev_appserver.py" --address=127.0.0.1 --port=8888 --smtp_host=SQL2005 --smtp_port=25 "%cd%\%1"
goto done

:error
echo Nothing to do !

:done

