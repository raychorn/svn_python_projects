from standalone import models
from django.utils.translation import ugettext_lazy as _

class GoogleAuthenticator(models.StandaloneModel):
    otpseed = models.CharField(_('otpseed'), max_length=16, unique=True)
    sitename = models.CharField(_('sitename'), max_length=32, unique=True)
    href = models.URLField(_('href'), unique=False)

    class Meta:
	db_table = u'GoogleAuthenticator'

