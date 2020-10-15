from google.appengine.ext import db
from google.appengine.ext import search

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class TestData(db.Model):
    user = db.ReferenceProperty(User, verbose_name=_('user'))
    count = db.IntegerProperty(verbose_name=_('count'))
    timestamp = db.DateTimeProperty(auto_now=True)
