# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

from django.contrib.auth.models import User

from vyperlogix.google.gae import unique

from vyperlogix.misc import _utils

class FacebookUser(unique.UniqueModel):
    """Basic user profile with personal details."""
    uid = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    expires = db.IntegerProperty(required=True)
    base_domain = db.StringProperty(required=True)
    perms = db.StringProperty(required=True)
    secret = db.StringProperty(required=True)
    sig = db.StringProperty(required=True)
    session_key = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    _uniques = set([
                    (uid,)
                    ])
    
    def __unicode__(self):
        return '%s' % (self.Timestamp)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

