@echo off

echo %COMPUTERNAME%

cronservice --json "./service_config.json" stop

