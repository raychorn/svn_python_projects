@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python27\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;
if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;

if exist stdout*.txt del stdout*.txt

c:\python27\python2.7 -O setup.py py2exe --packages=Crypto,paramiko

echo END!

