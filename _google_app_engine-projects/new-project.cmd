@echo off

set SDKPATH=Z:\python projects\_google_appengine_1_1_1
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%

set PYTHONPATH=%SDKPATH%\lib;c:\python25\lib;Z:\python projects\@lib;

python "%DJANGOPATH%\django-admin.py" startproject %1

