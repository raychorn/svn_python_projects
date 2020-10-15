@echo off

set MYPATH=C:\_@3_

mkdir %MYPATH% 2>NUL:

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

REM if exist ..\dist\pyEggs.exe ..\dist\pyEggs --egg --verbose --libroot="Z:\python projects\@lib" --nosource --libdest=%MYPATH% --ignore="[%libroot%\ext]"

REM if exist ..\dist\pyEggs.exe ..\dist\pyEggs --help

if exist ..\dist\pyEggs.exe ..\dist\pyEggs --egg --enc=simple --verbose --libroot="Z:\python projects\@lib" --nosource --libdest=%MYPATH% --ignore="[%libroot%\ext]"
