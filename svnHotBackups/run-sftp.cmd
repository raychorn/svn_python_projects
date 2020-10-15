@echo off
cls
echo BEGIN:

set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;

REM python sftp.py --computer=misha-lap.ad.magma-da.com --server=river --source=C:\@1\svn-4928.tar.gz --dest=/home/sfscript/@data

python sftp.py --computer=misha-lap.ad.magma-da.com --server=tide2 --source=C:\@1\ContactsWalker.zip --dest=/home/rhorn/@data

echo END!