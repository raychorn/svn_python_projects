@echo off

SET PATH=c:\python25;%PATH%
SET PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -OO compileall.py
python -OO pyHTTPServer.py --port=8080 --root="{'/'='J:\#rackspace\#source\ray.horn-20120808-LAM-907\app\html','py'='J:\#rackspace\#source\ray.horn-20120808-LAM-907\python\app'}" --index="index.html" --logging=logging.WARNING --retention=9000 %1 %2 %3 %4 %5 %6 %7 %8 %9

REM  --port=8080 --index="index.html" --logging=logging.WARNING --retention=9000 --root="{'/'::'J:\#rackspace\#source\ray.horn-20120808-LAM-907\app\html','py'::'J:\#rackspace\#source\ray.horn-20120808-LAM-907\python\app'}"

