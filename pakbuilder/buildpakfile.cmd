@echo off

echo %COMPUTERNAME%

"pakbuilder" 16.83.121.123 -v -p 22 -u root -w Compaq123 -s "c:\@vm1\Helloworld" -d "/root/@1" -a "/root/@1" -n hpOneViewAdapter3 -b 115 -i

