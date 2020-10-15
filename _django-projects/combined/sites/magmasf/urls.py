from django.conf.urls.defaults import *
from views import default

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'.*', default.default),
)
