@echo off
set PYTHONPATH=C:\Python27;J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;J:\@Vyper Logix Corp\@Projects\python-projects\_Django-1.3_Multi-Threaded;J:\@Vyper Logix Corp\@Projects\python-projects\_django-projects\cargochief;
"C:\Python27\python2.7.exe" manage2.py runserver --settings=settings 127.0.0.1:9999

REM START /HIGH /SEPARATE "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py runserver --settings=settings 127.0.0.1:9999

REM "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py syncdb
REM "j:\Python2557(Stackless)-09-02-2010\Python25\python25.exe" manage.py runserver --settings=settings --noreload 127.0.0.1:9999
