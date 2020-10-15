@echo off

set DJANGO_SETTINGS_MODULE=settings

set PYTHONPATH=c:\python25;Z:\python projects\_django_0_96_2;Z:\python projects\@lib

python manage.py runserver --noreload 127.0.0.1:8888