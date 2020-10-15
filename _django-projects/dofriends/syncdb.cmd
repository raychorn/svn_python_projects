@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django-projects;Z:\python projects\_django_1_1_1;
cls
c:\python25\python25 manage.py syncdb --settings=settings
