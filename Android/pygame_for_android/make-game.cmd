@echo off

REM %1 is the folder that contains the game
REM %2 is the name of the game
REM %3 is the version like 1.0

if %1. == . goto help
if %2. == . goto help
if %3. == . goto help
if %4. == . goto help
if %5. == debug. goto build
if %5. == release. goto build
if %5. == install. goto build
goto help

:build
cd pygame-package-0.9.2

set PATH=%PATH%;D:\Python25\;D:\Python25\Scripts;F:\Python27\;F:\Python27\Scripts;

python2.7 build.py --dir %1 --package com.vyperlogix.%2 --name %3 --version %4 --orientation portrait %5

if %5. == debug. goto skip_zipalign

zipalign -f 4 bin\%2-%4-release.apk bin\%2-%4-release-aligned.apk

zipalign -c -v 4 bin\%2-%4-release-aligned.apk

:skip_zipalign

cd ..

goto :exit

:help
echo BEGIN: HELP
echo %%1 is the folder that contains the game
echo %%2 is the name of the game
echo %%3 is the version like 1.0
echo
echo Sample: make-game ..\slidepuzzle slidepuzzle "Slide Puzzle" 1.0 debug
echo Sample: make-game ..\sample1 sample1 "Sample #1" 1.0 debug
echo END! HELP

:exit



