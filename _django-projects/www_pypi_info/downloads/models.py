from django.db import models

class Download(models.Model):
    name = models.CharField('Name', maxlength=255,db_index=True)
    descr = models.TextField('Description')
    source = models.CharField('Source',maxlength=256)
    active = models.BooleanField('Active')
    members_only = models.BooleanField('Members Only')
        
    class Meta:
        ordering = ['name']
    
    class Admin:
        pass
    
    def __str__(self):
        return '%s, %s, (Act=%s), (Members=%s)' % (self.name,self.source,'ACTIVE' if (self.active) else 'not active','MEMBERS ONLY' if (self.members_only) else 'OPEN ACCESS')
    
