@echo off

echo "buildrelease <%1>"

set PYTHONPATH=J:\@Vyper Logix Corp\@Projects\pygame-for-android\pgs4a-0.9.6\python-install\lib\python2.7;
python android.py build %1 release

:exit
