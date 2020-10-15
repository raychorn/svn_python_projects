from django.conf.urls.defaults import *
from views import default
from vyperlogix.django.static import django_static

from django.contrib.sitemaps import Sitemap

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       
                       (r'^crossdomain.xml$', django_static.static),
                       (r'^media/', django_static.static),    # this is intercepted and handled by cherokee
                       (r'^static/', django_static.static),    # this is intercepted and handled by cherokee
                       (r'^admin-static/', django_static.static),    # this is intercepted and handled by cherokee
                       (r'.*', default.default),
)

