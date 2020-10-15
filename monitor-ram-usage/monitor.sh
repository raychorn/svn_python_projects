export PYTHONPATH=/opt/ActivePython-2.5/lib:/home/admin/molten_utils/VyperLogixLib-1.0-py2.5.egg:/home/admin/molten_utils/VyperLogixMagmaLib-1.0-py2.5.egg:/home/admin/molten_utils/toshiba_fix:/home/admin/molten_utils/pyax:$PYTHONPATH

export PYTHON_EGG_CACHE=/home/admin/python-eggs

svn update /home/admin/molten_utils/pyax

/opt/ActivePython-2.5/bin/python2.5 /home/admin/molten_utils/monitor_ram_usage/monitor_ram_usage.pyc

