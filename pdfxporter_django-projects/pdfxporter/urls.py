from django.conf.urls.defaults import *
from views import current_datetime
from register.views import index as register_index
from views import default

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^register/', register_index),
    (r'^validate/', register_index),
    (r'^versioncheck/', register_index),
    (r'^feedback/', register_index),
    (r'^specials/', register_index),
    (r'^now/$', current_datetime.current_datetime),
    (r'^about/', default.about),
    (r'^tabs/', default.tabs),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'.*', default.default),
)
