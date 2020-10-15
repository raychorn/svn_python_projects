''' Copyright (c) 2006-2007, PreFab Software Inc. '''


from django.conf.urls.defaults import *

urlpatterns = patterns('blogmaker.comments.views',
    (r'^post/$', 'post_comment'),
    (r'^posted/$', 'comment_was_posted'),
)
