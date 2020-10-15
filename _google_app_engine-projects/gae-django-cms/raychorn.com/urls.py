# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from images.views import image
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
                                       ('^admin/(.*)', admin.site.root),
                                       # Override the default registration form
                                       ('^get-image/(.*)', image),
                                       (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                       #(r'.*', vypercms_default),
) + urlpatterns