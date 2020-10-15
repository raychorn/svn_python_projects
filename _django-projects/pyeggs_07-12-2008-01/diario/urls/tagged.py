# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: tagged.py 92 2008-01-23 04:55:17Z semente $
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


"""
URL definitions for weblog entries divided by tag.
"""

from django.conf.urls.defaults import *
from diario.models import Entry
from diario.settings import DIARIO_NUM_LATEST

info_dict = {
    'paginate_by': DIARIO_NUM_LATEST,
    'queryset_or_model': Entry.published_on_site.all(),
    'template_name': 'diario/entry_list_tagged.html',
    'template_object_name': 'entry',
}

urlpatterns = patterns(
    'tagging.views',

    # diario entries by tag
    url(
        regex  = '^(?P<tag>[^/]+)/$',
        view   = 'tagged_object_list',
        kwargs = info_dict,
        name   = 'diario-tagged-entry-list',
    ),
)
