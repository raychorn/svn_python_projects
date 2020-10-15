@echo off

echo %COMPUTERNAME%

cronservice --json "./service_config.json" remove

taskkill /F /IM cronservice

