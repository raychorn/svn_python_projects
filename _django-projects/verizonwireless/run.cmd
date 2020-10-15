@echo off
set PYTHONPATH=Z:\Python;Z:\python projects\@lib;Z:\python projects\_django_1_02;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\_django-projects\@projects\amfsample\django;
python manage.py runserver --settings=settings --noreload 127.0.0.1:8888
