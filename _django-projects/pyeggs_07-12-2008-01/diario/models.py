# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: models.py 110 2008-02-26 00:47:47Z semente $
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
Models definitions for Diário.
"""

from datetime import datetime

from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import gettext_lazy as _

from diario.utils import markuping
from diario.managers import PublishedManager, CurrentSitePublishedManager
from diario.settings import DIARIO_DEFAULT_MARKUP_LANG, HAS_TAG_SUPPORT


MARKUP_CHOICES = (
    ('markdown', 'Markdown'),
    ('rest',     'reStructuredText'),
    ('textile',  'Textile'),
    ('raw',      _('Raw text')),
)

ADMIN_FIELDS = ['title', 'slug', 'pub_date', 'body_source', 'tags', 'is_draft']

if HAS_TAG_SUPPORT:
    from tagging.fields import TagField
else:
    ADMIN_FIELDS.remove('tags')

_default_date = datetime.now()

class Entry(models.Model):
    """A weblog entry."""

    title = models.CharField(_('title'), maxlength=100) # , max_length=100
    slug = models.SlugField(
        _('slug'),
        unique_for_date='pub_date',
        prepopulate_from=('title',),
        help_text=_('Automatically built from the title. A slug is a short '
                    'label generally used in URLs.'),
    )
    body_source = models.TextField(_('body'))
    body = models.TextField(
        _('body in raw HTML'),
        blank=True,
        editable=False,
    )
    markup = models.CharField(
        _('markup language'),
        default=DIARIO_DEFAULT_MARKUP_LANG,
        maxlength=8,
        choices=MARKUP_CHOICES,
        radio_admin=True,
        help_text=_('Uses "Raw text" if you want enter directly in HTML (or '
                    'apply markup in other place).'),
    )
    is_draft = models.BooleanField(
        _('draft'),
        default=False,
        help_text=_('Drafts are not published.'),
    )
    pub_date = models.DateTimeField(
        _('date published'),
        default=_default_date,
        help_text=_('Entries in future dates are only published on '
                    'correct date.'),
    )
    publish_on = models.ManyToManyField(Site, verbose_name=_('publish on'))

    if HAS_TAG_SUPPORT:
        tags = TagField(blank=True)

    # managers
    objects   = models.Manager()
    published = PublishedManager()
    on_site   = CurrentSiteManager('publish_on')
    published_on_site = CurrentSitePublishedManager('publish_on')

    class Meta:
        get_latest_by = 'pub_date'
        ordering      = ('-pub_date',)
        verbose_name  = _('entry')
        verbose_name_plural = _('entries')

    class Admin:
        list_display  = ('title', 'pub_date', 'is_draft')
        list_filter   = ('is_draft', 'publish_on', 'markup')
        search_fields = ['title', 'slug', 'body']
        date_hierarchy = 'pub_date'
        fields = (
            (None, {'fields': ADMIN_FIELDS}),
            (_('Other options'), {
                'classes': 'collapse',
                'fields': ('markup', 'publish_on'),
            })
        )

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('diario-entry', None, {
            'year' : str(self.pub_date.year),
            'month': str(self.pub_date.month).zfill(2),
            'day'  : str(self.pub_date.day).zfill(2),
            'slug' : str(self.slug)
        })

    def in_future(self):
        return self.pub_date > datetime.now()

# signals
from django.db.models import signals
from django.dispatch import dispatcher

def entry_pre_save(sender, instance, signal, *args, **kwargs):
    try:
        # transform plain text markup in body_source to HTML
        instance.body = markuping(instance.markup, instance.body_source)
        # update instance's pub_date if entry was draft
        e = Entry.objects.get(id=instance.id)
        if e.is_draft:
            instance.pub_date = datetime.now()
    except Entry.DoesNotExist:
        pass

dispatcher.connect(entry_pre_save, signal=signals.pre_save, sender=Entry)
