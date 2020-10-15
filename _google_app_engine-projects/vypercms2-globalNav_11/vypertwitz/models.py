import pickle

from google.appengine.ext import db
from google.appengine.ext import search

from vyperlogix.google.gae import unique

from vyperlogix.misc import _utils

class WordType(unique.UniqueModel):
    word_type = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    _uniques = set([
                    (word_type,)
                    ])

    @classmethod
    def create(cls, word_type):
        w = WordType(word_type=word_type)
        w.save()
        return w

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Word_Type(self):
        return self.word_type

    def __str__(self):
        return '"%s"' % (self.word_type)
    
class Word(db.Model):
    word =  db.StringProperty(required=True)
    word_type =  db.ReferenceProperty(WordType,required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Word_Type(self):
        return self.word_type.word_type

    def __str__(self):
        return '"%s" (%s)' % (self.word,self.word_type)
    
class Link(unique.UniqueModel):
    url =  db.URLProperty(required=True)
    descr = db.StringProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now=True)

    _uniques = set([
                    (url,)
                    ])

    @classmethod
    def create(cls, url, descr):
        u = RssFeed(url=url, descr=descr)
        u.save()
        return u

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '"%s" (%s)' % (self.url,self.descr)
    
class RssFeed(db.Model):
    fid = db.StringProperty(required=False) # uuid value
    link =  db.ReferenceProperty(Link,required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    def save(self):
        import uuid
        if (self.fid == None) or (len(self.fid) == 0):
            self.fid = str(uuid.uuid4())
        super(RssFeed, self).save()

    def Link(self):
        return '%s, <small>(%s)</small>' % (self.link.descr,self.link.url)
    Link.allow_tags = True

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '%s "%s" (%s)' % (self.fid,self.link.url,self.link.descr)

class UsedLinkStat(unique.UniqueModel):
    feed =  db.ReferenceProperty(RssFeed,required=True)
    url =  db.URLProperty(required=True)
    count = db.FloatProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    _uniques = set([
                    (url,)
                    ])

    @classmethod
    def create(cls, feed, url, count):
        u = RssFeed(feed=feed, url=url, count=count)
        u.save()
        return u

    def Feed(self):
        return '%s' % (self.feed.link.descr)
    Feed.allow_tags = True

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '(%s) "%s" (%s)' % (self.feed,self.url,self.count)
    
class UsedLink(db.Model):
    feed =  db.ReferenceProperty(RssFeed,required=True)
    url =  db.URLProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now=True)

    def save(self):
        links = Link.all().filter('url',self.url)
        if (links.count() > 0):
            aLink = links[0]
            usedlinks = UsedLinkStats.all().filter('feed',self.feed).filter('link',aLink)
            if (usedlinks.count() == 0):
                aUsedLinkStat = UsedLinkStats(feed=self.feed,link=aLink,count=0)
                aUsedLinkStat.save()
            else:
                aUsedLinkStat = usedlinks[0]
                aUsedLinkStat.count = aUsedLinkStat.count+1
                aUsedLinkStat.save()
        super(UsedLink, self).save()
        
    def Feed(self):
        return '%s' % (self.feed.link.descr)
    Feed.allow_tags = True

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '"%s" (%s)' % (self.url,self.feed)
