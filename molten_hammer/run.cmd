@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

REM python main.py --host=pyeggs.dyn-o-saur.com --max_count=1000 --threads=10 --mode="gets|single" --url=/
REM 28 RPS 31 secs

Rem python main.py --host=pyeggs.dyn-o-saur.com --max_count=1000 --threads=10 --mode="gets|multi" --url=/
REM 29 RPS 31 secs

REM python main.py --host=pyeggs.dyn-o-saur.com --max_count=1000 --threads=100 --mode="gets|multi" --url=/

REM python main.py --host=192.168.64.132 --max_count=1000 --threads=100 --mode="posts|multi" --url=/contact/login_form

REM python main.py --host=192.168.64.133 --max_count=1000 --threads=100 --mode="posts|multi" --url=/contact/login_form

REM python main.py --host=ubuntu3.gateway.2wire.net --max_count=1000 --threads=100 --mode="posts|multi" --url=/info.php

REM python main.py --host=ubuntu3.gateway.2wire.net --max_count=1000 --threads=100 --mode="posts|multi" --url="/example/"

REM python main.py --host=pyeggs.dyn-o-saur.com:8080 --max_count=1000 --threads=100 --mode="gets|multi" --url="/"

REM python main.py --host=ubuntu3.pyeggs.com --max_count=1000 --threads=500 --mode="gets|multi" --url="/"

REM python main.py --host=ubuntu3.pypi.info:8080 --max_count=500 --threads=50 --mode="gets|multi" --url="/"

REM python main.py --host=molten.magma-da.com --max_count=200000 --threads=1000 --timeout=60 --mode="posts|multi" --url="/contact/login_form"

REM python main.py --procs=5

python main.py --host=www.vyperlogix.com --max_count=1000 --threads=100 --timeout=60 --mode="gets|multi" --url=/
