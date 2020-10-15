# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
from images.views import image
from myapp.views import create_admin_user
from blog.views import default
from facebook.views import default as default_facebook
from about.views import default as default_about
from django.contrib import admin

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from vyperlogix.misc import _utils

admin.autodiscover()

class RssEntriesFeed(Feed):
    title = "RayCHorn.Com News Feed"
    link = "/feed/"
    description = "Updates on changes and additions to RayCHorn.Com."

    title_template = 'rss_title_template.html'
    description_template = 'rss_description_template.html'
    
    def items(self):
        return [] #Entry.all().order('-publish_on')[:20]

    def item_link(self, item):
        return item.Location()
    
    def item_author_name(self, item):
        return '' # Not Yet Implemented
    
    def item_author_email(self, item):
        return '' # Not Yet Implemented

    def item_author_link(self, item):
        return '' # Not Yet Implemented

    def item_pubdate(self, item):
        return item.publish_on

    def item_guid(self, item):
        return item.id

    def item_categories(self, item):
        return item.Category()

    def item_copyright(self, item):
        return '&copy; Copyright %s, RayCHorn.Com, Creative Commons Attribution Share Alike 3.0 (http://creativecommons.org/licenses/by-sa/3.0/)'

class AtomEntriesFeed(RssEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesFeed.description
    
feeds = {
    'rss': RssEntriesFeed,
    'atom': AtomEntriesFeed,
}

handler500 = 'ragendja.views.server_error'

urlpatterns = auth_patterns + patterns('',
                                       ('^admin/(.*)', admin.site.root),
                                       ('^get-image/(.*)', image),
                                       ('^create_admin_user/', create_admin_user),
                                       #(r'^login/$', 'django.views.generic.simple.direct_to_template', {'template': 'registration/login.html'}),
                                       #(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main.html'}),
                                        (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
                                       #(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                                       ('^facebook[/]?$', default_facebook),
                                       ('^about[/]?$', default_about),
                                       ('^cancel/$', 'django.views.generic.simple.direct_to_template', {'template': 'payment-cancel.html'}),
                                       ('^success/$', 'django.views.generic.simple.direct_to_template', {'template': 'payment-success.html'}),
                                       (r'.*', default),
) + urlpatterns
