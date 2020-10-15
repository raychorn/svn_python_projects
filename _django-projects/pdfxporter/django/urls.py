from django.conf.urls.defaults import *
from views import current_datetime
from register.views import index as register_index
from views import default
from vyperlogix.django.static import django_static

urlpatterns = patterns('',
    # Example:
    (r'^register/', register_index),
    (r'^validate/', register_index),
    (r'^versioncheck/', register_index),
    (r'^feedback/', register_index),
    (r'^specials/', register_index),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^media/', django_static.static),    # this is intercepted and handled by cherokee
    (r'^static/', django_static.static),    # this is intercepted and handled by cherokee
    (r'^admin-static/', django_static.static),    # this is intercepted and handled by cherokee
    
    (r'.*', default.default),
)
