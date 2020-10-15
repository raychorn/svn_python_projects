@echo off
set PYTHONPATH=j:\Python2557(Stackless)-09-02-2010\Python25;j:\@Vyper Logix Corp\@Projects\python\@lib;J:\@Vyper Logix Corp\@Projects\python-projects\SQLAlchemy-0.7.1\lib;j:\@Vyper Logix Corp\@Projects\python-projects\_Django-1.5.1;J:\@Vyper Logix Corp\@Projects\python-projects\_django-projects\djangocloud;
"j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage2.py runserver --noreload --settings=settings 127.0.0.1:8088

REM START /HIGH /SEPARATE "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py runserver --proxy=127.0.0.1:8080 --noreload --settings=settings 127.0.0.1:8888

REM "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py syncdb
REM "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py runserver --settings=settings --noreload 127.0.0.1:9999
