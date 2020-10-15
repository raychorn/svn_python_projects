@echo off

echo %COMPUTERNAME%

"pakbuilder" 16.83.121.250 -v -p 22 -u root -w Compaq@123 -d "collector/wrapper.conf" -f "server=y,suspend=n,address=8004" -r
