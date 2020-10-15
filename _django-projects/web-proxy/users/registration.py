######################################################
import re
import datetime
import logging

from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from django.template import Context

from django.utils.translation import ugettext_lazy as _

from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.django import django_utils

from g import air_sender, air_site, current_site

__registration_activation_email_subject__ = '''Activation of your User Account for {{ site }} '''

__registration_activation_email__ = '''
Welcome to {{ site_name }} !

To activate your new User Account please copy and paste into your browsers address bar (if you do not see a link to click) or click on the link the following as required to Activate your Account:

http{{ ssl }}://{{ site }}{{ activation_symbol }}?x={{ activation_key }}
(copy and paste into your browsers address bar, as applicable)

Thanks,
Your {{ site_name }} Web Team
'''

__registration_activation_email_html__ = '''
<p>Welcome to {{ site_name }} !</p>

<p>To activate your new User Account please right click the following link to copy and paste into your browser's address bar or click the following as required to Activate your Account via <a href="http{{ ssl }}://{{ site }}{{ activation_symbol }}?x={{ activation_key }}" target="_blank">http{{ ssl }}://{{ site }}{{ activation_symbol }}?x={{ activation_key }}</a>.</p>

<p>Thanks,<br/>
Your {{ site_name }} Web Team</p>
'''

__account_password_email_subject__ = '''User Account Password Change for {{ site }} '''

__password_change_email__ = '''
Welcome to {{ site_name }} !

To change your User Account password please visit the following link:

http{{ ssl }}://{{ site }}/passwordChg/{{ key }}/{{ old_password }}/{{ password }}/{{ air_id }}/

Thanks,
Your {{ site_name }} Web Team
'''

__password_change_email_html__ = '''
<p>Welcome to {{ site_name }} !</p>

<p>To change your User Account password please visit the following link:</p>

<p><a href="http{{ ssl }}://{{ site }}/passwordChg/{{ key }}/{{ old_password }}/{{ password }}/{{ air_id }}/" target="_blank">http{{ ssl }}://{{ site }}/passwordChg/{{ key }}/{{ old_password }}/{{ password }}/{{ air_id }}/</a></p>

<p>Thanks,
<br/>Your {{ site_name }} Web Team</p>
'''

__registration_problem_email_subject__ = '''Problem Report from {{ fromName }} via {{ site }} '''

__problem_report_email__ = '''
{{ msg }}

From {{ fromName }}
'''

__problem_report_email_html__ = '''
<p>{{ msg }}</p>

<p>From {{ fromName }}</p>
'''

SHA1_RE = re.compile('^[a-f0-9]{40}$')

__uuid_bias__ = 16

class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, username, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, return the ``User``
        after activating.
        
        If the key is not valid or has expired, return ``False``.
        
        If the key is valid but the ``User`` is already active,
        return ``False``.
        
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        To execute customized logic when a ``User`` is activated,
        connect a function to the signal
        ``registration.signals.user_activated``; this signal will be
        sent (with the ``User`` as the value of the keyword argument
        ``user``) after a successful activation.
        
        """
        global __uuid_bias__
        from signals import user_activated
        
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        activation_key_expired = True
        _activation_key = activation_key[0:len(activation_key)-__uuid_bias__]
        if SHA1_RE.search(_activation_key):
            profile = RegistrationProfile.get_by_key_name("key_"+activation_key)
            if (not profile):
                registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (aRegistration.activation_key == activation_key)]
                if (len(registrations) > 0):
                    profile = registrations[0]
                    activation_key_expired = False
            if (profile.user.username == username):
                activation_key_expired = profile.activation_key_expired()
            if (not profile) or (activation_key_expired):
                return False
            if not activation_key_expired:
                user = profile.user
                user.is_active = True
                user.put()
                profile.activation_key = RegistrationProfile.ACTIVATED
                profile.put()
                user_activated.send(sender=self.model, user=user)
                return user
        return False
    
    def reactivate_user(self, username,air_id):
        registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (aRegistration.user.username == username)]
        if (len(registrations) > 0):
            profile = registrations[0]
            if (profile.activation_key == RegistrationProfile.ACTIVATED):
                new_profile = self.create_profile(profile.user)
                profile.activation_key = new_profile.activation_key
                profile.put()
                self.send_activation_email(profile.user,profile,air_id=air_id)
            else:
                self.send_activation_email(profile.user,profile,air_id=air_id)
            return True
        return False
    
    def send_activation_email(self,new_user,registration_profile,air_id='',domain_override=''):
        from vyperlogix.products import keys
        _current_site_ = domain_override if (domain_override and len(domain_override) > 0) else settings.CURRENT_SITE
        _current_site = _current_site_.replace('.appspot','').replace('.com','').capitalize()
        
        subject = django_utils.render_from_string(__registration_activation_email_subject__,context=Context({ 'site': _current_site },autoescape=False))
        subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines

        c = { 'activation_key': keys.encode('%s;%s'%(registration_profile.user.email,registration_profile.activation_key)),
              'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
              'site': _current_site_,
              'site_name': _current_site,
              'ssl':'s' if (settings.IS_PRODUCTION_SERVER) else '',
              }
        c['activation_symbol'] = '%sactivation/' % ('' if _current_site.endswith('/') else '/')
        message = django_utils.render_from_string(__registration_activation_email__,context=c)
        message_html = django_utils.render_from_string(__registration_activation_email_html__,context=c)

        try:
            if (settings.IS_PRODUCTION_SERVER):
                logging.log(logging.INFO,'sender="%s Support <%s>"' % (air_sender(air_id),air_sender(air_id)))
		if (settings.QUEUE_EMAILS):
		    queue_email(air_sender(air_id),new_user.email,"Your User Account Activation for %s" % (air_site(air_id)),message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
		else:
		    from google.appengine.api import mail
		    mail.send_mail(sender="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
			          to=new_user.email,
			          subject="Your User Account Activation for %s" % (air_site(air_id)),
			          body=message,
			          html=message_html)
            else:
                logging.info('RegistrationManager.create_inactive_user.INFO --> to=%s, message=%s' % (new_user.email,message))
		queue_email(air_sender(air_id),new_user.email,"Your User Account Activation for %s" % (air_site(air_id)),message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            logging.error('RegistrationManager.create_inactive_user.ERROR --> %s' % (info_string))
    
        #try:
            #if (settings.IS_PRODUCTION_SERVER):
                #from google.appengine.api import mail
                #logging.log(logging.INFO,'sender="%s Support <%s>"' % (air_sender(air_id),air_sender(air_id)))
                #mail.send_mail(sender="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
                              #to="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
                              #subject="New User Account Activation for %s (%s)" % (air_site(air_id),new_user.email),
                              #body=message,html=message_html)
            #else:
                #logging.info('RegistrationManager.create_inactive_user.INFO --> to=%s, message=%s' % (new_user.email,message))
        #except Exception, e:
            #info_string = _utils.formattedException(details=e)
            #logging.error('RegistrationManager.create_inactive_user.ERROR --> %s' % (info_string))
    
    def send_passwordChg_email(self,user,old_password,password,air_id='',domain_override=''):
        _current_site_ = domain_override if (domain_override and len(domain_override) > 0) else settings.CURRENT_SITE
        _current_site = _current_site_.replace('.appspot','').replace('.com','').capitalize()
        
        subject = django_utils.render_from_string(__registration_activation_email_subject__,context=Context({ 'site': _current_site },autoescape=False))
        subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines

        c = { 'key': user.id,
              'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
              'site': _current_site_,
              'site_name': _current_site,
              'ssl':'s' if (settings.IS_PRODUCTION_SERVER) else '',
	      'air_id':air_id,
	      'old_password':old_password,
	      'password':password,
              }
        message = django_utils.render_from_string(__password_change_email__,context=c)
        message_html = django_utils.render_from_string(__password_change_email_html__,context=c)
        
        try:
            if (settings.IS_PRODUCTION_SERVER):
		if (settings.QUEUE_EMAILS):
		    queue_email(air_sender(air_id),user.email,"Password Change Request for %s" % (air_site(air_id)),message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
		else:
		    from google.appengine.api import mail
		    mail.send_mail(sender="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
			          to=user.email,
			          subject="Password Change Request for %s" % (air_site(air_id)),
			          body=message,html=message_html)
            else:
                logging.info('RegistrationManager.changePassword.INFO --> to=%s, message=%s' % (user.email,message))
		queue_email(air_sender(air_id),user.email,"Password Change Request for %s" % (air_site(air_id)),message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            logging.error('RegistrationManager.changePassword.ERROR --> %s' % (info_string))
    
        #try:
            #if (settings.IS_PRODUCTION_SERVER):
                #from google.appengine.api import mail
                #mail.send_mail(sender="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
                              #to="%s Support <%s>" % (air_sender(air_id),air_sender(air_id)),
                              #subject="Password Change Request for %s (%s)" % (air_site(air_id),user.email),
                              #body=message,html=message_html)
            #else:
                #logging.info('RegistrationManager.changePassword.INFO --> to=%s, message=%s' % (user.email,message))
        #except Exception, e:
            #info_string = _utils.formattedException(details=e)
            #logging.error('RegistrationManager.changePassword.ERROR --> %s' % (info_string))
    
    def send_problem_email(self,fromName,email,msg,air_id='',domain_override=''):
        _current_site_ = domain_override if (domain_override and len(domain_override) > 0) else settings.CURRENT_SITE
        _current_site = _current_site_.replace('.appspot','').replace('.com','').capitalize()
        
        subject = django_utils.render_from_string(__registration_problem_email_subject__,context=Context({ 'fromName': fromName, 'site': _current_site },autoescape=False))
        subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines

        c = { 'msg': msg,
              'fromName': fromName,
              'site': _current_site_,
              'site_name': _current_site
              }
        message = django_utils.render_from_string(__problem_report_email__,context=c)
        message_html = django_utils.render_from_string(__problem_report_email_html__,context=c)
        
        try:
            if (settings.IS_PRODUCTION_SERVER):
		if (settings.QUEUE_EMAILS):
		    queue_email(email,air_sender(air_id),subject,message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
		else:
		    from google.appengine.api import mail
		    mail.send_mail(sender="%s <%s>" % (fromName,email),
			          to=air_sender(air_id),
			          subject=subject,
			          body=message,html=message_html)
            else:
                logging.info('RegistrationManager.create_inactive_user.INFO --> to=%s, message=%s' % (new_user.email,message))
		queue_email(email,air_sender(air_id),subject,message,message_html,air_id,settings.SUB_DOMAIN_NAME,is_html=True)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            logging.error('RegistrationManager.create_inactive_user.ERROR --> %s' % (info_string))
    
    def create_inactive_user(self, username, password, email, first_name, last_name, air_id='', domain_override="", send_email=True):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.
        
        To disable the email, call with ``send_email=False``.

        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. It receives one context variable, ``site``, which
            is the currently-active
            ``django.contrib.sites.models.Site`` instance. Because it
            is used as the subject line of an email, this template's
            output **must** be only a single line of text; output
            longer than one line will be forcibly joined into only a
            single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email. It
            will receive three context variables: ``activation_key``
            will be the user's activation key (for use in constructing
            a URL to activate the account), ``expiration_days`` will
            be the number of days for which the key will be valid and
            ``site`` will be the currently-active
            ``django.contrib.sites.models.Site`` instance.

        To execute customized logic once the new ``User`` has been
        created, connect a function to the signal
        ``registration.signals.user_registered``; this signal will be
        sent (with the new ``User`` as the value of the keyword
        argument ``user``) after the ``User`` and
        ``RegistrationProfile`` have been created, and the email (if
        any) has been sent..
        
        """
        # prepend "key_" to the key_name, because key_names can't start with numbers
        new_user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_active=False)
        new_user.set_password(password)
        new_user.save()
        
        registration_profile = self.create_profile(new_user)
        
        if (send_email):
            self.send_activation_email(new_user,registration_profile,air_id=air_id,domain_override=domain_override)

        return new_user
    
    def create_profile(self, user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        
        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        import sha
        import random
        import uuid
        global __uuid_bias__
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest() # 40
        activation_uuid = ''.join(str(uuid.uuid4()).split('-'))  # 32
        # prepend "key_" to the key_name, because key_names can't start with numbers
        activation_key += activation_uuid[len(activation_uuid)-__uuid_bias__:]
        registrationprofile = RegistrationProfile(user=user, activation_key=activation_key)
        registrationprofile.save()
        return registrationprofile
        
    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        for profile in RegistrationProfile.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()
                    profile.delete()

class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.
    
    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.
    
    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.
    
    """
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(User)
    activation_key = models.CharField(_('activation key'), max_length=128)
    objects = RegistrationManager()
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"Registration information for %s (%s) (%s) %s" % (self.user.username,self.user.email,_utils.getAsSimpleDateStr(self.timestamp,str(_utils.formatDjangoDateTimeStr())),self.activation_key)
    
    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == RegistrationProfile.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True

######################################################
