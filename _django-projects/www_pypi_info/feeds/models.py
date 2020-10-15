from django.db import models

class PyPI(models.Model):
    try:
        name = models.CharField('title', max_length=128)
    except TypeError:
        name = models.CharField('title', maxlength=128)
        
    try:
        version = models.CharField('version', max_length=32)
    except TypeError:
        version = models.CharField('version', maxlength=32)
        
    try:
        link = models.CharField('link', max_length=255)
    except TypeError:
        link = models.CharField('link', maxlength=255)

    descr = models.TextField('descr')
    timestamp = models.DateTimeField('timestamp')

    class Meta:
        ordering = ['-timestamp']
    
    class Admin:
        pass
    
    def __str__(self):
        return '%s, %s, %s' % (self.name,self.link,self.timestamp)
    
