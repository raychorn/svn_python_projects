@echo on

set SDKPATH=C:\Program Files\Google\google_appengine
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%
set PYTHONPATH=%SDKPATH%\lib;%PYTHONPATH%;Z:\python projects\PDFexporter\_google_app_engine-projects\pdfxporter;
REM set DJANGO_SETTINGS_MODULE=settings
if %1. == django-admin.py. python "%DJANGOPATH%\%1" %2 %3 %4 %5 %6 %7 %8 %9
if %1. == manage.py. python %1 %2 %3 %4 %5 %6 %7 %8 %9
