@echo off

echo %COMPUTERNAME%

START "start-proxy" /SEPARATE /HIGH ".\bin\run-github-proxy.cmd"
