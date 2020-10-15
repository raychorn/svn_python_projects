@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;
cls
if 0%1. == 0. goto help
python "Z:\python projects\_django-projects\resources\django\djangocerise\webserver.py" --conf myprojectconf --host 127.0.0.1:%1

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo Usage: run.cmd 8000
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

