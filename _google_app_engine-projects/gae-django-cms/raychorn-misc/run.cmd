@echo off
cls

C:\Python2557\python minify.py --deploy --yui --source="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\js-source" --dest="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\js.min" --zip --target="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn"

C:\Python2557\python minify.py --yui --deploy --source="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\static" --dest="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn-misc\static.min" --zip --target="Z:\python projects\_google_app_engine-projects\gae-django-cms\raychorn"
