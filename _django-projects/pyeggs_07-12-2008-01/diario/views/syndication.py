# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: syndication.py 114 2008-02-26 02:49:35Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2008 Guilherme Mesquita Gondim
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#

from django.contrib.syndication import feeds
from django.http import Http404, HttpResponse

def feed(request, slug, tag='', feed_dict=None):
    """
    FIXME: documment this.
    """
    if not feed_dict:
        raise Http404, "No feeds are registered."

    try:
        feed = feed_dict[slug]
    except KeyError:
        raise Http404, "Slug %r isn't registered." % slug

    try:
        feedgen = feed(slug, request).get_feed(tag)
    except feeds.FeedDoesNotExist:
        raise Http404, "Invalid feed parameters. Slug %r is valid, but tag," +\
            " or lack thereof, are not." % slug

    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response
