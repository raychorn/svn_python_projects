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
    
class Country(models.Model):
    iso = models.CharField(_('ISO'), max_length=2)
    name = models.CharField(_('Name'), max_length=80)
    printable_name = models.CharField(_('Printable Name'), max_length=80)
    iso3 = models.CharField(_('ISO3'), max_length=3)
    numcode = models.SmallIntegerField(_('NumCode'))

    def __str__(self):
        return self.printable_name
    
class State(models.Model):
    name = models.CharField(_('Name'), max_length=40)
    abbrev = models.CharField(_('Abbrev'), max_length=2)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(_('Name'), max_length=40)

    def __str__(self):
        return self.name
    
class User(models.Model):
    role = models.ForeignKey(Role)
    referred_by = models.ForeignKey('self',blank=True,null=True)
    companyname = models.CharField(_('Company Name'), max_length=30,blank=True,null=True)
    firstname = models.CharField(_('First Name'), max_length=30,blank=False,null=False)
    lastname = models.CharField(_('Last Name'), max_length=30,blank=False,null=False)
    email_address = models.EmailField(_('Email Address'), max_length=128, primary_key=True, unique=True, blank=False,null=False)
    password = models.CharField(_('Password'), max_length=100, editable=False, blank=True, null=True)
    street_address = models.CharField(_('Street Address'), max_length=60,blank=True,null=True)
    city = models.CharField(_('City'), max_length=30,blank=True,null=True)
    state = models.ForeignKey(State)
    country = models.ForeignKey(Country)
    zipcode = models.CharField(_('ZipCode'), max_length=30,blank=True,null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20,blank=True,null=True)
    activated = models.BooleanField(_('Activated'))
    activated_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return '%s' % (self.email_address)

class UserActivity(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(_('Action'), max_length=256)
    ip = models.IPAddressField(_('IP'))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('user activity')
        verbose_name_plural = _('user activities')
        ordering = ('-timestamp',)
        
    def __str__(self):
        return '%s,%s,%s,%s' % (self.user,self.action,self.ip,self.timestamp)

