from django.db import models

class MenuType(models.Model):
    try:
        menutype = models.CharField('Menu Type', max_length=10, primary_key=True)
    except TypeError:
        menutype = models.CharField('Menu Type', maxlength=10, primary_key=True)

    try:
        descr = models.CharField('Description', max_length=128)
    except TypeError:
        descr = models.CharField('Description', maxlength=128)

    class Admin:
        pass
    
    def __str__(self):
        return '%s, "%s"' % (self.menutype,self.descr)
    
class Content(models.Model):
    menutype = models.ForeignKey(MenuType)
    try:
        url = models.CharField('URL', max_length=30)
    except TypeError:
        url = models.CharField('URL', maxlength=30)

    try:
        descr = models.CharField('Description', max_length=128, blank=True, null=True)
    except TypeError:
        descr = models.CharField('Description', maxlength=128, blank=True, null=True)

    try:
        menu_tag = models.CharField('Menu Tag', max_length=30)
    except TypeError:
        menu_tag = models.CharField('Menu Tag', maxlength=30)

    try:
        target = models.CharField('Target', max_length=30, blank=True, null=True)
    except TypeError:
        target = models.CharField('Target', maxlength=30, blank=True, null=True)

    content = models.TextField()

    class Admin:
        pass
    
    def __str__(self):
        return '%s->%s (%s) :: %s -> %s' % (self.menutype,self.url,self.descr,self.menu_tag,self.target)
    
class SnippetType(models.Model):
    try:
        snippet_type = models.CharField('Snippet Type', max_length=30, primary_key=True)
    except TypeError:
        snippet_type = models.CharField('Snippet Type', maxlength=30, primary_key=True)

    try:
        descr = models.CharField('Description', max_length=128)
    except TypeError:
        descr = models.CharField('Description', maxlength=128)

    class Admin:
        pass
    
    def __str__(self):
        return '%s, "%s"' % (self.snippet_type,self.descr)
    
class Snippet(models.Model):
    snippet_type = models.ForeignKey(SnippetType)

    try:
        descr = models.CharField('Description', max_length=128, blank=True, null=True)
    except TypeError:
        descr = models.CharField('Description', maxlength=128, blank=True, null=True)

    try:
        snippet_tag = models.CharField('Snippet Tag', max_length=30)
    except TypeError:
        snippet_tag = models.CharField('Snippet Tag', maxlength=30)

    content = models.TextField()

    class Admin:
        pass
    
    def __str__(self):
        return '%s :: %s -> %s' % (self.snippet_type,self.descr,self.snippet_tag)
    
class URL(models.Model):
    try:
        url = models.CharField('URL', max_length=255, primary_key=True)
    except TypeError:
        url = models.CharField('URL', maxlength=255, primary_key=True)

    try:
        descr = models.CharField('Description', max_length=128, blank=True, null=True)
    except TypeError:
        descr = models.CharField('Description', maxlength=128, blank=True, null=True)

    try:
        url_tag = models.CharField('URL Tag', max_length=30)
    except TypeError:
        url_tag = models.CharField('URL Tag', maxlength=30)

    class Admin:
        pass
    
    def __str__(self):
        return '%s :: %s -> %s' % (self.url_tag,self.descr,self.url)
    
