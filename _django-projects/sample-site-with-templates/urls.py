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

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # catch-all - loads the default page for all otherwise unknown urls such as '/' as in http://mysite.com/
    (r'.*', default.default),
)
