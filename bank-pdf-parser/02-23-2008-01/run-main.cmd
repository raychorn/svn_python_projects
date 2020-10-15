@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;
C:\Python25\python -m cProfile -s cumulative main.py > main.txt
