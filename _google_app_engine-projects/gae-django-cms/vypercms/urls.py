# -*- coding: utf-8 -*-
import os, sys

from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from cms.forms import UserRegistrationForm
from django.contrib import admin

admin.autodiscover()

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
    ('^$', 'cms.views.index_page'),
    (r'^search', 'cms.views.search'),
    (r'^url/(?P<value>.+)$', 'cms.views.re_url'),
    (r'^install$', 'cms.views.install'),
    (r'^robots.txt$', 'cms.views.robots'),
    (r'^rss/latest/(?P<cate_id>.*)/rss.xml$', 'cms.views.rsslatest'),
    (r'^sitemap.xml$', 'cms.views.sitemap'),
    (r'^admin/(.*)', admin.site.root),
    (r'^themes/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.dirname(os.path.abspath(__file__)) + '/themes/'}),      
    #(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^account/register/$', 'registration.views.register',
        kwargs={'form_class': UserRegistrationForm},
        name='registration_register'),    
) + urlpatterns
