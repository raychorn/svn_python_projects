from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext
from google.appengine.ext import db
from mimetypes import guess_type
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user

from django.template import loader, Template, TemplateDoesNotExist
from django.template import Context
from django.conf import settings

from registration.forms import RegistrationFormTermsOfService as RegistrationForm 
from registration.forms import ResendRegistrationForm, ForgotPasswordForm, SendChangePasswordForm
from registration.models import RegistrationProfile

from feedback.forms import FeedbackForm

from facebook.models import FacebookUser

import forms

import models

import logging
import mimetypes

import uuid

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.hash import lists
from vyperlogix.classes.SmartObject import SmartObject

from google.appengine.api import memcache
from django.contrib.sitemaps.views import sitemap
from vyperlogix.feeds import feedparser

from vyperlogix.html import myOOHTML

_is_feed_valid = lambda foo:(foo) and (len(foo) > 0) and (foo['entries']) and (len(foo['entries']) > 0)

_feed_entries_cache_seconds_ = 60*60*24
_article_entries_cache_seconds_ = _feed_entries_cache_seconds_
_feed_entries_allowed_ = 50

_air_admin_tool_version = '0.30.1'

__api__ = '__api__'

__api_dict__ = {}
__api_dict__['account_password'] = '/account/password/'
__api_dict__['get_rest_get_menu'] = '/blog/rest/get/menu/'
__api_dict__['blog_rest_user_feedback'] = '/blog/rest/user/feedback/'
__api_dict__['blog_rest_user_sponsor'] = '/blog/rest/user/sponsor/'
__api_dict__['facebook_api_url'] = 'http://connect.facebook.net/en_US/all.js'
__api_dict__['facebook_api'] = '/js/js/facebook-api.min.js'
__api_dict__['blog_rest_get_admin'] = '/blog/rest/get/admin/'
__api_dict__['blog_rest_user_logout'] = '/blog/rest/user/logout/'
__api_dict__['blog_rest_user_login'] = '/blog/rest/user/login/'
__api_dict__['blog_rest_get_articles'] = '/blog/rest/get/articles/'
__api_dict__['blog_rest_get_externals'] = '/blog/rest/get/externals/'
__api_dict__['blog_rest_get_more'] = '/blog/rest/get/more/'
__api_dict__['blog_rest_get_categories'] = '/blog/rest/get/categories/'
__api_dict__['blog_rest_get_tags'] = '/blog/rest/get/tags/'
__api_dict__['blog_rest_get_languages'] = '/blog/rest/get/languages/'
__api_dict__['blog_rest_get_article'] = '/blog/rest/get/article/'
__api_dict__['blog_rest_get_tagged'] = '/blog/rest/get/tagged/'
__api_dict__['blog_rest_get_category'] = '/blog/rest/get/category/'
__api_dict__['blog_rest_get_language'] = '/blog/rest/get/language/'
__api_dict__['blog_rest_user_register'] = '/blog/rest/user/register/'
__api_dict__['blog_rest_register_tos'] = '/blog/rest/register/tos/'
__api_dict__['blog_rest_register_help'] = '/blog/rest/register/help/'
__api_dict__['blog_rest_post_register'] = '/blog/rest/post/register/'
__api_dict__['blog_rest_resend_register'] = '/blog/rest/resend/register/'
__api_dict__['blog_rest_forgot_password'] = '/blog/rest/forgot/password/'
__api_dict__['blog_rest_send_password'] = '/blog/rest/send/password/'
__api_dict__['account_activate'] = '/account/activate/'
__api_dict__['account_logout'] = '/account/logout/'
__api_dict__['blog_rest_login_help'] = '/blog/rest/login/help/'
__api_dict__['blog_rest_post_login'] = '/blog/rest/post/login/'
__api_dict__['blog_rest_set_facebook'] = '/blog/rest/set/facebook/'
__api_dict__['blog_rest_ssl_help'] = '/blog/rest/ssl/help/'
__api_dict__['blog_rest_get_comments'] = '/blog/rest/get/comments/'
__api_dict__['blog_rest_rssfeed_help'] = '/blog/rest/rssfeed/help/'
__api_dict__['blog_rest_post_rssfeed'] = '/blog/rest/post/rssfeed/'
__api_dict__['blog_rest_remove_rssfeed'] = '/blog/rest/remove/rssfeed/'
__api_dict__['blog_sitemap'] = '/blog/sitemap/'
__api_dict__['blog_rest_post_verification'] = '/blog/rest/post/verification/'
__api_dict__['blog_rest_remove_verification'] = '/blog/rest/remove/verification/'
__api_dict__['blog_link'] = '/blog/link/'
__api_dict__['blog_nav'] = '/blog/nav/'
__api_dict__['blog_rest_get_rssfeeds'] = '/blog/rest/get/rssfeeds/'

__domainName = ''.join(''.join(settings.APPSPOT_NAME.split('://')[-1]).split('/')[0]) if (len(settings.APPSPOT_NAME.split('.')) == 3) and (settings.IS_PRODUCTION_SERVER) else settings.LOCALHOST
__api_dict__['secure_endpoint'] = 'http%s://%s'%('s' if (settings.IS_PRODUCTION_SERVER) else '',__domainName) if (len(__domainName) > 0) else settings.LOCALHOST
__api_dict__['insecure_endpoint'] = 'http://%s'%(settings.DOMAIN_NAME if (settings.IS_PRODUCTION_SERVER) else settings.LOCALHOST)

#__api_dict__['feed'] = '/feed/'
# __api_dict__['REMOTE_ADDR']...

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>VyperCMS v2.0 ERROR</title></head><body>{{ content }}</body></html>'''

__idle_txt__ = '''
'''

__robots_txt__ = '''
User-agent: *
Disallow: /admin/
'''

__crossdomain_xml__ = '''
<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
	<site-control permitted-cross-domain-policies="all"/>
	<allow-access-from domain="*.raychorn.com" secure="false"/>
	<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>
'''

__like_button__ = '''
{% if isRunningLocal %}
    <iframe src="http://www.facebook.com/plugins/like.php?href={{ url_encoded }}&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;font=segoe+ui&amp;colorscheme=light&amp;height=80" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:80px;" allowTransparency="true"></iframe>
{% else %}
    <fb:like href="{{ url }}" font="segoe ui"></fb:like>
{% endif %}
'''

__fb_comments__ = '''
<fb:comments xid="{{ xid }}" numposts="{{ numposts }}" width="{{ width }}"></fb:comments>
'''

__fb_share__ = '''
<a id="a_faceBookShare"href="#" url="http://www.facebook.com/sharer.php?u={{ url }}&t={{ title }}" title="Share this: {{ title }}" target="_blank"><img src="/static/images/facebook-share-button.png" border="0"/></a>
'''

__self_help__ = '''
<p><a id="a_forgotPassword" href="#">Forgot Password ?</a>&nbsp;|&nbsp;<a id="a_resendRegistration" href="#">Resend Registration Confirmation ?</a></p>
'''

__registration_form__ = '''
<h3>Fill out this one-step form and you'll be blogging seconds later!</h3>
<div id="formRegister">
  <table>{{ form }}</table>
  <input id="btn_submitRegister" type="submit" value="Register" />
</div>
<div id="selfHelp">{{ selfHelp }}</div>
<p class="errorMessage">{{ status }}</p>
'''

__resend_registration_form__ = '''
<h3>Complete this form to get your Registration email resent!</h3>
<div id="formResendRegister">
  <table>{{ form }}</table>
  <input id="btn_submitResendRegister" type="submit" value="Resend Registration EMail" />
</div>
<p class="errorMessage">{{ status }}{{ reason }}</p>
<div id="selfHelp">{{ selfHelp }}</div>
'''

__send_password_form__ = '''
<h3>Complete this form to get your User Account Password changed!</h3>
<div id="formSendPassword">
  <table>{{ form }}</table>
  <input id="btn_submitSendPassword" type="submit" value="Send Change Password Link" />
</div>
<p class="errorMessage">{{ status }}{{ reason }}</p>
<div id="selfHelp">{{ selfHelp }}</div>
'''

__forgot_password_form__ = '''
<h3>Complete this form to get your User Account Password reset!</h3>
<div id="formForgotPassword">
  <table>{{ form }}</table>
  <input id="btn_submitForgotPassword" type="submit" value="Forgot Password" />
</div>
<p class="errorMessage">{{ status }}{{ reason }}</p>
<div id="selfHelp">{{ selfHelp }}</div>
'''

__feedback_form__ = '''
{% if authenticated %}
  <div id="formFeedback">
    <table>{{ form }}</table>
    <input id="btn_submitFeedback" type="submit" value="Feedback" />
  </div>
{% else %}
  <p>Please Register/Login to Leave Feedback.</p>
{% endif %}
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__login_form__ = '''
<div id="formLogin">
    <table>{{ form }}</table>
    <input id="btn_submitLogin" type="submit" value="Login" />
</div>
<div id="selfHelp">{{ selfHelp }}</div>
<p class="errorMessage">{{ status }}</p>
'''

__login_complete__ = '''
<h2>You are now Logged-In !</h2>
'''

__logout_complete__ = '''
<h2>You are now Logged-Out !</h2>
'''

__comment_form__ = '''
{% if authenticated %}
  <div id="formComment">
    <table>
       <tr>
          <td>
             <table>{{ form }}</table>
          </td>
       </tr>
       <tr>
          <td align="center">
             <input id="btn_submitComment" type="submit" value="Submit Comment" />
          </td>
       </tr>
    </table>
  </div>
{% else %}
  <p>Please Register/Login to Leave Comments.</p>
{% endif %}
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__comment_complete__ = '''
{{ content }}
<p class="errorMessage">{{ status }}</p>
'''

__tos__ = '''
<p>Be nice to others while using this site lest your comments and other actions be ignored and disposed of.  While you may be allowed to write comments
here there is no obligation for those comments to be published unless said comments are constructive and respectful and dare one hope even, useful.  All comments posted to this site are moderated and filtered by someone somewhere so don't get too carried away with yourself as your muse guides your thoughts.</p>
<p>Above all else, have fun !</p>
'''

__registration_complete__ = '''
<h2>Your Registraton has been processed...</h2>
<p class="successMessage">Your User Account is not yet Active however it has been processed and is pending Activation.</p>
<p class="successMessage">You should receive an email shortly with your Account Activation details.</p>
<p class="successMessage">Your pending Account Activation will remain in the system for no more than {{ expiration_days }} days.</p>
<p class="errorMessage">{{ status }}</p>
'''

__resend_registration_complete__ = '''
<h3>Your Registraton (Account Activation) Notice has been resent to<BR/>your email address...</h3>
<p class="successMessage">Your User Account is not yet Active however it has been processed and is pending Activation.</p>
<p class="successMessage">You should receive an email shortly with your Account Activation details.</p>
<p class="successMessage">Your pending Account Activation will remain in the system for no more<BR/>than {{ expiration_days }} days from the date of your original Registration.</p>
<p class="errorMessage">{{ status }}</p>
'''

__send_password_complete__ = '''
<h3>Your Change Password Link has been sent to<BR/>your email address...</h3>
<p class="successMessage">You should receive an email shortly with your Change Password Link.</p>
<p class="successMessage">Once you receive this email<BR/>click on the link and wait for additional instructions.</p>
<p class="errorMessage">{{ status }}</p>
'''

__forgot_password_complete__ = '''
<h2>Your Password has been reset...</h2>
<p class="successMessage">You should receive an email shortly with your new Account Activation Link.</p>
<p class="successMessage">Once you receive this email<BR/>click on the link and wait for additional instructions.</p>
<p class="errorMessage">{{ status }}</p>
'''

__feedback_complete__ = '''
<h2>Thank you...</h2>
<p class="errorMessage">{{ status }}</p>
'''

__registration_help__ = {}
__registration_help__['username'] = '''
<h2>User Name Hints and Tips</h2>
<p>Please enter a User Name that is composed of a single word that has a minimum of 4 characters (letters or numbers).</p>
<p>Notice the red border when your input has been rejected versus the green border that appears once your entry has been accepted.</p>
<p>User Names must be unique, you will see a red border whenever there is a problem with the User Name you have entered.</p>
<p>All required fields must be satisifed with a green border before you will be allowed to click the Register button.</p>
'''
__registration_help__['first_name'] = '''
<h2>First Name Hints and Tips</h2>
<p>Please enter a First Name that is composed of a single word that has a minimum of 1 character (letters or numbers).</p>
<p>Notice the red border when your input has been rejected versus the green border that appears once your entry has been accepted.</p>
<p>All required fields must be satisifed with a green border before you will be allowed to click the Register button.</p>
'''
__registration_help__['last_name'] = __registration_help__['first_name']
__registration_help__['password1'] = '''
<h2>Password Hints and Tips</h2>
<p>Please enter a Password that is composed of 6 or more letters, digits, underscores and hyphens.
Your Password must contain at least one upper case letter, one lower case letter and one digit.</p>
<p>Notice the red border when your input has been rejected versus the green border that appears once your entry has been accepted.</p>
<p>Both the Password and the Paasword verification entered must match exactly; you will see a red border around both until your
inputs have been accepted by the system for processing.</p>
<p>All required fields must be satisifed with a green border before you will be allowed to click the Register button.</p>
'''
__registration_help__['password2'] = __registration_help__['password1']
__registration_help__['password'] = __registration_help__['password1']
__registration_help__['email'] = '''
<h2>Email Address Hints and Tips</h2>
<p>Please enter your valid Internet Email Address; this is the address to which your Account Validation and Activation email will
be sent.  You cannot gain access to this site unless you enter valid information.</p>
<p>Notice the red border when your input has been rejected versus the green border that appears once your entry has been accepted.</p>
<p>Email Addresses must be unique, you will see a red border whenever there is a problem with the Email Address you have entered.</p>
<p>All required fields must be satisifed with a green border before you will be allowed to click the Register button.</p>
'''
__registration_help__['tos'] = '''
<h2>Terms of Service Hints and Tips</h2>
<p>Please read the Terms of Service and click the checkbox that indicates you are in agreement with the TOS.</p>
<p>All required fields must be satisifed with a green border before you will be allowed to click the Register button and you cannot
get Registered unless you agree with the Terms Of Service.</p>
'''

__rssfeed_help__ = {}
__rssfeed_help__['url'] = '''
<h2>Rss Feed Hints and Tips</h2>
<p>Please enter the URL for the Rss Feed from which you want to include content within your SiteMap.Xml file.</p>
'''

__ssl_help__ = '''
<h2>128-bit SSL Help</h2>
<p>This site is protected by 128-bit SSL via {{ secure_endpoint }}.</p>
<p>While it may not look like this site is being protected by 128-bit SSL, it is.</p>
<p>Those pages that bear the lock-symbol icon in the upper-right corner are being protected by 128-bit SSL.  The data coming from and going to the back-end server is encrypted and is not visible to anyone other than yourself and those you allow to see what you are doing.</p>
<p>The encryption is being handled by what is typically known as Cross-Domain AJAX.  The Cross-Domain part comes from the fact that the Google Cloud presently offers SSL for the default domain name through which your site is being served.  It is the default domain that is protected by SSL that is being used whenever you see the lock-symbol icon as previously mentioned.</p>
'''

__registration_activate__ = '''
{% extends 'base.html' %}
{% block title %}(VyperBlog&trade;){% endblock %}

{% block include-css %}{% endblock %}

{% block navigation %}
{% endblock %}

{% block navigation-home %} style="display:none;"{% endblock %}

{% block left_content %}
{% if account %}
  <h1 class="successMessage">Activation successful</h1>
  <p>Congratulations, {{ account.username }}. Your account has been Activated successfully.</p>
  <p>Click <a href="{{ site_domain }}" target="_top">here</a> to continue, you know - log-in and get using your account.</p>
{% else %}
  <h1 class="errorMessage">Activation failed :(</h1>
  <p>Sorry, there were problems with the activation.
  <BR/>
  Please make sure that the activation link was opened correctly in your Browser.
  <BR/>
  Please be also aware that activation links expire automatically.</p>
  <p>Click <a href="{{ site_domain }}" target="_top">here</a> to continue, you know - try again.</p>
{% endif %}
{{ info_string }}
{% endblock %}

{% block right_content %}
{% if account %}
  <BIG class="successMessage">Activation Successful !</BIG>
{% else %}
  <BIG class="errorMessage">Activation Failed !</BIG>
{% endif %}
{% endblock %}
'''

__registration_change_password__ = '''
{% extends 'base.html' %}
{% block title %}(VyperBlog&trade;){% endblock %}

{% block include-css %}{% endblock %}

{% block extra-head %}
{% if isJavaScriptOptimized %}
<script language="JavaScript1.2" type="text/javascript">
$js('/js/js/accountPassword.min.js',function(){});
$js('/js/js/selfHelpKiosk.min.js',function(){});
</script>
{% else %}
<script src="/js/js/accountPassword.min.js" type="text/javascript" language="JavaScript"></script>
<script src="/js/js/selfHelpKiosk.min.js" type="text/javascript" language="JavaScript"></script>
{% endif %}
{% endblock %}

{% block more-javascript %}
function __onWindowLoad(){
adjustAnchors();
}
{% endblock %}

{% block navigation %}
{% endblock %}

{% block navigation-home %} style="display:none;"{% endblock %}

{% block left_content %}
{% if account %}
  {{ forgotPasswordForm }}
{% else %}
  <h1 class="errorMessage">Change Password Failed :(</h1>
  <p>Sorry, but you cannot change your password at this time.
  <BR/>
  Please double check your information and try again.</p>
{% endif %}
{% endblock %}
'''

__cannot_admin__ = '''
<h2>Sorry but <B>YOU</B> are <B>NOT</B> authorized to access this part of the system</h2>
<p>Your IP address has been recorded and you have been reported to the FBI for computer fraud !</p>
'''
__cannot_facebook__ = '''
<h2>Sorry but <B>YOU</B> are <B>NOT</B> authorized to access the FaceBook App</h2>
<p>Please sign-up for your Free FaceBook User Account and then come back here and try again.</p>
'''

__doing_facebook__ = '''
<h2>Welcome to the FaceBook App</h2>
<p>Redirecting you to the FaceBook App...</p>
'''

__stopping_facebook__ = '''
<h2>Leaving FaceBook App...</h2>
<p>Redirecting you now...</p>
'''

__forbidden_request__ = '''
<p class="errorMessage">{{ status }}</p>
'''

__login_code__ = '''
<script src="/js/js/handleLogin.min.js" type="text/javascript" language="JavaScript"></script>
<script src="/js/js/selfHelpKiosk.min.js" type="text/javascript" language="JavaScript"></script>
<script src="/js/js/login.min.js" type="text/javascript" language="JavaScript"></script>
'''

__register_code__ = '''
<script src="/js/js/handleRegister.min.js" type="text/javascript" language="JavaScript"></script>
<script src="/js/js/selfHelpKiosk.min.js" type="text/javascript" language="JavaScript"></script>
<script src="/js/js/register.min.js" type="text/javascript" language="JavaScript"></script>
'''

__frame_wrapper__ = '''
  <head>
    <META HTTP-EQUIV="Pragma" CONTENT="no-cache">
    <META HTTP-EQUIV="Expires" CONTENT="-1">
    <meta http-equiv="Cache-Control" content="no-store" />
    <meta http-equiv="Cache-Control" content="no-cache">
    <meta http-equiv="Expires" content="Sat, 01 Dec 2001 00:00:00 GMT">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="alternate" type="application/rss+xml" title="VyperBlog News" href="/feed/">
    <title>&copy;RayCHorn.Com, All Rights Reserved.</title>
    <script src="/js/js/browser-detect.min.js" type="text/javascript" language="JavaScript"></script>
{% if isJavaScriptOptimized %}
    <script src="/js/js/core.min.js" type="text/javascript" language="JavaScript"></script>
    {{ code }}
{% else %}
    <script src="/js/js/core.min.js" type="text/javascript" language="JavaScript"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js" type="text/javascript" language="JavaScript"></script>
    <script src="/js/js/jquery/alerts/jquery.alerts.min.js" type="text/javascript" language="JavaScript"></script>
    <script src="/js/js/jquery/jdialog/jquery.jdialog.min.js" type="text/javascript" language="JavaScript"></script>
    {{ code }}
{% endif %}
    <script language="javascript" type="text/javascript">
	function _onLoadSWFObject(){}
	function _onDocumentReady(){}
	function _onNoFlashInstalled(){}
        function __onWindowLoad(){
            var act = $('#activity-icon');
            if (act.length > 0){
                act.hide();
            }
           if ( (window.parent.hide_google_balls) && (typeof(window.parent.hide_google_balls) == const_function_symbol) ) {
               try {window.parent.hide_google_balls();} catch (e) {debug_write('(window.parent.hide_google_balls).ERROR '+e.toString());}
           }
        }
    </script>
    <style type="text/css">
        #ssl-icon {
            float: right;
        }
        #activity-icon {
            float: left;
        }
        body {
            margin: 0 0%;
            background-color: #ffffff;
            font-family: Verdana, Arial, Helvetica, sans-serif;
            font-size: 0.75em;
            padding: 0px;
        }
    </style>
</head>
<body>
<div id="activity-icon"><BR/><STRONG><U>Secure</U> <span class="errorMessage">128-bit SSL</span> Connection Confirmed !</STRONG><img src="/static/images/activity/googleballs.gif"/></div>
<div id="ssl-icon"><img class="clickable" src="/static/images/icons/SSL-X-Domain.png" width="150"/></div>
<div id="column_left">
{{ contents }}
</div>
<div id="__debugContainer" style="font-size: 10px; display:none;"><textarea id="__debug" rows="8" cols="80" readonly></textarea></div>
</body>
</html>
'''

__script_wrapper__ = '''
<script type="text/javascript" language="JavaScript">
{{ contents }}
jAlert('(+++)');
</script>
'''

__sponsor_page__ = '''
{% if isRunningLocal %}
<iframe src="http://www.facebook.com/plugins/likebox.php?id={{ xid }}&amp;width={{ width }}&amp;connections={{ connections }}&amp;stream=true&amp;header=true&amp;height={{ height }}" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:550px; height:587px;" allowTransparency="true"></iframe>
{% else %}
<fb:like-box profile_id="{{ xid }}" width="{{ width }}"></fb:like-box>
{% endif %}
'''

__comments_blocked__ = '''
<h3>Comments can be left at this site by registered users only.</h3>
'''

__add_rss_form__ = '''
{% if is_superuser %}
  <div id="formAddRssFeed">
    <table>
       <tr>
          <td>
             <table id="theForm">{{ form }}</table>
          </td>
       </tr>
       <tr>
          <td align="center">
             <input id="btn_submitRssFeed" type="submit" value="Submit Feed" />
          </td>
       </tr>
    </table>
  </div>
{% else %}
  <p>Please Register/Login to perform Admin Functions.</p>
{% endif %}
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__add_verification_form__ = '''
{% if is_superuser %}
  <div id="formAddVerification">
    <table>
       <tr>
          <td>
             <table id="theForm">{{ form2 }}</table>
          </td>
       </tr>
       <tr>
          <td align="center">
             <input id="btn_submitVerification" type="submit" value="Submit Verification" />
          </td>
       </tr>
    </table>
  </div>
{% else %}
  <p>Please Register/Login to perform Admin Functions.</p>
{% endif %}
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__feeds__ = '''
<select id="s_rssfeeds">
<option value="">Choose...</option>
    {% for aChoice in choices %}
        <option value="{{ aChoice.value }}">{{ aChoice.text }}</option>
    {% endfor %}
</select>
<br/>
<input id="btn_removeRssFeed" type="submit" value="Remove this Feed" />
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__verifications__ = '''
<select id="s_verifications">
    {% for aChoice in verificationChoices %}
        <option value="{{ aChoice.value }}">{{ aChoice.text }}</option>
    {% endfor %}
</select>
<br/>
<input id="btn_removeVerification" type="submit" value="Remove this Verification" />
<p class="errorMessage">{{ status }}{{ reason }}</p>
'''

__sitemap_reference__ = '''
<iframe id="iframeSitemapRef" bordercolor="white" width="100%" height="2000" frameborder="0" scrolling="auto" src="{{ url }}"></iframe>
'''

__admin_page__ = '''
{% if is_superuser %}
<div id="tabs">
    <ul>
        <li><a href="#tabs-1">Admin App</a></li>
    </ul>
    <div id="tabs-1">
        <p>You can download the VyperBlog&trade; Admin Tool by clicking on the Install Now Button shown below.  The Install Now Button is only visible to those who have Administrative Credentials.</p>
        <table id="AIRDownloadMessageTable">
            <tr>
                <td>
                    <div id="airBadgeContainer">
                    </div>
                </td>
                <td>
                </td>
                    <BIG>OR</BIG>
                <td>
                Download <a href="/static/air/VyperBlogAdmin.air">VyperBlog&trade; Admin Tool</a> now.<br/><br/>
                <span id="AIRDownloadMessageRuntime">
                This application requires the Adobe&#174;&nbsp;AIR&#8482; runtime to be installed for 
                <a href="http://airdownload.adobe.com/air/mac/download/1.0/AdobeAIR.dmg">Mac OS</a> or 
                <a href="http://airdownload.adobe.com/air/win/download/1.0/AdobeAIRInstaller.exe">Windows</a>.</span>
                </td>
            </tr>
        </table>
    </div>
</div>
{% else %}
  {{ cannotAdmin }}
{% endif %}
'''

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__textMimetype = 'text/plain'

def dict_to_json(dct):
    json = ''
    try:
        from django.utils import simplejson
        json = simplejson.dumps(dct)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        json = {'__error__':info_string}
    return json

def xml_to_json(someXML):
    from xml.dom import minidom
    from django.utils import simplejson
    dom = minidom.parseString(someXML)
    return simplejson.load(dom)

def rest_handle_get_user(request,parms,browserAnalysis):
    _user = get_user(request)
    ignore = ['_entity','_parent','_password']
    valueOf = lambda v:_utils.getAsSimpleDateStr(v,str(_utils.formatDjangoDateTimeStr())) if (ObjectTypeName.typeClassName(v) == 'datetime.datetime') else str(v) if (v != None) else None
    d = dict([(str(k),valueOf(v)) for k,v in _user.__dict__.iteritems() if (k not in ignore) and (v)])
    d['FBID'] = settings.FACEBOOK_APP_ID
    if (browserAnalysis.isUsingAdobeAIR):
        d['air_version'] = _air_admin_tool_version
    if (parms[-2] == '0'):
        __api_dict__['REMOTE_ADDR'] = django_utils.get_from_META(request,'REMOTE_ADDR','')
        d[__api__] = __api_dict__
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_get_endpoints(request,browserAnalysis):
    d = {}
    if (browserAnalysis.isUsingAdobeAIR):
        d['REMOTE_ADDR'] = django_utils.get_from_META(request,'REMOTE_ADDR','')
        d['secure_endpoint'] = __api_dict__['secure_endpoint']
        d['insecure_endpoint'] = __api_dict__['insecure_endpoint']
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_refresh_admin(request,browserAnalysis):
    d = {}
    if (browserAnalysis.isUsingAdobeAIR):
        d['success'] = False
        try:
            from myapp.views import create_admin_user
            create_admin_user(request)
            d['success'] = True
        except:
            pass
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_post_domain(request,browserAnalysis,form_class=forms.DomainForm,extra_context=None):
    isFormValid = True
    isResendRegistrationComplete = False
    resendRegistrationReason = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                results = form.save(request)
                isFormComplete = results['bool']
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                pass
            if (browserAnalysis.isUsingAdobeAIR):
                d = {}
                d['success'] = isFormComplete
                json = dict_to_json(d)
                return HttpResponse(content=json,mimetype=__jsonMimetype)
        elif (browserAnalysis.isUsingAdobeAIR):
            d = lists.HashedLists()
            for k,v in form.errors.iteritems():
                d['error'] = v.as_text()
            d['success'] = False
            d = d.asDict()
            for k,v in d.iteritems():
                d[k] = v[0] if (misc.isList(v)) else v
            json = dict_to_json(d)
            return HttpResponse(content=json,mimetype=__jsonMimetype)
    d = {}
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_get_menu(request):
    _user = get_user(request)
    last_rank = lambda menu:menu[-1][menu[-1].keys()[-1]]['rank']
    _menu = [
        {'Home':{'title':'Home','rank':1}},
        {'About':{'title':'About','rank':2}},
        {'Categories':{'title':'Categories','rank':3}},
        {'Tags':{'title':'Tags','rank':4}},
        {'Languages':{'title':'Languages','rank':5}}]
    if (_user.is_authenticated()):
        _menu.append({'Logout':{'title':'Logout','rank':last_rank(_menu)+1}})
    else:
        _menu.append({'Register':{'title':'Register','rank':last_rank(_menu)+1}})
        _menu.append({'Login':{'title':'Login','rank':last_rank(_menu)+1}})
    if (_user.is_superuser):
        _menu.append({'Admin':{'title':'Admin','rank':last_rank(_menu)+1}})
    h = myOOHTML.Html()
    iCount = 1
    iMax = len(_menu)
    for m in _menu:
        _class = 'parent' if (iCount == 1) else 'last' if (iCount == iMax) else ''
        k = m.keys()[0]
        t = m[k]['title']
        hh = myOOHTML.Html()
        hh.tag_A(myOOHTML.renderSPAN(t),id='a_%s'%(k),title=t,class_=_class)
        liTag = h.tag_LI(hh.toHtml())
        iCount += 1
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def handle_references(qry,name,isRobot=False):
    l_items = []
    for anItem in qry:
        hh = myOOHTML.Html()
        if (isRobot):
            hh.tagSPAN(anItem.title)
        else:
            hh.tag_A(anItem.title,href='#',id='a_entry%s_%s'%(name,anItem.id),title=anItem.title)
        l_items.append(hh.toHtml())
    return l_items

def render_like_button(request,browserAnalysis,article):
    import urllib2
    context = RequestContext(request)
    url = article.Location() if (callable(article.Location)) else article.Location
    context['isRunningLocal'] = browserAnalysis.isRunningLocal(request)
    context['url'] = __api_dict__['insecure_endpoint']+url
    context['url_encoded'] = urllib2.quote(context['url'])
    return django_utils.render_from_string(__like_button__,context=context)

def render_fb_comments(request,browserAnalysis,article):
    context = RequestContext(request)
    context['xid'] = __api_dict__['insecure_endpoint']+article.Location()
    context['numposts'] = 10
    context['width'] = 750
    return django_utils.render_from_string(__fb_comments__,context=context)

def render_share_button(request,browserAnalysis,article):
    context = RequestContext(request)
    url = article.Location()
    context['url'] = __api_dict__['insecure_endpoint']+url
    context['title'] = article.title
    return django_utils.render_from_string(__fb_share__,context=context)

def render_articles_from(request,browserAnalysis,articles,onlyOne=False,isRobot=False,isExternal=False):
    h = myOOHTML.Html()
    for a in articles:
        d = h.tagDIV('')
        hh = myOOHTML.Html()
        if (isExternal):
            _url = a.Location() if (callable(a.Location)) else a.Location
            hh.tag_A(a.title,href='%s%s'%(__api_dict__['blog_link'],_url),id='a_externalEntry',title=a.title,target='_blank')
        else:
            hh.tag_A(a.title,href='#' if (not isRobot) else '/?article=%s'%(a.id),id='a_entry_%s'%(a.id),title=a.title)
        d.tag_H1(hh.toHtml())
        if (a.timestamp):
            if (ObjectTypeName.typeClassName(a.timestamp).find('datetime') == -1):
                import sitemaps
                a.timestamp = sitemaps.updated_as_timestamp(a.timestamp)
            try:
                d.tagP('%s %s' % (_utils.getAsSimpleDateStr(a.timestamp,fmt=_utils.formatShortBlogDateStr()),_utils.getAsSimpleDateStr(a.timestamp,fmt=_utils.formatSimpleBlogTimeStr())))  # JUNE 4, 2010 BY RAYCHORN LEAVE A COMMENT (EDIT)
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                logging.error(info_string)
            d.tagBR()
        if (onlyOne):
            d.tagDIV(a.content)
        else:
            d.tagDIV(a.teaser if (a.teaser) else '')
            d.tagBR()
            hh = myOOHTML.Html()
            _moreTitle = 'Read the Details...'
            hh.tag_A(_moreTitle,href='#' if (not isRobot) else '/?article=%s'%(a.id),id='a_entryDetails_%s'%(a.id),title=_moreTitle)
            d.tagP(hh.toHtml())
            d.tagBR()
            hh = myOOHTML.Html()
            _moreTitle = 'Comments...'
            hh.tag_A(_moreTitle,href='#' if (not isRobot) else '/?article=%s&comments=1'%(a.id),id='a_entryComments_%s'%(a.id),title=_moreTitle)
            d.tagDIV(hh.toHtml(),id='div_entryComments_%s'%(a.id))
            #d.tagBR()
            d.tagBR()
            #d.tagDIV(render_share_button(request,browserAnalysis,a))
            #if (browserAnalysis.isRunningLocal(request)):
            d.tagDIV(render_like_button(request,browserAnalysis,a))
            #else:
            #d.tagBR()
            #d.tagDIV(render_fb_comments(request,browserAnalysis,a))
        #d.tagBR()
        try:
            if (a.tag):
                tags = a.tag.all()
                if (tags.count() > 0):
                    d.tagP('Tags: %s' % (', '.join(handle_references(tags,'Tag',isRobot=isRobot))))
        except:
            pass
        try:
            if (a.language):
                languages = a.language.all()
                if (languages.count() > 0):
                    d.tagP('Languages: %s' % (', '.join(handle_references(languages,'Language',isRobot=isRobot))))
        except:
            pass
        try:
            if (a.category):
                categories = a.category.all()
                if (categories.count() > 0):
                    d.tagP('Categories: %s' % (', '.join(handle_references(categories,'Category',isRobot=isRobot))))
        except:
            pass
        d.tagOp(myOOHTML.oohtml.HR,width='500px',align='left',color='blue')
        d.tagBR()
        d.tagBR()
    return h

def _get_rss_articles(request,browserAnalysis):
    import sitemaps
    from vyperlogix.hash.lists import HashedLists
    d_entries = HashedLists()
    feeds = models.RssFeed.all()
    _cnt = feeds.count()
    avg_entries_per = _feed_entries_allowed_ / (_cnt if (_cnt > 0) else 1)
    for aFeed in feeds:
        entries = memcache.get('feed_%s'%(aFeed.url))
        if entries is None:
            foo = feedparser.parse(aFeed.url)
            if _is_feed_valid(foo):
                entries = foo['entries']
                d_entries[aFeed.url] = entries
                _cache_feed_entries(aFeed.url,entries,_feed_entries_cache_seconds_)
        else:
            entries = _uncache_feed_entries(entries)
            d_entries[aFeed.url] = entries
    all_entries = []
    i = _feed_entries_allowed_
    while (i > 0):
        for k,v in d_entries.iteritems():
            bucket = d_entries[k][0] if (misc.isList(d_entries[k])) else d_entries[k]
            if (len(bucket) > 0):
                all_entries.append(bucket.pop())
            i -= 1
            if (i <= 0):
                break
        if (i <= 0):
            break
        i -= 1
    _entries = []
    for entry in all_entries[0:_feed_entries_allowed_]:
        entry.timestamp = sitemaps.updated_as_timestamp(entry.updated)
        entry.teaser = entry.summary
        entry.Location = entry.link
        _entries.append(entry)
    h = render_articles_from(request,browserAnalysis,_entries,isExternal=True)
    return h

def _get_articles(request,browserAnalysis,usingID=None,usingTagID=None,usingCatID=None,usingLangID=None,onlyOne=False):
    today = _utils.today_localtime()
    articles = models.Entry.all()
    current_articles = []
    articles = articles.filter('publish_on >=',None).filter('publish_on <=',today)
    if (usingID) or (usingTagID) or (usingCatID) or (usingLangID):
        bools = []
        if (usingID):
            bools = [(item.id == usingID) for item in articles]
        elif (usingTagID):
            bools = [any([(aTag.id == usingTagID) for aTag in item.tag.all()]) for item in articles]
        elif (usingCatID):
            bools = [any([(aCat.id == usingCatID) for aCat in item.category.all()]) for item in articles]
        elif (usingLangID):
            bools = [any([(aLang.id == usingLangID) for aLang in item.language.all()]) for item in articles]
        if (any(bools)):
            if (usingTagID) or (usingCatID) or (usingLangID):
                ar = []
                for i in xrange(0,len(bools)):
                    if (bools[i]):
                        ar.append(articles[i])
                articles = ar
            else:
                i = bools.index(True)
                articles = articles[i+1:articles.count()] if (not onlyOne) else articles[i:i+1]
    else:
        current_articles = [item for item in articles if (item.timestamp.month == today.month) and (item.timestamp.year == today.year)]
    signal_more_articles = '' # nothing here means there are no more articles to show...
    if (len(current_articles) > 0):
        if (articles.count() > len(current_articles)):
            signal_more_articles = current_articles[-1].id # pick the last date from the current_articles and use it to signal for more articles...
        articles = current_articles
    h = render_articles_from(request,browserAnalysis,articles,onlyOne=onlyOne)
    if (len(signal_more_articles) > 0):
        hh = myOOHTML.Html()
        _moreTitle = 'MORE ARTICLES...'
        hh.tag_A(_moreTitle,href='#',id='a_entryMORE_%s'%(signal_more_articles),title=_moreTitle)
        h.tagP(hh.toHtml())
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def rest_handle_get_articles(request,browserAnalysis):
    _id = request.session['article_id'] if (request.session.has_key('article_id')) else None
    return _get_articles(request,browserAnalysis) if (not _id) else _get_articles(request,browserAnalysis,usingID=_id,onlyOne=True)

def _get_externals(request,browserAnalysis):
    h = myOOHTML.Html()
    hRSS = _get_rss_articles(request,browserAnalysis)
    h.tagDIV(hRSS.toHtml())
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def rest_handle_get_externals(request,browserAnalysis):
    return _get_externals(request,browserAnalysis)

def rest_handle_get_more_articles(request,parms,browserAnalysis):
    return _get_articles(request,browserAnalysis,usingID=parms[-2])

def rest_handle_get_one_article(request,parms,browserAnalysis):
    return _get_articles(request,browserAnalysis,usingID=parms[-2],onlyOne=True)

def rest_handle_get_one_tag(request,parms,browserAnalysis):
    return _get_articles(request,browserAnalysis,usingTagID=parms[-2])

def rest_handle_get_one_category(request,parms,browserAnalysis):
    return _get_articles(request,browserAnalysis,usingCatID=parms[-2])

def rest_handle_get_one_language(request,parms,browserAnalysis):
    return _get_articles(request,browserAnalysis,usingLangID=parms[-2])

def handle_get_classifications(request,qry,name):
    from vyperlogix.misc import pluralize
    parms = django_utils.parse_url_parms(request)
    url = '/%s' % (str('/'.join(parms)))
    h = myOOHTML.Html()
    hh = myOOHTML.Html()
    try:
        h.tagBR()
        h.tagBR()
        p = pluralize.plural(name)
        t = '%s:'%(p)
        tagH1 = hh.tagH1('')
        #tagH1.tag_A(t,href='#get=%s'%(p.lower()),id='a_%s'%(p),title=t)
        tagH1.tagB(t)
        a = hh.toHtml()
        h.tagP(a+'<BR/><BR/><BR/>%s' % ('<BR/><BR/>'.join(handle_references(qry,name))))
    except Exception, e:
        h.tagP('WARNING: Unable to retrieve data for the "%s" you selected.  Reason: %s'%(name,e))
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def rest_handle_get_categories(request):
    categories = models.Category.all()
    return handle_get_classifications(request,categories,'Category')

def rest_handle_get_tags(request):
    tags = models.Tag.all()
    return handle_get_classifications(request,tags,'Tag')

def rest_handle_get_languages(request):
    languages = models.Language.all()
    return handle_get_classifications(request,languages,'Language')

def rest_handle_set_facebook(request):
    context = RequestContext(request)
    if (request.method == 'POST'):
        _uid_ = request.POST['uid']
        _access_token_ = django_utils.get_from_post(request,'access_token','')
        _expires_ = django_utils.get_from_post(request,'expires',0)
        _expires_ = int(_expires_) if (not isinstance(_expires_,int)) and (len(_expires_) > 0) else 0
        _base_domain_ = django_utils.get_from_post(request,'base_domain','')
        _perms_ = django_utils.get_from_post(request,'perms','')
        _secret_ = django_utils.get_from_post(request,'secret','')
        _sig_ = django_utils.get_from_post(request,'sig','')
        _session_key_ = django_utils.get_from_post(request,'session_key','')
        if (len(_uid_) > 0):
            if (not request.session.has_key('facebookUser_id')):
                users = [aUser for aUser in FacebookUser.all() if (aUser.uid == _uid_)]
            else:
                _uid_ = request.session['facebookUser_id']
                users = [aUser for aUser in FacebookUser.all() if (aUser.id == _uid_)]
            if (len(users) == 0):
                aFacebookUser = FacebookUser(uid=_uid_,access_token=_access_token_,expires=_expires_,base_domain=_base_domain_,perms=_perms_,secret=_secret_,sig=_sig_,session_key=_session_key_)
                aFacebookUser.save()
            else:
                aFacebookUser = users[0]
            request.session['facebookUser_id'] = aFacebookUser.id
            request.session.save()
            _content = django_utils.compressContent(django_utils.render_from_string(__doing_facebook__,context=context))
            return HttpResponse(content=_content,mimetype=__mimetype)
        else:
            if (request.session.has_key('facebookUser_id')):
                _uid_ = request.session['facebookUser_id']
                users = [aUser for aUser in FacebookUser.all() if (aUser.id == _uid_)]
                if (len(users) > 0):
                    aFacebookUser = users[0]
                    aFacebookUser.delete()
                del request.session['facebookUser_id']
                request.session.save()
            _content = django_utils.compressContent(django_utils.render_from_string(__stopping_facebook__,context=context))
            return HttpResponse(content=_content,mimetype=__mimetype)
    _content = django_utils.compressContent(django_utils.render_from_string(__cannot_facebook__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def handle_account_logout(request):
    return HttpResponseRedirect('/admin/')

def rest_handle_resend_register(request,form_class=ResendRegistrationForm,extra_context=None):
    isFormValid = True
    isResendRegistrationComplete = False
    resendRegistrationReason = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        domain_override = request.get_host()
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                hasEmailBeenSent = form.save(domain_override=domain_override,isRunningLocal=django_utils.isRunningLocal(request))
                isResendRegistrationComplete = hasEmailBeenSent['bool']
                resendRegistrationReason = hasEmailBeenSent['reason']
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                pass
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isResendRegistrationComplete):
        context['form'] = form
        context['selfHelp'] = __self_help__
        context['reason'] = resendRegistrationReason if (resendRegistrationReason) else ''
    context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
    _content = django_utils.compressContent(django_utils.render_from_string(__resend_registration_form__ if (not isResendRegistrationComplete) else __resend_registration_complete__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_send_password(request,form_class=SendChangePasswordForm,extra_context=None):
    isFormValid = True
    isSendPasswordComplete = False
    sendPasswordReason = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        domain_override = request.get_host()
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                hasEmailBeenSent = form.save(domain_override=domain_override)
                isSendPasswordComplete = hasEmailBeenSent['bool']
                sendPasswordReason = hasEmailBeenSent['reason']
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                pass
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isSendPasswordComplete):
        context['form'] = form
        context['selfHelp'] = __self_help__
        context['reason'] = sendPasswordReason if (sendPasswordReason) else ''
    context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
    _content = django_utils.compressContent(django_utils.render_from_string(__send_password_form__ if (not isSendPasswordComplete) else __send_password_complete__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_forgot_password(request,form_class=ForgotPasswordForm,extra_context=None):
    isFormValid = True
    isForgotPasswordComplete = False
    forgotPasswordReason = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        domain_override = request.get_host()
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                hasEmailBeenSent = form.save(domain_override=domain_override)
                isForgotPasswordComplete = hasEmailBeenSent['bool']
                forgotPasswordReason = hasEmailBeenSent['reason']
            except:
                pass
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isForgotPasswordComplete):
        context['form'] = form
        context['selfHelp'] = __self_help__
        context['reason'] = forgotPasswordReason if (forgotPasswordReason) else ''
    _content = django_utils.compressContent(django_utils.render_from_string(__forgot_password_form__ if (not isForgotPasswordComplete) else __forgot_password_complete__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_user_feedback(request,form_class=FeedbackForm,extra_context=None):
    isFormValid = True
    isFeedbackComplete = False
    feedbackReason = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        domain_override = request.get_host()
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                _user = get_user(request)
                result = form.save(domain_override=domain_override,user=_user)
                isFeedbackComplete = result['bool']
                feedbackReason = result['reason']
            except:
                pass
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isFeedbackComplete):
        _user = get_user(request)
        context['form'] = form
        context['authenticated'] = _user.is_authenticated()
    _content = django_utils.compressContent(django_utils.render_from_string(__feedback_form__ if (not isFeedbackComplete) else __feedback_complete__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_register(request,queryObject,browserAnalysis,form_class=RegistrationForm,extra_context=None):
    isFormValid = True
    isRegistrationComplete = False
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        domain_override = request.get_host()
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                new_user = form.save(domain_override)
                isRegistrationComplete = True
            except:
                pass
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isRegistrationComplete):
        context['form'] = form
        context['selfHelp'] = __self_help__
        _content = django_utils.render_from_string(__registration_form__,context=context)
    else:
        context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
        _content = django_utils.render_from_string(__registration_complete__,context=context)
    _content = django_utils.compressContent(_content)
    if (queryObject.fr == '1'):
        context['isRunningLocal'] = browserAnalysis.isRunningLocal(request)
        context['isJavaScriptOptimized'] = browserAnalysis.isJavaScriptOptimized
        context['contents'] = _content
        context['code'] = __register_code__
        _content = django_utils.compressContent(django_utils.render_from_string(__frame_wrapper__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_login(request,queryObject,browserAnalysis,form_class=forms.AuthenticationForm,extra_context=None):
    isFormValid = True
    isLoginComplete = False
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                from django.contrib.auth import login
                login(request, form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                isLoginComplete = True
            except:
                pass
            if (browserAnalysis.isUsingAdobeAIR):
                aUser = get_user(request)
                d = {}
                d['success'] = d['loggedin'] = aUser.is_active and aUser.is_authenticated() and aUser.is_superuser
                json = dict_to_json(d)
                return HttpResponse(content=json,mimetype=__jsonMimetype)
        elif (browserAnalysis.isUsingAdobeAIR):
            d = lists.HashedLists()
            for k,v in form.errors.iteritems():
                d['error'] = v.as_text()
            d['success'] = d['loggedin'] = False
            d = d.asDict()
            for k,v in d.iteritems():
                d[k] = v[0] if (misc.isList(v)) else v
            json = dict_to_json(d)
            return HttpResponse(content=json,mimetype=__jsonMimetype)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isLoginComplete):
        context['form'] = form
        context['selfHelp'] = __self_help__
        _content = django_utils.render_from_string(__login_form__,context=context)
    else:
        _content = django_utils.render_from_string(__login_complete__,context=context)
    _content = django_utils.compressContent(_content)
    if (queryObject.jsp == '1') and (queryObject.cb) and (queryObject.dst) and (queryObject.p):
        _content = "try{%s($('#%s'),'%s','%s');}catch(e){jAlert('WARNING: Something went wrong with the server - please try back later...');}" % (queryObject.p,queryObject.dst,_content,queryObject.cb)
    #elif (queryObject.fr == '1') and (queryObject.cb) and (queryObject.dst) and (queryObject.p):
        #_content = django_utils.render_from_string(__script_wrapper__,context=context)
    elif (queryObject.fr == '1'):
        context['isRunningLocal'] = browserAnalysis.isRunningLocal(request)
        context['isJavaScriptOptimized'] = browserAnalysis.isJavaScriptOptimized
        context['contents'] = _content
        context['code'] = __login_code__
        _content = django_utils.compressContent(django_utils.render_from_string(__frame_wrapper__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_post_rssfeed(request,queryObject,browserAnalysis,form_class=forms.RssForm):
    isFormValid = True
    isFormComplete = False
    response = {'status':''}
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                results = form.save(request)
                choices = get_rss_feed_choices(isPythonObj=True,isUsingAdobeAIR=browserAnalysis.isUsingAdobeAIR)
                isFormComplete = results['bool']
                response['choices'] = choices
                response['status'] = 'The Feed URL you entered was invalid or was not a valid RSS Feed URL.  Please try again.' if (not isFormComplete) else ''
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                response['status'] = 'Something went wrong with %s.' % (e)
            if (browserAnalysis.isUsingAdobeAIR):
                d = {}
                d['choices'] = choices
                json = dict_to_json(d)
                return HttpResponse(content=json,mimetype=__jsonMimetype)
        elif (browserAnalysis.isUsingAdobeAIR):
            d = lists.HashedLists()
            for k,v in form.errors.iteritems():
                d['error'] = v.as_text()
            d['success'] = d['loggedin'] = False
            d = d.asDict()
            for k,v in d.iteritems():
                d[k] = v[0] if (misc.isList(v)) else v
            json = dict_to_json(d)
            return HttpResponse(content=json,mimetype=__jsonMimetype)

    if (not isFormValid):
        response['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
        for k,v in form.errors.iteritems():
            response[k] = v
    context = RequestContext(request)
    context['choices'] = choices
    context['status'] = response['status'] if (response.has_key('status')) else ''
    _content = django_utils.compressContent(django_utils.render_from_string(__feeds__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_get_rssfeeds(request,browserAnalysis):
    d = {}
    choices = get_rss_feed_choices(isPythonObj=True,isUsingAdobeAIR=browserAnalysis.isUsingAdobeAIR) if (browserAnalysis.isUsingAdobeAIR) else []
    d['choices'] = choices
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_post_verification(request,queryObject,browserAnalysis,form_class=forms.VerificationForm):
    isFormValid = True
    isFormComplete = False
    verifications = []
    response = {'status':''}
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                results = form.save(request)
                verifications = get_verifications()
                isFormComplete = results['bool']
                response['status'] = 'The Google Site Verification you entered was invalid or was not valid.  Please try again.' if (not isFormComplete) else ''
            except Exception, e:
                info_string = _utils.formattedException(details=e)
                response['status'] = 'Something went wrong with %s.' % (e)
    
    context = RequestContext(request)
    if (not isFormValid):
        response['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
        for k,v in form.errors.iteritems():
            response[k] = v
        verifications = get_verifications()
        context['status'] = response['status']
    else:
        context['status'] = ''
    context['verificationChoices'] = verifications
    _content = django_utils.compressContent(django_utils.render_from_string(__verifications__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_remove_rssfeed(request,queryObject,browserAnalysis,form_class=forms.RssForm):
    isFormValid = True
    isFormComplete = False
    response = {'status':''}
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                results = form.remove()
                choices = get_rss_feed_choices(isPythonObj=True,isUsingAdobeAIR=browserAnalysis.isUsingAdobeAIR)
                isFormComplete = results['bool']
                response['choices'] = choices
            except:
                pass
            if (browserAnalysis.isUsingAdobeAIR):
                d = {}
                d['choices'] = choices
                json = dict_to_json(d)
                return HttpResponse(content=json,mimetype=__jsonMimetype)
        elif (browserAnalysis.isUsingAdobeAIR):
            d = lists.HashedLists()
            for k,v in form.errors.iteritems():
                d['error'] = v.as_text()
            d['success'] = d['loggedin'] = False
            d = d.asDict()
            for k,v in d.iteritems():
                d[k] = v[0] if (misc.isList(v)) else v
            json = dict_to_json(d)
            return HttpResponse(content=json,mimetype=__jsonMimetype)
    
    if (not isFormValid):
        response['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
        for k,v in form.errors.iteritems():
            response[k] = v
    context = RequestContext(request)
    context['choices'] = choices
    _content = django_utils.compressContent(django_utils.render_from_string(__feeds__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_remove_verification(request,queryObject,browserAnalysis,form_class=forms.VerificationForm):
    isFormValid = True
    isFormComplete = False
    response = {'status':''}
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                results = form.remove()
                isFormComplete = results['bool']
            except:
                pass
    
    if (not isFormValid):
        response['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
        for k,v in form.errors.iteritems():
            response[k] = v
    context = RequestContext(request)
    context['verificationChoices'] = get_verifications(isPythonObj=True)
    _content = django_utils.compressContent(django_utils.render_from_string(__verifications__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def rest_handle_user_sponsor(request,browserAnalysis):
    context = RequestContext(request)
    context['isRunningLocal'] = browserAnalysis.isRunningLocal(request)
    context['xid'] = settings.FACEBOOK_SPONSOR_ID
    context['width'] = 550
    context['connections'] = 10
    context['height'] = 587
    _content = django_utils.compressContent(django_utils.render_from_string(__sponsor_page__,context=context))
    return HttpResponse(content=_content,mimetype=__mimetype)

def get_rss_feed_choices(isPythonObj=False,isUsingAdobeAIR=False):
    choices = []
    feeds = dict([(feed.id,feed.url) for feed in models.RssFeed.all()])
    minLens = misc.sort([len(v) for v in feeds.values()])
    l = minLens[0] if (misc.isList(minLens)) and (len(minLens) > 0) else 30
    for k,v in feeds.iteritems():
        so = SmartObject()
        so.value = k
        so.text = v[0:l]+'...' if (not isUsingAdobeAIR) else v
        choices.append(so.asPythonDict() if (isPythonObj) else so)
    return choices

def get_verifications(isPythonObj=False):
    choices = []
    values = dict([(aValue.id,aValue.value) for aValue in models.Setting.all() if (aValue.name == forms.google_site_verification)])
    for k,v in values.iteritems():
        so = SmartObject()
        so.value = k
        so.text = v
        choices.append(so.asPythonDict() if (isPythonObj) else so)
    return choices

def rest_handle_get_admin(request):
    _user = get_user(request)
    if (_user.is_superuser):
        choices = get_rss_feed_choices()
        verifications = get_verifications()
        context = RequestContext(request)
        context['is_superuser'] = _user.is_superuser
        context['cannotAdmin'] = __cannot_admin__
        context['form'] = forms.RssForm()
        context['form2'] = forms.VerificationForm()
        context['choices'] = choices
        context['verificationChoices'] = verifications
        context['verifications'] = django_utils.compressContent(django_utils.render_from_string(__verifications__,context=context))
        context['form_content'] = django_utils.compressContent(django_utils.render_from_string(__add_rss_form__,context=context))
        context['form2_content'] = django_utils.compressContent(django_utils.render_from_string(__add_verification_form__,context=context))
        context['feeds'] = django_utils.compressContent(django_utils.render_from_string(__feeds__,context=context))
        _content = django_utils.compressContent(django_utils.render_from_string(__admin_page__,context=context))
        return HttpResponse(content=_content,mimetype=__mimetype)
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__cannot_admin__,context=context)),mimetype=__mimetype)

def rest_handle_logout(request):
    from django.contrib.auth import logout
    logout(request)
    context = RequestContext(request)
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__logout_complete__,context=context)),mimetype=__mimetype)

def rest_handle_register_tos(request):
    context = RequestContext(request)
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__tos__,context=context)),mimetype=__mimetype)

def rest_handle_register_help(request,parms):
    context = RequestContext(request)
    try:
        return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__registration_help__[parms[-2]],context=context)),mimetype=__mimetype)
    except:
        pass
    return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(['Unable to retrieve the requested information.  Please try again at a later time...'])), mimetype=__mimetype)

def rest_handle_login_help(request,parms):
    context = RequestContext(request)
    try:
        return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__registration_help__[parms[-2]],context=context)),mimetype=__mimetype)
    except:
        pass
    return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(['Unable to retrieve the requested information.  Please try again at a later time...'])), mimetype=__mimetype)

def rest_handle_rssfeed_help(request,parms):
    context = RequestContext(request)
    try:
        return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__rssfeed_help__[parms[-2]],context=context)),mimetype=__mimetype)
    except:
        pass
    return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(['Unable to retrieve the requested information.  Please try again at a later time...'])), mimetype=__mimetype)

def rest_handle_ssl_help(request):
    try:
        context = RequestContext(request)
        context['secure_endpoint'] = __api_dict__['secure_endpoint']
        return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__ssl_help__,context=context)),mimetype=__mimetype)
    except:
        pass
    return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(['Unable to retrieve the requested information.  Please try again at a later time...'])), mimetype=__mimetype)

def rest_handle_send_mail(request):
    context = RequestContext(request)
    registrations = [item for item in RegistrationProfile.all() if (not item.activation_key_expired())]
    # this code does nothing for now because one cannot simply pick unrealized dreams and make them happen - could be too many...
    try:
        return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__registration_help__[parms[-2]],context=context)),mimetype=__mimetype)
    except:
        pass
    return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(['Unable to retrieve the requested information.  Please try again at a later time...'])), mimetype=__mimetype)

def render_comments_from(request,browserAnalysis,comments):
    h = myOOHTML.Html()
    iComment = 1
    nComment = len(comments)
    for a in comments:
        d = h.tagDIV('')
        hh = myOOHTML.Html()
        d.tag_H1(hh.toHtml())
        d.tagP('Comment #%d by %s on %s at %s' % (iComment,a.user,_utils.getAsSimpleDateStr(a.timestamp,fmt=_utils.formatShortBlogDateStr()),_utils.getAsSimpleDateStr(a.timestamp,fmt=_utils.formatSimpleBlogTimeStr())))
        d.tagBR()
        d.tagDIV(a.content)
        if (iComment < nComment):
            d.tagBR()
            d.tagBR()
            d.tagOp(myOOHTML.oohtml.HR,width='500px',align='left',color='#C0C0C0')
        d.tagBR()
        iComment += 1
    d.tagOp(myOOHTML.oohtml.HR,width='500px',align='left',color='black')
    d.tagBR()
    d.tagBR()
    return h.toHtml()

def get_user_comment_form(request,browserAnalysis,recid,form_class=forms.CommentForm,extra_context=None):
    isFormValid = True
    isCommentComplete = False
    commentReason = None
    aComment = None
    if (request.method == 'POST'):
        form = form_class(data=request.POST, files=request.FILES)
        isFormValid = form.is_valid()
        if (isFormValid):
            try:
                _user = get_user(request)
                result = form.save(recid=recid,user=_user)
                isCommentComplete = result['bool']
                commentReason = result['reason']
                aComment = result['comment']
            except:
                pass
    else:
        form = form_class(recid=recid)
    
    if extra_context is None:
        extra_context = {}
    if (not isFormValid):
        extra_context['status'] = 'WARNING: Invalid entries submitted.  Please correct and try again...'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if (not isCommentComplete):
        _user = get_user(request)
        context['form'] = form
        context['authenticated'] = _user.is_authenticated()
    else:
        context['content'] = render_comments_from(request,browserAnalysis,[aComment])
    return django_utils.render_from_string(__comment_form__ if (not isCommentComplete) else __comment_complete__,context=context)

def rest_handle_get_comments(request,parms,browserAnalysis,isRobot=False):
    t = ''
    _user = get_user(request)
    if (_user.is_authenticated()):
        recid = parms[-2] if (request.method == 'GET') else django_utils.get_from_post_or_get(request,'recid')
        comments = [c for c in models.Comment.all() if (c.entry.id == recid)]
        t = 'Be the first to leave a comment...' if (len(comments) == 0) else render_comments_from(request,browserAnalysis,comments)
        t += get_user_comment_form(request,browserAnalysis,recid)
    else:
        t = __comments_blocked__
    context = RequestContext(request)
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(t,context=context)),mimetype=__mimetype)

def handle_account_activate(request,parms,extra_context=None):
    #         template_name='registration/activate.html',
    #         extra_context=None):
    """
    Activate a ``User``'s account from an activation key, if their key
    is valid and hasn't expired.
    
    **Context:**
    
    ``account``
        The ``User`` object corresponding to the account, if the
        activation was successful. ``False`` if the activation was not
        successful.
    
    ``expiration_days``
        The number of days for which activation keys stay valid after
        registration.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    """
    info_string = ''
    activation_key = parms[-1].lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    context['account'] = account
    context['expiration_days'] = settings.ACCOUNT_ACTIVATION_DAYS
    context['info_string'] = info_string
    context['site_domain'] = 'http://%s/'%(settings.DOMAIN_NAME) if (settings.IS_PRODUCTION_SERVER) else '/'
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__registration_activate__,context=context)),mimetype=__mimetype)

def handle_account_password(request,parms,browserAnalysis,qryObj,extra_context=None):
    from vyperlogix.products import keys
    email_address = keys._decode(parms[-1])
    registrations = [aRegistration for aRegistration in RegistrationProfile.all() if (aRegistration.activation_key_expired()) and (aRegistration.user.email == email_address)]
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    context['account'] = registrations[0] if (len(registrations) > 0) else None
    #context['selfHelp'] = __self_help__
    context['form'] = ForgotPasswordForm()
    context['forgotPasswordForm'] = django_utils.render_from_string(__forgot_password_form__,context=context)
    d={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj}
    for k,v in d.iteritems():
        context[k] = v
    return HttpResponse(content=django_utils.compressContent(django_utils.render_from_string(__registration_change_password__,context=context)),mimetype=__mimetype)

def handle_sitemap_entry(request,parms,browserAnalysis):
    _id = parms[-1]
    articles = [item for item in models.Entry.all() if (item.id == _id)]
    h = render_articles_from(request,browserAnalysis,articles,isRobot=True) #  if (browserAnalysis.isRunningLocal(request)) else browserAnalysis.isRobot
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def handle_sitemap_category(request,parms,browserAnalysis):
    _id = parms[-1]
    articles = [item for item in models.Entry.all() if (item.category.id == _id)]
    h = render_articles_from(request,browserAnalysis,articles,isRobot=True) #  if (browserAnalysis.isRunningLocal(request)) else browserAnalysis.isRobot
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def handle_sitemap_language(request,parms,browserAnalysis):
    _id = parms[-1]
    articles = [item for item in models.Entry.all() if (item.language.id == _id)]
    h = render_articles_from(request,browserAnalysis,articles,isRobot=True) #  if (browserAnalysis.isRunningLocal(request)) else browserAnalysis.isRobot
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def handle_sitemap_tag(request,parms,browserAnalysis):
    _id = parms[-1]
    articles = [item for item in models.Entry.all() if (item.tag.id == _id)]
    h = render_articles_from(request,browserAnalysis,articles,isRobot=True if (browserAnalysis.isRunningLocal(request)) else browserAnalysis.isRobot)
    return HttpResponse(content=h.toHtml(),mimetype=__mimetype)

def _handle_blog_link(request,url,parms,browserAnalysis):
    context = RequestContext(request)
    context['url'] = url
    _content = django_utils.render_from_string(__sitemap_reference__,context=context)
    verifications = get_verifications()
    _verification = verifications[0].text if (len(verifications) > 0) else False
    response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'content':_content,'google_site_verification':_verification,'isShowingFlash':False,'isShowingTitleBar':True})
    return response

def _handle_blog_frames(request,url,parms,browserAnalysis):
    context = RequestContext(request)
    verifications = get_verifications()
    _verification = verifications[0].text if (len(verifications) > 0) else False
    response = render_to_response(request, 'frameset.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'topFrame':'/blog/nav/','mainFrame':url,'google_site_verification':_verification,'title':'VyperBlog'})
    return response

def handle_sitemap_reference(request,parms,browserAnalysis):
    _url = '/'.join(parms[2:]).replace('http:/','http://').replace('https:/','https://')
    _isRobot=browserAnalysis.isRobot #True if (browserAnalysis.isRunningLocal(request)) else browserAnalysis.isRobot
    if (_isRobot):
        import urllib, urlparse
        #from vyperlogix.soup.BeautifulSoup import BeautifulSoup
        #toks = urlparse.urlparse(_url)
        f = urllib.urlopen(_url)
        _content = f.read()
        f.close()
        #soup = BeautifulSoup(_content)
        #anchors = [a for a in soup.findAll('a') if (a.attrMap) and (a.attrMap.has_key('href')) and (a.attrMap['href'].find(toks[1]) > -1)]
        #for anchor in anchors:
            #aParent = anchor.parent
            # modify the anchor and shove it back into its parent...
            # each href gets wrapped with a URL from this site.
        # use the modified content for the returned values.
        response = HttpResponse(content=_content,mimetype=__mimetype)
    else:
        response = _handle_blog_link(request,_url,parms,browserAnalysis)
    return response

def handle_blog_link(request,parms,browserAnalysis):
    _url = '/'.join(parms[2:]).replace('http:/','http://').replace('https:/','https://')
    response = _handle_blog_frames(request,_url,parms,browserAnalysis)
    return response

def handle_blog_nav(request,parms,browserAnalysis):
    response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'content':'','google_site_verification':False,'isShowingFlash':False,'isShowingTitleBar':False})
    return response

def _cache_feed_entries(key,entries,seconds):
    d = [dict([(k,v) for k,v in item.iteritems()]) for item in entries]
    _d_ = []
    for _d in d:
        for k,v in _d.iteritems():
            if (misc.isList(v)):
                _newList = []
                for item in v:
                    if (ObjectTypeName.typeClassName(item).find('.FeedParserDict') > 1):
                        _newList.append(dict([(kk,vv) for kk,vv in item.iteritems()]))
                _d[k] = _newList
            elif (ObjectTypeName.typeClassName(v).find('.FeedParserDict') > 1):
                _d[k] = dict([(kk,vv) for kk,vv in v.iteritems()])
        _d_.append(_d)
    memcache.add('feed_%s'%(key), _d_, seconds)
    
def _uncache_feed_entries(entries):
    return [SmartObject(item) for item in entries]

def handle_sitemap(request,parms,browserAnalysis):
    import sitemaps
    _sitemaps = sitemaps.sitemaps
    feeds = models.RssFeed.all()
    for aFeed in feeds:
        entries = memcache.get('feed_%s'%(aFeed.url))
        if entries is None:
            foo = feedparser.parse(aFeed.url)
            if _is_feed_valid(foo):
                entries = foo['entries']
                _cache_feed_entries(aFeed.url,entries,_feed_entries_cache_seconds_)
        else:
            entries = _uncache_feed_entries(entries)
        _sitemaps[aFeed.url] = sitemaps.DynamicSitemap(entries)
    return sitemap(request,_sitemaps)

def give_response_named_id_using(request,response,key,value):
    request.session[key] = value
    request.session.save()

def give_response_api_key(request,response):
    django_utils.give_response_session_id_using(request,response,__api__)

def default(request):
    
    qryObj = django_utils.queryObject(request)
    parms = django_utils.parse_url_parms(request)
    browserAnalysis = django_utils.get_browser_analysis(request,parms,False)
    context = RequestContext(request)
       
    try:
        s_response = ''
        __error__ = ''

        url = '/%s' % (str('/'.join(parms)))
        
        isParms = len(parms) > 0
        
        isRestGetUser = isRestGetMenu = isRestGetArticles = isRestGetMoreArticles = isRestGetCategories = isRestGetTags = isRestGetLanguages = isRestGetOneArticle = isRestGetTaggedArticles = isRestGetCategoryArticles = isRestGetLanguageArticles = isRestGetExternals = isRestUserRegister = isRestUserRegisterTOS = isRestUserRegisterHelp = isRestPostRegister = isRestResendRegister = isRestForgotPassword = isRestSendPassword = isAccountActivate = isAccountPassword = isAccountLogout = isRestUserLogin = isRestUserLoginHelp = isRestPostLogin = isRestPostRssFeed = isRestAdminRssFeedHelp = isRestRemoveRssFeed = isRestPostVerification = isRestRemoveVerification = isRestSSLHelp = isRestGetComments = isRestUserLogout = isRestUserFeedback = isRestUserSponsor = isRestGetAdmin = isRestSetFacebookLogin = isMailSender = isSiteMapGetEntry = isSiteMapGetCategory = isSiteMapGetTag = isSiteMapGetLanguage = isSiteMapReference = isRobotsTxt = isCrossDomainXml = isSitemapXml = isIdle = isBlogLink = isBlogNav = False

        if (isParms):
            isRestGetUser = (django_utils.isURL(parms,'/blog/rest/get/user/'))
            isRestGetEndpoints = (django_utils.isURL(parms,'/blog/rest/get/endpoints/'))
            isRestRefreshAdmin = (django_utils.isURL(parms,'/blog/rest/refresh/admin/'))
            isRestPostDomain = (django_utils.isURL(parms,'/blog/rest/post/domain/'))

            isIdle = (django_utils.isURL(parms,'/blog/idle/'))
            
            isRestGetMenu = (django_utils.isURL(parms,__api_dict__['get_rest_get_menu']))
            isRestGetArticles = (django_utils.isURL(parms,__api_dict__['blog_rest_get_articles']))
            isRestGetMoreArticles = (django_utils.isURL(parms,__api_dict__['blog_rest_get_more'])) # /blog/rest/get/more/recID/
            isRestGetCategories = (django_utils.isURL(parms,__api_dict__['blog_rest_get_categories']))
            isRestGetTags = (django_utils.isURL(parms,__api_dict__['blog_rest_get_tags']))
            isRestGetLanguages = (django_utils.isURL(parms,__api_dict__['blog_rest_get_languages']))
            isRestGetOneArticle = (django_utils.isURL(parms,__api_dict__['blog_rest_get_article'])) # /blog/rest/get/article/recID/
            isRestGetTaggedArticles = (django_utils.isURL(parms,__api_dict__['blog_rest_get_tagged'])) # /blog/rest/get/tagged/recID/
            isRestGetCategoryArticles = (django_utils.isURL(parms,__api_dict__['blog_rest_get_category'])) # /blog/rest/get/category/recID/
            isRestGetLanguageArticles = (django_utils.isURL(parms,__api_dict__['blog_rest_get_language'])) # /blog/rest/get/language/recID/
            
            isRestGetExternals = (django_utils.isURL(parms,__api_dict__['blog_rest_get_externals']))
    
            isRestUserRegister = (django_utils.isURL(parms,__api_dict__['blog_rest_user_register']))
            isRestUserRegisterTOS = (django_utils.isURL(parms,__api_dict__['blog_rest_register_tos']))
            isRestUserRegisterHelp = (django_utils.isURL(parms,__api_dict__['blog_rest_register_help'])) # /blog/rest/register/help/['username','password1','first_name','last_name','password2','email','tos']/
            isRestPostRegister = (django_utils.isURL(parms,__api_dict__['blog_rest_post_register']))
    
            isRestResendRegister = (django_utils.isURL(parms,__api_dict__['blog_rest_resend_register']))
            isRestForgotPassword = (django_utils.isURL(parms,__api_dict__['blog_rest_forgot_password']))
            isRestSendPassword = (django_utils.isURL(parms,__api_dict__['blog_rest_send_password']))
            
            isAccountActivate = (django_utils.isURL(parms,__api_dict__['account_activate'])) # /account/activate/02d82a46d9c91c65f1ea2ee56295ec29fe1725a1/
            isAccountPassword = (django_utils.isURL(parms,__api_dict__['account_password'])) # /account/password/02d82a46d9c91c65f1ea2ee56295ec29fe1725a1/
    
            isAccountLogout = (django_utils.isURL(parms,__api_dict__['account_logout']))
            
            isRestUserLogin = (django_utils.isURL(parms,__api_dict__['blog_rest_user_login'])) # /blog/rest/user/login/[username/password/]
            isRestUserLoginHelp = (django_utils.isURL(parms,__api_dict__['blog_rest_login_help'])) # /blog/rest/login/help/['username','password']/
            isRestPostLogin = (django_utils.isURL(parms,__api_dict__['blog_rest_post_login']))
    
            isRestPostRssFeed = (django_utils.isURL(parms,__api_dict__['blog_rest_post_rssfeed']))
            isRestAdminRssFeedHelp = (django_utils.isURL(parms,__api_dict__['blog_rest_rssfeed_help'])) # /blog/rest/rssfeed/help/['url']/
            isRestRemoveRssFeed = (django_utils.isURL(parms,__api_dict__['blog_rest_remove_rssfeed']))

            isRestGetRssFeeds = (django_utils.isURL(parms,__api_dict__['blog_rest_get_rssfeeds']))
            
            isRestPostVerification = (django_utils.isURL(parms,__api_dict__['blog_rest_post_verification']))
            isRestRemoveVerification = (django_utils.isURL(parms,__api_dict__['blog_rest_remove_verification']))
            
            isRestSSLHelp = (django_utils.isURL(parms,__api_dict__['blog_rest_ssl_help']))
            
            isRestGetComments = (django_utils.isURL(parms,__api_dict__['blog_rest_get_comments']))
            
            isRestUserLogout = (django_utils.isURL(parms,__api_dict__['blog_rest_user_logout']))
    
            isRestUserFeedback = (django_utils.isURL(parms,__api_dict__['blog_rest_user_feedback']))
            
            isRestUserSponsor = (django_utils.isURL(parms,__api_dict__['blog_rest_user_sponsor']))
    
            isRestGetAdmin = (django_utils.isURL(parms,__api_dict__['blog_rest_get_admin']))
            
            isRestSetFacebookLogin = (django_utils.isURL(parms,__api_dict__['blog_rest_set_facebook']))
    
            isMailSender = (django_utils.isURL(parms,'/mail/send/'))
            
            isSiteMapGetEntry = (django_utils.isURL(parms,'/blog/entry/'))       # /blog/entry/YYYY/MM/DD/title-goes-here/id/
            isSiteMapGetCategory = (django_utils.isURL(parms,'/blog/category/')) # /blog/category/YYYY/MM/DD/title-goes-here/id/
            isSiteMapGetTag = (django_utils.isURL(parms,'/blog/tag/'))           # /blog/tag/YYYY/MM/DD/title-goes-here/id/
            isSiteMapGetLanguage = (django_utils.isURL(parms,'/blog/language/')) # /blog/language/YYYY/MM/DD/title-goes-here/id/
            
            isSiteMapReference = (django_utils.isURL(parms,__api_dict__['blog_sitemap'])) # /blog/sitemap/[url-encoded-url]/

            isBlogLink = (django_utils.isURL(parms,__api_dict__['blog_link'])) # /blog/link/[url-encoded-url]/
            
            isBlogNav = (django_utils.isURL(parms,__api_dict__['blog_nav']))

            isRobotsTxt = (django_utils.isURL(parms,u'robots.txt'))
            
            isCrossDomainXml = (django_utils.isURL(parms,u'crossdomain.xml'))
            
            isSitemapXml = (django_utils.isURL(parms,u'sitemap.xml'))
        
        browserAnalysis = django_utils.get_browser_analysis(request,parms,any([isSiteMapGetEntry,isSiteMapGetCategory,isSiteMapGetTag,isSiteMapGetLanguage,isAccountActivate,isAccountPassword,isRobotsTxt,isCrossDomainXml,isSitemapXml,isSiteMapReference,isBlogLink,isIdle,isBlogNav]))
        
        if (url == '/'):
            if (request.session.has_key('facebookUser_id')):
                _uid_ = request.session['facebookUser_id']
                users = [aUser for aUser in FacebookUser.all() if (aUser.id == _uid_)]
                if (len(users) > 0):
                    return HttpResponseRedirect('/facebook/')
            verifications = get_verifications()
            _verification = verifications[0].text if (len(verifications) > 0) else False
            _user = get_user(request)
            response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'google_site_verification':_verification,'isShowingFlash':True,'isShowingTitleBar':True,'is_superuser':_user.is_superuser})
            if (qryObj.article):
                give_response_named_id_using(request,response,'article_id',qryObj.article)
            django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
            return response
        else:
            referer = django_utils.get_from_META(request,'HTTP_REFERER','UNKNOWN REFERER')
            __xxx__ = request.COOKIES[settings.APP_SESSION_KEY] if (request.COOKIES.has_key(settings.APP_SESSION_KEY)) else None
            if ( (__xxx__ == parms[-1]) or (browserAnalysis.isUsingAdobeAIR) ) and (browserAnalysis.isUsingSupportedBrowser): #  and (browserAnalysis.isRefererAcceptable)
                if (isRestSetFacebookLogin):
                    response = rest_handle_set_facebook(request)
                elif (isRestGetComments):
                    response = rest_handle_get_comments(request,parms,browserAnalysis)
                elif (isRestSSLHelp):
                    response = rest_handle_ssl_help(request)
                elif (isAccountLogout):
                    response = handle_account_logout(request)
                elif (isRestGetAdmin):
                    response = rest_handle_get_admin(request)
                elif (isRestUserFeedback):
                    response = rest_handle_user_feedback(request)
                elif (isRestUserSponsor):
                    response = rest_handle_user_sponsor(request,browserAnalysis)
                elif (isRestForgotPassword):
                    response = rest_handle_forgot_password(request)
                elif (isRestSendPassword):
                    response = rest_handle_send_password(request)
                elif (isRestResendRegister):
                    response = rest_handle_resend_register(request)
                elif (isMailSender):
                    response = rest_handle_send_mail(request)
                elif (isRestGetUser):
                    response = rest_handle_get_user(request,parms,browserAnalysis)
                elif (isRestUserLogin):
                    response = rest_handle_login(request,qryObj,browserAnalysis)
                elif (isRestUserLogout):
                    response = rest_handle_logout(request)
                elif (isRestAdminRssFeedHelp):
                    response = rest_handle_rssfeed_help(request,parms)
                elif (isRestUserLoginHelp):
                    response = rest_handle_login_help(request,parms)
                elif (isRestRemoveRssFeed):
                    response = rest_handle_remove_rssfeed(request,qryObj,browserAnalysis)
                elif (isRestRemoveVerification):
                    response = rest_handle_remove_verification(request,qryObj,browserAnalysis)
                elif (isRestPostRssFeed):
                    response = rest_handle_post_rssfeed(request,qryObj,browserAnalysis)
                elif (isRestGetRssFeeds):
                    response = rest_handle_get_rssfeeds(request,browserAnalysis)
                elif (isRestPostVerification):
                    response = rest_handle_post_verification(request,qryObj,browserAnalysis)
                elif (isRestPostLogin):
                    response = rest_handle_login(request,qryObj,browserAnalysis)
                elif (isAccountActivate):
                    response = handle_account_activate(request,parms)
                elif (isAccountPassword):
                    response = handle_account_password(request,parms,browserAnalysis,qryObj)
                elif (isRestUserRegister):
                    response = rest_handle_register(request,qryObj,browserAnalysis)
                elif (isRestPostRegister):
                    response = rest_handle_register(request,qryObj,browserAnalysis)
                elif (isRestUserRegisterTOS):
                    response = rest_handle_register_tos(request)
                elif (isRestUserRegisterHelp):
                    response = rest_handle_register_help(request,parms)
                elif (isRestGetMenu):
                    response = rest_handle_get_menu(request)
                elif (isRestGetArticles):
                    response = rest_handle_get_articles(request,browserAnalysis)
                elif (isRestGetExternals):
                    response = rest_handle_get_externals(request,browserAnalysis)
                elif (isRestGetMoreArticles):
                    response = rest_handle_get_more_articles(request,parms,browserAnalysis)
                elif (isRestGetOneArticle):
                    response = rest_handle_get_one_article(request,parms,browserAnalysis)
                elif (isRestGetCategories):
                    response = rest_handle_get_categories(request)
                elif (isRestGetTags):
                    response = rest_handle_get_tags(request)
                elif (isRestGetLanguages):
                    response = rest_handle_get_languages(request)
                elif (isRestGetTaggedArticles):
                    response = rest_handle_get_one_tag(request,parms,browserAnalysis)
                elif (isRestGetCategoryArticles):
                    response = rest_handle_get_one_category(request,parms,browserAnalysis)
                elif (isRestGetLanguageArticles):
                    response = rest_handle_get_one_language(request,parms,browserAnalysis)
                elif (isRestGetEndpoints):
                    response = rest_handle_get_endpoints(request,browserAnalysis)
                elif (isRestRefreshAdmin):
                    response = rest_handle_refresh_admin(request,browserAnalysis)
                elif (isRestPostDomain):
                    response = rest_handle_post_domain(request,browserAnalysis)
                else:
                    try:
                        response = render_to_response(request, url.replace('/',''))
                    except Exception, e:
                        cname = django_utils.get_from_META(request,'HTTP_HOST','')
                        response = render_to_response(request, '404.html', {'details':'<BR/>'.join(_utils.formattedException(details=e).split('\n')),'HTTP_HOST':cname} if (django_utils.isRunningLocal(request)) else {})
                django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                return response
            else:
                response = None
                if (isSiteMapGetEntry):
                    response = handle_sitemap_entry(request,parms,browserAnalysis)
                elif (isSiteMapGetCategory):
                    response = handle_sitemap_category(request,parms,browserAnalysis)
                elif (isSiteMapGetLanguage):
                    response = handle_sitemap_language(request,parms,browserAnalysis)
                elif (isSiteMapGetTag):
                    response = handle_sitemap_tag(request,parms,browserAnalysis)
                elif (isBlogLink):
                    response = handle_blog_link(request,parms,browserAnalysis)
                elif (isBlogNav):
                    response = handle_blog_nav(request,parms,browserAnalysis)
                elif (isSiteMapReference):
                    response = handle_sitemap_reference(request,parms,browserAnalysis)
                elif (isBlogLink):
                    response = handle_blog_link(request,parms,browserAnalysis)
                elif (isSitemapXml):
                    response = handle_sitemap(request,parms,browserAnalysis)
                elif (isRobotsTxt):
                    response = HttpResponse(content=django_utils.render_from_string(__robots_txt__,context=context),mimetype=__textMimetype)
                elif (isCrossDomainXml):
                    response = HttpResponse(content=django_utils.render_from_string(__crossdomain_xml__,context=context),mimetype=__textMimetype)
                elif (isRestUserLogin):
                    response = rest_handle_login(request,qryObj,browserAnalysis)
                elif (isRestUserRegister):
                    response = rest_handle_register(request,qryObj,browserAnalysis)
                elif (isAccountActivate):
                    response = handle_account_activate(request,parms)
                elif (isAccountPassword):
                    response = handle_account_password(request,parms,browserAnalysis,qryObj)
                elif (isIdle):
                    import random
                    from google.appengine.api.labs import taskqueue
                    hot_handler_queue = taskqueue.Queue(name='hothandler')
                    next_token = str(random.random())
                    url = '%s%s/0/'%(django_utils.unsplit_url(parms[0:2]),next_token)
                    next_task = taskqueue.Task(countdown=10, url=url)
                    hot_handler_queue.add(next_task)
                    response = HttpResponse(content=django_utils.render_from_string(__idle_txt__,context=context),mimetype=__textMimetype)
                    return response
                if (response):
                    django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                    return response
                remoteIP = django_utils.get_from_META(request,'REMOTE_ADDR','UNKNOWN IP')
                _content = '' #'%s'%('Forbidden Request...  Your IP Address (%s) has been recorded...'%(remoteIP))
                logging.warning('Forbidden Request from "%s" to "%s" ("%s").'%(remoteIP,parms,referer))
                response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content,'isShowingFlash':False,'isShowingTitleBar':True})
                django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                return response
        response = render_to_response(request, '404.html', {'details':'UNKNOWN FAILURE'})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.warning(info_string)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))) if (not browserAnalysis.isRunningLocal(request)) else ''
        response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':django_utils.get_from_META(request,'HTTP_USER_AGENT',''),'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal(request),'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content,'isShowingFlash':False,'isShowingTitleBar':True})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response
