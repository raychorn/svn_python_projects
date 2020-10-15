@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib

for /f %%i in ('cd') do set cwd=%%i

REM if exist %cwd%\build rmdir /S /Q %cwd%\build
REM if exist %cwd%\dist rmdir /S /Q %cwd%\dist

python setup.py py2exe > report-py2exe.txt