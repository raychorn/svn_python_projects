from django.contrib.sitemaps import Sitemap

import urllib
import logging
import datetime

class SampleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def __init__(self, entries):
        self.entries = entries

    def items(self):
        return self.entries

    def lastmod(self, obj):
        return updated_as_timestamp(obj.updated)

    def location(self, obj):
        return '/sitemap/%s/'%(urllib.quote_plus(obj.link))
    
sitemaps = {
    'entries': SampleSitemap(),
}

