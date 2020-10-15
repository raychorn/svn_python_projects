from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'vyperlogix1.homeapp.index', name='index'),
    #url(r'^home/', include('homeapp.urls')),
    url(r'^$', include('homeapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

