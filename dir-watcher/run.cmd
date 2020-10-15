@echo off

echo %COMPUTERNAME%

START "dir-watcher" /SEPARATE /HIGH "dirwatcher" -w "%1" -c -v
