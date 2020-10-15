# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import ugettext_lazy as _, ugettext as __
from cms.models import Globalvar, Categories, Allad, Links, Redirect, Photo, Comment
from ragendja.auth.models import UserTraits
from ragendja.forms import FormWithSets
from registration.forms import RegistrationForm, RegistrationFormUniqueEmail
from registration.models import RegistrationProfile

class GlobalvarForm(forms.ModelForm):
    name = forms.CharField(required=True, help_text=_(u'Letters, underscores, numbers, spaces can not be'), label=_(u'Variable name'))
    value = forms.CharField(required=True, label=_(u'Variable value'))
    description = forms.CharField(required=False, label=_(u'Variable Description'))
    
    class Meta:
        model = Globalvar

class CategoriesForm(forms.ModelForm):
    sort = forms.IntegerField(required=True, initial=0, label=_(u'Priority level'))
    display = forms.IntegerField(required=True, initial=1, help_text=_(u'Whether or not displays In the navigation bar 1 / 0'), label=_(u'display'))
    name = forms.CharField(required=True, label=_(u'Categories'))
    
    class Meta:
        model = Categories

class AlladForm(forms.ModelForm):
    name = forms.CharField(required=True, help_text=_(u'Letters, underscores, numbers, spaces can not be'), label=_(u'Variable name'))
    description = forms.CharField(required=False, help_text=_(u'Optional'), label=_(u'Variable Description'))    
    
    class Meta:
        model = Allad

class LinksForm(forms.ModelForm):
    class Meta:
        model = Links

class RedirectForm(forms.ModelForm):
    value = forms.CharField(required=True)
    redirto = forms.CharField(required=True, initial='http://')
    class Meta:
        model = Redirect

class CommentForm(forms.ModelForm):
    name = forms.CharField(required = True, max_length=20, label=_(u'Name (required)'))
    email = forms.EmailField(required = False, max_length=30, label=_(u'E-mail (optional)'))
    site = forms.URLField(required = False, max_length=150, help_text=u'http://xxx.com', label=_(u'Website (optional)'))
    content = forms.CharField (required = True, widget=forms.widgets.Textarea(attrs={'style':"width:400px;height:60px;"}),max_length=300, help_text=_(u'A maximum of 300 characters'),label=_(u'Message (Required)'))
     
    class Meta:
        model = Comment
        exclude = ['article','pub_date']

class PhotoForm(forms.ModelForm):
    filename = forms.CharField(required=False, label=_(u'Image title'))

    def clean(self):
        file = self.cleaned_data.get('avatar')
        if not self.cleaned_data.get('filename'):
            if isinstance(file, UploadedFile):
                self.cleaned_data['filename'] = file.name
            else:
                del self.cleaned_data['filename']
        return self.cleaned_data

    class Meta:
        model = Photo

PhotoForm = FormWithSets(PhotoForm)

class UserRegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', max_length=30,
        label=_(u'Username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)),
         label=_(u'Email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'Password (again)'))

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        user = User.get_by_key_name("key_"+self.cleaned_data['username'].lower())
        if user and user.is_active:
            raise forms.ValidationError(__(u'This username is already taken. Please choose another.'))
        return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(__(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, domain_override=""):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            domain_override=domain_override)
        self.instance = new_user
        return super(UserRegistrationForm, self).save()

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        email = self.cleaned_data['email'].lower()
        if User.all().filter('email =', email).filter(
                'is_active =', True).count(1):
            raise forms.ValidationError(__(u'This email address is already in use. Please supply a different email address.'))
        return email

    class Meta:
        model = User
        exclude = UserTraits.properties().keys()
