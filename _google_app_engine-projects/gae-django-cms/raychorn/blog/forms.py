# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets, FormSetField

import models

from django.contrib.auth import authenticate

attrs_dict = { 'class': 'required' }
attrs_rss_feed_dict = { 'size':50, 'maxlength':256 }
attrs_verification_dict = { 'size':50, 'maxlength':256 }
attrs_domain_dict = { 'size':50, 'maxlength':256 }

combine_dicts = lambda a,b:dict([(k,v) for k,v in a.iteritems()]+[(k,v) for k,v in b.iteritems()])

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class CommentForm(forms.Form):
    """
    Form for providing comments.
    """
    comment = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),label=_(u'Comment'))
    recid = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, recid=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.base_fields['recid'].initial = recid

    def save(self, recid='', user=None):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('comment')):
            entries = [e for e in models.Entry.all() if (e.id == recid)]
            if (len(entries) > 0):
                aComment = models.Comment(content=self.cleaned_data['comment'],entry=entries[0],user=user)
                aComment.save()
                results['bool'] = True
                results['comment'] = aComment
            else:
                raise forms.ValidationError(_(u'Missing a record id - this is an error the typical user should never see.'))
        else:
            raise forms.ValidationError(_(u'You must enter a comment.'))
        return results

class RssForm(forms.Form):
    """
    Form for providing external rss links.
    """
    url = forms.CharField(widget=forms.TextInput(attrs=combine_dicts(attrs_dict,attrs_rss_feed_dict)),label=_(u'Rss Feed'))
    
    def __init__(self, recid=None, *args, **kwargs):
        super(RssForm, self).__init__(*args, **kwargs)

    def save(self, request):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('url')):
            from vyperlogix.feeds import feedparser
            url = self.cleaned_data['url']
            try:
                foo = feedparser.parse(url)
                if (foo) and (len(foo) > 0) and (foo['entries']) and (len(foo['entries']) > 0):
                    aFeed = models.RssFeed(url=url)
                    aFeed.save()
                    results['bool'] = True
            except:
                results['bool'] = False
        else:
            raise forms.ValidationError(_(u'You must enter an RSS Feed Url.'))
        return results

    def remove(self):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('url')):
            feeds = [f for f in models.RssFeed.all() if (f.id == self.cleaned_data['url']) or (f.url == self.cleaned_data['url'])]
            if (len(feeds) > 0):
                aFeed = feeds[0]
                aFeed.delete()
            results['bool'] = True
        else:
            raise forms.ValidationError(_(u'You must enter an RSS Feed Url.'))
        return results

google_site_verification = 'google-site-verification'

class VerificationForm(forms.Form):
    """
    Form for providing verification for Google Webmaster Tools.
    """
    content = forms.CharField(widget=forms.TextInput(attrs=combine_dicts(attrs_dict,attrs_verification_dict)),label=_(u'Verification'))
    
    def __init__(self, recid=None, *args, **kwargs):
        super(VerificationForm, self).__init__(*args, **kwargs)

    def save(self, request):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('content')):
            content = self.cleaned_data['content']
            try:
                aSetting = models.Setting(name=google_site_verification,value=content)
                aSetting.save()
                results['bool'] = True
            except:
                results['bool'] = False
        else:
            raise forms.ValidationError(_(u'You must enter the google-site-verification number.'))
        return results

    def remove(self):
        """
        Saves the message in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('content')):
            values = [v for v in models.Setting.all() if (v.name == google_site_verification) and (v.value == self.cleaned_data['content'])]
            if (len(values) > 0):
                aValue = values[0]
                aValue.delete()
            results['bool'] = True
        else:
            raise forms.ValidationError(_(u'You must make a choice before clicking the removal button.'))
        return results

class DomainForm(forms.Form):
    """
    Form for providing domain name for installation tracking.
    """
    domain = forms.CharField(widget=forms.TextInput(attrs=combine_dicts(attrs_dict,attrs_domain_dict)),label=_(u'Domain'))
    
    def __init__(self, recid=None, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)

    def save(self, request):
        """
        Saves the installation in the database...
        """
        results = {'bool':False}
        if (self.cleaned_data.has_key('domain')):
            domain = self.cleaned_data['domain']
            try:
                anInstallation = models.Installation(domain=domain)
                anInstallation.save()
                results['bool'] = True
            except:
                results['bool'] = False
        else:
            raise forms.ValidationError(_(u'You must enter a domain name.'))
        return results

