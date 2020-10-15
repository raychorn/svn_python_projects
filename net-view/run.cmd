@echo off
SET PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -m cProfile -s cumulative disk-space-windows-linux.py > reports-disk-space-windows-linux.txt
