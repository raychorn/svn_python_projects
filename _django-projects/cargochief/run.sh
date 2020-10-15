#!/bin/bash

export PYTHONPATH=/usr/local/cargochief/cargochief:/usr/local/cargochief/vyperlogix_2_7_0.zip:/usr/local/cargochief/_Django-1.3_Multi-Threaded:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=cargochief.settings
#python 
python /usr/local/cargochief/cargochief/manage.py runserver --settings=settings 127.0.0.1:9999