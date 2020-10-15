export PYTHONPATH=/opt/ActivePython-2.5/lib:/local/var/www/apps/molten4/VyperLogixLib-1.0-py2.5.egg:/local/var/www/apps/molten4/_django_0_96_2:/local/var/www/apps/molten4/magma_molten_4:/local/var/www/apps/molten4/pyro:$PYTHONPATH

rm -f /local/var/www/apps/molten4/magma_molten_4/djangocerise/logs/*

/opt/ActivePython-2.5/bin/python2.5 /local/var/www/apps/molten4/magma_molten_4/djangocerise/webserver.pyc --conf myprojectconf --host 0.0.0.0:9000


