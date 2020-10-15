##################################################################
## To-Do:
##   HTTPS/HTTP by expected URL.
##   HTTPS For activations...
##   Optimize the static content...
##   Add Perks and Reasons for people to pay money...
##
##  Bugs:
##  * Make sure nippet_tags for Admin types cannot be used by users for their tags...
##  * Make sure nobody can claim a sub-domain that is currently in-use for the domain...
##  
##################################################################

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings
from django.db.models import Q

import mimetypes

from vyperlogix.django.decorators import cache

import os, sys
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.html import stripper

from vyperlogix.js import minify

from vyperlogix.django import forms
from vyperlogix.django.forms import form_as_html
from vyperlogix.django import captcha

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.misc import FormatWithCommas

from vyperlogix.crypto import md5
from vyperlogix.misc import GenPasswd

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.django.rss import content as rss_content

from vyperlogix.misc import ObjectTypeName

from vyperlogix.lists import ListWrapper

from content import models as content_models

from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.enum.Enum import Enum

from django.db.models import Q

import urllib

import socket

import utils

_title = 'Vyper Logix Corp, The 21st Century Python Company'

__product__ = 'Vyper-CMS&trade;'
__version__ = '1.0.0.16'

class MenuTypes(Enum):
    none = 0
    MenuBarHorizontal = 1
    XML = 2

from vyperlogix.products import keys

def get_is_logged_in(request):
    try:
	return request.session.get('is_logged_in', False)
    except:
	pass
    return False

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

def get_smtp_server():
    from vyperlogix.mail.mailServer import GMailServer
    #smtp = GMailServer(keys._decode('696E766573746F72734076797065726C6F6769782E636F6D'), keys._decode('7065656B61623030'), server='smtpout.secureserver.net', port=3535)
    smtp = GMailServer(keys._decode('76797065726C6F67697840676D61696C2E636F6D'), keys._decode('7065656B61623030'))
    return smtp

def send_problem_email(email_address,problem_msg,subject):
    try:
	from vyperlogix.mail.message import Message
	msg = Message(email_address,'support@vyperlogix.com', problem_msg, subject=subject)
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

    return msg_context

def send_registration_email(email_address, product_name, product_link, site_link):
    t_EULA = get_template('vyper-cms_EULA.txt')
    EULA_context = {'PRODUCT_NAME':product_name, 'COMPANY_NAME':'Vyper Logix Corp.'}
    EULA_content = t_EULA.render(Context(EULA_context, autoescape=False))

    t_content = get_template('vyper-cms_Registration_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'EULA':EULA_content}
    msg_content = t_content.render(Context(msg_context, autoescape=False))

    try:
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not _utils.isBeingDebugged) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), msg_content, subject="We have received your %s Registration Request." % (product_name))
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

    return msg_context

def send_activation_email(email_address, password):
    t = get_template('vyper-cms_Activation_Email.txt')
    c = {'PRODUCT_PASSWORD':password}
    content = t.render(Context(c, autoescape=False))

    try:
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not _utils.isBeingDebugged) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), content, subject="This is your Vyper-CMS(tm) Account Password.")
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

def send_password_email(email_address, password):
    t = get_template('vyper-cms_Forgot_Password_Email.txt')
    c = {'PASSWORD':password}
    content = t.render(Context(c, autoescape=False))

    try:
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not _utils.isBeingDebugged) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), content, subject="This is your new Vyper-CMS(tm) Account Password.")
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

def _send_registration_email(request,email_address):
    return send_registration_email(email_address, 'Vyper-CMS(tm) FREE Site Builder (www.%s)' % (django_utils.get_server_name(request)), 'http://%s/registration/activate/%s' % (django_utils.get_fully_qualified_http_host(request),keys._encode('%s,%s' % (email_address,_utils.timeSecondsFromTimeStamp(_utils.getFromDateTimeStr(_utils.timeStamp()))))), 'http://%s' % (django_utils.get_fully_qualified_http_host(request)))

def process_registration(request,email_address):
    html_context = _send_registration_email(request,email_address)
    t_content = get_template('_registered.html')
    if (html_context.has_key('EULA')):
	html_context['EULA'] = oohtml.render_BR().join(html_context['EULA'].split('\n'))
    aUser = utils.get_user_by_email(email_address,activated=0)
    if (aUser is not None):
	admin_user_role = utils.get_admin_user_role()
	if (aUser.role != admin_user_role):
	    aUser.role = admin_user_role
	    aUser.save()
    else:
	aUser = utils.get_user_by_email(email_address,activated=1)
	if (aUser is None):
	    send_problem_email(email_address,'User cannot get the role of "%s" and is NOT Activated.' % (admin_user_role),'WARNING: Technical Problem')
    return html_context

def on_successful_registration(form,request):
    emailField = form.email_fields[0]
    email_address = emailField.value

    aUser = utils.get_current_user(request)
    SITE_ID = utils.get_current_site(request,aUser)
    aSiteName = utils.get_sitename_for_SITE_ID(SITE_ID)
    if (aSiteName is None):
	html_context = process_registration(request,email_address)
    else:
	aUser = aSiteName.user
	##############################################################################################################
	## For now this part of the function does the same thing as the code above.                                 ##
	## Later-on this part of the function will process the user as a Member of ap specific site with the option ##
	## of allowing the new User to get their own site in addition to becoming a member of a specific site.      ##
	##############################################################################################################
	html_context = process_registration(request,email_address)
    aUserOwner = utils.get_user_owner(SITE_ID)
    
    return html_context

def on_unsuccessful_registration(form,context):
    return form_as_html.form_as_html(form,callback=_form_for_model,context=context)

def on_before_form_save(form,request,obj):
    # This could be used to pre-assign a password however the password should be assigned when the Account is activated.
    pass

def on_registration_form_error(form,request):
    try:
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', keys._decode('72617963686F726E40686F746D61696C2E636F6D'), form.last_error, subject="ERROR: Registration Request (%s) (%s)" % (django_utils._cname,django_utils.get_fully_qualified_http_host(request)))
	smtp = get_smtp_server()
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

def _form_for_model(form, request=None, context={}):
    f = form
    if (f.form_name == 'register'):
	f.fields['firstname'].min_length = 2
	f.fields['firstname'].required = True
	f.fields['lastname'].min_length = 2
	f.fields['lastname'].required = True
	f.fields['email_address'].required = True
	f.fields['email_address'].max_length = 128
	f.fields['phone_number'].max_length = 20
	f.fields['phone_number'].min_length = 12
	for k,v in f.fields.iteritems():
	    if (k not in ['firstname', 'lastname', 'email_address']):
		v.required = False
	f.fields['state'].required = True
	f.fields['country'].required = True

	f.set_choice_model_for_field_by_name('state',SmartObject({'value_id':'abbrev','text_id':'name'}))
	f.set_choice_model_for_field_by_name('country',SmartObject({'value_id':'iso3','text_id':'printable_name'}))
	
	f.set_choice_model_default_for_field_by_name('state',context['VALUE_STATE'] if (context.has_key('VALUE_STATE')) else '')
	f.set_choice_model_default_for_field_by_name('country',context['VALUE_COUNTRY'] if (context.has_key('VALUE_COUNTRY')) else '')

	validation_condition = lambda self:((len(self.fields['state'].value) == 0) and (self.fields['country'].value == 'USA')) or ((len(self.fields['state'].value) > 0) and (self.fields['country'].value != 'USA'))
	validation_message = 'Either the State or Country is invalid.'
	validation_tuple = tuple([validation_condition,{'STATE':validation_message,'COUNTRY':validation_message}])
	f.field_validation = validation_tuple
	
	f.first_field_name = 'companyname'
	f.next_field_name = 'firstname'
	f.next_field_name = 'lastname'
	f.next_field_name = 'email_address'
	f.next_field_name = 'street_address'
	f.next_field_name = 'city'
	f.next_field_name = 'state'
	f.next_field_name = 'zipcode'
	f.next_field_name = 'country'
	f.next_field_name = 'phone_number'
	
	f.add_hidden_field('activated','')
	f.add_hidden_field('site','')
	f.add_hidden_field('role','')
	f.add_hidden_field('activated_on','')
	f.add_hidden_field('referred_by','')
	
	f.add_extra_field('site_id',settings.SITE_ID)
	f.add_extra_field('role_id',utils.default_role_id())
	f.add_extra_field('activated',0)
	
	f.submit_button_title = 'Get Registered.'
	f.submit_button_value = 'Submit Registration'
    elif (f.form_name == 'upload'):
	f.add_hidden_field('site','')

	f.submit_button_title = 'Upload Image.'
	f.submit_button_value = 'Upload Image'
	
    html = f.as_html()
    return html

def render_menu(request,menutype,id="MenuBar1", class_=MenuTypes.MenuBarHorizontal, target='/', SITE_ID=settings.SITE_ID, content=''):
    def does_this_match(item,search):
	try:
	    return item.menu_tag == search
	except:
	    pass
	return False
    
    def does_target_match(item,search):
	try:
	    return item.url == search
	except:
	    pass
	return False
    
    if (ObjectTypeName.typeClassName(menutype) == 'django.db.models.query.QuerySet') and (len(menutype) > 0):
	menutype = menutype[0]
    menutype_any = content_models.MenuType.objects.filter(menutype='*')
    if (len(menutype_any) > 0):
	menutype_any = menutype_any[0]
    target = target if (misc.isString(target)) else '/'

    _admin_mode = 0 if (not get_is_logged_in(request)) else 1

    contents1 = content_models.Content.objects.filter(Q(menutype=menutype), Q(sites=SITE_ID), ~Q(url=target), Q(admin_mode=_admin_mode))
    contents1 = contents1.filter(Q(target='*') | Q(target='%s' % (target)))

    contents2 = content_models.Content.objects.filter(Q(menutype=menutype_any), Q(sites=SITE_ID), ~Q(url=target), Q(admin_mode=_admin_mode))
    contents2 = contents2.filter(Q(target='*') | Q(target='%s' % (target)))
    
    contents3 = content_models.Content.objects.filter(Q(url=target), Q(sites=SITE_ID), Q(admin_mode=_admin_mode))
    
    contents = [c for c in contents1] + [c for c in contents2]

    l = ListWrapper.SmartList(contents)
    
    if (menutype.menutype == 'top'):
	i = l.findFirstMatching(target,callback=does_target_match)
	if (i == -1):
	    contents = contents + [c for c in contents3]

    l = ListWrapper.SmartList(list(set(contents)))

    i = l.findFirstMatching('Home',callback=does_this_match)
    
    _contents = []
    if (i > -1):
	_contents = l.copy_excluding_with(i,'menu_tag')
    else:
	_contents = contents

    from vyperlogix.django import tabs
    from vyperlogix.django import pages

    _navigation_tabs = []
    if (not get_is_logged_in(request)):
	for aContent in _contents:
	    isLocal = not re.search(r"^(http)(s?)://((www\.)+[a-zA-Z0-9\-.?,'/\\+&amp;=:%$#_]*)?", aContent.url)
	    _navigation_tabs.append(tuple([aContent.url,aContent.menu_tag,aContent.descr]))
    else:
	if (menutype.menutype == 'top'):
	    has_valid_domain = request.session.get('has_valid_domain',False)
	    _navigation_tabs.append(tuple(['/','Home','Welcome to Vyper-CMS&trade;.']))
	    _navigation_tabs.append(tuple(['/vyper-cms/domain/','Site Domain','Configure the Domain for your Site.']))
	    if (has_valid_domain):
		_navigation_tabs.append(tuple(['/vyper-cms/layout/','Site Layout','Build your Site Layout (Header, Banner and Footer).']))
		_navigation_tabs.append(tuple(['/vyper-cms/content/','Site Content','Build your Site Content (Add Pages to your Site).']))
		_navigation_tabs.append(tuple(['/vyper-cms/changelog/','Changelog','Review recent changes to the system.']))
	else:
	    _navigation_tabs.append(tuple(['/user/logout/','Logout','User Logout']))
    if (menutype.menutype == 'top'):
	if (not get_is_logged_in(request)):
	    _navigation_tabs.append(tuple(['/user/login/','Login','User Login']))
	else:
	    _navigation_tabs.append(tuple(['/user/logout/','Logout','User Logout']))
	#if (not get_is_logged_in(request)):
	    #_navigation_tabs.append(tuple(['/user/register/','Register','User Registration']))
    if (class_ == MenuTypes.XML):
	html_tabs_content = '<m m="meta" d="i">'
	html_tabs_content += '<meta xmlLabel="t"/><meta xmlUrl="u"/>'
	for t in _navigation_tabs:
	    t = [urllib.quote_plus(i) for i in list(t)]
	    html_tabs_content += '<i u="%s" t="%s" s="%s"/>' % (tuple(t))
	html_tabs_content += '</m>'
    else:
	t_tabs_content = get_template('_tabs_content.html')
	html_tabs_content = t_tabs_content.render(Context({'MENU_TYPE':settings.NAVIGATION_MENU_TYPE,
	                                                   'NAVIGATION_TABS':pages.get_tabs_nav_html(_navigation_tabs,request,content=content),
	                                                   'NAVIGATION_CONTENT':pages.get_tabs_nav_content_html(_navigation_tabs)
	                                                   }, autoescape=False))
    return html_tabs_content

def get_layouts_for_current_site(aUser):
    layout_snippet_type = content_models.get_layout_snippet_type()
    aSitename = utils.get_sitename_for_current_site(aUser)
    if (aSitename is not None):
	layout_snippets = content_models.Snippet.objects.filter(Q(snippet_type=layout_snippet_type), Q(sites=aSitename.site))
	if (layout_snippets.count() > 0):
	    aLayoutSnippet = layout_snippets[0]
	    sites = aLayoutSnippet.sites.filter(id=aSitename.site.id)
	    if (sites.count() > 0):
		return [aLayoutSnippet]
    return []

def add_layout_to_current_site(aLayoutSnippet,aUser):
    sitenames = content_models.SiteName.objects.filter(user=aUser)
    if (sitenames.count() > 0):
	aSitename = sitenames[0]
	aLayoutSnippet.sites.add(aSitename.site)

def rest(request):
    url_toks = [item for item in django_utils.parse_url_parms(request) if (len(item) > 0)]
    params = _utils.get_dict_as_pairs(url_toks)

    site_handle = utils.get_site_handle(request)
    
    has_valid_domain = request.session.get('has_valid_domain',False)
    
    snippet_types_unrestricted_list = utils.get_snippet_types_list(admin=0)
    
    _url_toks = [''] + url_toks + ['']
    _expected_target = '/' if (len(url_toks) == 0) else '/'.join(_url_toks)

    if (_url_toks == ['', u'rest', u'getMenuXML', '']):
	_menu_id_top = "MenuBarTop"
	_menu_class = MenuTypes.XML
	menutype_top = content_models.MenuType.objects.filter(menutype='top')
	menu = render_menu(request,menutype_top,id=_menu_id_top,class_=_menu_class,target=_expected_target,SITE_ID=site_handle.SITE_ID,content='')
	return HttpResponse(content='<?xml version="1.0" encoding="utf-8"?>'+menu,mimetype='text/xml')
    return HttpResponse(content='<?xml version="1.0" encoding="utf-8"?><x></x>',mimetype='text/xml')

def default(request):
    global _title
    
    _reIS_TEMPLATE = re.compile(r"\{\{ (?P<name>.*) \}\}", re.IGNORECASE)
    try:
	url_toks = [item for item in django_utils.parse_url_parms(request) if (len(item) > 0)]
	params = _utils.get_dict_as_pairs(url_toks)
    
	site_handle = utils.get_site_handle(request)
	
	aLayoutSnippet = None
	has_valid_domain = request.session.get('has_valid_domain',False)
	
	snippet_types_unrestricted_list = utils.get_snippet_types_list(admin=0)
    
	s_expected_target = utils._anchor_expected_target(url_toks)
	t_expected_target = utils._anchor_expected_target(url_toks[0:-1])
	a_expected_target =  utils.anchor_expected_target(url_toks,['accepted'])
	
	_stderr = sys.stderr
	_log_path = os.path.join(os.path.dirname(sys.argv[0]),'logs','%s.log' % (os.path.dirname(sys.argv[0]).split(os.sep)[-1]))
	_utils.makeDirs(_log_path)
	
	l_url_toks = ListWrapper.ListWrapper(url_toks)
	l_query_string = django_utils.parse_Secure_Query_String(request)
	
	django_utils.site_id_for_requestor(request)
	    
	_url_toks = [''] + url_toks + ['']
	_expected_target = '/' if (len(url_toks) == 0) else '/'.join(_url_toks)

	menutype_top = content_models.MenuType.objects.filter(menutype='top')
	menutype_bottom = content_models.MenuType.objects.filter(menutype='bottom')

	content_peeler_head = ''
	content_styles_head = ''
	content_layout_head = ''
	if (site_handle.aUserOwner is not None):
	    _title = site_handle.aSiteName.site.name
	    uploads_path = utils.get_uploads_path(site_handle.aSiteName)
	    layouts = get_layouts_for_current_site(site_handle.aUser)
	    if (len(layouts) > 0):
		aLayoutSnippet = layouts[0]
	else:
	    t_styles_head = get_template('new/_styles.html')
	    c_styles_head = Context({}, autoescape=False)
	    content_styles_head = t_styles_head.render(c_styles_head)
	    
	    t_layout_head = get_template('new/_layout.html')
	    c_layout_head = Context({}, autoescape=False)
	    content_layout_head = t_layout_head.render(c_layout_head)

	# Put some logic here to determine if the site being viewed should have adverts or not.
	t_peeler_head = get_template('_page_peeler.html')
	c_peeler_head = Context({}, autoescape=False)
	content_peeler_head = t_peeler_head.render(c_peeler_head)

	t_head = get_template('new/_head.html')
	c_head = Context({'STYLES':content_styles_head+content_layout_head+content_peeler_head}, autoescape=False)
	
	ctx_head = Context({'TABS_id':settings.NAVIGATION_TYPE}, autoescape=False)
	
	head_snippets = utils.get_head_snippets().filter(sites=site_handle.SITE_ID).filter(Q(snippet_tag=_expected_target) | Q(snippet_tag='*')).order_by('snippet_tag')
	c_head['HEAD'] = '' if (not c_head.has_key('HEAD')) else c_head['HEAD']
	for aSnippet in head_snippets:
	    c_head['HEAD'] += django_utils.render_from_string(aSnippet.content,context=ctx_head)
	title_snippet = utils.get_title_snippets().filter(sites=site_handle.SITE_ID)
	if (title_snippet.count() > 0):
	    title_snippet = title_snippet[0]
	    _title = stripper.strip(title_snippet.content)
	c_head['TITLE'] = '%s, %s' % (_title,'%s %s' % (__product__,__version__))
	content_head = django_utils.render_template_with_context(t_head,c_head)

	javascript_content = ''
	javascript_snippets = utils.get_javascript_snippets().filter(sites=site_handle.SITE_ID).filter(Q(snippet_tag=_expected_target) | Q(snippet_tag='*')).order_by('snippet_tag')
	for aSnippet in javascript_snippets:
	    javascript_content += aSnippet.content
	javascript_content += '\n//+++MORE_SCRIPTS+++'
	content_head = content_head.replace('//+++MORE_SCRIPTS+++',javascript_content)
	
	normalize_url = lambda url:'/' if (not str(url).startswith('/')) else ''
	
	t_analytics = get_template('new/_google_analytics.html')
	t_pageflip = get_template('_pageflip_div.html')
	t_ribbon_banner = get_template('_ribbon_banner.html')
	t_footer = get_template('new/_footer.html')
	t_menu = get_template('new/_site_menu.html')
	_menu_id_top = "MenuBarTop"
	_menu_id_bottom = "MenuBarBottom"
	_menu_class = "MenuBarHorizontal"
	s_menu_content = render_menu(request,menutype_bottom,id=_menu_id_top,class_=_menu_class,target=_expected_target,SITE_ID=site_handle.SITE_ID)
	s_ajax_loading_content = '<div id="anim-ajax-loading" style="display:none;"><img src="/static/images/ajax/ajax-loader.gif" border="0" /></div>'
	t_menu_content = django_utils.render_template_with_context(t_menu,Context({'MENU_CONTENT':s_menu_content}, autoescape=False))
	c_footer = {'CURRENT_YEAR':_utils.timeStampLocalTime(format=_utils.formatDate_YYYY()),
	            'PRODUCT':__product__,
	            'VERSION':__version__,
	            'MENU':t_menu_content,
	            }
	if (site_handle.aUserOwner is not None):
	    c_footer['STYLES'] = utils._styles
	t_content_footer = t_footer.render(Context(c_footer, autoescape=False))
	_context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({}, autoescape=False)),
		    'INNER_CONTENT':'',
		    'SALUTATION':request.session.get('SALUTATION','<a href="/user/register/" title="Claim your FREE <u>UNLIMITED</u> Web Site now!"><BIG>Register</BIG></a> to claim your <BIG style="color:#0F0"><b>FREE</b></BIG> Web Site, <BIG style="color:#0F0"><b>%s</b></BIG> FREE UNLIMITED Sites are online now... Get <a href="/user/register/" title="Claim your FREE <u>UNLIMITED</u> Web Site now!"><BIG>YOURS</BIG></a> Now !' % (FormatWithCommas.FormatWithCommas('%d',utils.get_sitenames_count()))),
		    'MENU_ID':_menu_id_bottom,
		    'MEDIA_URL':settings.MEDIA_URL,
		    'FOOTER':t_content_footer,
		    'MENU':django_utils.render_template_with_context(t_menu,Context({'MENU_CONTENT':render_menu(request,menutype_top,id=_menu_id_top,class_=_menu_class,target=_expected_target,SITE_ID=site_handle.SITE_ID,content=s_ajax_loading_content)}, autoescape=False)),
		    'TITLE':'%s - %s (%s)',
		    'HEAD':content_head,
	            'PAGEFLIP':t_pageflip.render(Context({}, autoescape=False)),
	            'RIBBON_BANNER':t_ribbon_banner.render(Context({'IMAGE':utils.choose_ribbon_image()}, autoescape=False)),
		    }
	
	def find_tuple_token(item,search):
	    _item = item[0] if (isinstance(item,tuple)) else item
	    return _item.lower() == search.lower()
	
	i = l_query_string.findFirstMatching('django',find_tuple_token)
	if (i > -1):
	    for t in l_query_string[i+1:]:
		if (t[0] == 'TWITTER_LINK'):
		    try:
			_context[t[0]] = keys._decode(t[-1])
		    except:
			_context[t[0]] = t[-1]
		else:
		    _context[t[0]] = t[-1]
	    
	_context['INNER_CONTENT'] = ''
	sub_title = ''

	_admin_mode = site_handle.is_admin_role # 0 if (not get_is_logged_in(request)) else 1
	contents = content_models.Content.objects.filter(Q(url=_expected_target), Q(sites=site_handle.SITE_ID), Q(admin_mode=_admin_mode))
	
	if (contents.count() > 0):
	    sub_title = contents[0].menu_tag
	elif (contents.count() == 0):
	    body_snippet_type = content_models.get_body_snippet_type()
	    javascript_snippet_type = content_models.get_javascript_snippet_type()
	    contents = content_models.Snippet.objects.filter(Q(snippet_tag=_expected_target), Q(sites=site_handle.SITE_ID))
	    if (contents.count() > 0):
		for aContent in contents:
		    _is_content_ok = True
		    try:
			_is_content_ok = (aContent.snippet_type != javascript_snippet_type)
		    except:
			pass
		    if (_is_content_ok):
			sub_title += contents[0].descr
	if (contents.count() > 0):
	    for aContent in contents:
		_is_content_ok = True
		try:
		    _is_content_ok = (aContent.snippet_type != javascript_snippet_type)
		except:
		    pass
		if (_is_content_ok):
		    _context['INNER_CONTENT'] += aContent.content
	if (_admin_mode):
	    if (url_toks == []):
		ctx = {}
		ctx['HAS_VALID_DOMAIN'] = 'true' if (has_valid_domain) else 'false'
		request.session['_error_msg'] = ''
		_context['INNER_CONTENT'] = django_utils.render_from_string(_context['INNER_CONTENT'],context=ctx)
	    elif (url_toks == ['vyper-cms','domain']):
		aSitename = utils.get_sitename_for_user(site_handle.aUser)
		_site_name = ''
		_site_title = ''
		if (aSitename is not None):
		    _site_name = aSitename.site.domain.replace('.'+django_utils.get_server_name(request),'')
		    _site_title = aSitename.site.name
		ctx = {}
		ctx['SITE_NAME'] = _site_name if (misc.isString(_site_name)) else ''
		ctx['SITE_TITLE'] = _site_title if (misc.isString(_site_title)) else ''
		ctx['ERROR_MSG'] = django_utils.get_from_session(request,'_error_msg','')
		request.session['_error_msg'] = ''
		_context['INNER_CONTENT'] = django_utils.render_from_string(_context['INNER_CONTENT'],context=ctx)
	    elif (url_toks == ['vyper-cms','layout']):
		_items = []
		layout_snippet_type = content_models.get_layout_snippet_type()
		layout_snippets = content_models.Snippet.objects.filter(snippet_type=layout_snippet_type)
		_layouts = get_layouts_for_current_site(site_handle.aUser)
		for aLayoutSnippet in layout_snippets:
		    is_being_used = any([l == aLayoutSnippet for l in _layouts])
		    _url = '/'+'/'.join(url_toks+[urllib.quote_plus(aLayoutSnippet.snippet_tag)])+'/'
		    h = oohtml.Html()
		    span = h.tagSPAN('')
		    span.tag_IMG(src='/static/images/layouts/%s.jpg' % (aLayoutSnippet.snippet_tag))
		    span.tagBR()
		    span.tagB(oohtml.render_CENTER(aLayoutSnippet.descr))
		    _items.append([oohtml.renderAnchor(_url,span.toHtml(),target='_top',title=aLayoutSnippet.descr) if (not is_being_used) else span.toHtml()])
		ctx = {}
		ctx['LEFT'] = oohtml.render_table_from_list(_items,align='center')
		_aLayoutSnippet = None
		if (len(_layouts) > 0):
		    _aLayoutSnippet = _layouts[0]
		ctx['RIGHT'] = oohtml.render_IMG(src='/static/images/layouts/%s.jpg' % ('none' if (_aLayoutSnippet is None) else _aLayoutSnippet.snippet_tag))
		_context['INNER_CONTENT'] = django_utils.render_from_string(_context['INNER_CONTENT'],context=ctx)
	    elif (url_toks == ['vyper-cms','content']):
		ctx = {}
		_context['INNER_CONTENT'] = django_utils.render_from_string(_context['INNER_CONTENT'],context=ctx)
	    elif (url_toks == ['vyper-cms', 'domain', 'check']):
		aSitename = utils.get_sitename_for_user(site_handle.aUser)
		if (aSitename is not None):
		    request.session['has_valid_domain'] = utils.is_domain_valid(aSitename.site.domain)
		    resp = utils._domain_test(aSitename.site.domain,request.session.get('has_valid_domain',False))
		else:
		    request.session['has_valid_domain'] = False
		    resp = '<span class="errorBg">You have <b>NOT</b> yet selected your Site Name or Domain Name.  You <b>cannot</b> proceed until you enter a valid Domain Name for your site.</span>'
		return HttpResponse(resp,mimetype='text/plain')
	    elif (url_toks == ['vyper-cms', 'domain', 'sitename']):
		from content import sites
		return sites.accept_site_name(request,user=site_handle.aUser,onSuccess=a_expected_target)
	    elif (url_toks[0:-1] == ['vyper-cms', 'domain', 'get-sitename-count']):
		resp = '%d' % (utils.get_sitenames_count())
		return HttpResponse(resp,mimetype='text/plain')
	    elif (url_toks[0:-1] == ['vyper-cms', 'domain', 'validate-sitename']):
		_domain_name = url_toks[-1]
		_zone_name = django_utils.get_server_name(request)
		_dname = '%s.%s' % (_domain_name,_zone_name)
		_is_domain_owned_by_user = str(_dname).lower() == str(site_handle.aSiteName.site.domain).lower()
		resp = '0' if (not _is_domain_owned_by_user) and (not utils.perform_domain_check(_domain_name,_zone_name)) else '1'
		return HttpResponse(resp,mimetype='text/plain')
	    elif (url_toks == ['vyper-cms', 'domain', 'domainname']):
		from content import sites
		return sites.accept_domain_name(request,user=site_handle.aUser,onSuccess=a_expected_target)
	    elif (url_toks == ['vyper-cms', 'domain', 'accepted']):
		t_expected_target = '/%s/' % ('/'.join(url_toks[0:-1]))
		return HttpResponseRedirect(t_expected_target)
	    elif (t_expected_target == '/vyper-cms/layout/'):
		tag = url_toks[-1]
		layout_snippet_type = content_models.get_layout_snippet_type()
		layout_snippets = content_models.Snippet.objects.filter(Q(snippet_type=layout_snippet_type), Q(snippet_tag=tag))
		if (layout_snippets.count() > 0):
		    aLayoutSnippet = layout_snippets[0]
		    _site_id = -1
		    if (site_handle.aSiteName is None):
			sitenames = content_models.SiteName.objects.filter(user=site_handle.aUser)
			if (sitenames.count() > 0):
			    aSiteName = sitenames[0]
			    _site_id = aSiteName.site.id
		    else:
			_site_id = site_handle.aSiteName.site.id
		    sites = aLayoutSnippet.sites.filter(id=_site_id)
		    if (sites.count() > 0):
			pass # remove the old layout
		    add_layout_to_current_site(aLayoutSnippet,site_handle.aUser)
		return HttpResponseRedirect(t_expected_target)
	    elif (url_toks == ['vyper-cms', 'content', 'populate', 'content-pages']):
		normalize_content = lambda foo:[anItem for anItem in foo if (anItem.sites.count() == 1)]
		
		aSitename = utils.get_sitename_for_user(site_handle.aUser)
		snippet_types = utils.get_snippet_types(admin=0)
		snippets = content_models.Snippet.objects.filter(Q(snippet_type__in=snippet_types), Q(sites=aSitename.site.id))
		contents = content_models.Content.objects.filter(Q(sites=aSitename.site.id), Q(admin_mode=0))
    
		h = oohtml.HtmlCycler()
		h.use_cycler = True
		h.table_header_attrs = {'bgColor':'silver','align':'center','style':'font-weight:bold;'}
		h.cycle_func = oohtml.HtmlCycler.shaded_class_cycler_function2()
    
		delete_btn_func = lambda foo:oohtml.render_Button(id='btn_delete_content',src='/static/images/icons/16X16/delete.gif',title='Delete #%s \'%s\' (%s).' % (foo.id,foo.descr,foo.snippet_type.snippet_type),onClick="handle_delete_content('%s','%d');" % (foo.snippet_type.snippet_type,foo.id))
		edit_btn_func = lambda foo:oohtml.render_Button(id='btn_edit_content',src='/static/images/icons/16X16/script.gif',title='Edit #%s \'%s\' (%s).' % (foo.id,foo.descr,foo.snippet_type.snippet_type),onClick="handle_edit_content('%s','%d');" % (foo.snippet_type.snippet_type,foo.id))

		href = 'http://%s/' % (site_handle.aSiteName.site.domain)
		rows = [[oohtml.render_Button(id='btn_add_content',src='/static/images/icons/16X16/add.gif',title='Add a New Page.',onClick="this.disabled=true;popup_add_content();"),'#','Page Type','URL','Description','Menu Tag','<a href="%s" title="Site Preview" class="popupwindow" rel="windowCenter" target="_blank">Site Preview</a>' % (href)]]
    
		func_content = lambda foo:[delete_btn_func(foo),foo.id,foo.menutype.menutype,foo.url,foo.descr,foo.menu_tag,edit_btn_func(foo)]
		for aContent in normalize_content(contents):
		    so = SmartObject(aContent.__dict__)
		    so.snippet_type = SmartObject({'snippet_type':'content'})
		    so.menutype = SmartObject({'menutype':aContent.menutype.menutype})
		    rows.append(func_content(so))
    
		func_snippet = lambda foo:[delete_btn_func(foo),foo.id,foo.snippet_type.snippet_type,foo.snippet_tag,foo.descr,'&nbsp;',edit_btn_func(foo)]
		for aSnippet in normalize_content(snippets):
		    rows.append(func_snippet(aSnippet))
    
		h.table_cell_attrs = {'align':'center', 'bgColor':'#666'}
		h.table_header_attrs['bgColor'] = 'black'
		h.table_header_attrs['align'] = 'center'
		h.html_simple_table_with_header(rows,border='1')
		return HttpResponse(h.toHtml(),mimetype='text/html')
	    elif (url_toks == ['vyper-cms', 'content', 'editor', 'submit']):
		menutypes = content_models.MenuType.objects.filter(menutype='top')
		aMenutype = None
		if (menutypes.count() > 0):
		    aMenutype = menutypes[0]
		
		s_response = '1=success'
		
		url = django_utils.get_from_post(request,'url','')
		pagetype = django_utils.get_from_post(request,'pagetype','')
		menu_tag = django_utils.get_from_post(request,'menu_tag','')
		content = django_utils.get_from_post(request,'content','')
		descr = django_utils.get_from_post(request,'descr','')
		rec_id = django_utils.get_from_post(request,'rec_id',-1)
    
		if (aMenutype is not None):
		    if (pagetype == 'content'):
			aContent = content_models.Content(menutype=aMenutype,admin_mode=False,url=url,descr=descr,menu_tag=menu_tag,target='*',content=content)
			aContent.save()
			aContent.sites.add(site_handle.aSiteName.site)
		    else:
			snippettypes = content_models.get_snippet_types_by_type(snippet_type=pagetype)
			aSnippetType = None
			if (snippettypes.count() > 0):
			    aSnippetType = snippettypes[0]
			if (aSnippetType is not None):
			    url = url if (aSnippetType.snippet_type != 'header') else aSnippetType.snippet_type
			    if (rec_id > -1):
				snippets = content_models.Snippet.objects.filter(id=rec_id)
				if (snippets.count() > 0):
				    aSnippet = snippets[0]
				    aSnippet.descr = descr
				    aSnippet.content = content
				    aSnippet.save()
				else:
				    s_response = '-300=Cannot update the Snippet because the Snippet cannot be found using the id of "%s".' % (rec_id)
			    else:
				is_okay_to_add = True
				if (aSnippetType.snippet_type == 'header'):
				    snippets = content_models.Snippet.objects.filter(Q(snippet_type=aSnippetType),Q(sites=site_handle.aSiteName.site))
				    if (snippets.count() > 0):
					is_okay_to_add = False
				if (is_okay_to_add):
				    aSnippet = content_models.Snippet(snippet_type=aSnippetType,descr=descr,snippet_tag=url,content=content)
				    aSnippet.save()
				    aSnippet.sites.add(site_handle.aSiteName.site)
				else:
				    s_response = '-400=Cannot add another "%s" because there can be only the one.' % (aSnippetType)
			else:
			    s_response = '-100=Cannot save the Snippet because the Snippet Type cannot be identified.'
		else:
		    s_response = '-200=Cannot save the Content because the Menu Type cannot be identified.'
		return HttpResponse(s_response,mimetype='text/html')
	    elif (len(url_toks) > 2) and (url_toks[0:-2] == ['vyper-cms', 'content', 'populate', 'delete']):
		pagetype,_id = url_toks[-2:]
		if (pagetype == 'content'):
		    snippets = content_models.Content.objects.filter(id=_id)
		else:
		    snippets = content_models.Snippet.objects.filter(id=_id)
		for aSnippet in snippets:
		    aSnippet.delete()
		return HttpResponse('1=%s,%s' % (pagetype,_id),mimetype='text/html')
	    elif (url_toks[0:3] == ['vyper-cms', 'content', 'editor']) and ( (len(url_toks) == 3) or (len(url_toks) > 3) and (url_toks[3] in snippet_types_unrestricted_list) and (str(url_toks[-1]).isdigit()) ):
		url = ''
		menu_tag = ''
		content = ''
		descr = ''
		pagetype = ''
		_id = ''
		if (len(url_toks) > 3):
		    pagetype,_id = url_toks[len(url_toks)-2:]
		    if (pagetype == 'content'):
			snippets = content_models.Content.objects.filter(id=_id)
			aSnippet = snippets[0] if (snippets.count() > 0) else None
		    else:
			snippets = content_models.Snippet.objects.filter(id=_id)
			aSnippet = snippets[0] if (snippets.count() > 0) else None
		    if (aSnippet is not None):
			content = aSnippet.content
			descr = aSnippet.descr
			try:
			    url = aSnippet.url
			    menu_tag = aSnippet.menu_tag
			except:
			    url = aSnippet.snippet_tag
			if (len(_context['INNER_CONTENT']) == 0):
			    xpected_url = utils._anchor_expected_target(url_toks[0:3])
			    contents = content_models.Content.objects.filter(Q(url=xpected_url), Q(sites=site_handle.SITE_ID), Q(admin_mode=_admin_mode))
			    if (contents.count() > 0):
				_context['INNER_CONTENT'] = contents[0]
			    else:
				snippettypes = content_models.get_snippet_types_by_type(snippet_type=pagetype)
				aSnippetType = None
				if (snippettypes.count() > 0):
				    aSnippetType = snippettypes[0]
				if (aSnippetType is not None):
				    snippets = content_models.Snippet.objects.filter(Q(sites=site_handle.SITE_ID),Q(snippet_tag=xpected_url))
				    if (snippets.count() > 0):
					_context['INNER_CONTENT'] = snippets[0].content
		snippet_types = utils.get_snippet_types().order_by('snippet_type')
    
		iCount_headers = 0
		aSitename = utils.get_sitename_for_user(site_handle.aUser)
		snippets = utils.get_header_snippets().filter(sites=aSitename.site)
		if (snippets.count() > 0):
		    iCount_headers += 1
    
		c = {}
		h = oohtml.Html()
		if (len(pagetype) > 0) and (str(_id).isdigit()):
		    h.tagINPUT('pagetype',value=pagetype,readonly="readonly",id='pagetype',title='ReadOnly: Page Type - Upgrade to the Enterprise Version to change PageTypes.')
		else:
		    choices = [tuple([aSnippetType.snippet_type,aSnippetType.snippet_type]) for aSnippetType in snippet_types]
		    if (iCount_headers > 0):
			choices = [aChoice for aChoice in choices if (aChoice[0] != 'header')]
		    choices.insert(0,tuple(['','Choose...']))
		    h.tagSELECT(choices,pagetype,id='pagetype',name='pagetype',title='Page Type',onclick='handle_page_types_choice(this);')
		c['PAGETYPE'] = h.toHtml()
		c['URL_VALUE'] = url
		c['DESCR_VALUE'] = descr
		c['MENUTAG_VALUE'] = menu_tag
		c['CONTENT'] = content
		c['RECORD_ID'] = _id
		s_content = django_utils.render_from_string(_context['INNER_CONTENT'],context=c)
		return HttpResponse(s_content if (len(s_content) > 0) else '<h1 class="error2">SYSTEM ERROR - Cannot process your request.</h1><input id="btn_close_content_editor" type="button" value="[Close]" title="Close..." onclick="toggle_add_content();"/>',mimetype='text/html')
	    elif (len(url_toks) == 5) and (url_toks[0:3] == ['vyper-cms', 'content', 'editor']):
		c = {}
		if (url_toks[-2:] in [['media','manager'],['media','refresh']]):
		    allowed_file_types = utils.allowed_media_file_types
		    uploads_path = utils.get_uploads_path(site_handle.aSiteName)
		    files = [(f,os.stat(f)) for f in [os.path.join(uploads_path,f) for f in os.listdir(uploads_path) if (os.path.splitext(f)[-1] in allowed_file_types)]]
		if (url_toks[-2:] == ['media','manager']):
		    if (site_handle.aSiteName is not None):
			h = oohtml.HtmlCycler()
			rows = [['Choose your media file and one-click to upload.']]
			_input = oohtml.tag_INPUT(name='fileToUpload',id_="fileToUpload",type_="file",size="45",class_="input")
			_button = oohtml.tag_BUTTON('Upload',class_="button",id_="buttonUpload",onclick="return ajaxFileUpload();")
			rows.append([_input+_button])
			rows.append(['<b>Please select a file of type (%s) and click the upload button.</b>' % (', '.join(['"%s"' % (t) for t in allowed_file_types]))])
			h.html_simple_table_with_header(rows,border='0')
			
			div = h.tagDIV('',id_='div_media_library')
			utils.media_table_refresh(div,files)
			_context['INNER_CONTENT'] = h.toHtml()
		elif (url_toks[-2:] == ['media','refresh']):
		    h = oohtml.HtmlCycler()
		    utils.media_table_refresh(h,files)
		    _context['INNER_CONTENT'] = h.toHtml()
		s_content = django_utils.render_from_string(_context['INNER_CONTENT'],context=c)
		return HttpResponse(s_content,mimetype='text/html')
	    elif (url_toks == ['vyper-cms', 'content', 'editor', 'media', 'manager', 'upload']):
		acceptable_mimes = utils.acceptable_media_mimes
		uploads_path = utils.get_uploads_path(site_handle.aSiteName)
		responses = []
		try:
		    for k,aList in request.FILES.iteritems():
			for item in aList:
			    d = lists.HashedFuzzyLists2(item)
			    _filename = d['filename']
			    _content = d['content']
			    _content_type = d['content-type']
			    if (_content_type in acceptable_mimes):
				fpath = os.path.join(uploads_path,_filename)
				_utils.writeFileFrom(fpath,_content,mode='wb')
				responses.append('INFO: Successfully uploaded "%s".' % (_filename))
			    else:
				responses.append('WARNING: Cannot upload "%s" because it is not an image.' % (_filename))
		except Exception, e:
		    responses.append('WARNING the file upload resulted in an error because "%s".' % (str(e)))
		s_response = '<br/>'.join(responses)
		return HttpResponse(s_response,mimetype='text/html')
	    elif (url_toks == ['user','logout']):
		if (request.session.get('SALUTATION',None) is not None):
		    del request.session['SALUTATION']
		if (request.session.get('user_id',None) is not None):
		    del request.session['user_id']
		request.session['is_logged_in'] = False
		return HttpResponseRedirect('/')
	    elif (url_toks == ['user','login','accepted']):
		if (site_handle.aUser is not None):
		    _users_name = '%s %s' % (site_handle.aUser.firstname,site_handle.aUser.lastname)
		    request.session['SALUTATION'] = 'Welcome back %s.<br/>Please %s if you are not %s.' % (_users_name,oohtml.renderAnchor('/user/logout/','click here',title='Logout',target="_top"),_users_name)
		    aSitename = utils.get_sitename_for_user(site_handle.aUser)
		    if (aSitename is not None):
			request.session['has_valid_domain'] = utils.is_domain_valid(aSitename.site.domain)
		anActivity = content_models.UserActivity(user=site_handle.aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
		anActivity.save()
		_redirect = '/'
		if (django_utils.is_request_HTTPS(request)):
		    _redirect = 'http://%s' % (django_utils.get_fully_qualified_http_host(request))
		return HttpResponseRedirect(_redirect)
	elif (url_toks == ['user','login']) or (url_toks == ['user','login','process']) or (l_url_toks.findFirstMatching('forgot-password') > -1):
	    if (l_url_toks.findFirstMatching('accepted') > -1):
		t_content = get_template('_UserForgotPasswordSent.htm')
		_context['INNER_CONTENT'] += t_content.render(Context({}, autoescape=False))
	    else:
		from content import login
		i = l_url_toks.findFirstMatching('login')
		if (i == -1):
		    i = l_url_toks.findFirstMatching('forgot-password')
		_template = '%s.html' % (url_toks[i])
		_url_prefix_http = _url_prefix_https = ''
		if (not django_utils.is_request_HTTPS(request)):
		    _url_prefix_https = 'https://%s' % (django_utils.get_fully_qualified_http_host(request))
		    _url_prefix_http = 'http://%s' % (django_utils.get_fully_qualified_http_host(request))
		if (l_url_toks.findFirstMatching('forgot-password') == -1):
		    resp = login.login(request,template=_template,onAction='/user/%s/process/' % (url_toks[i]),onSuccess='%s/user/%s/accepted/' % (_url_prefix_http,url_toks[i]))
		else:
		    resp = login.forgot(request,template=_template,onAction='/user/%s/process/' % (url_toks[i]),onSuccess='%s/user/%s/accepted/' % (_url_prefix_http,url_toks[i]))
		if (ObjectTypeName.typeClassName(resp) == 'django.http.HttpResponseRedirect'):
		    return resp
		js_head = login._login_header()
		_context['HEAD'] = _context['HEAD'].replace('//+++SCRIPTS+++',js_head)
		_context['INNER_CONTENT'] += resp + login.login_scripts()
	elif (l_url_toks.findFirstMatching('register') > -1) or (l_url_toks.findFirstMatching('registration') > -1):
	    _url_prefix_https = ''
	    if (not django_utils.is_request_HTTPS(request)):
		_url_prefix_https = 'https://%s' % (django_utils.get_fully_qualified_http_host(request))
	    d_context = {}
	    form_register = forms.DjangoForm(request,'register', content_models.User, '%s/register/process/' % (_url_prefix_https))
	    if (url_toks == ['user', 'register']):
		form_register.use_captcha = True
		form_register.captcha_form_name = 'captcha_form_fields.html'
		form_register.captcha_font_name = 'BerrysHandegular.ttf'
		form_register.captcha_font_size = 32
		form_register.captcha_fill = (255,255,255)
		form_register.captcha_bgImage = 'bg.jpg'
		try:
		    form_html = form_as_html.form_as_html(form_register,callback=_form_for_model)
		except Exception, e:
		    form_html = _utils.formattedException(details=e)
		s = django_utils.render_from_string(_context['INNER_CONTENT'],context={'REGISTER_FORM':form_html})
		h = oohtml.Html()
		div = h.tagDIV(s,style=utils._styles_ if (site_handle.aUserOwner is not None) else '')
		_context['INNER_CONTENT'] = h.toHtml()
	    elif (len(url_toks) > 1) and (url_toks[-1] == 'process'):
		try:
		    email_address = request.POST['email_address']
		    users = content_models.User.objects.filter(Q(email_address=email_address))
		    if (users.count() == 0):
			form_register.use_captcha = True
			form_register.captcha_form_name = 'captcha_form_fields.html'
			form_register.captcha_font_name = 'BerrysHandegular.ttf'
			form_register.captcha_font_size = 32
			form_html = form_as_html.form_as_html(form_register,request=request,callback=_form_for_model)
			if (captcha.is_captcha_form_valid(request)):
			    _form_for_model(form_register, context=d_context)
			    form_html = form_register.validate_and_save(request,d_context,callback=on_successful_registration,callback_beforeSave=on_before_form_save,callback_validation_failed=on_unsuccessful_registration,callback_error=on_registration_form_error)
			    if (lists.isDict(form_html)):
				html_context = form_html
				t_content = get_template('_registered.html')
				form_html = t_content.render(Context(html_context, autoescape=False))
			    else:
				if (len(form_register.last_error) > 0):
				    h = oohtml.Html()
				    h.tagDIV('<BR/>'.join(form_register.last_error.split('\n')),class_='error')
				    form_html = h.toHtml() + form_html
			else:
			    h = oohtml.Html()
			    div = h.tagDIV('',class_='errorBg')
			    div.tagP('WARNING: "%s" does not match the expected value.  Please try again.' % (request.POST['imgtext']))
			    form_html = h.toHtml() + form_html
		    else:
			aUser = users[0]
			if (aUser.activated == 0):
			    html_context = _send_registration_email(request,email_address)
			    t_content = get_template('_registered.html')
			    form_html = '<br/>'.join(t_content.render(Context(html_context, autoescape=False)).split('\n'))
			else:
			    t_content = get_template('_activated.html')
			    form_html = t_content.render(Context({}, autoescape=False))
		except Exception, e:
		    form_html = _utils.formattedException(details=e)
		h = oohtml.Html()
		div = h.tagDIV(form_html,style=utils._styles_ if (site_handle.aUserOwner is not None) else '')
		_context['INNER_CONTENT'] += h.toHtml()
	    elif ('/'.join(url_toks[0:-1]).lower().find('registration/activate') > -1):
		try:
		    email_address, ts = keys._decode(url_toks[-1]).split(',')
		    now = _utils.timeSecondsFromTimeStamp(_utils.getFromDateTimeStr(_utils.timeStamp()))
		    secs = float(now) - float(ts)
		    if (secs < 86400):
			users = content_models.User.objects.filter(Q(email_address=email_address), Q(activated=0))
			if (users.count() > 0):
			    aUser = users[0]
			    password = GenPasswd.GenPasswdFriendly()
			    aUser.password = md5.md5(password)
			    aUser.activated = 1
			    aUser.activated_on = _utils.today_localtime()
			    aUser.save()
			    anActivity = content_models.UserActivity(user=aUser,ip=django_utils.get_from_environ(request,'REMOTE_ADDR'),action='/'.join(url_toks))
			    anActivity.save()
			    t_content = get_template('_active.html')
			    form_html = t_content.render(Context({}, autoescape=False))
			    send_activation_email(email_address, password)
			else:
			    users = content_models.User.objects.filter(Q(email_address=email_address), Q(activated=1))
			    if (users.count() > 0):
				t_content = get_template('_activated.html')
				form_html = t_content.render(Context({}, autoescape=False))
			    else:
				form_html = 'Cannot Activate - Please Register again to get back into the system as a new user.'
		    else:
			form_html = 'Cannot Activate - Please Register again to get back into the system as a new user.'
		except:
		    form_html = 'Cannot Activate - Please Register again to get back into the system as a new user.'
		_context['INNER_CONTENT'] += form_html
	
	now = _utils.timeStamp(format=pages.formatTimeStr())
	_context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
	if (site_handle.aUserOwner is not None):
	    content_header = ''
	    header_snippets = utils.get_header_snippets().filter(sites=site_handle.SITE_ID)
	    for aSnippet in header_snippets:
		content_header += aSnippet.content
	    
	    _context['SITE_HEADER'] = content_header
	    _context['SITE_CONTENT'] = _context['INNER_CONTENT']
	    _context['SITE_FOOTER'] = _context['FOOTER']
	    return HttpResponse(content=django_utils.render_from_string(aLayoutSnippet.content if (aLayoutSnippet is not None) else '<h1>No Content has been defined for this site...</h1>',context=_context))
	matches = _reIS_TEMPLATE.search(_context['INNER_CONTENT'])
	if (contents.count() > 0) and (matches) and (any([(re.search(r"\{\{ %s \}\}" % (k), _context['INNER_CONTENT']) is not None) for k in _context.keys()])):
	    _context['INNER_CONTENT'] = django_utils.render_from_string(_context['INNER_CONTENT'],_context)
	return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder='new')
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	mimetype = mimetypes.guess_type('.html')[0]
	return HttpResponse('<br/>'.join(info_string.split('\n')), mimetype=mimetype)

