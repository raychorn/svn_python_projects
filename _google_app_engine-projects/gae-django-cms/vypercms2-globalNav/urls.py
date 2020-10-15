# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from globalNav.views import default as globalNav_default
from users.views import default as users_default
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
                                       ('^admin/(.*)', admin.site.root),
                                       ('^rest/users/(.*)', users_default),
                                       ('^users/(.*)', users_default),
                                       (r'.*', globalNav_default),
) + urlpatterns

