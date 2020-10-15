# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

from django.contrib.auth.models import User

from vyperlogix.misc import _utils

class Feedback(db.Model):
    """Basic user profile with personal details."""
    subject = db.StringProperty(required=True)
    message = db.StringProperty(required=True)
    user =  db.ReferenceProperty(User,required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    def __unicode__(self):
        return '%s from %s' % (self.subject, self.user)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

