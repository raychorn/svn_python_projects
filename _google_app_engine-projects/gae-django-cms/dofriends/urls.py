# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from myapp.forms import UserRegistrationForm
from users.views import default as users_default
from vypercms.views import default as vypercms_default
from vypercms.views import admin as vypercms_admin
from images.views import image
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
                                       ('^admin/(.*)', admin.site.root),
                                       #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                       (r'^_main/', 'django.views.generic.simple.direct_to_template',
                                           {'template': '_main.html'}),
                                       # Override the default registration form
                                       url(r'^account/register/$', 'registration.views.register',
                                           kwargs={'form_class': UserRegistrationForm},
                                           name='registration_register'),
                                       ('^rest/users/(.*)', users_default),
                                       ('^users/(.*)', users_default),
                                       ('^vypercms/admin/(.*)', vypercms_admin),
                                       ('^get-image/(.*)', image),
                                       (r'.*', vypercms_default),
) + urlpatterns
