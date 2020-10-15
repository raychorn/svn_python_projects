from django.db import models

from django.utils.translation import ugettext_lazy as _

####################################################################################
## BEGIN: Model
####################################################################################
class SampleModel(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('sample')
        verbose_name_plural = _('sample')
        ordering = ('timestamp',)

    def __str__(self):
        return '%s' % (self.timestamp)
####################################################################################
## END! Models
####################################################################################
