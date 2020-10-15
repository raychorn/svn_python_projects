from django.db import models

from django.utils.translation import ugettext_lazy as _

import registration

####################################################################################
## BEGIN: Gelocation Models
####################################################################################
class Geolocation(models.Model):
    gps = models.CharField(_('gps'), max_length=32, unique=False)
    altitude = models.FloatField(verbose_name=_('altitude'))
    heading = models.FloatField(verbose_name=_('heading'))
    horizontalAccuracy = models.FloatField(verbose_name=_('horizontal_accuracy'))
    speed = models.FloatField(verbose_name=_('speed'))
    _type = models.CharField(_('type'), max_length=32, unique=False)
    verticalAccuracy = models.FloatField(verbose_name=_('vertical_accuracy'))
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('geolocation')
        verbose_name_plural = _('geolocation')
        ordering = ('gps',)

    def __str__(self):
        return '%s' % (self.gps)
####################################################################################
## END! Gelocation Models
####################################################################################
