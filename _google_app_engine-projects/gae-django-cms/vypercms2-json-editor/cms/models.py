import pickle

from google.appengine.ext import db
from google.appengine.ext import search

class UserModel(db.Model):
   username = db.StringProperty(required=True)
   password = db.StringProperty(required=True)
   usertype = db.StringProperty(required=True, choices=set(["admin", "user"]))

class BlobModel(db.Model):
   bid = db.StringProperty(required=True)
   name = db.StringProperty(required=True)
   blob = db.BlobProperty(required=True)
   type = db.StringProperty(required=True)
   size = db.IntegerProperty(required=True)
