from django.conf.urls import patterns, include, url

from django.conf.urls import *
from django.contrib import admin

from views import default as default_view
from views import contact as contact_view
from views import terms as terms_view
from jobsportal.views import default as jobs_view

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^jobs/', jobs_view),
    (r'^contact/', contact_view),
    (r'^terms/', terms_view),
    ('^$', default_view),
)
