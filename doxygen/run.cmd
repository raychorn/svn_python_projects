if exist "C:\Program Files (x86)\doxygen\bin\doxygen.exe" goto win64
goto win32

:win32
set PATH=C:\Program Files\doxygen\bin\;%PATH
set PYTHONPATH=c:\python25\lib;

goto doit

:win64
set PATH=C:\Program Files (x86)\doxygen\bin\;%PATH
set PYTHONPATH=c:\python25\lib;

:doit
if not exist C:\_@4_ mkdir C:\_@4_
doxygen config.dox

:exit
