from django.conf.urls.defaults import *

from vyperlogix.google.gae import gae_utils
_is_running_local = gae_utils.is_running_local()

from views import default
from views import _admin

urlpatterns = patterns('',
                       (r'^$', default.default),
                       (r'^folder/', default.default),
                       (r'^about/', default.about),
                       (r'^search/', default.default),
                       (r'^robots.txt', default.static),
                       (r'^favicon.ico', default.static),
)

if (_is_running_local):
    urlpatterns += patterns('',
                            (r'^icons/', default.static),
                            )

    urlpatterns += patterns('',
                            #(r'^_admin/', _admin._admin),
                            (r'^admin/', include('django.contrib.admin.urls')),
                            
                            (r'.*', default.default),
                            )
