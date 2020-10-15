@echo on

REM img2py.cmd logo "Z:\python projects\PDFexporter\assets\logo\3dfa\pdfexporter2b.png" logo.py
REM img2py.cmd name "name.png" name.py

set PYTHONPATH=c:\python25;

if not exist %2 goto err1

c:\python25\python25 C:\Python25\Lib\site-packages\wx-2.8-msw-ansi\wx\tools\img2py.py -n %1 -c %2 %3

goto exit

:err1
echo %2 does not exit.

:exit
