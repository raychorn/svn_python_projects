@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python25\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;

python -O setup.py py2exe

echo END!

