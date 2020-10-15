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
    
class Json(models.Model):
    name = models.CharField(_('menu name'), max_length=50, unique=True, primary_key=True)
    json = models.TextField(_('json'), unique=False)
    xml = models.TextField(_('xml'), unique=False)
    state = models.CharField(_('menu state'), max_length=16, unique=False)
    uuid = models.CharField(_('uuid'), max_length=36,blank=True,null=True)
    class Meta:
        verbose_name = _('json')
        verbose_name_plural = _('json')
        ordering = ('name',)

    def __str__(self):
        return '%s (%s)' % (self.name,self.uuid)
    
class Protocols(models.Model):
    name = models.CharField(_('protocol name'), max_length=16, unique=True, primary_key=True)
    value = models.CharField(_('protocol value'), max_length=16, unique=False)
    uuid = models.CharField(_('uuid'), max_length=36,blank=True,null=True)
    class Meta:
        verbose_name = _('protocol')
        verbose_name_plural = _('protocols')
        ordering = ('name',)

    def __str__(self):
        return '%s-->"%s" (%s)' % (self.name,self.value,self.uuid)
    
class Environments(models.Model):
    name = models.CharField(_('environment name'), max_length=32, unique=True, primary_key=True)
    domain = models.CharField(_('environment domain'), max_length=64, unique=True, primary_key=False)
    uuid = models.CharField(_('uuid'), max_length=36,blank=True,null=True)
    class Meta:
        verbose_name = _('environment')
        verbose_name_plural = _('environments')
        ordering = ('name',)

    def __str__(self):
        return '%s-->%s (%s)' % (self.name,self.domain,self.uuid)
    
