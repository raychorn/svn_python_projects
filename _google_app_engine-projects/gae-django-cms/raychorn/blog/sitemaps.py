from django.contrib.sitemaps import Sitemap
from blog.models import Entry, Tag, Category, Language

import urllib
import logging
import datetime

from vyperlogix.misc import _utils

def isTimeFragment(timeString):
    import re
    _reTimeFrag = re.compile(r"((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))")
    matches = _reTimeFrag.search(timeString)
    return matches

def make_sense_of_time_string(timeString):
    import datetime
    now = datetime.datetime.today()
    dow = now.weekday()
    dow_offset = dow - 0 + 1
    delta = datetime.timedelta(dow_offset)
    now = now - delta
    a = []
    aa = []
    b = []
    bb = []
    for i in xrange(0,7):
        delta = datetime.timedelta(days=i)
        now = now + delta
        a.append(now.strftime('%a'))
        aa.append(now.strftime('%A'))
    moy = now.month
    moy_offset = moy - 1 + 1
    delta = datetime.timedelta(moy_offset*31)
    now = now - delta
    for i in xrange(1,13):
        delta = datetime.timedelta(31)
        now = now + delta
        b.append(now.strftime('%b'))
        bb.append(now.strftime('%B'))
    toks = timeString.split()
    fmt = []
    while (len(toks) > 0):
        t = toks[0]
        _found = False
        for foo in a:
            if (t.find(foo) > -1):
                tt = t.replace(foo,'')
                if (len(tt) < len(t)):
                    _found = True
                    break
        if (_found):
            fmt.append('%a'+tt)
            del toks[0]
            continue
        else:
            _found = False
            for foo in aa:
                if (t.find(foo) > -1):
                    tt = t.replace(foo,'')
                    if (len(tt) < len(t)):
                        _found = True
                        break
            if (_found):
                fmt.append('%A'+tt)
                del toks[0]
                continue
            else:
                _found = False
                for foo in b:
                    if (t.find(foo) > -1):
                        tt = t.replace(foo,'')
                        if (len(tt) < len(t)):
                            _found = True
                            break
                if (_found):
                    fmt.append('%b'+tt)
                    del toks[0]
                    continue
                else:
                    _found = False
                    for foo in bb:
                        if (t.find(foo) > -1):
                            tt = t.replace(foo,'')
                            if (len(tt) < len(t)):
                                _found = True
                                break
                    if (_found):
                        fmt.append('%B'+tt)
                        del toks[0]
                        continue
        if (t.isdigit()):
            if (len(t) == 2):
                v = int(t)
                if (v >= 1) and (v <= 12):
                    fmt.append('%m')
                    del toks[0]
                    continue
                elif (v >= 0) and (v <= 99):
                    fmt.append('%y')
                    del toks[0]
                    continue
            elif (len(t) == 4):
                fmt.append('%Y')
                del toks[0]
                continue
        fragments = isTimeFragment(t)
        if (fragments):
            frags = t.split(':')
            if (len(frags) == 3):
                frags[0] = frags[0] if (frags[0].isdigit()) else frags[0].split('T')[-1]
                v_frag = int(frags[0])
                _fmt = ''
                if (v_frag >= 0) and (v_frag <= 24):
                    _fmt += '%H'
                else:
                    _fmt += '%I'
                _fmt += ':%M:%S'
                fmt.append(_fmt)
                del toks[0]
                continue
        fmt.append('%Z')
        del toks[0]
        continue
    return ' '.join(fmt)

def updated_as_timestamp(updated):
    import re
    from vyperlogix.lists.ListWrapper import ListWrapper
    try:
        _reOtherDate = re.compile(r"(19|20)[0-9]{2}[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])T((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))\+(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?)")
        if (not isinstance(updated,datetime.datetime)):
            matches = _reOtherDate.search(updated)
            try:
                return _utils.getFromDateStr(updated.split('+')[0].strip(),format=_utils.formatMetaHeaderExpiresOn()) if (not matches) else _utils.getFromDateStr(updated.split('+')[0],format=_utils._formatTimeStr())
            except:
                return _utils.getFromDateStr(updated,format=_utils.formatMetaHeaderExpiresOnZ())
    except Exception, e:
        #info_string = _utils.formattedException(details=e)
        try:
            return _utils.getFromDateStr(updated.split('+')[0].strip(),format=_utils._formatTimeStr())
        except:
            fmt = make_sense_of_time_string(updated)
            try:
                return _utils.getFromDateStr(updated,format=fmt)
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                toks_fmt = fmt.split()
                toks = updated.split()
                if (toks_fmt[-1] == '%Z'):
                    del toks_fmt[-1]
                    del toks[-1]
                    updated = ' '.join(toks)
                    fmt = ' '.join(toks_fmt)
                try:
                    return _utils.getFromDateStr(updated,format=fmt)
                except Exception, e:
                    info_string = _utils.formattedException(details=e)
                    #logging.warning(info_string)
                pass
    return updated

class EntrySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Entry.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return obj.Location()
    
class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Tag.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return obj.Location()
    
class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Category.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return obj.Location()
    
class LanguageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Language.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return obj.Location()
    
class DynamicSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def __init__(self, entries):
        self.entries = entries

    def items(self):
        return self.entries

    def lastmod(self, obj):
        return updated_as_timestamp(obj.updated)

    def location(self, obj):
        return '/blog/sitemap/%s/'%(urllib.quote_plus(obj.link))
    
sitemaps = {
    'entries': EntrySitemap(),
    'tags': TagSitemap(),
    'categories': CategorySitemap(),
    'languages': LanguageSitemap(),
}

