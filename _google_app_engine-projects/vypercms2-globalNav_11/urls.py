# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from myapp.forms import UserRegistrationForm
from globalNav.views import default as globalNav_default
from users.views import default as users_default
from vypercms.views import default as vypercms_default
from vypercms.views import admin as vypercms_admin
from businessdata.views import default as businessdata_default
from vypertwitz.views import default as vypertwitz_default
from myapp.views import create_admin_user
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
                                       ('^admin/(.*)', admin.site.root),
                                       #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                       #(r'^_main/', 'django.views.generic.simple.direct_to_template',
                                           #{'template': '_main.html'}),
                                       # Override the default registration form
                                       #url(r'^account/register/$', 'registration.views.register',
                                           #kwargs={'form_class': UserRegistrationForm},
                                           #name='registration_register'),
                                       ('^create_admin_user/', create_admin_user),
                                       ('^rest/users/(.*)', users_default),
                                       ('^users/(.*)', users_default),
                                       ('^global-navigation/(.*)', globalNav_default),
                                       ('^vypercms/admin/(.*)', vypercms_admin),
                                       ('^vypertwitz/(.*)', vypertwitz_default),
                                       ('^businessdata/(.*)', businessdata_default),
                                       (r'^pdfxporter/', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/pdfxporter.html'}),
                                       (r'^polymorphical/', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/polymorphical.html'}),

                                       (r'^main/', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                       (r'^home/', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                       (r'^who-we-are/', 'django.views.generic.simple.direct_to_template', {'template': 'who-we-are.html'}),
                                       (r'^what-we-do/', 'django.views.generic.simple.direct_to_template', {'template': 'what-we-do.html'}),
                                       (r'^our-work/', 'django.views.generic.simple.direct_to_template', {'template': 'our-work.html'}),
                                       (r'^flash/$', 'django.views.generic.simple.direct_to_template', {'template': 'flash.html'}),
                                       (r'^android/', 'django.views.generic.simple.direct_to_template', {'template': 'android.html'}),
                                       (r'^platforms/$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms.html'}),
                                       
                                       (r'^chartingdemo.html$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/chartingdemo.html'}),
                                       (r'^polymorphical.html$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/polymorphical.html'}),
                                       (r'^pdfxporter.html$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/pdfxporter.html'}),
                                       (r'^vyperlogos.html$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/vyperlogos.html'}),
                                       (r'^free-4u.html$', 'django.views.generic.simple.direct_to_template', {'template': 'platforms/free-4u.html','extra_context':{}}),

                                       (r'.*', vypercms_default),
) + urlpatterns
