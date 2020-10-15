from django.db import models
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _

from django.contrib.sites.models import SiteManager

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
## BEGIN: Geonosis Models
####################################################################################
class GeonosisClass(models.Model):
    name = models.CharField(_('name'), max_length=32, unique=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('GeonosisClass')
        verbose_name_plural = _('GeonosisClass')
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self._class)


class GeonosisObject(models.Model):
    cid = models.ForeignKey('GeonosisClass')
    key = models.CharField(_('key'), max_length=128, unique=False)
    value= models.CharField(_('value'), max_length=128, unique=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('GeonosisObject')
        verbose_name_plural = _('GeonosisObjects')
        ordering = ('cid','key','value',)

    def __str__(self):
        return '%s.%s=%s' % (self.cid,self.key,self.value)
####################################################################################
## END! Geonosis Models
####################################################################################
