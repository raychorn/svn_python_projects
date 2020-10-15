@echo off
set PYTHONPATH=c:\python25;J:\@Vyper Logix Corp\@Projects\python\@lib;

if exist build rmdir /S /Q build 

if exist dist rmdir /S /Q dist 

c:\python25\python25 -O ".\setup.py" py2exe >./setup.log 2>&1

