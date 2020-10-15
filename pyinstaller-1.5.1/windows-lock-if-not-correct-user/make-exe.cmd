@echo off

python25 ../Configure.py

python25 ../Makespec.py -c -F "J:\@Vyper Logix Corp\@Projects\python\windows-user-scripts\windows-lock-if-not-correct-user.py"

python25 ../Build.py "J:\@Research\@Python\PyInstaller 1.5.1\pyinstaller-1.5.1\windows-lock-if-not-correct-user\windows-lock-if-not-correct-user.spec"
