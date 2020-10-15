@echo off
cls
set PYTHONPATH=Z:\python projects\@lib;c:\python25;

REM --production ... tells the system to disable some profiling statements to maximize speed.
REM --logging ...... tells the system to do some performance logging (this may impact performance).

c:\python25\python25 server.py --logging %1 %2 %3 %4 %5 %6 %7 %8 %9

