# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id$
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

from django.views.generic.date_based import object_detail
from diario.models import Entry

def entry_detail(request, *args, **kwargs):
    """
    A thin wrapper around ``django.views.generic.date_based.object_detail``
    which creates a ``QuerySet`` containing drafts and future entries if
    user has permission to change entries (``diario.change_entry``).

    This is useful for preview entries with your own templates and CSS.

    Tip: Uses the *View on site* button in Admin interface to access yours
    drafts and entries in future.
    """
    if request.user.has_perm('diario.change_entry'):
        kwargs['allow_future'] = True
        kwargs['queryset'] = Entry.on_site.all()
    return object_detail(request, *args, **kwargs)
