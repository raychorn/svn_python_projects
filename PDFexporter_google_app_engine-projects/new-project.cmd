@echo off

if %1. == . goto error

do_django django-admin.py startproject %1
goto done

:error
echo Nothing to do !

:done

