@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\@lib-magma;

del build /F /S /Q >NUL
rmdir build /S /Q

del dist /F /S /Q >NUL
rmdir dist /S /Q

c:\python25\python25 -O "Z:\python projects\boost-process\setup.py" py2exe
