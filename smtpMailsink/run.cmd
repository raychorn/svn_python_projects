@echo off

set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_pyax-0.9.7.2-py2.5;

c:\python25\python smtpMailsink.py --cwd="Z:\python projects\smtpMailsink\smtpMailsink_logs" --host=0.0.0.0:8025 --redirect=gmail --bcc=raychorn@hotmail.com 
