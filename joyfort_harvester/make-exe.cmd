@echo off
set PYTHONPATH=C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25;C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25\Lib;C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25\Lib\site-packages;c:\@DriveD\python-projects\@lib\12-13-2011-01

if exist build rmdir /S /Q build 

if exist dist rmdir /S /Q dist 

REM c:\python25\python2.5

c:\python25\python2.5 -O ".\setup.py" py2exe >./setup.log 2>&1


