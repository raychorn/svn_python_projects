@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\@lib;
cls

python VyperProxy.py --port=8888 --num=1 --start --django="Z:\python projects\_django-projects\resources\django\djangocerise\run.cmd" --django_port=8000 --django_num=3 --django_pythonpath="C:\Python25\lib;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;"

