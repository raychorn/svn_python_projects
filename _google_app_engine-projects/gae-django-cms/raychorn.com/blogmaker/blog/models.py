''' 
Copyright (c) 2006-2007, PreFab Software Inc.

Copyright (c) 2006, Andrew Gwozdziewycz <apgwoz@gmail.com>
All rights reserved.
'''


import datetime, logging, re, socket, threading, xmlrpclib

from django.db import models 
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.markup.templatetags.markup import markdown
from django.conf import settings
from django.utils.html import strip_tags

from blogmaker.util import expand_shortcuts, strip_domain_and_rest, unescape
import blogmaker.blog.trackback_client as tc

################################### Ping URL ###########################################

# Thanks to http://www.imalm.com/blog/2007/feb/10/using-django-signals-ping-sites-update/
# for this code!

class PingUrl(models.Model): 
    ping_url = models.URLField(verify_exists=False)
    blog_url = models.URLField(verify_exists=False)
    blog_name = models.CharField(maxlength=200)
    
    class Admin:
        list_display = ('ping_url','blog_url', 'blog_name')

        
    @staticmethod
    def pingAll():
        def _pingAll():
            oldTimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(30)
            for pingObj in PingUrl.objects.all():
              try:
                  s = xmlrpclib.Server(pingObj.ping_url) 
                  reply = s.weblogUpdates.ping(pingObj.blog_name, pingObj.blog_url)
              except:
                  logging.error('Ping failed for ' + pingObj.ping_url, exc_info=True)
            socket.setdefaulttimeout(oldTimeout)
            
        threading.Thread(target=_pingAll).start()


################################### Tag ###########################################

class Tag(models.Model):
    tag = models.CharField(maxlength=255, core=True, help_text="Use single words only, no spaces!")
    
    class Admin:
        pass

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return '%stag/%s/' % (settings.BLOG_ROOT, self.tag)


################################### Entry ###########################################

class EntryManager(models.Manager):
    def current_active(self):
        ''' A QuerySet of all active entries before the current date/time '''
        
        # Note: The value of 'now' is cached in the returned QuerySet
        # so don't cache and reuse the QuerySet itself
        now = datetime.datetime.now()
        return self.filter(active=True).exclude(pub_date__gt=now)
        
    def index_blog(self):
    	''' The most recent entry object with truncated body '''
    	blog_entry = self.current_active()[0]
    	body = blog_entry.body
    	body = markdown(body)
    	body = expand_shortcuts(body)
    	body = body.replace('<span class="info_icon">i</span>', '')
    	body = re.split('<(hr|table|blockquote|div)', body)[0]
    	body = strip_tags(body)
    	body = body.split()
    	body = ' '.join(body[:15])
    	body = "%s ..." % body.strip()
    	
    	return blog_entry.headline, body
    

class Entry(models.Model):

    objects = EntryManager()
    
    pub_date = models.DateTimeField(db_index=True)
    slug = models.SlugField(unique_for_date='pub_date', prepopulate_from=('headline',),
        maxlength=120, help_text="Slug is the same as headline, but with dashes for spaces")
    headline = models.CharField(maxlength=255)
    summary = models.CharField(maxlength=255, null=True, blank=True, help_text="Leave this field blank")
    image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    copyright = models.CharField(maxlength=255, null=True, blank=True, help_text="Choose an image file and input any attribution info")
    body = models.TextField()
    active = models.BooleanField(default=True, help_text="Is post viewable on site?")
    user = models.ForeignKey(User, default=settings.DEFAULT_BLOG_USER, related_name="user_entries")
    tags = models.ManyToManyField(Tag, blank=True)
    related_entries = models.ManyToManyField("self", blank=True, symmetrical=False)
    externalId = models.IntegerField(blank=True, null=True)

    class Admin:
        list_display = ('slug', 'headline', 'pub_date', 'image')
        fields = (
            ('Essentials', {
                'fields': ('headline',
                		'slug',
                        'pub_date',
                        ('image', 'copyright'),
                        'body',
                        'tags',
                        'related_entries',
                        'user',
                        'active',
                       ),
             }),
            ('Optional', {
                'classes': 'collapse',
                'fields': ('summary', 'externalId'
                           ),
            }),
            )
        
        js = [(settings.BLOG_MEDIA_PREFIX + 'js/jquery.js'), (settings.BLOG_MEDIA_PREFIX + 'js/entry_change_form.js')]
        save_on_top = True
                       

    class Meta:
        get_latest_by = "pub_date"
        ordering = ['-pub_date']
        verbose_name_plural = "entries"

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return '%s%s/%s/' % (settings.BLOG_ROOT, self.pub_date.strftime('%Y/%m/%d'), self.slug)

    def get_tags(self):
        return self.tags.all()

    def get_related_entries(self):
        return self.related_entries.all()

    anchorRe = re.compile(r'''<a [^>]*>''', re.DOTALL)
    hrefRe = re.compile(r'''href=['"](http.*?)['"]''')
    markdownAnchorRe = re.compile(r'\[[^\]]+\]\((http[^\s)]+)', re.DOTALL)
    
    @property
    def links(self):
        ''' Return a list of the target href of all links in this entry '''
        links = set()
        
        # <a> tags
        for anchor in self.anchorRe.findall(self.body):
            m = self.hrefRe.search(anchor)
            if m:
                links.add(m.group(1))
        
        # Markdown links
        links.update(anchor for anchor in self.markdownAnchorRe.findall(self.body))
        
        return links

    @property
    def excerpt(self):
        ''' A brief excerpt for trackbacks '''
        return unescape(strip_tags(expand_shortcuts(markdown(self.body))).decode('utf-8'))[:200]

    def save(self):
        models.Model.save(self)
        self.update_trackbacks()
        if (self.active):
            PingUrl.pingAll()

    # Don't send trackbacks to any of these sites
    _dontTrackbackSites = set('google.com technorati.com alexa.com quantcast.com'.split())
    
    def update_trackbacks(self):
        ''' Update the current list of trackbacks to match the current links '''
        trackbacksToDelete = dict((tb.link, tb) for tb in self.trackbacks.all())
        for link in self.links:
            if link in trackbacksToDelete:
                # Link has a trackback, keep it
                del trackbacksToDelete[link]
            else:
                host, rest = strip_domain_and_rest(link)
                
                # Skip known don't trackback sites
                if host in self._dontTrackbackSites:
                    continue
                # Skip links with no path info or just /blog/
                if rest in ('/', '/blog'):
                    continue
                    
                # Create a new trackback for this link
                self.trackbacks.create(link=link)
        
        # Delete trackbacks that no longer have links unless they have some status
        for tb in trackbacksToDelete.values():
            if tb.status == 'NotYet':
                tb.delete()
                
            
    @staticmethod
    def entryCreateOrUpdate(pub_date, headline, body, user, externalId, active=True):
    	    
    	lowerHeadline = headline.lower()
    	slug = re.sub(' & ', '-and-', lowerHeadline)
    	slug = re.sub(r'[\s/\?]+', '-', slug)
    	slug = re.sub(r'[^\w.:~-]', '', slug)
    	try:
    		entry = Entry.objects.get(externalId=externalId)
    	except:
    		entry = Entry(externalId=externalId)
    	entry.slug = slug
    	entry.headline = headline
    	entry.body = body
    	entry.pub_date = pub_date
    	entry.user = User.objects.get(id=user)
    	entry.active = active
    	
    	entry.save()


################################### Trackback Status ###########################################

class TrackbackStatus(models.Model):
    ''' This model holds status for trackbacks from our entries. In other words it
        represents outgoing trackbacks.
    '''
    # Note: If entry is marked edit_inline, deleting a link in an entry will not be
    # able to delete the corresponding TrackbackStatus because it will be added back
    # in by the admin save handler
    
    #: The entry for which the trackback was posted
    entry = models.ForeignKey(Entry, verbose_name='referring entry', related_name='trackbacks')
    
    #: The outside blog entry referenced from our entry
    link = models.URLField('entry link', maxlength=300, verify_exists=False, core=True)
    
    #: The link to post the trackback to
    trackbackUrl = models.URLField('trackback link', verify_exists=False, blank=True)

    #: Datetime of most recent trackback attempt
    attempted = models.DateTimeField(null=True, blank=True)
    
    #: Options for status
    statusChoices = (
        ('NotYet', 'Not attempted'),
        ('NoLink', 'No trackback URL found'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Dont', 'Do not attempt'),
    )
    
    #: Result of most recent trackback attempt
    status = models.CharField(maxlength=10, blank=False, choices=statusChoices, default='NotYet')
    
    @property
    def eligible(self):
        ''' Is this trackback eligible to be attempted? '''
        return (self.status=='NotYet'
            or (self.status=='Failed' and 'Throttled' in self.message)
            or (self.status=='NoLink' and self.trackbackUrl))
        
    #: Additional status info e.g. error message received
    message = models.TextField('additional status', blank=True)
    
    class Admin:
        list_display = 'link status attempted message'.split()

    class Meta:
        verbose_name_plural='trackbacks'
        ordering = ('link',)

    def __str__(self):
        return '%s (%s)' % (self.link, self.status)


    def appendMessage(self, message):
        if self.message:
            self.message = self.message + '\n' + message
        else:
            self.message = message
            
            
    def attempt(self):
        ''' Attempt to post this trackback if it is eligible.
            Sets our status code and message.
        '''
        if not self.eligible:
            # Don't retry
            return
        
        self.attempted = datetime.datetime.now()
        self.message= ''
        
        try:
            # Get the trackback URL
            if not self.trackbackUrl:
                self.trackbackUrl, self.page_data = tc.discover(self.link)
                if self.trackbackUrl is None:
                    # Try appending /trackback/
                    self.appendMessage('Using /trackback/')
                    if self.link.endswith('/'):
                        self.trackbackUrl = self.link + 'trackback/'
                    else:
                        self.trackbackUrl = self.link + '/trackback/'
            
            if self.trackbackUrl:
                # Do the actual trackback
                siteName = Site.objects.get(id=settings.SITE_ID).name
                tc.postTrackback(self.trackbackUrl, self.entry.get_absolute_url(), self.entry.headline, self.entry.excerpt, siteName)
                self.status = 'Success'
            else:
                self.status = 'NoLink'
                        
        except Exception, e:
            self.status = 'Failed'
            msg = '%s: %s' % (e.__class__.__name__, e)
            # Ensure valid utf-8 with possibly some minor data loss
            msg = msg.decode('utf-8', 'replace').encode('utf-8')
            self.appendMessage(msg)

        self.save()
        
    
    @staticmethod
    def attempt_all_current():
        ''' Attempt to trackback all eligible trackback whose Entries are current. '''
        now = datetime.datetime.now()
        oneWeekAgo = now - datetime.timedelta(days=7)
        for tb in TrackbackStatus.objects.exclude(entry__pub_date__gt=now).exclude(entry__pub_date__lt=oneWeekAgo):
            tb.attempt()
