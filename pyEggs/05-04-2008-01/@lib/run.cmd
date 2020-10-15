@echo off

set MYPATH=C:\_@3_

if exist %MYPATH% rmdir /S /Q %MYPATH%

mkdir %MYPATH% 2>NUL:

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

if exist ..\dist\pyEggs.exe ..\dist\pyEggs --egg --verbose --libroot="Z:\python projects\@lib" --nosource --libdest=%MYPATH% --ignore="[%libroot%\ext]"
