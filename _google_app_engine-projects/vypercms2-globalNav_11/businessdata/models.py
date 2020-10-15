# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

class State(db.Model):
    name = db.StringProperty(required=True)
    url =  db.URLProperty(required=True)
    fieldName =  db.StringProperty(required=False)
    fieldLen =  db.IntegerProperty(required=False)
    abbrev = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

