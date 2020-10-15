@echo off

set PYTHONPATH=%s
python Setup.py build_ext --inplace -c mingw32
