@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\@lib;

for /f %%i in ('cd') do set cwd=%%i

if %1. == 1. python -O pySFProxy.py --cwd=%cwd% --local-ip=127.0.0.1:80 --remote-ip=ubuntu.dyn-o-saur.com:8085 --verbose --logging=logging.INFO
if %1. == 2. python -O pySFProxy.py --cwd=%cwd% --local-ip=127.0.0.1:443 --remote-ip=cs1.salesforce.com:443 --verbose --logging=logging.INFO

if %1. == 1. goto exit
if %1. == 2. goto exit

:help
echo "1 = python -O pySFProxy.py --local-ip=127.0.0.1:80 --remote-ip=ubuntu.dyn-o-saur.com:8085"
echo "2 = python -O pySFProxy.py --local-ip=127.0.0.1:443 --remote-ip=cs1.salesforce.com:443"

:exit
