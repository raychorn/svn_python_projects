# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: sitemaps.py 107 2008-02-08 01:22:58Z semente $
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

from django.contrib.sitemaps import Sitemap
from diario.models import Entry

class DiarioSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5    

    def items(self):
        return Entry.published_on_site.all()

    def lastmod(self, obj):
        return obj.pub_date
