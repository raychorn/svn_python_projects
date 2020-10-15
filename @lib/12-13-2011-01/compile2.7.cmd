@echo off

set PYTHONPATH=c:\python27;

if exist "C:\@python-projects\trunk\@lib\12-13-2011-01" goto doC
if exist "J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" goto doJ
if exist "T:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" goto doT

:doC
C:
cd "C:\@python-projects\trunk\@lib\12-13-2011-01"
goto skip1

:doJ
j:
cd "J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01"
goto skip1

:doT
t:
cd "T:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01"
goto skip1

:skip1
if exist compile-all.pyc del compile-all.pyc
if exist compile-all.pyo del compile-all.pyo

if exist compile2.7.log del compile2.7.log

c:\python27\python2.7.exe -OO compile-all.py vyperlogix > compile2.7.log 2>&1

if .%1 == .END goto CLOSEIT

goto SKIPCLOSE

:CLOSEIT
exit

:SKIPCLOSE
