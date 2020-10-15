@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;Z:\python projects\_django-projects\magma_molten_4.1.0\pyro_SalesForceProxy;
cls
python webserver.py --conf myprojectconf --host 127.0.0.1:8888

echo END!

