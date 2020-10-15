from django.conf.urls.defaults import *

import os, sys

import settings

from views import current_datetime
from home.views import index
from home.views import detail
from views import default

from vyperlogix.django.static import django_static

from vyperlogix.google.gae import gae_utils
_is_running_local = gae_utils.is_running_local()

try:
    from settings import MEMCACHE_ADDRESS
except ImportError:
    MEMCACHE_ADDRESS = '127.0.0.1::11211'

urlpatterns = patterns('',
                       (r'^$', default.default),
                       (r'^login/', default.login),
                       (r'^robots.txt', django_static.static),
                       (r'^favicon.ico', django_static.static),
)

if (_is_running_local):
    #<LocationMatch "/((css|js|img|swf|pdf)/|favicon.ico)">
    #SetHandler None
    #</LocationMatch>

    is_memcachable = True
    try:
        import memcache
    except ImportError:
        is_memcachable = False
        
    if (is_memcachable):
        mc = memcache.Client([MEMCACHE_ADDRESS], debug=0)
        is_memcachable = all([s.connect() for s in mc.servers])

    is_in_memcache = False
    if (is_memcachable):
        _patterns = mc.get('STATIC_PATTERNS')
        #if (_patterns is not None):
            #urlpatterns += _patterns

    urlpatterns += patterns('',
                            (r'^admin/', include('django.contrib.admin.urls')),
                            (r'^static/*$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
                            )

urlpatterns += patterns('',
                        (r'.*', default.default),
                        )
