''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2006, Andrew Gwozdziewycz <apgwoz@gmail.com>
All rights reserved.
'''


from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

from blogmaker.blog.models import Entry, Tag 
import datetime

class blogmakerEntryFeed(Feed): 

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "%s" % self._site.name.title()
        
    def copyright(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        if not settings.COPYRIGHT:
            copyright = "copyright %s" % self._site.name.title()
        else:
            copyright = settings.COPYRIGHT
        return "%s" % copyright

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)
        
    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "Latest posts on %s" % self._site.name.title()

    def items(self):
        return Entry.objects.current_active().order_by('-pub_date')[:20]

    def item_pubdate(self, item):
        return item.pub_date
        
    def item_categories(self, item):
        all = item.tags.all()
        tags = []
        for tag in all:
            linked_tag = "<a href='%stag/%s/'>%s</a>" % (settings.BLOG_ROOT, tag.tag, tag.tag)
            tags.append(linked_tag)
        return tags
        
    def item_author_name(self, item):
        return item.user.first_name.title()


