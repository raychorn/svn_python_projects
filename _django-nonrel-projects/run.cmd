@echo off

set PYTHONPATH=c:\python25;j:\Python2557(Stackless)-09-02-2010\Python25;j:\@Vyper Logix Corp\@Projects\python\@lib;j:\@Vyper Logix Corp\@Projects\python\SQLAlchemy-0.7.1\lib;j:\@Vyper Logix Corp\@Projects\python\Django-Nonrel;

python25 make-nonrel.py --verbose --threaded --target="J:\@Vyper Logix Corp\@Projects\python\_django-nonrel-projects\sample-app1" --source="J:\@Vyper Logix Corp\@Projects\python\Django-Nonrel" --option=djangoappengine --scaffold="J:\@Vyper Logix Corp\@Projects\python\_django-nonrel-projects\django-nonrel-testapp"
