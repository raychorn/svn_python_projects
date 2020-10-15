from django.conf.urls.defaults import *
from views import current_datetime
from home.views import index
from home.views import detail
from views import default

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^home/', index),
    (r'^details/(?P<id>\d+)/$', detail),
    (r'^now/$', current_datetime.current_datetime),
    (r'^about/', default.about),

    (r'^pyeggs/home/', index),
    (r'^pyeggs/now/$', current_datetime.current_datetime),
    (r'^pyeggs/about/', default.about),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^pyeggs/admin/', include('django.contrib.admin.urls')),

    (r'.*', default.default),
)

