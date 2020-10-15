from django.db import models

from django.utils.translation import ugettext_lazy as _

import registration

from django.contrib.auth.models import User

class GoogleAuthenticator(models.Model):
    otpseed = models.CharField(_('otpseed'), max_length=16, unique=True)
    sitename = models.CharField(_('sitename'), max_length=32, unique=True)
    href = models.URLField(_('href'), unique=False)

    def __str__(self):
        return '[%s] [%s]' % (self.otpseed,self.sitename)
    
    def asDict(self):
        return {'otpseed':self.otpseed,'sitename':self.sitename}

