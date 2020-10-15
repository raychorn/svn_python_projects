@echo on

cd "J:/@Vyper Logix Corp/@Projects/python-projects/@lib/12-13-2011-01"

J:

START "compile2.7" /SEPARATE /HIGH "compile2.7.cmd" END

START "compile-egg2.7" /SEPARATE /HIGH compile-egg2.7.cmd "C:/Python27/Lib/site-packages/Crypto" Crypto END

START "compile-egg2.7" /SEPARATE /HIGH compile-egg2.7.cmd "C:/Python27/Lib/site-packages/paramiko-1.10.1-py2.7.egg/paramiko" paramiko END

START "compile-egg2.7" /SEPARATE /HIGH compile-egg2.7.cmd "C:/Python27/Lib/site-packages/OpenSSL" OpenSSL END

