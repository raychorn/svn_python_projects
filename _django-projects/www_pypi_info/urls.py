from django.conf.urls.defaults import *
from views import default
from vyperlogix.django.static import django_static
from vyperlogix.django import django_utils
from django.conf import settings
from downloads import default as downloads

from feeds import models as feed_models

from django.contrib.sitemaps import Sitemap

from vyperlogix.django.decorators import cache

from vyperlogix.misc import _utils

import sqlalchemy_model

import urllib

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return sqlalchemy_model.frontpage_items()

    def lastmod(self, obj):
        return obj.Jos_Content.created

    def location(self, obj):
        return '/view/article/%d/' % (obj.Jos_Content.id)
    
class DownloadsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return downloads.fetch_remote_token(downloads.TokenOptions.rawlist)

    def lastmod(self, obj):
        return _utils.today_localtime()

    def location(self, obj):
        return '/downloads/%s/' % (urllib.quote_plus(obj))
    
class PyPISitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0

    def items(self):
        return feed_models.PyPI.objects.all()

    def lastmod(self, obj):
        return obj.timestamp

    def location(self, obj):
        return '/view/pypi-feed/%d/' % (obj.id)

#'blog': BlogSitemap(),
sitemaps = {
    'downloads': DownloadsSitemap(),
    'pypi': PyPISitemap(),
}

from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import add_domain
from django.conf import settings

from vyperlogix.classes.CooperativeClass import Cooperative

class PypiFeed(Cooperative,Feed):

    feed_type = feedgenerator.Rss201rev2Feed

    title_template = None
    description_template = None

    def categories(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        categories as iterable over strings.
        """
        return []

    def items(self, obj):
        """
        Takes the object returned by get_object() and returns a list of
        items to publish in this feed.
        """
        return []

    def get_object(self, bits):
        """
        Takes a list of strings gleaned from the URL and returns an object
        represented by this feed. Raises
        django.core.exceptions.ObjectDoesNotExist on error.
        """
        return ''

    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        return ''

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return ''

    def item_author_email(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        author's e-mail as a normal Python string.
        """
        return ''

    def item_author_link(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        author's URL as a normal Python string.
        """
        return ''

    def item_enclosure_url(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        enclosure URL.
        """
        return ''

    def item_enclosure_length(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        enclosure length.
        """
        return ''

    def item_enclosure_mime_type(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        enclosure mime type.
        """
        return ''

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return ''

    def item_categories(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        categories.
        """
        return ''

    def item_copyright(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        copyright notice as a normal Python string.
        """
        return ''

class RssSiteNewsFeed(PypiFeed):
    title = "Your 21st Century Premier Python Information News (www.pypi.info)"
    link = '/sitenews/'
    copyright = "(c). Copyright %s, www.pypi.info, All Rights Reserved." % (_utils.timeStamp(format='%Y'))
    description = 'Your Premier Python Information Source (www.pypi.info), %s' % (copyright)

    title_template = 'rss/title.html'
    description_template = 'rss/description.html'
    
    def __get_dynamic_attr(self, attname, obj, default=None):
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default
        if callable(attr):
            if hasattr(attr, 'func_code'):
                argcount = attr.func_code.co_argcount
            else:
                argcount = attr.__call__.func_code.co_argcount
            if argcount == 2: # one argument is 'self'
                return attr(obj)
            else:
                return attr()
        return attr

    def get_feed(self, url=None):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raises FeedDoesNotExist for invalid parameters.
        """
        if url:
            try:
                obj = self.get_object(url.split('/'))
            except (AttributeError, ObjectDoesNotExist):
                raise FeedDoesNotExist
        else:
            obj = None

        current_site = Site.objects.get_current()
        link = self.__get_dynamic_attr('link', obj)
        link = add_domain(current_site.domain, link)

        feed = self.feed_type(
            title = self.__get_dynamic_attr('title', obj),
            link = link,
            description = self.__get_dynamic_attr('description', obj),
            language = settings.LANGUAGE_CODE.decode(),
            feed_url = add_domain(current_site, self.__get_dynamic_attr('feed_url', obj)),
            author_name = self.__get_dynamic_attr('author_name', obj),
            author_link = self.__get_dynamic_attr('author_link', obj),
            author_email = self.__get_dynamic_attr('author_email', obj),
            categories = self.__get_dynamic_attr('categories', obj),
            feed_copyright = self.__get_dynamic_attr('feed_copyright', obj),
        )

        for item in self.__get_dynamic_attr('items', obj):
            link = add_domain(current_site.domain, self.__get_dynamic_attr('item_link', item))
            enc = None
            enc_url = self.__get_dynamic_attr('item_enclosure_url', item)
            if enc_url:
                enc = feedgenerator.Enclosure(
                    url = enc_url.decode('utf-8'),
                    length = str(self.__get_dynamic_attr('item_enclosure_length', item)).decode('utf-8'),
                    mime_type = self.__get_dynamic_attr('item_enclosure_mime_type', item).decode('utf-8'),
                )
            author_name = self.__get_dynamic_attr('item_author_name', item)
            if author_name is not None:
                author_email = self.__get_dynamic_attr('item_author_email', item)
                author_link = self.__get_dynamic_attr('item_author_link', item)
            else:
                author_email = author_link = None
            try:
                feed.add_item(
                    title = self.__get_dynamic_attr('item_title', item),
                    link = link,
                    description = self.__get_dynamic_attr('item_descr', item),
                    unique_id = link,
                    enclosure = enc,
                    pubdate = self.__get_dynamic_attr('item_pubdate', item),
                    author_name = author_name,
                    author_email = author_email,
                    author_link = author_link,
                    categories = self.__get_dynamic_attr('item_categories', item),
                    item_copyright = self.__get_dynamic_attr('item_copyright', item),
                )
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                pass
        return feed
    
    @cache.cache(settings.CACHE_TIMER)
    def items(self):
        return sqlalchemy_model.agent.asSmartObjects(sqlalchemy_model.frontpage_items_qry().slice(0,20))

    def item_title(self, item):
        return _utils.ascii_only(item.Jos_Content.title)
    
    def item_descr(self, item):
        return _utils.ascii_only(item.Jos_Content.introtext)
    
    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        try:
            return '/view/article/%s/' % (item.Jos_Content.id if (item.has_key('Jos_Content')) else item.id)
        except AttributeError:
            pass

    def get_user_for_item(self, item):
        aUser = None
        try:
            if (self.aUser):
                self.aUser = aUser = self.aUser
        except AttributeError:
            users = sqlalchemy_model.user_by_id(item.Jos_Content.created_by if (item.has_key('Jos_Content')) else item.created_by)
            if (users):
                self.aUser = aUser = users[0]
        return aUser
    
    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        _name = ''
        aUser = self.get_user_for_item(item)
        try:
            _name = aUser.name
        except:
            pass
        return _name

    def item_author_email(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's e-mail as a normal Python string.
        """
        _email = ''
        aUser = self.get_user_for_item(item)
        try:
            _email = aUser.email
        except:
            pass
        return _email

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.Jos_Content.publish_up if (item.has_key('Jos_Content')) else item.publish_up

    def item_categories(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        categories.
        """
        cats = []
        if (item.has_key('Jos_Categories')):
            cat_id = int(item.Jos_Categories.id)
            sect_id = int(item.Jos_Categories.section)
            aCategory = sqlalchemy_model.category_by_id(cat_id)
            aSection = sqlalchemy_model.section_by_id(sect_id)
            try:
                cats.append('%s:%s' % (aCategory.title,aSection.title))
            except:
                pass
        return cats

    def item_copyright(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        copyright notice as a normal Python string.
        """
        return self.copyright

class PypiChronoFeed(RssSiteNewsFeed):

    def __init__(self, feed_url,num=-1,month=-1,year=-1):
        self.month = int(month) if (str(month).isdigit()) else month
        self.year = int(year) if (str(year).isdigit()) else year
        toks = str(num).split('/')
        if (len(toks) > 1) and (str(toks[-1]).isdigit()):
            num = toks[-1]
        self.num = int(num) if (str(num).isdigit()) else num
        super(PypiChronoFeed, self).__init__('', feed_url)

class RssSiteChronoNewsFeed(PypiChronoFeed):
    def items(self):
        if (self.month == -1) and (self.year == -1):
            return super(RssSiteChronoNewsFeed, self).items()
        items = sqlalchemy_model.frontpage_items_qry(self.month,self.year).all()
        return sqlalchemy_model.agent.asSmartObjects(items)

class RssSiteRecentNewsFeed(PypiChronoFeed):
    def items(self):
        items = sqlalchemy_model.frontpage_items_qry(self.month,self.year).slice(0,20 if (self.num == -1) else self.num if (self.num > 5) else 5)
        return sqlalchemy_model.agent.asSmartObjects(items)

class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = feedgenerator.Atom1Feed
    
class PypiPackageIndexFeed(RssSiteNewsFeed):
    
    title = "Your 21st Century Premier Python Package Index Information Feed (www.pypi.info)"
    
    def __init__(self, feed_url,num=-1,month=-1,year=-1):
        self.month = int(month) if (str(month).isdigit()) else month
        self.year = int(year) if (str(year).isdigit()) else year
        toks = str(num).split('/')
        if (len(toks) > 1) and (str(toks[-1]).isdigit()):
            num = toks[-1]
        self.num = int(num) if (str(num).isdigit()) else num
        super(PypiPackageIndexFeed, self).__init__('', feed_url)
        
    def items(self):
        return feed_models.PyPI.objects.all()

    def item_title(self, item):
        return '%s %s' % (item.name,item.version)
    
    def item_descr(self, item):
        return item.descr
    
    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        try:
            return '/view/pypi-feed/%d/' % (item.id)
        except AttributeError:
            pass

    def get_user_for_item(self, item):
        aUser = None
        return aUser
    
    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        _name = ''
        return _name

    def item_author_email(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's e-mail as a normal Python string.
        """
        _email = ''
        return _email

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.timestamp

    def item_categories(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        categories.
        """
        cats = []
        return cats

    def item_copyright(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        copyright notice as a normal Python string.
        """
        return self.copyright

feeds = {
    'rss': RssSiteChronoNewsFeed,
    'rss2': RssSiteRecentNewsFeed,
    'rss-pypi': PypiPackageIndexFeed,
    'atom': AtomSiteNewsFeed,
}

from django.contrib.syndication import feeds as syndicationFeeds
from django.http import HttpResponse, Http404

def chronoFeed(request, url, feed_dict=None, num=-1, month=-1, year=-1):
    if not feed_dict:
        raise Http404, "No feeds are registered."

    try:
        f = feed_dict[url]
    except KeyError:
        raise Http404, "Url %r isn't registered." % url

    try:
        feedgen = f(request.path,num=num,month=month,year=year).get_feed('')
    except syndicationFeeds.FeedDoesNotExist:
        raise Http404, "Invalid feed parameters. Slug %r is valid, but other parameters, or lack thereof, are not." % slug

    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response

urlpatterns = patterns('',
    # Example:
    (r'^about/', default.about),
    #(r'^view/', default.view),
    #(r'^section/', default.view),
    #(r'^category/', default.view),
    #(r'^doc_download/', default.doc_download),
    #(r'^search/', default.search),
    (r'^grid/', default.grid),
    (r'^login/', default.login),
    (r'^change/', default.login),
    (r'^register/', default.login),
    (r'^subscribe/', default.login),
    (r'^forgot/', default.login),
    (r'^logout/', default.login),
    (r'^problems/', default.problems),
    #(r'^download/', default.download),
    (r'^pypi/', default.pypi),
    (r'^downloads/', downloads.downloads),
    (r'^remote-count/', downloads.remote_count),
    (r'^remote-list/', downloads.remote_list),
    (r'^pypi-rss/', default.pypi_rss),

    (r'^administrator/', default.administrator),

    (r'^feeds/(?P<url>.*)/(?P<month>\d{2})/(?P<year>\d{4})/$', chronoFeed, {'feed_dict': feeds}),
    (r'^feeds/(?P<url>.*)/(?P<num>\d+)/$', chronoFeed, {'feed_dict': feeds}),
    (r'^feeds/(?P<url>.*)/$', chronoFeed, {'feed_dict': feeds}),
    (r'^feeds/', default.feeds),
    (r'^index.php$', default.feeds),
    
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^static/', django_static.static),    # this is intercepted and handled by cherokee
    (r'.*', default.default),
)

