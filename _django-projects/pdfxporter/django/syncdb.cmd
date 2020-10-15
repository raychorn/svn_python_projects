@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django-projects;Z:\python projects\_django_0_96_3;
cls
python manage.py syncdb --settings=settings
