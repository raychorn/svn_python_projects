@echo on

set PYTHONPATH=c:\python25;

if exist compile-all.pyc del compile-all.pyc
if exist compile-all.pyo del compile-all.pyo

if exist "J:\@Vyper Logix Corp\@Projects\python\@lib\dist_2.5.5" rmdir /S /Q "J:\@Vyper Logix Corp\@Projects\python\@lib\dist_2.5.5"

c:\python25\python25.exe -OO compile-all.py vyperlogix > compile2.5.log 2>&1
