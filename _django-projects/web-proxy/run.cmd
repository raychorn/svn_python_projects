@echo off
set PYTHONPATH=c:\Python25;j:\Python2557(Stackless)-09-02-2010\Python25;j:\@Vyper Logix Corp\@Projects\python\@lib;j:\@Vyper Logix Corp\@Projects\python\SQLAlchemy-0.7.1\lib;J:\@Vyper Logix Corp\@Projects\python\Django-1.3_Multi-Threaded;j:\@Vyper Logix Corp\@Projects\python\_django-projects\smithmicro-projects\heat-maps-prototype;
 python manage.py runserver --settings=settings --noreload 127.0.0.1:9999
REM python manage.py syncdb
REM python manage.py runserver --settings=settings --noreload 127.0.0.1:9999
