@echo off
set PYTHONPATH=J:\Python2557(Stackless)-09-02-2010\Python25;J:\@Vyper Logix Corp\@Projects\python\@lib;

if exist build rmdir /S /Q build 

if exist dist rmdir /S /Q dist 

"J:\Python2557(Stackless)-09-02-2010\Python25\python25" -O ".\setup.py" py2exe
