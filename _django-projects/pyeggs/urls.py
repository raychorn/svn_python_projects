from django.conf.urls.defaults import *
from views import default
from vyperlogix.django.static import django_static

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^static/', django_static.static),
    (r'.*', default.default),
)
