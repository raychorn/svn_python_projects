from django.conf.urls.defaults import *
from views import default
from vyperlogix.django.static import django_static

from django.contrib.sitemaps import Sitemap

from content import models as content_models

from vyperlogix.misc import _utils

class ContentSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return content_models.Content.objects.all()

    def lastmod(self, obj):
        return _utils.getFromNativeTimeStamp(_utils.timeStamp())

    def location(self, obj):
        return obj.url
    
sitemaps = {
    'content': ContentSitemap(),
}

urlpatterns = patterns('',
    (r'^grid/', default.grid),
                       
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^tinymce/', include('tinymce.urls')),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^media/', django_static.static),    # this is intercepted and handled by cherokee
    (r'^static/', django_static.static),    # this is intercepted and handled by cherokee
    (r'^admin-static/', django_static.static),    # this is intercepted and handled by cherokee
    (r'.*', default.default),
)

urlpatterns = urlpatterns
