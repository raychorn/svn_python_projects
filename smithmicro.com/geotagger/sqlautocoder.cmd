@echo off

 sqlautocode mysql://root:peekab00@127.0.0.1:3306/django-heat-maps-prototype -o djangoTables.py -t smithmicro_sampleheatmapdata,users_geolocation
 sqlautocode_cleanup --input=djangoTables.py

REM sqlautocode mysql://root:peekab00@127.0.0.1:3306/geotagger_sample1 -o dataTables.py