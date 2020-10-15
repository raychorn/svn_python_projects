@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

REM python zoneclient.py -v -l -i "Local Area Connection" Rhorn6 peekab00 vyperlogix.com,pyeggs.com,magma-sf.net,magma-sf.com,pypi.info

REM python zoneclient.py -v -l -a 76.251.90.62 Rhorn6 peekab00 vyperlogix.com,pyeggs.com,magma-sf.net,magma-sf.com,pypi.info

python zoneclient.py -t -v -r "http://192.168.1.254/xslt?PAGE=B01&THISPAGE=C01&NEXTPAGE=B01" Rhorn6 peekab00 vyperlogix.com,pyeggs.com,magma-sf.net,magma-sf.com,pypi.info

