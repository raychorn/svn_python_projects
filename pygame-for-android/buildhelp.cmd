@echo off

echo "buildhelp <%1>"

python android.py build %1 help

:exit
