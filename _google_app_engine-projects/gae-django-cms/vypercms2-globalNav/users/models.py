import pickle

from google.appengine.ext import db
from google.appengine.ext import search

from vyperlogix.google.gae import unique

class User(unique.UniqueModel):
    uid = db.StringProperty(required=True) # uuid value
    username = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    fullname = db.StringProperty(required=False)
    isloggedin = db.BooleanProperty(required=True)
    loggedin = db.DateTimeProperty(required=False)
    isApproved = db.BooleanProperty(required=True)
    isAdmin = db.BooleanProperty(required=True)

    _uniques = set([
                    (username,)
                    ])

    @classmethod
    def create(cls, uid, username, password, fullname, isloggedin, isApproved, isAdmin):
        u = User(uid=uid, username=username, password=password, fullname=fullname, isloggedin=isloggedin, isApproved=isApproved, isAdmin=isAdmin)
        u.put()
        return u

    def __str__(self):
        return '%s "%s" pwd=[%s] uid=(%s) isloggedin=(%s) isApproved=(%s) isAdmin=(%s)' % (self.username,self.fullname,self.password,self.uid,self.isloggedin,self.isApproved,self.isAdmin)

class Domains(db.Model):
    is_active = db.BooleanProperty(required=True)
    domain = db.StringProperty(required=True)

    def __str__(self):
        return '(%s) %s' % (self.is_active,self.domain)

