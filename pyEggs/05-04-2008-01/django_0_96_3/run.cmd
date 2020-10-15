@echo off

set MYPATH=C:\_@3_

mkdir %MYPATH% 2>NUL:

if exist %MYPATH% rmdir /S /Q %MYPATH%

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

if exist ..\dist\pyEggs.exe ..\dist\pyEggs --egg --verbose --libroot="Z:\python projects\_django_0_96_3" --nosource --libdest=%MYPATH% --ignore="[%libroot%\docs,%libroot%\examples,%libroot%\extras,%libroot%\scripts,%libroot%\tests]"
