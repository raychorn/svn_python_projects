@echo off

echo %COMPUTERNAME%

START "windows-service-restart" /SEPARATE /HIGH "windows-service-restart" --machine=%COMPUTERNAME% --action=status --service=TntDrive
