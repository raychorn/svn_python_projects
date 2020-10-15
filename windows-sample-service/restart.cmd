@echo off

echo %COMPUTERNAME%

net stop aservice

net start aservice

