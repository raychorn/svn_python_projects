@echo off
set PYTHONPATH=c:\python25;Z:\python projects\_django_0_96_2;Z:\python projects\@lib;Z:\python projects\_django-projects;
START "djangocerise_1_2:8880" /SEPARATE /HIGH python djangocerise_1_2/webserver.py --conf myprojectconf --host 127.0.0.1:8880
START "djangocerise_1_2:8881" /SEPARATE /HIGH python djangocerise_1_2/webserver.py --conf myprojectconf --host 127.0.0.1:8881
START "djangocerise_1_2:8882" /SEPARATE /HIGH python djangocerise_1_2/webserver.py --conf myprojectconf --host 127.0.0.1:8882
