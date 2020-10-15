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
## BEGIN: Github Manager Models
####################################################################################
from django.db import models

def document_file_name(instance, filename):
    '''
    'documents/%Y/%m/%d'
    '''
    from vyperlogix.misc import _utils
    normalize = lambda username:'documents%s/%s/%s/%s' % (tuple(['/%s'%(username) if (username and (len(username) > 0)) else ''])+tuple(_utils.timeStampLocalTime().split('T')[0].split('-')))
    fpath = normalize(None)
    githubuser = GitHubUser.objects.get(user=instance.user)
    if (githubuser):
        fpath = normalize('%s+%s'%(instance.user.username,githubuser.username))
    return '/'.join([fpath, filename])

class Document(models.Model):
    docfile = models.FileField(upload_to=document_file_name)
    user = models.ForeignKey(User, unique=False)
    
    def __str__(self):
        return '%s (%s)' % (self.docfile,self.user)
    
    def __json__(self):
        return {'docfile':{'name':self.docfile.name,'url':self.docfile.url},'user':{'username':self.user.username,'email':self.user.email,'first_name':self.user.first_name,'last_name':self.user.last_name}}

class GitHubUser(models.Model):
    username = models.CharField(_('username'), max_length=64, unique=True)
    password = models.CharField(_('password'), max_length=64, unique=False)
    name = models.CharField(_('name'), max_length=64, unique=False)
    email = models.EmailField(_('email'), max_length=64, unique=True)
    user = models.ForeignKey(User, unique=True)

    def __str__(self):
        return '%s [%s] [%s] (%s)' % (self.username,self.name,self.email,self.user)
    
    def asDict(self):
        return {'username':self.username,'name':self.name,'email':self.email,'userid':self.user.id}

####################################################################################
## END! DjangoCloud Models
####################################################################################
