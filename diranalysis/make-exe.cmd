@echo off

cls
echo BEGIN:

if exist "Z:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" set PYTHONPATH=c:\python27\lib;Z:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;
if exist "F:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" set PYTHONPATH=c:\python27\lib;F:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;
if exist "J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;
if exist "C:\@python-projects\trunk\@lib\12-13-2011-01" set PYTHONPATH=c:\python27\lib;C:\@python-projects\trunk\@lib\12-13-2011-01;

if 0%1. == 0. goto help

if exist stdout*.txt del stdout*.txt

if %1. == 1. c:\python27\python2.7 -O setup.py py2exe > make-exe.log 2>&1

if %1. == help. c:\python27\python2.7 -O setup.py --help py2exe

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means setup.py
echo "help" means --help py2exe
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!
