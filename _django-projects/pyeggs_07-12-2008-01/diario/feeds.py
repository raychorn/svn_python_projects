# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: feeds.py 113 2008-02-26 01:33:33Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007 Guilherme Mesquita Gondim
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#

from django.conf import settings
from django.contrib.comments.models import FreeComment
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from diario.models import Entry
from diario.settings import HAS_TAG_SUPPORT

if HAS_TAG_SUPPORT:
    from tagging.models import Tag


class RssEntriesFeed(Feed):
    description = _('Latest entries on Weblog')
    title_template = 'feeds/diario_title.html'
    description_template = 'feeds/diario_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's Weblog") % {'title': self._site.name}

    def link(self):
        return reverse('diario-entry-list')

    def get_query_set(self):
        return Entry.published_on_site.order_by('-pub_date')

    def items(self):
        return self.get_query_set()[:15]

    def item_pubdate(self, item):
        return item.pub_date

    def item_categories(self, item):
        try:
            return item.tags.split()
        except AttributeError:
            pass      # ignore if not have django-tagging support

class AtomEntriesFeed(RssEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesFeed.description


class RssEntriesByTagFeed(RssEntriesFeed):
    def get_object(self, bits):
        # In case of "rss/tag/example/foo/bar/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def title(self, obj):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _('%(title)s\'s Weblog: entries tagged "%(tag name)s"') % \
               {'title': self._site.name, 'tag name': obj.name}

    def description(self, obj):
        return _('Latest entries for tag "%(tag name)s"') % \
               {'tag name': obj.name}

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return reverse('diario-tagged-entry-list', args=[obj.name])

    def get_query_set(self, obj):
        queryset = Entry.published_on_site.filter(tags__contains=obj.name)
        return queryset.order_by('-pub_date')

    def items(self, obj):
        return self.get_query_set(obj)[:15]

class AtomEntriesByTagFeed(RssEntriesByTagFeed):
    feed_type = Atom1Feed
    subtitle = RssEntriesByTagFeed.description

class RssFreeCommentsFeed(Feed):
    description = _('Latest comments on Weblog')
    title_template = 'feeds/comments_title.html'
    description_template = 'feeds/comments_description.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(title)s's Weblog comments") % \
               {'title': self._site.name}

    def link(self):
        return reverse('diario-entry-list')

    def item_pubdate(self, item):
        return item.submit_date

    def get_query_set(self):
        get_list_function = FreeComment.objects.filter
        kwargs = {
            'is_public': True,
            'site__pk': settings.SITE_ID,
            'content_type__app_label__exact': 'diario',
            'content_type__model__exact': 'entry',
        }
        return get_list_function(**kwargs)

    def items(self):
        return self.get_query_set()[:30]

class AtomFreeCommentsFeed(RssFreeCommentsFeed):
    feed_type = Atom1Feed
    subtitle = RssFreeCommentsFeed.description
