# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: entries.py 107 2008-02-08 01:22:58Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007, 2008 Guilherme Mesquita Gondim
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""
URL definitions for weblog entries.
"""

from django.conf.urls.defaults import *
from diario.models import Entry
from diario.settings import DIARIO_NUM_LATEST


info_dict = {
    'queryset': Entry.published_on_site.all(),
    'template_object_name': 'entry',
}

urlpatterns = patterns('',
                      
    # diario entry detail
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view   = 'diario.views.entries.entry_detail',
        kwargs = dict(info_dict, slug_field='slug', month_format='%m', date_field='pub_date'),
        name   = 'diario-entry'
    ),

    # diario archive day
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\d{2})/$',
        view   = 'django.views.generic.date_based.archive_day',
        kwargs = dict(info_dict, month_format='%m', date_field='pub_date'),
        name   = 'diario-archive-day'
    ),

    # diario archive month
    url(
        regex  = '^(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        view   = 'django.views.generic.date_based.archive_month',
        kwargs = dict(info_dict, month_format='%m', date_field='pub_date'),
        name   = 'diario-archive-month'
     ),

    # diario archive year
    url(
        regex  = '^(?P<year>\d{4})/$',
        view   = 'django.views.generic.date_based.archive_year',
        kwargs = dict(info_dict, date_field='pub_date'),
        name   = 'diario-archive-year'
    ),

    # diario entry list
    url(
        regex  = '^$',
        view   = 'django.views.generic.list_detail.object_list',
        kwargs = dict(info_dict, paginate_by=DIARIO_NUM_LATEST),
        name   = 'diario-entry-list'
    ),
)
