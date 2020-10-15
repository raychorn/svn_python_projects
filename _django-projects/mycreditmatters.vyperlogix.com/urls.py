from django.conf.urls.defaults import *
from views import current_datetime
from home.views import index
from home.views import detail
from views import default

#from polls.views import index as polls_index

urlpatterns = patterns('',
    # Example:
    (r'^$', default.default),
    (r'^home/', index),
    (r'^about/', default.about),
    (r'^tabs/', default.tabs),

    #(r'^polls/$', polls_index),
    #(r'^polls/(?P<poll_id>\d+)/$', 'mysite.polls.views.detail'),
    #(r'^polls/(?P<poll_id>\d+)/results/$', 'mysite.polls.views.results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'.*', default.default),
)

