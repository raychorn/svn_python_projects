export PYTHONPATH=/usr/local/cargochief/cargochief:/usr/local/cargochief/vyperlogix_2_7_0.zip:/usr/local/cargochief/_Django-1.3_Multi-Threaded:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=settings
#python test2.py
python /usr/local/cargochief/cargochief/manage2.py runserver --settings=settings --noreload 127.0.0.1:8001 

