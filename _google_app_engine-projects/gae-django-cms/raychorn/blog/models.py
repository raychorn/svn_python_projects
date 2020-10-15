from google.appengine.ext import db
from google.appengine.ext import search

from vyperlogix.google.gae import unique

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

clean_up_title = lambda s:''.join([ch for ch in str(s) if (str(ch).isalnum()) or (ch in ['-'])])
_location_title = lambda title:'-'.join([s for s in [clean_up_title(t) for t in title.split()] if (len(s) > 0)])
normalized_className = lambda obj:'/'.join([c.lower() for c in ObjectTypeName.typeClassName(obj).split('.')[-3:] if (c.lower() != 'models')])
location_title = lambda obj:'/%s/%s/%s/%s/'%(normalized_className(obj),'/'.join(_utils.getAsSimpleDateStr(obj.timestamp,str(_utils.formatDate_YYYYMMDD_dashes())).split('-')),obj.LocationTitle(),obj.id)

class Tag(unique.UniqueModel):
    title = db.StringProperty(required=True, verbose_name=_('title'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (title,)
                    ])

    @classmethod
    def create(cls, title):
        w = Tag(title=title)
        w.save()
        return w

    def Location(self):
        return location_title(self)

    def LocationTitle(self):
        return _location_title(self.title)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Title(self):
        return self.title

    def __str__(self):
        return '"%s"' % (self.title)
    
class Category(unique.UniqueModel):
    title = db.StringProperty(required=True, verbose_name=_('title'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (title,)
                    ])

    @classmethod
    def create(cls, title):
        w = Category(title=title)
        w.save()
        return w

    def Location(self):
        return location_title(self)

    def LocationTitle(self):
        return _location_title(self.title)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Title(self):
        return self.title

    def __str__(self):
        return '"%s"' % (self.title)
    
class Language(unique.UniqueModel):
    title = db.StringProperty(required=True, verbose_name=_('title'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (title,)
                    ])

    @classmethod
    def create(cls, title):
        w = Language(title=title)
        w.save()
        return w

    def Location(self):
        return location_title(self)

    def LocationTitle(self):
        return _location_title(self.title)

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Title(self):
        return self.title

    def __str__(self):
        return '"%s"' % (self.title)
    
class Entry(unique.UniqueModel):
    title = db.StringProperty(required=True, verbose_name=_('title'))
    teaser = db.TextProperty(required=False, verbose_name=_('teaser'))
    content = db.TextProperty(required=True, verbose_name=_('content'))
    views = db.FloatProperty(required=False, verbose_name=_('views'))
    tag =  db.ReferenceProperty(Tag,required=True, verbose_name=_('tag'))
    language =  db.ReferenceProperty(Language,required=False, verbose_name=_('language'))
    category =  db.ReferenceProperty(Category,required=True, verbose_name=_('category'))
    publish_on = db.DateTimeProperty(auto_now=False,required=False, verbose_name=_('publish_on'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (title,)
                    ])

    @classmethod
    def create(cls, title, content):
        w = Entry(title=title,content=content,views=views,tag=tag,language=language,category=category,publish_on=publish_on)
        w.save()
        return w

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def Location(self):
        return location_title(self)

    def Title(self):
        return self.title

    def LocationTitle(self):
        return _location_title(self.title)

    def Language(self):
        return ', '.join([item.title for item in self.language.all()])

    def Category(self):
        return ', '.join([item.title for item in self.category.all()])

    def Tag(self):
        return ', '.join([item.title for item in self.tag.all()])

    def Views(self):
        return ('%15.0f' % (self.views)) if (self.views) else ''

    def PublishOn(self):
        return _utils.getAsSimpleDateStr(self.publish_on,str(_utils.formatDjangoDateTimeStr())) if (self.publish_on) else ''

    def __str__(self):
        return '"%s"' % (self.title)
    
class Comment(db.Model):
    user = db.ReferenceProperty(User,required=True, verbose_name=_('user'))
    content = db.TextProperty(required=True, verbose_name=_('content'))
    entry =  db.ReferenceProperty(Entry,required=True, verbose_name=_('entry'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    def title(self):
        return self.entry.title

    def Title(self):
        return self.entry.title

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '"%s" at "%s"' % (self.entry.title,self.Timestamp())
    
class RssFeed(unique.UniqueModel):
    url = db.StringProperty(required=True, verbose_name=_('url'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (url,)
                    ])

    @classmethod
    def create(cls, url):
        w = RssFeed(url=url)
        w.save()
        return w

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '"%s"' % (self.url)
    
class Setting(unique.UniqueModel):
    name = db.StringProperty(required=True, verbose_name=_('name'))
    value = db.StringProperty(required=True, verbose_name=_('value'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (name,)
                    ])

    @classmethod
    def create(cls, name, value):
        w = Setting(name=name,value=value)
        w.save()
        return w

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '%s="%s"' % (self.name,self.value)
    
class Installation(unique.UniqueModel):
    domain = db.StringProperty(required=True, verbose_name=_('name'))
    timestamp = db.DateTimeProperty(auto_now=True, verbose_name=_('timestamp'))

    _uniques = set([
                    (domain,)
                    ])

    @classmethod
    def create(cls, domain):
        w = Setting(domain=domain)
        w.save()
        return w

    def Timestamp(self):
        return _utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr()))

    def __str__(self):
        return '%s' % (self.domain)
    
