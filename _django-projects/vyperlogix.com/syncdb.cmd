@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django-projects;Z:\python projects\_django_1_02;
cls
set DJANGO_SETTINGS_MODULE=settings
python manage.py syncdb --settings=settings
