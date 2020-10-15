import os, sys

from django.db import models
from django.conf import settings
from django.contrib import admin

from django.contrib.sites.models import SiteManager

from vyperlogix.html import myOOHTML as oohtml

from vyperlogix import misc
from django.utils.translation import ugettext_lazy as _

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
    
class MenuType(models.Model):
    menutype = models.CharField('Menu Type', max_length=10, primary_key=True)
    descr = models.CharField('Description', max_length=128)

    class Admin:
	list_display = ('menutype', 'descr')
	search_fields = ['menutype']
	ordering = ['menutype']
    
    def __str__(self):
        return '%s' % (self.menutype)

class Content(models.Model):
    sites = models.ManyToManyField(Site)
    menutype = models.ForeignKey(MenuType)
    admin_mode = models.BooleanField()
    url = models.CharField('URL', max_length=128)
    descr = models.CharField('Description', max_length=128, blank=True, null=True)
    menu_tag = models.CharField('Menu Tag', max_length=30)
    target = models.CharField('Target', max_length=30, blank=True, null=True)

    content = models.TextField()

    def __str__(self):
        return '%s :: (%s) %s->%s (%s) :: %s -> %s' % (str([item.name for item in self.sites.all()]),'ADMIN' if (self.admin_mode) else '',self.menutype,self.url,self.descr,self.menu_tag,self.target)

class SnippetType(models.Model):
    admin = models.BooleanField('Administrative', blank=False, null=False)
    snippet_type = models.CharField('Snippet Type', max_length=30, primary_key=True)
    descr = models.CharField('Description', max_length=128)

    def __str__(self):
        return '%s%s' % ('+' if (self.admin) else '-',self.snippet_type)

def get_snippet_types_by_type(snippet_type=None):
    return SnippetType.objects.filter(snippet_type=snippet_type)

def get_snippet_type_by_type(snippet_type=None):
    aSnippetType = None
    if (misc.isString(snippet_type)):
	snippettypes = get_snippet_types_by_type(snippet_type=snippet_type)
	if (snippettypes.count() > 0):
	    aSnippetType = snippettypes[0]
    return aSnippetType

def get_header_snippet_type():
    return get_snippet_type_by_type(snippet_type='header')

def get_wiki_layout_snippet_type():
    return get_snippet_type_by_type(snippet_type='wiki-layout')

def get_layout_snippet_type():
    return get_snippet_type_by_type(snippet_type='layout')

def get_content_snippet_type():
    return get_snippet_type_by_type(snippet_type='content')

def get_body_snippet_type():
    return get_snippet_type_by_type(snippet_type='body')

def get_title_snippet_type():
    return get_snippet_type_by_type(snippet_type='title')

def get_head_snippet_type():
    return get_snippet_type_by_type(snippet_type='head')

def get_javascript_snippet_type():
    return get_snippet_type_by_type(snippet_type='javascript')

class Snippet(models.Model):
    sites = models.ManyToManyField(Site)
    snippet_type = models.ForeignKey(SnippetType)

    descr = models.CharField('Description', max_length=128, blank=True, null=True)
    snippet_tag = models.CharField('Snippet Tag', max_length=128)

    content = models.TextField()

    def __str__(self):
        return '%s :: %s :: %s -> %s' % (str([item.name for item in self.sites.all()]),self.snippet_type,self.descr,self.snippet_tag)

class URL(models.Model):
    sites = models.ManyToManyField(Site)
    url = models.CharField('URL', max_length=255, primary_key=True)
    descr = models.CharField('Description', max_length=128, blank=True, null=True)
    url_tag = models.CharField('URL Tag', max_length=30)
    
    def __str__(self):
        return '%s -> %s' % (self.url_tag,self.url)

class Country(models.Model):
    iso = models.CharField('ISO', max_length=2)
    name = models.CharField('Name', max_length=80)
    printable_name = models.CharField('Printable Name', max_length=80)
    iso3 = models.CharField('ISO3', max_length=3)
    numcode = models.SmallIntegerField('NumCode')

    def __str__(self):
        return self.printable_name
    
class State(models.Model):
    name = models.CharField('Name', max_length=40)
    abbrev = models.CharField('Abbrev', max_length=2)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField('Name', max_length=40)

    def __str__(self):
        return self.name
    
class User(models.Model):
    role = models.ForeignKey(Role)
    referred_by = models.ForeignKey('self',blank=True,null=True)
    companyname = models.CharField('Company Name', max_length=30,blank=True,null=True)
    firstname = models.CharField('First Name', max_length=30,blank=False,null=False)
    lastname = models.CharField('Last Name', max_length=30,blank=False,null=False)
    email_address = models.EmailField('Email Address', max_length=128, primary_key=True, unique=True, blank=False,null=False)
    password = models.CharField('Password', max_length=100, editable=False, blank=True, null=True)
    street_address = models.CharField('Street Address', max_length=60,blank=True,null=True)
    city = models.CharField('City', max_length=30,blank=True,null=True)
    state = models.ForeignKey(State)
    country = models.ForeignKey(Country)
    zipcode = models.CharField('ZipCode', max_length=30,blank=True,null=True)
    phone_number = models.CharField('Phone Number', max_length=20,blank=True,null=True)
    activated = models.BooleanField('Activated')
    activated_on = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return '%s' % (self.email_address)

class UserActivity(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField('Action', max_length=256)
    ip = models.IPAddressField('IP')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('user activity')
        verbose_name_plural = _('user activities')
        ordering = ('-timestamp',)
        
    def __str__(self):
        return '%s,%s,%s,%s' % (self.user,self.action,self.ip,self.timestamp)

class SiteName(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)

    def __str__(self):
        return '"%s" for %s' % (self.site,self.user)

###########################################################################

class CssParent(models.Model):
    snippet = models.ForeignKey(Snippet)
    name = models.CharField('Name', max_length=64)
        
    class Admin:
        pass
    
    def __str__(self):
        return '"%s" --> %s' % (self.snippet,self.name)

class CssNodeType(models.Model):
    name = models.CharField('Name', max_length=16)
        
    class Admin:
        pass
    
    def __str__(self):
        return '%s' % (self.name)

class CssNode(models.Model):
    parent = models.ForeignKey(CssParent)
    site = models.ForeignKey(Site)
    nodeType = models.ForeignKey(CssNodeType)
    name = models.CharField('Name', max_length=64)
    value = models.CharField('Value', max_length=256)
        
    class Admin:
        pass
    
    def __str__(self):
        return '%s --> "%s" (%s) --> %s=%s' % (self.site,self.parent,self.nodeType,self.name,self.value)

class Image(models.Model):
    site = models.ForeignKey(Site)
    image = models.ImageField('Image',upload_to='%s' % (os.path.join(settings.MEDIA_ROOT,'uploads')))
        
    class Admin:
        pass
    
    def __str__(self):
        return '%s --> %s' % (self.site,self.image)

