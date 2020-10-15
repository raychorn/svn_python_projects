@echo off

set SDKPATH=Z:\python projects\_google_appengine_1_1_7\google_appengine
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%

set PYTHONPATH=%SDKPATH%\lib;c:\python25\lib;Z:\python projects\@lib;

python "%SDKPATH%\dev_appserver.py" --address=127.0.0.1 --port=8888 --smtp_host=SQL2005 --smtp_port=25 "Z:\python projects\_google_app_engine-projects\resources"
