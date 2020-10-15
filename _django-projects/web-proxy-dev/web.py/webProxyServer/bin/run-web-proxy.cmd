@echo off

echo %COMPUTERNAME%

SET PYTHONPATH=j:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;

if %COMPUTERNAME% == HPDV7-6163US goto HOME

echo "Using Proxy"
python webProxyServer.py %1 --proxy=%2

goto END

:HOME

echo "NO Proxy"
python webProxyServer.py %1

:END
