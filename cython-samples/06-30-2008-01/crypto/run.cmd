@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -m cProfile -s cumulative coder-test.py > coder-test-report.txt

python -m cProfile -s cumulative coder-test2.py > coder-test2-report.txt
