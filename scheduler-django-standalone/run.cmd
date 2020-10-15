@echo off

set PYTHONPATH=c:\@python-projects\trunk\_Django-1.5.1;C:\@python-projects\trunk\@lib\12-13-2011-01;C:\@python-projects\trunk\_google_appengine_1.9.0\lib;

python scheduler.py -d scheduler -v -utc -t 24
