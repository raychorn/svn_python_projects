@echo off

SET PATH=c:\python25;%PATH%
SET PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -OO compileall.py
python -OO pyMonit.py --port=8080 --logging=logging.WARNING --retention=9000 %1 %2 %3 %4 %5 %6 %7 %8 %9
