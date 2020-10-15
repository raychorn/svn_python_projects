@echo off

set SDKPATH=Z:\python projects\_google_appengine_1_1_1\google_appengine
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%

set PYTHONPATH=%SDKPATH%\lib;c:\python25\lib;Z:\python projects\@lib;

python "%SDKPATH%\dev_appserver.py" --address=127.0.0.1 --port=8888 --smtp_host=SQL2005 --smtp_port=25 "J:\@Vyper Logix Corp\@Projects\python-projects\_google_app_engine-projects\vypercms2-globalNav_11"

REM --address=127.0.0.1 --port=8888 "J:\@Vyper Logix Corp\@Projects\python-projects\_google_app_engine-projects\vypercms2-globalNav_11"

REM ==================================================================================

REM --email=raychorn@gmail.com update "J:\@Vyper Logix Corp\@Projects\python-projects\_google_app_engine-projects\gae-django-cms\cargochief"

