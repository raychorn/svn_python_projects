import pickle

from google.appengine.ext import db
from google.appengine.ext import search

class UserModel(db.Model):
   username = db.StringProperty(required=True)
   password = db.StringProperty(required=True)
   usertype = db.StringProperty(required=True, choices=set(["admin", "user"]))

class BlobModel(db.Model):
   name = db.StringProperty(required=True)
   blob = db.BlobProperty(required=True)
   type = db.StringProperty(required=True, choices=set(["template", "pickle"]))
