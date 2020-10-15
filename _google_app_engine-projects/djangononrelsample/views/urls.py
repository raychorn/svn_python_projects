from django.conf.urls import patterns, include, url

from django.conf.urls import *
#from django.contrib import admin

from views import default as default_view
from views import contact as contact_view
from views import terms as terms_view
from views import not_yet_implemented
from views import acceptable_use_policy

__has_users__ = False
try:
    from users.views import default as users_view
    from users.views import login as users_login
    from users.views import register as users_register
    from users.views import registeruser as users_registeruser
    __has_users__ = True
except ImportError:
    pass

#admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    #(r'^admin/', include(admin.site.urls)),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^not-yet-implemented/', not_yet_implemented),
    (r'^acceptable-use-policy/', acceptable_use_policy),
    (r'^contact/', contact_view),
    (r'^terms/', terms_view),
)

if (__has_users__):
    urlpatterns += patterns('',
        (r'^__admin__/', users_view),
        (r'^login/', users_login),
        (r'^register/', users_register),
        (r'^registeruser/', users_registeruser),
    )
else:
    urlpatterns += patterns('',
        (r'^__admin__/', not_yet_implemented),
    )

urlpatterns += patterns('',
    ('^$', default_view),
)
