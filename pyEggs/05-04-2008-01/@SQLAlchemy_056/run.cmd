@echo off

set MYPATH=C:\_@3_

mkdir %MYPATH% 2>NUL:

if exist %MYPATH% rmdir /S /Q %MYPATH%

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

if exist ..\dist\pyEggs.exe ..\dist\pyEggs --egg --verbose --libroot="Z:\python projects\@SQLAlchemy-0_5_6\lib" --nosource --libdest=%MYPATH% --ignore="[%libroot%\SQLAlchemy.egg-info]"
