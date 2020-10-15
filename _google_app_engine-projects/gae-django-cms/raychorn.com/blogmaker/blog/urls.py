''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2006, Andrew Gwozdziewycz <apgwoz@gmail.com>
All rights reserved.
'''


from django.conf.urls.defaults import include, patterns
from blogmaker.blog.models import Entry
from django.contrib.syndication.views import feed 
from django.views.generic.date_based import object_detail, archive_month, archive_year, archive_index
from blogmaker.blog.views import view_tagged_items, view_tags, view_user_items, search, extras_day, trackback

from blogmaker.blog.feeds import blogmakerEntryFeed
from blogmaker.blog.trackback_views import postTrackbacks
from blogmaker.comments.feeds import LatestCommentsFeed


feeds = {
    'posts' : blogmakerEntryFeed,
    'comments': LatestCommentsFeed,
}

info_dict = {
    'queryset': Entry.objects.filter(active=True),
    'date_field': 'pub_date',
}

urlpatterns = patterns('',
    (r'^tag/(?P<tag>[a-zA-Z0-9_.-]+)/$', view_tagged_items),
    (r'^tag/$', view_tags),
    (r'^user/(?P<user>[a-zA-Z0-9_.-]+)/$', view_user_items),
    (r'^search/$', search),
    (r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}), 
    (r'^comments/', include('blogmaker.comments.urls')),
    (r'^tools/', include('blogmaker.blog.urls_tools')),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\w{1,2})/$', extras_day, dict(info_dict, month_format='%m')),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', object_detail, dict(info_dict, slug_field='slug', month_format='%m', allow_future=False)),
    (r'^\d{4}/\d{2}/\d{1,2}/(?P<slug>[-\w]+)/trackback/$', trackback),
    (r'^\d{4}/\d{2}/\d{1,2}/(?P<slug>[-\w]+)/postTrackbacks/$', postTrackbacks),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', archive_month, dict(info_dict, month_format='%m')),
    (r'^(?P<year>\d{4})/$', archive_year, dict(info_dict, make_object_list=True)),
    (r'^$', archive_index, dict(info_dict, num_latest=5, date_field='pub_date')),
)

