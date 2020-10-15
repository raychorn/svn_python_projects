@echo off
if %1. == 1. python -O proxy.py -l 127.0.0.1 -p 80 -r ubuntu.dyn-o-saur.com -P 8085
if %1. == 2. python -O proxy.py -l 127.0.0.1 -p 443 -r cs1.salesforce.com -P 443

if %1. == 1. goto exit
if %1. == 2. goto exit

:help
echo "1 = proxy.py -l 127.0.0.1 -p 80 -r ubuntu.dyn-o-saur.com -P 8085"
echo "2 = python -O proxy.py -l 127.0.0.1 -p 443 -r cs1.salesforce.com -P 443"

:exit
