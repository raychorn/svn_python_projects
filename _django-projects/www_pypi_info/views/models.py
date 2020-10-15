from django.db import models

class Keyword(models.Model):
    gid = models.IntegerField('gid')
        
    keyword = models.CharField('keyword', maxlength=32)
        
    division = models.SmallIntegerField('division')
        
    class Meta:
        ordering = ['keyword']
    
    class Admin:
        pass
    
    def __str__(self):
        return '%s, %s' % (self.id,self.keyword)
    
class User(models.Model):
    name = models.CharField('Name', maxlength=255,db_index=True)
    username = models.CharField('UserName', maxlength=150,db_index=True)
    email = models.EmailField('Email Address',db_index=True)
    password = models.CharField('Password',maxlength=100,editable=False,blank=True,null=True)
    usertype = models.CharField('User Type', maxlength=25,db_index=True)
    block = models.BooleanField('Block')
    sendEmail = models.BooleanField('Send Email')
    lastvisitDate = models.DateTimeField('Last Visit Date',null=True)
    registerDate = models.DateTimeField('Register Date',null=True)
    activation = models.CharField('Activation',maxlength=100,null=True)
        
    class Meta:
        ordering = ['name']
    
    class Admin:
        pass
    
    def __str__(self):
        return '%s, %s, %s, %s, (Reg=%s), (Last=%s)' % (self.usertype,self.name,self.email,'BLOCKED' if (self.block) else 'ACCESS',self.registerDate,self.lastvisitDate)
    
