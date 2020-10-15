@echo off
set PYTHONPATH=Z:\Python;Z:\python projects\@lib;Z:\python projects\_django-projects;Z:\python projects\_django_1_1;
cls
REM python "Z:\python projects\_django_1_1\django\bin\django-admin.py" syncdb --settings=settings

REM -- Pass this to manage.py ...
REM syncdb --settings=settings

REM runserver --settings=settings --noreload 127.0.0.1:8888