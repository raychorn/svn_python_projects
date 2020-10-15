from django.db import models

class Content(models.Model):
    try:
        url = models.CharField('URL', max_length=30)
    except TypeError:
        url = models.CharField('URL', maxlength=30)

    try:
        menu_tag = models.CharField('Menu Tag', max_length=30)
    except TypeError:
        menu_tag = models.CharField('Menu Tag', maxlength=30)

    content = models.TextField()

    class Admin:
        pass
    
    def __str__(self):
        return '%s :; %s' % (self.url,self.menu_tag)
    
