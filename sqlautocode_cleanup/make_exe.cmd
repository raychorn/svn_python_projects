@echo off

python25 "J:\@Research\@Python\PyInstaller 1.5.1\pyinstaller-1.5.1\Configure.py"

python25 "J:\@Research\@Python\PyInstaller 1.5.1\pyinstaller-1.5.1\Makespec.py" -c -F "J:\@Vyper Logix Corp\@Projects\python\sqlautocode_cleanup\sqlautocode_cleanup.py"

python25 "J:\@Research\@Python\PyInstaller 1.5.1\pyinstaller-1.5.1\Build.py" sqlautocode_cleanup.spec
