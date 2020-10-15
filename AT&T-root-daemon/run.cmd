@echo off

echo %COMPUTERNAME%

START "loggerwebservice" /SEPARATE /HIGH "loggerwebservice" 127.0.0.1:9999
