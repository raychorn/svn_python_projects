@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python25\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;

if 0%1. == 0. goto help

if %1. == 1. python -O make_AndroidAIRPackager.py py2exe --packages=Crypto,paramiko

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means make_AndroidAIRPackager.py
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

