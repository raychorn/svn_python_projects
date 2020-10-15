@echo off

set PYTHONPATH=C:\Python25;Z:\python projects\@lib\lib;
REM python mySQLBackups.py --host=near-by.info --username=nearbyin_admin --password=peekab00 --binpath="C:\Program Files\MySQL\MySQL Server 5.0\bin" --destpath="\\Sql2005\k$\MySQL Backups" --maxbackups=60
REM python mySQLBackups.py --host=near-by.info --username=nearbyin_admin --password=peekab00 --binpath="C:\Program Files\MySQL\MySQL Server 5.0\bin" --destpath=. --maxbackups=60

if exist mySQLBackups.exe mySQLBackups --host=near-by.info --username=nearbyin_admin --password=peekab00 --binpath="C:\Program Files\MySQL\MySQL Server 5.0\bin" --destpath=. --maxbackups=60