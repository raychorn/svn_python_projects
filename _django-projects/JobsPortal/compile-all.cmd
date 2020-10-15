@echo off

set PYTHONPATH=Z:\python projects\@lib;c:\python25;

if exist compile-all.pyc del compile-all.pyc
if exist compile-all.pyo del compile-all.pyo

del /Q "Z:\python projects\_django-projects\@projects\vyperlogix_site\django\static\captcha\*.*"

c:\python25\python25.exe -OO compile-all.py