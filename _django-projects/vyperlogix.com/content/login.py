from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _, gettext
try:
    from django import forms
    _Form = forms.Form
except AttributeError:
    from django import newforms as forms
    _Form = forms.Form
from django.template import Context

from django.db.models import Q

from vyperlogix.js import minify

from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import captcha

from vyperlogix.django import django_utils

import utils

_scripts_loginHead = '''
'''

_scripts_loginForm = '''
'''

def _login_header():
    return minify.minify_js(_scripts_loginHead)

def login_header():
    return oohtml.render_scripts(_login_header)

def login_scripts():
    return oohtml.render_scripts(_scripts_loginForm)

class LoginForm(_Form):
    from content import models as content_models
    f_password = content_models.User._meta.get_field('password')
    l_password = 100
    
    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('Password'),widget=forms.PasswordInput(render_value=False),max_length=l_password)
    user = None
    
    def login(self, request):
        post_data = request.POST.copy()
        if (self.is_valid()) and (captcha.is_captcha_form_valid(request)):
            users = self.content_models.User.objects.filter(email_address=post_data['username'])
	    _debug = ''
	    if (users.count() > 0):
		_debug += 'user-password=[%s]' % (users[0].password)
	    _debug += 'posted-password=[%s]' % (post_data['password'])
            if (users.count() > 0) and (users[0].password == post_data['password']):
		aUser = users[0]
                request.session['user_id'] = aUser.email_address
		url_toks = django_utils.parse_url_parms(request)
		anActivity = self.content_models.UserActivity(user=aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
		anActivity.save()
                return True,'You are now logged-in.'
            return False,'Unable to login using username of "%s", are you sure you are a Registered User ?' % (post_data['username'])
        return False,'Unable to perform login, change your username or retrieve your password and try again.'
    
class ForgotPasswordForm(_Form):
    from content import models as content_models

    username = forms.CharField(label=_('username'))
    user = None   # allow access to user object     
    are_you_sure = 'Unable to send a new password to your email address.<br/>Are you sure you are a Registered user ?<br/>Are you sure you have activated your Account ?<br/>In case you did not receive your Account Activation email you may Register again to get back into the system as a new user.'

    def process(self, request):
	from vyperlogix.crypto import md5
	from vyperlogix.misc import GenPasswd
	
	from views.default import send_password_email

        post_data = request.POST.copy()
        if (self.is_valid()) and (captcha.is_captcha_form_valid(request)):
	    email_address = post_data['username']
            users = self.content_models.User.objects.filter(Q(email_address=email_address), Q(activated=1))
            if (users.count() > 0):
		aUser = users[0]
		password = GenPasswd.GenPasswdFriendly()
		aUser.password = md5.md5(password)
		aUser.save()
		send_password_email(email_address, password)
		url_toks = django_utils.parse_url_parms(request)
		anActivity = self.content_models.UserActivity(user=aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
		anActivity.save()
                return True,'Your new password has been sent to your email address.'
            return False,ForgotPasswordForm.are_you_sure
        return False,ForgotPasswordForm.are_you_sure
    
def login(request,template='login.html',onAction='',onSuccess='',captcha_form_name='captcha_form_fields.html',captcha_font_name='BerrysHandegular.ttf',captcha_font_size=32):
    from django.template import loader
    from vyperlogix.django import django_utils

    form = None

    _error_msg = ''
    if (request.method.lower() == 'POST'.lower()):
        post_data = request.POST.copy()
        form = LoginForm(post_data)
        if (form.is_valid()):
            success = form.login(request)
            if (isinstance(success,tuple)):
                success, _error_msg = success
                if (success is True):
                    request.session['is_logged_in'] = True
                    request.session['has_valid_domain'] = False
                    return HttpResponseRedirect(onSuccess)
            else:
                _error_msg = 'Unable to perform login due to some kind of technical issue... try back later...'
        else:
	    h = oohtml.Html()
	    ul = h.tagUL()
	    for k,v in form.errors.iteritems():
		hh = oohtml.Html()
		_ul = hh.tagUL()
		for item in v:
		    _ul.tagLI(item)
		ul.tag_LI(hh.toHtml())
            _error_msg = h.toHtml()
    else:
        form = LoginForm() #if (onAction.find('forgot-password') == -1) else ForgotPasswordForm()
    if ((request.META.has_key('HTTP_HOST')) and ( (django_utils.isProduction(django_utils._cname)) or (django_utils.isStaging(django_utils._cname)) ) ):
        onAction = 'https://%s%s' % (request.META['HTTP_HOST'],onAction)
    h = oohtml.Html()
    h.tagDIV(captcha.render_captcha_form(request,form_name=captcha_form_name,font_name=captcha_font_name,font_size=captcha_font_size,choices=utils.captcha_choices,fill=(255,255,255),bgImage='bg.jpg'))
    c = {'form':form, 'FORM_ACTION':onAction, 'ERROR_MESSAGE':_error_msg, 'CAPTCHA':h.toHtml()}
    site_handle = utils.get_site_handle(request)
    if (site_handle.aUserOwner is not None):
	c['STYLES'] = utils._styles
    ctx = Context(c, autoescape=False)
    return loader.render_to_string(template, context_instance=ctx)

def forgot(request,template='forgot-password.html',onAction='',onSuccess='',captcha_form_name='captcha_form_fields.html',captcha_font_name='BerrysHandegular.ttf',captcha_font_size=32):
    from django.template import loader
    from vyperlogix.django import django_utils

    form = None

    _error_msg = ''
    if (request.method.lower() == 'POST'.lower()):
        post_data = request.POST.copy()
        form = ForgotPasswordForm(post_data)
        if (form.is_valid()):
            success = form.process(request)
            if (isinstance(success,tuple)):
                success, _error_msg = success
                if (success is True):
                    return HttpResponseRedirect(onSuccess)
            else:
                _error_msg = ForgotPasswordForm.are_you_sure
        else:
            _error_msg = ForgotPasswordForm.are_you_sure
    else:
        form = ForgotPasswordForm()
    if ((request.META.has_key('HTTP_HOST')) and ( (django_utils.isProduction(django_utils._cname)) or (django_utils.isStaging(django_utils._cname)) ) ):
        onAction = 'https://%s%s' % (request.META['HTTP_HOST'],onAction)
    h = oohtml.Html()
    h.tagDIV(captcha.render_captcha_form(request,form_name=captcha_form_name,font_name=captcha_font_name,font_size=captcha_font_size,choices=utils.captcha_choices,fill=(255,255,255),bgImage='bg.jpg'))
    ctx = Context({'form':form, 'FORM_ACTION':onAction, 'ERROR_MESSAGE':_error_msg, 'CAPTCHA':h.toHtml()}, autoescape=False)
    return loader.render_to_string(template, context_instance=ctx)
