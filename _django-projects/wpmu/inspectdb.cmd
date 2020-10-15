@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django-projects;Z:\python projects\_django_1_1;
cls
python manage.py inspectdb --settings=settings
