@echo off
set DJANGO_SETTINGS_MODULE=settings
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django-projects;z:\python projects\_django_1_1_1;
cls
python manage.py syncdb --settings=settings