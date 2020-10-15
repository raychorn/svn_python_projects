@echo off
cls
echo BEGIN:

REM "simple-message-bus.exe" -i "message_box1" -o "message_box2"

"simple-message-bus.exe" -i "message_box1" -o "127.0.0.1:55555" -r -l "127.0.0.1:50555"


exit

echo END!

