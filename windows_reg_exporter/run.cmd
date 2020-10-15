@echo off

if not exist dist/winregdump.exe goto error

echo "OK"

REM "dist/winregdump.exe" --search="C:\Program Files (x86)" --verbose --debug >./winreg2b.log 2>&1

"dist/winregdump.exe" --json >./winregdump.json 2>&1

goto exit

:error

echo "ERROR"

goto exit

:exit

echo "DONE!"