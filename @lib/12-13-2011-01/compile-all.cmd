@echo off

if exist "C:\@python-projects\trunk\@lib\12-13-2011-01" goto doC
if exist "J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" goto doJ
if exist "T:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01" goto doT

:doC
C:
cd "C:\@python-projects\trunk\@lib\12-13-2011-01"
START "compile2.5" /I /HIGH /MIN /WAIT "C:\@python-projects\trunk\@lib\compile2.5.cmd"
START "compile2.7" /I /HIGH /MIN /WAIT "C:\@python-projects\trunk\@lib\compile2.7.cmd"
goto skip1

:doJ
j:
cd "J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01"
START "compile2.5" /I /HIGH /MIN /WAIT "J:\@Vyper Logix Corp\@Projects\python\@lib\compile2.5.cmd"
START "compile2.7" /I /HIGH /MIN /WAIT "J:\@Vyper Logix Corp\@Projects\python\@lib\compile2.7.cmd"
goto skip1

:doT
t:
cd "T:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01"
START "compile2.5" /I /HIGH /MIN /WAIT "T:\@Vyper Logix Corp\@Projects\python\@lib\compile2.5.cmd"
START "compile2.7" /I /HIGH /MIN /WAIT "T:\@Vyper Logix Corp\@Projects\python\@lib\compile2.7.cmd"
goto skip1

:skip1
