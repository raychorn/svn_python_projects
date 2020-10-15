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
## BEGIN: CargoChief Models
####################################################################################
class QuoteContact(models.Model):
    name = models.CharField(_('name'), max_length=32, unique=True)
    email = models.CharField(_('email'), max_length=128, unique=True)
    phone = models.CharField(_('phone'), max_length=10, unique=True)

    class Meta:
        verbose_name = _('QuoteContact')
        verbose_name_plural = _('QuoteContacts')
        ordering = ('name','email','phone')

    def __str__(self):
        return '%s' % (self._class)

class Cities(models.Model):
    locId = models.IntegerField(_('locId'), unique=True)
    country = models.CharField(_('country'), max_length=16, unique=False)
    region = models.CharField(_('region'), max_length=16, unique=False)
    city = models.CharField(_('city'), max_length=128, unique=False)
    postalCode = models.CharField(_('postalCode'), max_length=128, unique=False)
    latitude = models.FloatField(_('latitude'), unique=False)
    longitude = models.FloatField(_('longitude'), unique=False)
    metroCode = models.IntegerField(_('metroCode'), unique=False)
    areaCode = models.IntegerField(_('areaCode'), unique=False)

    class Meta:
        verbose_name = _('Cities')
        verbose_name_plural = _('Cities')
        ordering = ('locId','country','region','city','postalCode','latitude','longitude','metroCode','areaCode')

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.locId,self.country,self.region,self.city,self.postalCode,self.latitude,self.longitude,self.metroCode,self.areaCode)

####################################################################################
## END! CargoChief Models
####################################################################################
