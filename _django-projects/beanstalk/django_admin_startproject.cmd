@echo off

set PYTHONPATH=C:\#kbrwyle-development\#source\.backend\Python2.7.14\Lib\site-packages;

if %1. == . goto error

"C:/#kbrwyle-development/#source\.backend\Python2.7.14\python.exe" "C:\#kbrwyle-development\#source\.backend\Python2.7.14\Lib\site-packages\django\bin\django-admin.py" startproject %1
goto done

:error
echo You must specify a project name.

:done


