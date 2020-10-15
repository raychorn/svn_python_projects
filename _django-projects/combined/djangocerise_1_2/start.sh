export PYTHONPATH=$HOME:$HOME/combined:$HOME/lib/python2.5/site-packages:$HOME/python25/lib/VyperLogixLib-1.0-py2.5.egg:$HOME/python25/lib/VyperLogixPyaxLib-1.0-py2.5.egg:$HOME/python25/lib/SQLAlchemy-0.5.3-py2.5.egg:/usr/lib/python2.5/site-packages:/var/lib/python-support/python2.5:$HOME/python25/lib/Django-0.96.3-py2.5.egg:$HOME/python25/lib/MySQL_python-1.2.3b2-py2.5-linux-i686.egg:$PYTHONPATH

echo $PYTHONPATH
python2.5 webserver.pyc --conf myprojectconf --host 127.0.0.1:9000 --daemon=1
python2.5 webserver.pyc --conf myprojectconf --host 127.0.0.1:9001 --daemon=1
python2.5 webserver.pyc --conf myprojectconf --host 127.0.0.1:9002 --daemon=1

