@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python27\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;
REM if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;J:\pyinstaller-2.0\PyInstaller;
if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python27\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;

if 0%1. == 0. goto help

if exist stdout*.txt del stdout*.txt

REM if %1. == 1. c:\python27\python2.7 -O setup_svnHotBackups.py py2exe
if %1. == 1. c:\python27\python2.7 -O setup_svnHotBackups.py py2exe --packages=Crypto,paramiko
if %1. == 2. c:\python27\python2.7 -O setup_sftp.py py2exe --packages=Crypto,paramiko
if %1. == 3. c:\python27\python2.7 -O setup_remove-oldest-files.py py2exe --packages=Crypto,paramiko
REM if %1. == 4. c:\python27\python2.7 "J:\pyinstaller-2.0\pyinstaller.py" boto-test.py --onefile -c
REM if %1. == 5. c:\python27\python2.7 "J:\pyinstaller-2.0\utils\Makespec.py" boto-test.py --onefile -c

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means setup_svnHotBackups.py
echo "2" means setup_sftp.py
echo "3" means setup_remove-oldest-files.py
REM echo "4" means pyinstaller.py boto-test.py
REM echo "5" means Makespec.py boto-test.py
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

