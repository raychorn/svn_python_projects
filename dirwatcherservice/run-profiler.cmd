@echo off

echo %COMPUTERNAME%

set PYTHONPATH=j:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;j:\@Vyper Logix Corp\@Projects\python-projects\_Django-1.5.1;

python -m cProfile -s cumulative utils.py

