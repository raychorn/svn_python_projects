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

from registration.models import RegistrationProfile

from vyperlogix.django import django_utils

from django.conf import settings

from vyperlogix.misc import _utils

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should either preserve the base ``save()`` or implement
    a ``save()`` method which returns a ``User``.
    
    """
    username = forms.RegexField(regex=r'^\w+$',max_length=30,widget=forms.TextInput(attrs=attrs_dict),label=_(u'User Name'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password (again)'))
    first_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),label=_(u'First Name'))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attrs_dict),label=_(u'Last Name'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,size=50,maxlength=128)),label=_(u'Email Address'))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        user = User.get_by_key_name("key_"+self.cleaned_data['username'].lower())
        if user:
            raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
        return self.cleaned_data['username']
        
    def clean_email(self):
        """
        Validate that the email is unique and is not already
        in use.
        
        """
        users = User.all().filter('email',self.cleaned_data['email'].lower())
        if users.count() > 0:
            raise forms.ValidationError(_(u'This email address is already taken. Please choose another.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        _name = self.cleaned_data['first_name']+' '+self.cleaned_data['last_name']
        users = [aUser for aUser in User.all() if (aUser.first_name+' '+aUser.last_name) == _name]
        if (len(users) > 0):
            raise forms.ValidationError(_(u'Another user have already taken your first and last name. Please be more unique.'))
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password twice.'))
        return self.cleaned_data
    
    def save(self, domain_override=""):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User`` (by calling
        ``RegistrationProfile.objects.create_inactive_user()``).
        
        """
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    first_name=self.cleaned_data['first_name'],
                                                                    last_name=self.cleaned_data['last_name'],
                                                                    domain_override=domain_override,
                                                                    )
        return new_user

def getRegistrationEmailMessage(aRegistration,domain_override):
    from models import __registration_activation_email_subject__, __registration_activation_email__

    subject = django_utils.render_from_string(__registration_activation_email_subject__,context=Context({ 'site': domain_override },autoescape=False))
    subject = ''.join(subject.splitlines())

    c = { 'activation_key': aRegistration.activation_key,
          'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
          'site': domain_override 
          }
    context = Context(c,autoescape=False)
    body = django_utils.render_from_string(__registration_activation_email__,context=context)
    return (subject,body)

def getAccountPasswordEmailMessage(aRegistration,domain_override):
    from vyperlogix.products import keys
    from models import __account_password_email_subject__, __account_password_email__

    subject = django_utils.render_from_string(__account_password_email_subject__,context=Context({ 'site': domain_override },autoescape=False))
    subject = ''.join(subject.splitlines())

    c = { 'email_address': keys._encode(aRegistration.user.email),
          'site': domain_override 
          }
    context = Context(c,autoescape=False)
    body = django_utils.render_from_string(__account_password_email__,context=context)
    return (subject,body)

class ResendRegistrationForm(forms.Form):
    """
    Form for requesting the Registration be re-sent.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,size=50,maxlength=128)),label=_(u'Email Address'))
    
    def save(self, domain_override="", isRunningLocal=False):
        """
        Resends the Registration email...
        """
        hasEmailBeenSent = {'bool':False}
        _email = self.cleaned_data['email']
        registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (not aRegistration.activation_key_expired()) and (aRegistration.user.email == _email)]
        if (len(registrations) == 0):
            hasEmailBeenSent['reason'] = 'Cannot resend your Registration (Activation) Notice because<BR/>it has expired or has been used.<BR/><BR/>Are you sure you have not simply forgotten your password ?!?'
        for aRegistration in registrations:
            aMemKey = "ResendRegistrationForm_%s" % (aRegistration.activation_key)
            aMemToken = memcache.get(aMemKey)
            if aMemToken is not None:
                hasEmailBeenSent['reason'] = 'Cannot resend your Registration (Activation) Notice until tomorrow.<BR/>Please try back later.'
            else:
                subject, body = getRegistrationEmailMessage(aRegistration,domain_override)
    
                hasEmailBeenSent['bool'] = True
    
                from django.core.mail import send_mail
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [aRegistration.user.email]
                try:
                    send_mail(subject, body, from_email, to_email)
                    aMemToken = {'subject':subject,'body':body,'from_email':from_email,'to_email':to_email}
                    memcache.add(aMemKey, aMemToken, 60*60*24)
                except Exception, e:
                    info_string = _utils.formattedException(details=e)
                    logging.error('ResendRegistrationForm.save.ERROR --> %s' % (info_string))
        return hasEmailBeenSent

class SendChangePasswordForm(forms.Form):
    """
    Form for requesting the Change Password Form Link.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,size=50,maxlength=128)),label=_(u'Email Address'))
    
    def save(self, domain_override=""):
        """
        Sends the Change Password email...
        """
        hasEmailBeenSent = {'bool':False}
        _email = self.cleaned_data['email']
        registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (aRegistration.activation_key_expired()) and (aRegistration.user.email == _email)]
        if (len(registrations) == 0):
            hasEmailBeenSent['reason'] = 'Cannot send your Change Password Notice because<BR/>your account is not Active.<BR/><BR/>Are you sure you know your email address ?!?'
        for aRegistration in registrations:
            aMemKey = "SendChangePasswordForm_%s" % (aRegistration.activation_key)
            aMemToken = memcache.get(aMemKey)
            if aMemToken is not None:
                hasEmailBeenSent['reason'] = 'Cannot send your Change Password Notice until tomorrow.<BR/>Please try back later.'
            else:
                subject, body = getAccountPasswordEmailMessage(aRegistration,domain_override)
    
                hasEmailBeenSent['bool'] = True
    
                from django.core.mail import send_mail
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [aRegistration.user.email]
                try:
                    send_mail(subject, body, from_email, to_email)
                    aMemToken = {'subject':subject,'body':body,'from_email':from_email,'to_email':to_email}
                    memcache.add(aMemKey, aMemToken, 60*60*24)
                except Exception, e:
                    info_string = _utils.formattedException(details=e)
                    logging.error('SendChangePasswordForm.save.ERROR --> %s' % (info_string))
        return hasEmailBeenSent

class ForgotPasswordForm(forms.Form):
    """
    Form for requesting the Registration be re-sent.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,size=50,maxlength=128)),label=_(u'Email Address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=_(u'Password (again)'))
    
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, domain_override=""):
        """
        Resends the Registration email...
        """
        hasEmailBeenSent = {'bool':False}
        _email = self.cleaned_data['email']
        _password1 = self.cleaned_data['password1']
        _password2 = self.cleaned_data['password2']
        registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (aRegistration.activation_key_expired()) and (aRegistration.user.email == _email)]
        if (len(registrations) == 0):
            hasEmailBeenSent['reason'] = 'Cannot reset your Password because<BR/>you either have not Activated your Registration<BR/>or you have not submitted your Registration.'
        for aRegistration in registrations:
            aMemKey = "ResendRegistrationForm_%s" % (aRegistration.activation_key)
            try:
                aRegistration.user.is_active = False
                salt = sha.new(str(random.random())).hexdigest()[:5]
                aRegistration.activation_key = sha.new(salt+aRegistration.user.username).hexdigest()
                aRegistration.user.set_password(_password1)
                aRegistration.user.save()
                aRegistration.save()

                subject, body = getRegistrationEmailMessage(aRegistration,domain_override)

                from django.core.mail import send_mail
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [aRegistration.user.email]
                try:
                    send_mail(subject, body, from_email, to_email)
                    aMemToken = {'subject':subject,'body':body,'from_email':from_email,'to_email':to_email}
                    memcache.add(aMemKey, aMemToken, 60*60*24)
                except Exception, e:
                    info_string = _utils.formattedException(details=e)
                    logging.error('ForgotPasswordForm.save.ERROR.1 --> %s' % (info_string))
                hasEmailBeenSent['bool'] = True
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                logging.error('ForgotPasswordForm.save.ERROR.2 --> %s' % (info_string))
        return hasEmailBeenSent


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': u"You must agree to the terms to register" })


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        email = self.cleaned_data['email'].lower()
        if User.all().filter('email =', email).count(1):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return email


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_(u'Registration using free email addresses is prohibited. Please supply a different email address.'))
        return self.cleaned_data['email']
