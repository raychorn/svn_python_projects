@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;
cls
START "webserver:8000" /SEPARATE /HIGH python "Z:\python projects\_django-projects\resources\django\djangocerise\webserver.py" --conf myprojectconf --host 127.0.0.1:8000
START "webserver:8001" /SEPARATE /HIGH python "Z:\python projects\_django-projects\resources\django\djangocerise\webserver.py" --conf myprojectconf --host 127.0.0.1:8001
START "webserver:8002" /SEPARATE /HIGH python "Z:\python projects\_django-projects\resources\django\djangocerise\webserver.py" --conf myprojectconf --host 127.0.0.1:8002
