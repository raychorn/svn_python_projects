@echo off

SET PATH=c:\python25;%PATH%
SET PYTHONPATH=c:\python25;Z:\python projects\@lib;
python -OO compileall.py

SET DEST=C:\@1b
if not exist %DEST% mkdir %DEST%
xcopy *.py %DEST% /s /v /y
xcopy *.pyo %DEST% /s /v /y

if exist %DEST%\compileall.py del %DEST%\compileall.py
if exist %DEST%\diags.py del %DEST%\diags.py
if exist %DEST%\setup.py del %DEST%\setup.py
if exist %DEST%\test-auth.py del %DEST%\test-auth.py
if exist %DEST%\tester.py del %DEST%\tester.py

if exist %DEST%\pyHTTPServer.py del %DEST%\pyHTTPServer.py

if exist %DEST%\compileall.pyo del %DEST%\compileall.pyo
if exist %DEST%\diags.pyo del %DEST%\diags.pyo
if exist %DEST%\setup.pyo del %DEST%\setup.pyo
if exist %DEST%\test-auth.pyo del %DEST%\test-auth.pyo
if exist %DEST%\tester.pyo del %DEST%\tester.pyo
