@echo on

set PYTHONPATH=c:\python25;Z:\python projects\@lib;

if not exists %2 goto err1

c:\python25\python25 C:\Python25\Lib\site-packages\wx-2.8-msw-ansi\wx\tools\img2py.py -n %1 -c %2 %3

goto exit

:err1
echo %2 does not exit.

:exit
