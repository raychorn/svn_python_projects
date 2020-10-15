@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -m cProfile -s cumulative mainPDF.py > reports-mainPDF.txt
