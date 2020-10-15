@echo off
SET PYTHONPATH=c:\python25;Z:\python projects\@lib;
REM python -m cProfile -s cumulative reports.py --year=2005 --source=paypal > reports-paypal_2005.txt
REM python reports.py --year=2005 --source=paypal > reports-paypal_2005.txt
REM python reports.py --year=2006 --source=paypal > reports-paypal_2006.txt
REM python reports.py --year=2007 --source=paypal > reports-paypal_2007.txt
C:\Python25\python reports.py --year=2009 --source=paypal > reports-paypal_2009.txt