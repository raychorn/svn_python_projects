@echo off

echo %COMPUTERNAME%

REM goto SKIP1

"gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -v -b 20 -s 100

REM "gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -v -b 90 -s 100

REM "gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -v -b 180 -s 100

REM "gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -v -b 270 -s 100

goto EXIT
:SKIP1

REM "gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -v -x -s 100
"gps-fences" -1 "52, -1.8, 10000" -2 "52.1, -1.9, 10000" -x -s 100

:EXIT
