@echo off
set PYTHONPATH=c:\python25;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;Z:\python projects\_django-projects;
REM set PYTHONPATH=c:\python25;Z:\python projects\_django_1_02;Z:\python projects\@lib;Z:\python projects\_django-projects;
python manage.py runserver --noreload 127.0.0.1:8880
