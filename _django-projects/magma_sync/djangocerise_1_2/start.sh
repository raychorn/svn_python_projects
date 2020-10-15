export PYTHONPATH=/opt/ActivePython-2.5/lib:/home/admin/molten_utils/VyperLogixLib-1.0-py2.5.egg:/home/admin/molten_utils/VyperLogixMagmaLib-1.0-py2.5.egg:/home/admin/molten_utils/www/magmaSync:/home/admin/molten_utils/pyax:/home/admin/molten_utils/_django_1_02/Django-1.0.2-final:$PYTHONPATH

export PYTHON_EGG_CACHE=/home/admin/python-eggs

svn update /home/admin/molten_utils/pyax
svn update /home/admin/molten_utils/_django_0_96_2
svn update /home/admin/molten_utils/_django_1_02

/opt/ActivePython-2.5/bin/python2.5 webserver.pyc --conf myprojectconf --host 0.0.0.0:9000

