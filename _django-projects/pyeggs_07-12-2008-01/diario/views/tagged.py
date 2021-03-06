# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: tagged.py 92 2008-01-23 04:55:17Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2008 Guilherme Mesquita Gondim
#  Copyright (c) 2007 Eric Moritz
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


from django.http import Http404
from django.views.generic.list_detail import object_list

from tagging.models import Tag
from tagging.utils import get_tag
from diario.models import Entry


def tagged_entry_list(request, tag, related_tags=False,
                      related_tag_counts=True, **kwargs):
    """
    NOTE: This method is deprecated, use tagging.views.tagged_object_list
          instead.
    
    A thin wrapper around
    ``django.views.generic.list_detail.object_list`` which creates a
    ``QuerySet`` containing instances of entries tagged with
    the given tag.

    In addition to the context variables set up by ``object_list``, a
    ``tag`` context variable will contain the ``Tag`` instance
    for the given tag.

    If ``related_tags`` is ``True``, a ``related_tags`` context variable
    will contain tags related to the given tag for the given model.
    Additionally, if ``related_tag_counts`` is ``True``, each related tag
    will have a ``count`` attribute indicating the number of items which
    have it in addition to the given tag.
    """
    import warnings
    warnings.warn("diario.views.tagged.tagged_entry_list view is deprecated. "
                  "Use tagging.views.tagged_object_list instead.",
                  DeprecationWarning)

    if tag is None:
        try:
            tag = kwargs['tag']
        except KeyError:
            raise AttributeError(u'tagged_object_list must be called with a tag.')

    tag_instance = get_tag(tag)
    
    if tag_instance is None:
        raise Http404(u'No Tag found matching "%s".' % tag)

    queryset = Entry.published_on_site.tagged(tag_instance)
    
    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}
    kwargs['extra_context']['tag'] = tag_instance
    
    if related_tags:
        kwargs['extra_context']['related_tags'] = \
            Tag.objects.related_for_model(tag_instance, model,
                                          counts=related_tag_counts)
    return object_list(request, queryset, **kwargs)
