from django.conf.urls.defaults import *
from views import current_datetime
from home.views import index
from home.views import detail
from views import default

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^contact/', default.contact),
    (r'^home/', default.default),
    (r'^login/', default.default),
    (r'^FAQ/', default.default),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'.*', default.default),
)
