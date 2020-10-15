@echo off
REM %1 is the version number of the Python we wish to execute.
REM %2 is the program we wish to launch - full path to the executable...

SET MULTIPY_1="C:\Program Files\Wing IDE 3.0\bin\wing.exe"
SET MULTIPY_2=%ComSpec% "/k"
SET MULTIPY_3=epydoc.pyw

REM multiPy 23 1 <-- Runs Wing IDE for Python 2.3
REM multiPy 24 1 <-- Runs Wing IDE for Python 2.4
REM multiPy 25 1 <-- Runs Wing IDE for Python 2.5

if %1. == 23. goto run23
if %1. == 24. goto run24
if %1. == 25. goto run25
goto runError

:run23
goto validVersion

:run24
goto validVersion

:run25
goto validVersion

:validVersion
set old_path = %Path%
set Path=c:\python%1;c:\python%1\scripts;%Path%

set old_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=C:\Python%1

if %2. == . "%PYTHONPATH%\python.exe"
if %2. == 1. %MULTIPY_1%
if %2. == 2. %MULTIPY_2%
if %2. == 3. %PYTHONPATH%\python.exe %PYTHONPATH%\Scripts\%MULTIPY_3%

set path=%old_path%
set PYTHONPATH=%old_PYTHONPATH%

goto exit

:runError
echo ERROR - Cannot execute the version "%1".
goto exit

:exit
echo Run done.

