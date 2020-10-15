@echo off
cls
echo BEGIN:

set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;

python25 compdb.py analytics_portal_test-bouygues-portal.sql analytics_portal_dev_test.sql

echo END!
