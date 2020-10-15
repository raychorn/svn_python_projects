from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

class JsonData(models.Model):
    statename = models.CharField(_('statename'), max_length=2, unique=True)
    data = models.TextField(_('data'), unique=False)

    def __str__(self):
        return '[%s]' % (self.statename)
    
    def asDict(self):
        return {'statename':self.statename,'data':self.data}

