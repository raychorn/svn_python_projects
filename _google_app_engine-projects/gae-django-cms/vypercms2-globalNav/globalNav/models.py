import pickle

from google.appengine.ext import db
from google.appengine.ext import search

class User(db.Model):
    uid = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

    @classmethod
    def create(cls, uid, name, password):
        Unique.check("uid", uid)
        u = User(uid=uid, name=name, password=password)
        u.put()
        return u

    def __str__(self):
        return '%s [%s] (%s)' % (self.name,self.password,self.uid)

class State(db.Model):
    state = db.StringProperty(required=True, choices=set(['loggedIn', 'loggedIn', 'loggedOut', 'loggedOut']))

    @classmethod
    def create(cls, state):
        Unique.check("state", state)
        s = State(state=state)
        s.put()
        return s

    def __str__(self):
        return '%s' % (self.state)

class Json(db.Model):
    name = db.StringProperty(required=True)
    json = db.TextProperty(required=True)
    state = db.StringProperty(required=True)
    uuid = db.StringProperty(required=True)
    user = db.ReferenceProperty(User)
    state = db.ReferenceProperty(State)

    def __str__(self):
        return '%s (%s) for %s (%s)' % (self.name,self.uuid,self.user,self.state)

class Menu(db.Model):
    user = db.ReferenceProperty(User)
    json = db.ReferenceProperty(Json)
    state = db.ReferenceProperty(State)

    def __str__(self):
        return '%s --> %s (%s)' % (self.user,self.json,self.state)

