@echo off

echo %COMPUTERNAME%

START "windows-temporary-file-cleaner" /SEPARATE /HIGH "windows-temporary-file-cleaner" --verbose
