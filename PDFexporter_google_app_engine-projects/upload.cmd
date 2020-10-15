set SDKPATH=C:\Program Files\Google\google_appengine
set DJANGOPATH=%SDKPATH%\lib\django\django\bin
set PATH=%PATH%;%SDKPATH%;%DJANGOPATH%
set PYTHONPATH=%SDKPATH%;c:\python25\lib;Z:\python projects\PDFexporter\_google_app_engine-projects;
REM python "%DJANGOPATH%\django-admin.py" syncdb pdfxporter
python "%SDKPATH%\appcfg.py" update vyperlogix_bloog/

