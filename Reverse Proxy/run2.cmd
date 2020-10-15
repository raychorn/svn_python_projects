@echo off
set PYTHONPATH=C:\Python25\lib;Z:\python projects\@lib;
cls
START "TinyHTTPProxy:8888" /SEPARATE /HIGH python TinyHTTPProxy.py 8888
