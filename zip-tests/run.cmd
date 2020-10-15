@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;

python -m cProfile -s cumulative zip-tests.py > report-zip-tests.txt

:exit
