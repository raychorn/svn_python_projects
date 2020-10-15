from django.db import models
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _

from django.contrib.sites.models import SiteManager

from django.contrib.auth.models import User

class Site(models.Model):
    domain = models.CharField(_('domain name'), max_length=100, unique=True)
    name = models.CharField(_('display name'), max_length=50)
    uuid = models.CharField(_('uuid'), max_length=36,blank=True,null=True)
    objects = SiteManager()
    class Meta:
        db_table = 'django_site'
        verbose_name = _('site')
        verbose_name_plural = _('sites')
        ordering = ('domain',)

    def __str__(self):
        return '%s' % (self.domain)
    
####################################################################################
## BEGIN: DjangoCloud Models
####################################################################################
class DjangoServer(models.Model):
    servername = models.CharField(_('servername'), max_length=64, unique=True)
    user = models.ForeignKey(User, unique=True)

    class Meta:
        verbose_name = _('DjangoServer')
        verbose_name_plural = _('DjangoServer')
        ordering = ('servername','user')

    def __str__(self):
        return '%s' % (self.Meta.verbose_name)

class DjangoApplication(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True)
    server = models.ForeignKey(DjangoServer, unique=True)
    user = models.ForeignKey(User, unique=True)

    class Meta:
        verbose_name = _('DjangoApplication')
        verbose_name_plural = _('DjangoApplications')
        ordering = ('name','user')

    def __str__(self):
        return '%s' % (self.Meta.verbose_name)

####################################################################################
## END! DjangoCloud Models
####################################################################################
