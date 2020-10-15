@echo off

cls

dist\edgeworld_harvester.exe --verbose --secs1=30 --secs2=600 --x1=0 --y1=0 --x2=0 --y2=20

REM ('--y2=?', 'yOffset2 (can be positive or negative).')
REM ('--x1=?', 'xOffset1 (can be positive or negative).')
REM ('--y1=?', 'yOffset1 (can be positive or negative).')
REM ('--x2=?', 'xOffset2 (can be positive or negative).')

REM set PYTHONPATH=C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25;C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25\Lib;C:\@DriveD\Python2557(Stackless)-09-02-2010\Python25\Lib\site-packages;C:\@DriveD\python\@lib;

REM c:\python25\python2.5 edgeworld_harvester.py --verbose --secs1=10 --secs2=15 --x1=0 --y1=0 --x2=0 --y2=20
