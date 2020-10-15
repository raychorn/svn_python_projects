@echo off

set PYTHONPATH=c:\#kbrwyle-development\utils;c:\#kbrwyle-development\#source\.backend\Python2.7.14\Lib\site-packages\pip\_vendor;c:\#kbrwyle-development\#source\.backend\Python2.7.14\Lib\site-packages;c:\#python-projects\python\_django-projects\beanstalk\vyperlogix1;c:\#python-projects\python\@lib\12-13-2011-01;

if %1. == . got error

cd vyperlogix1
"C:/#kbrwyle-development/#source\.backend\Python2.7.14\python.exe" "manage.py" startapp %1
cd ..
goto done

:error
echo Please specify an app name.

:done


