@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;Z:\python projects\_django-projects\magma_molten_4.1.0\pyro_SalesForceProxy;
cls
START "webserver:9000" /SEPARATE /HIGH python webserver.py --conf myprojectconf --host 127.0.0.1:9000
START "webserver:9001" /SEPARATE /HIGH python webserver.py --conf myprojectconf --host 127.0.0.1:9001
START "webserver:9002" /SEPARATE /HIGH python webserver.py --conf myprojectconf --host 127.0.0.1:9002
