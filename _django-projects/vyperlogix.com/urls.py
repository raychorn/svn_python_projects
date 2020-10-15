from django.conf.urls.defaults import *
from views import default
from views import admin as custom_admin
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
    
class SnippetSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [c for c in content_models.Snippet.objects.all() if (c.snippet_tag[0] == '/') and (c.snippet_tag[-1] == '/')]

    def lastmod(self, obj):
        return _utils.getFromNativeTimeStamp(_utils.timeStamp())

    def location(self, obj):
        return obj.snippet_tag
    
sitemaps = {
    'content': ContentSitemap(),
    'snippet': SnippetSitemap(),
}

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/migrate-content/', custom_admin.default),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       
                       #(r'^tinymce/', include('tinymce.urls')),
                       
                       (r'^crossdomain.xml$', django_static.static),
                       (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       (r'^media/', django_static.static),            # this is intercepted and handled by cherokee
                       (r'^static/', django_static.static),           # this is intercepted and handled by cherokee
                       (r'^admin-static/', django_static.static),     # this is intercepted and handled by cherokee
                       (r'^rest/', default.rest),                     
                       (r'.*', default.default),
)

urlpatterns = urlpatterns
