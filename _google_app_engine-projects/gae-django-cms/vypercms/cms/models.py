# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from google.appengine.ext import db

class UtcTzinfo(datetime.tzinfo):
    def utcoffset(self, dt): return datetime.timedelta(0)
    def dst(self, dt): return datetime.timedelta(0)
    def tzname(self, dt): return 'UTC'
    def olsen_name(self): return 'UTC'

class EstTzinfo(datetime.tzinfo):
    def utcoffset(self, dt): return datetime.timedelta(hours=+8)#set your utcoffset
    def dst(self, dt): return datetime.timedelta(0)
    def tzname(self, dt): return 'EST'
    def olsen_name(self): return 'US/Eastern'

class Globalvar(db.Model):
    name = db.StringProperty(required=True)
    value = db.StringProperty(required=True)
    description = db.StringProperty()

class Categories(db.Model):
    sort = db.IntegerProperty(default=0)
    display = db.IntegerProperty(default=1)
    name = db.StringProperty()

class Article(db.Model):
    cate = db.ReferenceProperty(Categories, required=True, collection_name='article_set')
    title = db.StringProperty(required=True)
    tags = db.StringListProperty()
    browse = db.IntegerProperty(default=1)
    author = db.ReferenceProperty(User, collection_name='author_set')
    pub_date = db.DateTimeProperty()
    
    def EST_time(self):
        self.pub_date = self.pub_date.replace(tzinfo=UtcTzinfo())
        return self.pub_date.astimezone(EstTzinfo())    

class ArticleContent(db.Model):
    content = db.TextProperty(required=True)
    
class Comment(db.Model):
    article = db.ReferenceProperty(Article, collection_name='comment_set')
    name = db.StringProperty(required=True)
    email = db.StringProperty()
    site = db.StringProperty()
    content = db.TextProperty(required=True)
    pub_date = db.DateTimeProperty(auto_now=True)
    
    def EST_time(self):
        self.pub_date = self.pub_date.replace(tzinfo=UtcTzinfo())
        return self.pub_date.astimezone(EstTzinfo())    

class Allad(db.Model):
    name = db.StringProperty(required=True)
    value = db.TextProperty()
    description = db.StringProperty()

class Links(db.Model):
    sort = db.IntegerProperty(default=0)
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True,default='http://')

class Redirect(db.Model):
    """http://xxxx.com/url/value"""
    value = db.StringProperty(required=True)
    redirto = db.StringProperty(required=True,default='http://')

class Slide(db.Model):
    title = db.StringProperty(default='')
    stitle = db.StringProperty(default='')
    link = db.StringProperty()
    imgsrc = db.StringProperty()
    pub_date = db.DateTimeProperty(auto_now=True)

class Photo(db.Model):
    filename = db.StringProperty()
    avatar = db.BlobProperty(required=True)

class Articleid(db.Model):
    idstr = db.TextProperty()

class Tag(db.Model):
    tag = db.StringProperty(multiline=False)
    tagcount = db.IntegerProperty(default=1)
