@echo off
cls

echo %COMPUTERNAME%

echo BEGIN:

if exist message_box1 goto skip1

mkdir message_box1

:skip1

if exist message_box2 goto skip2

mkdir message_box2

:skip2
if exist message_box3 goto skip3

mkdir message_box3

:skip3
START "run1" /SEPARATE /HIGH ".\bin\run1.cmd"

timeout /t 1

START "run2" /SEPARATE /HIGH ".\bin\run2.cmd"

goto exit

:exit

echo END!

