@echo off

python -mcompileall a

xcopy a\*.pyc b /s /v
