from google.appengine.ext import db
from google.appengine.ext import search

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class LogosType(db.Model):
    user = db.ReferenceProperty(User, verbose_name=_('user'))
    name = db.StringProperty(verbose_name=_('name'))
    timestamp = db.DateTimeProperty(auto_now=True)

class LogosData(db.Model):
    aType = db.ReferenceProperty(LogosType, verbose_name=_('aType'))
    data = db.TextProperty(verbose_name=_('data'))
    timestamp = db.DateTimeProperty(auto_now=True)
