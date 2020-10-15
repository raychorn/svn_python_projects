@echo off

echo %COMPUTERNAME%

SET PYTHONPATH=j:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;

if %COMPUTERNAME% == HPDV7-6163US goto HOME

echo "Using Proxy"
python githubProxyServer.py 127.0.0.1:9909 --proxy=127.0.0.1:8888

goto END

:HOME

echo "NO Proxy"
python githubProxyServer.py 127.0.0.1:9909

:END
