@echo on

cls

call workon web-proxy1

set DJANGO_SITENAME=webproxy1
set DJANGO_SETTINGS_MODULE=webproxy1.settings

set PYTHONPATH=C:\Users\raychorn\Envs\web-proxy1\Lib\site-packages;c:\Users\raychorn\Envs\web-proxy1\Lib\site-packages;C:\#python-projects\vyperlogix-library;c:\@python-projects\django-projects\web-proxy-dev;c:\@python-projects\django-projects\web-proxy-dev\webproxy1;

django-admin migrate

