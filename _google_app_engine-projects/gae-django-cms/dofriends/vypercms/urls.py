# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import default
from views import admin

urlpatterns = patterns('vypercms.views',
                       ('^admin/(.*)', admin),
                       #(r'.*', default),
)
