@echo off

echo %COMPUTERNAME%

"dist/yalidator" -i "infrastructure.yml" -v

