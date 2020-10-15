@echo off
set PYTHONPATH=c:\python25;j:\@Vyper Logix Corp\@Projects\python\SQLAlchemy-0.7.1\lib;j:\@Vyper Logix Corp\@Projects\python\@lib;

if exist build goto del_build
goto skip_build

:del_build
del build /F /S /Q >NUL
rmdir build /S /Q

:skip_build

if exist dist goto del_dist
goto skip_dist

:del_dist
del dist /F /S /Q >NUL
rmdir dest /S /Q

:skip_dist

c:\python25\python25 -O setup.py py2exe
