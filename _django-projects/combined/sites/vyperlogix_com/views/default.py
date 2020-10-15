from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from django.newforms import form_for_model, form_for_instance, save_instance, BaseForm, Form, CharField

import os

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.django.rss import content as rss_content

from models import User, Product, Activation, Activity

import urllib

import socket

_title = 'Vyper Logix Corp, The 21st Century Python Company'

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    t_analytics = get_template('_google_analytics.html')
    _context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({})),
		'MENU_HOME_STATE':'',
		'MENU_PRODUCTS_STATE':'',
		'HOME_MENU_TITLE':'',
		'MENU_ABOUT_STATE':'',
		'ABOUT_MENU_TITLE':'',
		'MENU_LEGAL_STATE':'',
		'LEGAL_MENU_TITLE':'',
		'RIGHT_SIDE_CONTENT':'',
		'TITLE':'%s - %s (%s)'
		}
    sub_title = ''
    sub_title = ''
    if (len(url_toks) == 0):
	inner_home_context = {'LATEST_NEWS_CONTENT':rss_content.rss_content('http://www.pypi.info/index.php?format=feed&type=rss'),
			      'LEFT_SIDE_UPPER_CONTENT':'<== HOME PAGE',
			      }
	_context['INNER_CONTENT'] = render_static_html(request,'','_inner_home.html',template_folder='21',context=inner_home_context)
	_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
	c = {'PYEGGS_URL':'http://www.pyeggs.com/' if (_cname != 'ubuntu.localdomain') else 'http://pyeggs.dyn-o-saur.com'}
	_context['RIGHT_SIDE_CONTENT'] = render_static_html(request,'','_home.html','21',context=c)
	_context['MENU_HOME_STATE'] = '_down'
	_context['HOME_MENU_TITLE'] = 'Home'
    elif (url_toks[0] == 'vyper-proxy'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_vyperproxy_content.html',template_folder='21',context={})
	sub_title = 'Vyper-Proxy&trade;'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
    elif (url_toks[0] == 'products'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_products_content.html',template_folder='21',context={})
	sub_title = 'Vyper Logix Products'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
	_context['MENU_PRODUCTS_STATE'] = '_down'
	_context['PRODUCTS_MENU_TITLE'] = 'Products'
    elif (url_toks[0] == 'vyper_cloud_sdk'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_vyper-cloud-sdk_content.html',template_folder='21',context={})
	sub_title = 'Vyper-Cloud&trade; SDK'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
    elif (url_toks[0] == 'ruby-python-bridge'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_ruby_python_bridge.html',template_folder='21',context={})
	sub_title = 'Ruby-Python-Bridge&trade;'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
    elif (url_toks[0] == 'django20'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_django_20_content.html',template_folder='21',context={})
	sub_title = 'Django 2.0&trade;'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
    elif (url_toks[0] == 'about'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_about.html',template_folder='21',context={})
	sub_title = 'About Vyper Logix Corp'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
	_context['MENU_ABOUT_STATE'] = '_down'
	_context['ABOUT_MENU_TITLE'] = 'About'
    elif (url_toks[0] == 'legal'):
	_yyyy = _utils.timeStamp(format=pages.formatYYYYStr())
	_context['INNER_CONTENT'] = render_static_html(request,'','_legal.html',template_folder='21',context={'current_year':_yyyy})
	sub_title = 'Vyper Logix Corp Legal'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
	_context['MENU_LEGAL_STATE'] = '_down'
	_context['LEGAL_MENU_TITLE'] = 'Legal'
    elif (url_toks[0] == 'ruby-to-django'):
	_context['INNER_CONTENT'] = render_static_html(request,'','_ruby_to_django_content.html',template_folder='21',context={})
	sub_title = 'Ruby on Rails to Django&trade;'
	_context['RIGHT_SIDE_CONTENT'] = sub_title
    now = _utils.timeStamp(format=pages.formatTimeStr())
    _context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
    return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder='21')

def vyperProxy(request):
    return default(request)
    
def products(request):
    return default(request)

def vyper_cloud_sdk(request):
    return default(request)

def ruby_python_bridge(request):
    return default(request)

def django20(request):
    return default(request)

def about(request):
    return default(request)

def legal(request):
    return default(request)

def ruby_to_django(request):
    return default(request)

# ================================================================================================================

_styles_registrationForm = '''
.error{
color: red;
}
'''

# Come back to this later on... Differences between IE and FireFox are a bit of a bitch.
_scripts_registrationForm = '''function validate_name(obj,event) {
   if (obj != null) {
      try {
         //className = obj.className;
         //toks = className.split(',');
	 //minLength = toks[toks.length-1];
	 //className = toks[0];
	 //alert('1. ' + 'className=[' + className + ']' + ', minLength=[' + minLength + '], ' + ezObjectExplainer(obj));
	 alert('1. '); //  + ezObjectExplainer(obj)
      } catch (e) { alert(ezObjectExplainer(e) + ', ' + ezObjectExplainer(obj)); };
   }
}
'''

_vyper_proxy_menu = [('download','_vyperProxy_downloads.html'),
		     ('installation','_vyperProxy_installation.html'),
		     ('demo','_vyperProxy_demo.html'),
		     ('upgrade','_vyperProxy_upgrades.html'),
		     ('feedback','_vyperProxy_feedback.html'),
		     ('support','_vyperProxy_support.html'),
		     ('vps',('Virtual Private Servers','_vyperProxy_vsp.html')),
		     ('appliance',('Appliances','_vyperProxy_appliance.html')),
		     ]
d_vyper_proxy_menu = lists.HashedOrderedList(_vyper_proxy_menu)

def render_vyper_proxy_header(d,selector=''):
    h = oohtml.Html()
    try:
	_text = 'Vyper-Proxy&trade;'
	h.tagTD(oohtml.render_U(_text) if (selector == '') else oohtml.renderAnchor('/vyper-proxy/',_text,target="_top"))
	for k,v in d.iteritems():
	    _k = k.capitalize() if (not isinstance(v,tuple)) else v[0]
	    h.tagTD(oohtml.render_U(_k) if (k == selector) else oohtml.renderAnchor('/vyper-proxy/%s/' % (k),_k,target="_top"))
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print info_string
    return h.toHtml()

def make_formfield(f):
    ff = f.formfield()
    #if (f.name == 'firstname'):
        #ff.widget.attrs['onblur'] = "validate_name(this,event)"
        #ff.widget.attrs['class'] = "required,2"
    return ff

def get_freehosts():
    import sqlalchemy_models
    return sqlalchemy_models.get_freehosts()
    
def get_freehost_by_name(domain_name):
    import sqlalchemy_models
    return sqlalchemy_models.get_freehost_by_name(domain_name)
    
def _form_for_model(form, context={}):
    from vyperlogix.classes.SmartObject import SmartObject
    f = form
    if (f.form_name == 'registration'):
	f.fields['firstname'].min_length = 2
	f.fields['firstname'].required = True
	f.fields['lastname'].min_length = 2
	f.fields['lastname'].required = True
	f.fields['email_address'].required = True
	f.fields['email_address'].max_length = 128
	f.fields['phone_number'].max_length = 20
	f.fields['phone_number'].min_length = 12
	f.fields['product'].required = True
	f.fields['product'].min_length = 1
	for k,v in f.fields.iteritems():
	    if (k not in ['firstname', 'lastname', 'email_address']):
		v.required = False
	f.fields['state'].required = True
	f.fields['country'].required = True
	f.fields['product'].required = True

	f.set_choice_model_for_field_by_name('state',SmartObject({'value_id':'abbrev','text_id':'name'}))
	f.set_choice_model_for_field_by_name('country',SmartObject({'value_id':'iso3','text_id':'printable_name'}))
	f.set_choice_model_for_field_by_name('product',SmartObject({'value_id':'name','text_id':'name'}))
	
	f.set_choice_model_default_for_field_by_name('state',context['VALUE_STATE'] if (context.has_key('VALUE_STATE')) else '')
	f.set_choice_model_default_for_field_by_name('country',context['VALUE_COUNTRY'] if (context.has_key('VALUE_COUNTRY')) else '')
	f.set_choice_model_default_for_field_by_name('product',context['VALUE_PRODUCT'] if (context.has_key('VALUE_PRODUCT')) else '')

	validation_condition = lambda self:((len(self.fields['state'].value) == 0) and (self.fields['country'].value == 'USA')) or ((len(self.fields['state'].value) > 0) and (self.fields['country'].value != 'USA'))
	validation_message = 'Either the State or Country is invalid.'
	validation_tuple = tuple([validation_condition,{'STATE':validation_message,'COUNTRY':validation_message}])
	f.field_validation = validation_tuple

    html = f.as_html()
    return html

def get_html_styles_contexts(form, additional_form_context={}, js=[]):
    from vyperlogix.django.forms import templates

    form_html = _form_for_model(form, context=additional_form_context)
    form_template = templates.template_for_form(form_html)
    _styles_context = {'ADDITIONAL_STYLES':oohtml.render_styles(_styles_registrationForm),
		       'ADDITIONAL_JS':'' # oohtml.render_scripts(minify.minify_js(_scripts_registrationForm))
		       }
    form_content = form_template.render(Context(additional_form_context))
    html_context = {'DOWNLOAD_FORM':form_content}
    return html_context,_styles_context

def datasource_for_counties():
    import sqlalchemy_models
    countries = sqlalchemy_models.get_countries()
    return countries

def datasource_for_states():
    import sqlalchemy_models
    states = sqlalchemy_models.get_states()
    return states

def send_registration_email(email_address, product_name, product_link, site_link):
    t_EULA = get_template('VyperProxy_EULA.txt')
    EULA_context = {'PRODUCT_NAME':product_name, 'COMPANY_NAME':'Vyper Logix Corp.'}
    EULA_content = t_EULA.render(Context(EULA_context))

    t_content = get_template('VyperProxy_Registration_Email.txt')
    msg_context = {'PRODUCT_NAME':product_name, 'PRODUCT_LINK':product_link, 'SITE_LINK':site_link, 'EULA':EULA_content}
    msg_content = t_content.render(Context(msg_context))

    try:
	from vyperlogix.mail.mailServer import GMailServer
	from vyperlogix.mail.message import Message
	msg = Message('support@vyperlogix.com', email_address if (not settings.DEBUG) else keys._decode('72617963686F726E40686F746D61696C2E636F6D'), msg_content, subject="We have received your %s Registration Request." % (product_name))
	smtp = GMailServer('investors@vyperlogix.com', keys._decode('7065656B61623030'), server='smtpout.secureserver.net', port=3535)
	smtp.sendEmail(msg)
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	pass

    return msg_context

def on_successful_registration(form,request):
    emailField = form.email_fields[0]
    email_address = emailField.value
    productField = form.get_fields_by_name('product')[0]
    product_name = productField.value
    html_context = send_registration_email(email_address, product_name, 'http://%s/vyper-proxy/download/registration/activate/%s' % (request.environ['HTTP_HOST'],keys._encode('%s,%s' % (email_address,product_name))), 'http://%s/vyper-proxy/upgrade/' % (request.environ['HTTP_HOST']))
    t_content = get_template('_vyperProxy_registered.html')
    if (html_context.has_key('EULA')):
	html_context['EULA'] = oohtml.render_BR().join(html_context['EULA'].split('\n'))
    return html_context

def _vyperProxy(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    use_default = True
    d_items = d_vyper_proxy_menu
    t_content = get_template('_vyperproxy_content.html')
    html_header_content = render_vyper_proxy_header(d_vyper_proxy_menu)
    t_analytics = get_template('_vyperproxy_google_analytics.html')
    html_context = {}
    _styles_context = {}
    js = []
    
    def on_unsuccessful_registration(form,d_context):
	html_context,_styles_context = get_html_styles_contexts(form, additional_form_context=d_context, js=js)
	return [html_context,_styles_context]
    
    if (params.has_key('vyper-proxy')):
        _item = d_items[params['vyper-proxy']]
        if (_item is not None):
	    html_header_content = render_vyper_proxy_header(d_vyper_proxy_menu,selector=params['vyper-proxy'])
            t_content = get_template(_item[-1] if (not isinstance(_item,str)) else _item)
            if (params['vyper-proxy'] == 'download'):
		d_context = {}
		from vyperlogix.django import forms
		form_registration = forms.DjangoForm('registration', User, '/vyper-proxy/download/registration/submit/')
                if (params['registration'] == 'submit'):
		    _form_for_model(form_registration, context=d_context)
		    form_registration.get_freehost_by_name = get_freehost_by_name
		    t = form_registration.validate_and_save(request,d_context,callback=on_successful_registration,callback_validation_failed=on_unsuccessful_registration)
		    if (isinstance(t,dict)):
			html_context = t
			t_content = get_template('_vyperProxy_registered.html')
		    else:
			html_context,_styles_context = tuple(t)
		elif (params['registration'] == 'activate'):
		    pass
                else:
		    html_context,_styles_context = get_html_styles_contexts(form_registration, additional_form_context=d_context, js=js)
	    elif (params['vyper-proxy'] == 'installation'):
		t_analytics = get_template('_vyperproxy_installation_google_analytics.html')
	    elif (params['vyper-proxy'] == 'demo'):
		t_analytics = get_template('_vyperproxy_demo_google_analytics.html')
	    elif (params['vyper-proxy'] == 'upgrade'):
		t_analytics = get_template('_vyperproxy_upgrade_google_analytics.html')
	    elif (params['vyper-proxy'] == 'feedback'):
		t_analytics = get_template('_vyperproxy_feedback_google_analytics.html')
	    elif (params['vyper-proxy'] == 'support'):
		t_analytics = get_template('_vyperproxy_support_google_analytics.html')
	else:
	    d_items = params['vyper-proxy']
	    if (lists.isDict(d_items)):
		if (d_items['download'] == 'registration') and (d_items.has_key('activate')):
		    try:
			activation_key = keys._decode(d_items['activate'])
			activation_email, product_name = activation_key.split(',')
			aProduct = Product.objects.get(name=product_name)
			aUser = User.objects.get(email_address=activation_email,product=aProduct)
			already_activated = True
			try:
			    anAct = Activation.objects.get(user=aUser,product=aProduct)
			except Exception, details:
			    already_activated = False
			if (not already_activated):
			    try:
				anActivation = Activation(user=aUser,product=aProduct)
				anActivation.save()
			    finally:
				t_content = get_template('_vyperProxy_activation_completed.html')
				t_analytics = get_template('_vyperproxy_community_edition_activation_completed_google_analytics.html')
				# Send email with download link.
			else:
			    t_content = get_template('_vyperProxy_already_activated.html')
			    t_analytics = get_template('_vyperproxy_community_edition_already_activated_google_analytics.html')
			    # Send email with download link.
			pass
		    except:
			t_content = get_template('_vyperProxy_activation_failed.html')
			t_analytics = get_template('_vyperproxy_community_edition_activation_failed_google_analytics.html')
		    pass
	    else:
		pass
	    pass
    else:
	pass
    html_content = t_content.render(Context(html_context))
    _context = {'VYPERPROXY_HEADER':html_header_content,'VYPERPROXY_CONTENT':html_content}
    _footer_context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({}))}
    return pages.render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'vyperProxy_content.html',tabs._navigation_menu_type,tabs._navigation_tabs,styles_context=_styles_context,context=_context,footer_context=_footer_context,js=js)

def freehosts(request):
    hosts = get_freehosts()
    _context = {'FREEHOST_DOMAINS':oohtml.render_table_from_list(hosts,text_id='Domain__c',num_wide=6)}
    t_analytics = get_template('_google_analytics.html')
    _footer_context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({}))}
    return pages.render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'freehosts_content.html',tabs._navigation_menu_type,tabs._navigation_tabs,context=_context,footer_context=_footer_context)

def sync_iso(request):
    from models import Country
    countries = datasource_for_counties()
    for country in countries:
	aCountry = Country(iso=country.iso,name=country.name,printable_name=country.printable_name,iso3=country.iso3,numcode=country.numcode)
	aCountry.save()
    from models import State
    states = datasource_for_states()
    for state in states:
	aState = State(name=state.name,abbrev=state.abbrev)
	aState.save()
    pass

def handle_404(request):
    return HttpResponseNotFound(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'404_content.html',tabs._navigation_menu_type,tabs._navigation_tabs,context={}))

def static(request):
    url_toks = django_utils.parse_url_parms(request)
    fpath = '/'.join([settings.MEDIA_ROOT,_utils.eat_leading_token_if_empty(request.path,delim='/')]).replace('/static/media/','/static/')
    if (os.path.exists(fpath)):
        if (fpath.split('.')[-1] == 'txt'):
            content = _utils.readFileFrom(fpath)
            return HttpResponse(content)
        else:
            try:
                from django.views.static import serve
                return serve(request,request.path.replace('/media/',''),settings.MEDIA_ROOT)
            except:
                return HttpResponseNotAllowed(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'405_content.html',tabs._navigation_menu_type,tabs._navigation_tabs,context={}))
    return HttpResponseNotFound(pages._render_the_page(request,'Vyper-Proxy&trade; - %s' % (_title),'404_content.html',tabs._navigation_menu_type,tabs._navigation_tabs,context={}))
