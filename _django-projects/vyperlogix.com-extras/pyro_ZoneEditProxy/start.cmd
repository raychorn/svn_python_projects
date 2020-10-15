@echo off

START "Pyro Name Server for Molten 4.1.0" /B /I /HIGH ns.cmd > ns.txt

set PYTHONPATH=Z:\python projects\@lib;c:\python25;

START "Pyro Name Server for Molten 4.1.0" /I /HIGH c:\python25\python25 server.py

