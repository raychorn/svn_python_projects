''' Copyright (c) 2006-2007, PreFab Software Inc. '''


from django.conf.urls.defaults import include, patterns
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

from blogmaker.blog.models import Entry

index = {
    'template' : 'blog/tools/index.html', 
    'extra_context' : dict(title='Tools index'),
}

urlpatterns = patterns('',
    ('^entry/(?P<id>[\d]+)/$', 'blogmaker.blog.views.tools.edit_entry'),
    ('^entry/add/$', 'blogmaker.blog.views.tools.edit_entry'),
    ('^entry/$', 'blogmaker.blog.views.tools.existing_entries'),
    ('^$', login_required(direct_to_template), index),
)

