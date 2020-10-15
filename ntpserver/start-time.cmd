@echo off

w32tm /config /manualpeerlist:time.windows.com /syncfromflags:manual /reliable:yes /update
w32tm /config /syncfromflags:domhier /update

w32tm /config /manualpeerlist:time.windows.com,0x1 /syncfromflags:manual /reliable:yes /update

net stop w32time
net start w32time

w32tm /resync /rediscover
