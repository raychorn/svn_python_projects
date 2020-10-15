@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python27\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;
REM if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;J:\pyinstaller-2.0\PyInstaller;
if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;

if 0%1. == 0. goto help

if exist stdout*.txt del stdout*.txt

if %1. == 1. c:\python27\python2.7 -O setup.py py2exe --packages=Crypto,paramiko

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means setup.py
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

