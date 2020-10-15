@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

python main.py --host=molten.magma-da.com --max_count=2000 --threads=999 --timeout=10 --mode="posts|multi" --url="/contact/login_form"

