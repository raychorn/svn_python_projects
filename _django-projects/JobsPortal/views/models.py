import simplejson

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
## BEGIN: JobsPortal Models
####################################################################################
from django.db import models

def document_file_name(instance, filename):
    '''
    'documents/%Y/%m/%d'
    '''
    from vyperlogix.misc import _utils
    from users.models import User
    normalize = lambda username:'documents%s/%s/%s/%s' % (tuple(['/%s'%(username) if (username and (len(username) > 0)) else ''])+tuple(_utils.timeStampLocalTime().split('T')[0].split('-')))
    fpath = normalize(None)
    user = User.objects.get(id=instance.user_id)
    if (user):
        fpath = normalize('%s'%(_utils.ascii_valid_dos_filename_chars(user.username)))
    return '/'.join([fpath, filename])

class Document(models.Model):
    docfile = models.FileField(upload_to=document_file_name)
    user_id = models.IntegerField(unique=False)
    
    def __str__(self):
        return '%s (%s)' % (self.docfile,self.user_id)
    
    def __json__(self):
        return {'docfile':{'name':self.docfile.name,'url':self.docfile.url},'user_id':self.user_id}

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

class Candidate(models.Model):
    fullname = models.CharField(max_length=32,unique=True)
    phone = models.CharField(max_length=16,unique=True)
    relocateable = models.BooleanField(default=False,unique=False)
    user = models.OneToOneField(User, primary_key=True)
    city = models.OneToOneField(Cities, primary_key=False)
    
    def __str__(self):
        return '%s (%s)' % (self.fullname,self.user)
    
    def __json__(self):
        d = {'candidate':{'fullname':self.fullname,'relocateable':self.relocateable,'relocateable_yes':'checked' if (self.relocateable) else '','relocateable_no':'checked' if (not self.relocateable) else '','phone':self.phone}}
        d['country'] = None
        d['city'] = None
        d['state'] = None
        d['zipcode'] = None
        try:
            d['country'] = self.city.country
            d['city'] = self.city.city
            d['state'] = self.city.region
            d['zipcode'] = self.city.postalCode
        except:
            pass
        return simplejson.dumps(d)

    def asDict(self):
        return simplejson.loads(self.__json__())

####################################################################################
## END! JobsPortal Models
####################################################################################
