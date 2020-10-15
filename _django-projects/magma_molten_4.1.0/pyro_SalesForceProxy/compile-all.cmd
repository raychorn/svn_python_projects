@echo off

set PYTHONPATH=Z:\python projects\@lib;c:\python25;

if exist compile-all.pyc del compile-all.pyc
if exist compile-all.pyo del compile-all.pyo

python -OO compile-all.py