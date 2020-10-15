@echo off

set PYTHONPATH=C:\Python27\Lib\site-packages;C:\#python-projects\python\@lib\12-13-2011-01;

if not exist "%~dp0deploy.py" goto error1

"C:\Python27\python.exe" "%~dp0deploy.py"
goto exit

:error1
echo deploy.py is missing...

:exit

