@echo off

set PYTHONPATH=c:\python25;J:\python-projects\@lib\12-13-2011-01;
python -m cProfile -s cumulative benchmark1.py > reports-bench1.txt

python -m cProfile -s cumulative optimizer.py > reports-optimizer-bench1.txt


