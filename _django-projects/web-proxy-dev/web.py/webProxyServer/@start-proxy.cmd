@echo off

echo %COMPUTERNAME%

START "start-proxy" /SEPARATE /HIGH ".\bin\run-web-proxy.cmd"
