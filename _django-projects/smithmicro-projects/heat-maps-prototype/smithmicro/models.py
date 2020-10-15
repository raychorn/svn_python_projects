from django.db import models

from django.utils.translation import ugettext_lazy as _

class SampleHeatMapData(models.Model):
    id = models.CharField(verbose_name=_('id'), max_length=36, unique=True, primary_key=True,auto_created=False)
    heat_gps = models.CharField(_('heat_gps'), max_length=128)
    heat_lat = models.IntegerField(verbose_name=_('heat_lat'))
    heat_lng = models.IntegerField(verbose_name=_('heat_lng'))
    heat_x = models.IntegerField(verbose_name=_('heat_x'))
    heat_y = models.IntegerField(verbose_name=_('heat_y'))
    heat_num = models.IntegerField(verbose_name=_('heat_num'))
    data_name = models.CharField(_('data_name'), max_length=50)
    data_value = models.IntegerField(verbose_name=_('data_value'))
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = _('SampleHeatMapGeocode')
        verbose_name_plural = _('SampleHeatMapGeocode')
        ordering = ('heat_gps','heat_lat','heat_lng','heat_x','heat_y','heat_num')

    def __str__(self):
        return '{%s} %s,%s {%s,%s} (%s)' % (self.heat_gps,self.heat_x,self.heat_y,self.heat_lat,self.heat_lng,self.heat_num)
