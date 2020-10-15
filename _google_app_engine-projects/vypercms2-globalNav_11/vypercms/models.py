# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

class StyleSheet(db.Model):
    name = db.StringProperty(required=True)
    url =  db.URLProperty(required=False)
    content = db.BlobProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now=True)

class Title(db.Model):
    name = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

class Head(db.Model):
    name = db.StringProperty(required=True)
    url =  db.URLProperty(required=False)
    content = db.BlobProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now=True)

class Template(db.Model):
    name = db.StringProperty(required=True)
    url =  db.URLProperty(required=False)
    content = db.BlobProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now=True)

class Domain(db.Model):
    name = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

class Page(db.Model):
    name = db.StringProperty(required=True)
    domain =  db.ReferenceProperty(Domain,required=True)
    url =  db.StringProperty(required=True)
    title = db.ReferenceProperty(Title,required=True)
    css = db.ReferenceProperty(StyleSheet,required=True)
    head = db.ReferenceProperty(Head,required=False)
    template = db.ReferenceProperty(Template,required=True) # can be HTML or Django Template
    parentPage = db.SelfReferenceProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now=True)
