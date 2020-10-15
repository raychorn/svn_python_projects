@echo off
cls
echo BEGIN:

REM "simple-message-bus.exe" -i "message_box2" -o "message_box3"

"simple-message-bus.exe" -i "127.0.0.1:55555" -o "message_box2"

exit

echo END!

