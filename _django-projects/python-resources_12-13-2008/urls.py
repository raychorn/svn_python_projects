from django.conf.urls.defaults import *
from views import current_datetime
from home.views import index
from home.views import detail
from views import default
from library.views import index as library_index
from library.views import catalog as catalog_index
from library.views import grid as library_grid

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^library', library_index),
    (r'^library/left', library_index),
    (r'^library/right', library_index),
    (r'^library/js', library_index),
    (r'^catalog', catalog_index),
    (r'^grid/', library_grid),
    (r'^home/', index),
    (r'^about/', default.about),
    (r'^tabs/', default.tabs),
    (r'^crossdomain.xml', default.crossdomain),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'.*', default.default),
)

