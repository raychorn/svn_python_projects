@echo off

if not exist dist/MiddleWareJSONRPC.exe goto error

echo "OK"

"dist/MiddleWareJSONRPC.exe" --port=7777

goto exit

:error

echo "ERROR"

goto exit

:exit

echo "DONE!"