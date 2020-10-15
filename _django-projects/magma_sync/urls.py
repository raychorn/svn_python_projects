from django.conf.urls.defaults import *
from views import current_datetime
from views import default

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^case/', default.default),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    # catch-all - loads the default page for all otherwise unknown urls such as '/' as in http://mysite.com/
    (r'.*', default.default),
)
