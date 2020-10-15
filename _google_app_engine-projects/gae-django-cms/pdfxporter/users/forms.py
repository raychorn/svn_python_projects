"""
Forms and validation code for user registration.

"""
import logging
import sha
import random

from google.appengine.api import memcache

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.template import Context

from vyperlogix.django import django_utils

from django.conf import settings

from vyperlogix.misc import _utils

attrs_dict = { 'class': 'required' }

class SmartForm(forms.Form):
    """
    """
    username = forms.RegexField(regex=r'^\w+$',max_length=30,widget=forms.TextInput(attrs=attrs_dict),label=_(u'User Name'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password (again)'))
    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),label=_(u'First Name'))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),label=_(u'Last Name'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,size=50,maxlength=128)),label=_(u'Email Address'))
    
