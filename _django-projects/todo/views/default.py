from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from vyperlogix.django.decorators import cache

#from django.newforms import form_for_model, form_for_instance, save_instance, BaseForm, Form, CharField

import os
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.html import stripper

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.django.rss import content as rss_content

from vyperlogix.misc import ObjectTypeName

from vyperlogix.lists import ListWrapper

from models import ToDo

from content import models as content_models

from django.db.models import Q

from vyperlogix.django import forms
from vyperlogix.django.forms import form_as_html

import urllib

import socket

_title = 'todo.raychorn.com, Manage your Life&trade;'

grid_verb_symbol = 'grid'

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

@cache.cache(settings.CACHE_TIMER)
def rss_feed(url):
    return rss_content.rss_content(url)

def render_menu(menutype,id="MenuBar1", class_="MenuBarHorizontal", target='/'):
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
    target = target if (isinstance(target,str)) else '/'

    contents1 = content_models.Content.objects.filter(menutype=menutype)
    contents1 = contents1.filter(Q(target='*') | Q(target='%s' % (target)))

    contents2 = content_models.Content.objects.filter(menutype=menutype_any)
    contents2 = contents2.filter(Q(target='*') | Q(target='%s' % (target)))
    
    contents3 = content_models.Content.objects.filter(url=target)
    
    contents = [c for c in contents1] + [c for c in contents2]
    
    l = ListWrapper.SmartList(contents)

    try:
	if (menutype.menutype == 'top'):
	    i = l.findFirstMatching(target,callback=does_target_match)
	    if (i == -1):
		contents = contents + [c for c in contents3]
		l = ListWrapper.SmartList(contents)
    except:
	pass

    i = l.findFirstMatching('Home',callback=does_this_match)
    
    _contents = []
    if (i > -1):
	_contents = l.copy_excluding_with(i,'menu_tag')
    else:
	_contents = contents

    h = oohtml.Html()
    ul = h.tagUL(id=id, class_=class_)
    for aContent in _contents:
	isLocal = not re.search(r"^(http)(s?)://((www\.)+[a-zA-Z0-9\-.?,'/\\+&amp;=:%$#_]*)?", aContent.url)
	_target = "_top" if (isLocal) else "_blank"
	_menu_tag = aContent.menu_tag
	if (aContent.url == target):
	    _menu_tag = '['+aContent.menu_tag+']'
	link = oohtml.renderAnchor(aContent.url, _menu_tag, target=_target, title=aContent.descr)
	ul._tagLI(link)
    return h.toHtml()

def grid(request):
    from django.db.models import Q
    from vyperlogix.classes import SmartObject
    from vyperlogix.html.flexigrid.grid_handler import grid_handler
    
    url_toks = django_utils.parse_url_parms(request)
    articles = SmartObject.SmartObject()
    d_parms = _utils.get_dict_as_pairs(url_toks)
    _query = django_utils.get_from_post(request,'query','')
    _qtype = django_utils.get_from_post(request,'qtype','')
    if (d_parms[grid_verb_symbol] in ['items','item']):
	_page = django_utils.get_from_post(request,'page',1)
	_rp = django_utils.get_from_post(request,'rp',10)
	_start = ((_page-1) * _rp)
	_stop = _start + _rp

        num = 1
	_items = ToDo.objects
	if (len(_qtype) > 0) and (len(_query) > 0):
	    try:
		_q = eval("Q(%s='%s')" % (_qtype,_query))
		_items = _items.filter(_q)
	    except:
		pass
	if (len(url_toks) == 3):
	    _items = _items.order_by('%s' % (url_toks[-1]))
	_items = _items.all()[_start:_stop]
        _items_ = []
	for anItem in _items:
	    url = 'http://%s/item/%d/' % (django_utils.get_fully_qualified_http_host(request),anItem.id)
	    _link = oohtml.renderAnchor(url,'%d' % (anItem.id),target='_top')
	    d_rec = {'id':_link, 'name':anItem.name, 'duedate':_utils.getAsDateTimeStr(anItem.duedate,fmt=_utils.formatDate_MMDDYYYY_slashes()), 'status':anItem.status}
	    _items_.append(SmartObject.SmartObject(d_rec))
	    num += 1
	content = grid_handler(request,_items_,lambda r:[r.id, r.name, r.duedate, r.status])
    else:
	info_string = '%s :: Unknown "%s".' % (misc.funcName(),url_toks)
	content = '<h3>%s</h3>' % (info_string)
    response = HttpResponse(content, mimetype="text/x-json")
    response['Expires'] = _utils.timeStampLocalTime(format=_utils.formatMetaHeaderExpiresOn())
    response['Last-Modified'] = _utils.timeStampLocalTime(format=_utils.formatMetaHeaderExpiresOn())
    response['Cache-Control'] = 'no-cache, must-revalidate'
    response['Pragma'] = 'no-cache'
    return response

def grid_head():
    from vyperlogix.html.flexigrid import script
    head_list = script.head_list('/static/flexigrid')
    return head_list

def grid_content_items(request,name,id_=-1,width=500,height=350):
    from vyperlogix.html.flexigrid import script
    colModel = '''
{display: '#', id : 'id', width : 30, sortable : true, align: 'left', hide: false},
{display: 'Name', name : 'name', width : 100, sortable : true, align: 'left', hide: false},
{display: 'Due Date', duedate : 'duedate', width : 150, sortable : true, align: 'left', hide: false},
{display: 'Status', status : 'status', width : 120, sortable : true, align: 'left', hide: false},
    '''
    searchitems = '''
{display: 'Name', name : 'name'},
{display: 'Due Date', name : 'duedate'},
{display: 'Status', name : 'status'},
    '''
    url = 'http://%s/grid/items/' % (django_utils.get_fully_qualified_http_host(request))
    if (str(id_).isdigit()) and (id_ > -1):
	url = 'http://%s/grid/item/%d/' % (django_utils.get_fully_qualified_http_host(request),id_)
    js = script.script_head(name,url,'Items',colModel,searchitems,'name','asc',width=width,height=height)
    return js

def calendar_content(request):
    t_content = get_template('new/_calendar_template.html')
    js = oohtml.render_scripts(t_content.render(Context({})))
    return js

def _form_for_model(form, context={}):
    from vyperlogix.classes.SmartObject import SmartObject
    f = form
    if (f.form_name == 'add'):
	f.fields['status'].required = True

	f.fields['name'].min_length = 2
	f.fields['name'].required = True
	
	f.set_choice_model_for_field_by_name('status',SmartObject({'value_id':'value','text_id':'text'}))

	#validation_condition = lambda self:((len(self.fields['state'].value) == 0) and (self.fields['country'].value == 'USA')) or ((len(self.fields['state'].value) > 0) and (self.fields['country'].value != 'USA'))
	#validation_message = 'Either the State or Country is invalid.'
	#validation_tuple = tuple([validation_condition,{'STATE':validation_message,'COUNTRY':validation_message}])
	#f.field_validation = validation_tuple

def on_successful_todo(form,request):
    return {}

def on_before_form_save(form,request,obj):
    pass

def on_unsuccessful_todo(form,context):
    return form_as_html.form_as_html(form,callback=_form_for_model,context=context)

def on_todo_form_error(form,request):
    pass
    
def default(request):
    global _title
    from vyperlogix.html.flexigrid import script
    
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    try:
	_url_toks = [''] + url_toks if (len(url_toks) > 0) else url_toks + ['']
	_expected_target = '/' if (len(url_toks) == 0) else '/'.join(_url_toks)
	menutype_top = content_models.MenuType.objects.filter(menutype='top')
	menutype_bottom = content_models.MenuType.objects.filter(menutype='bottom')

	t_head = get_template('new/_head.html')
	c_head = Context({})
	
	head_snippet_type = content_models.SnippetType.objects.filter(snippet_type='head')
	if (head_snippet_type.count() > 0):
	    head_snippet_type = head_snippet_type[0]
	head_snippet = content_models.Snippet.objects.filter(snippet_type=head_snippet_type)
	if (head_snippet.count() > 0):
	    head_snippet = head_snippet[0]
	title_snippet_type = content_models.SnippetType.objects.filter(snippet_type='title')
	if (title_snippet_type.count() > 0):
	    title_snippet_type = title_snippet_type[0]
	title_snippet = content_models.Snippet.objects.filter(snippet_type=title_snippet_type)
	if (title_snippet.count() > 0):
	    title_snippet = title_snippet[0]
	    _title = stripper.strip(title_snippet.content)
	c_head = Context({'TITLE':_title})
	content_head = t_head.render(c_head)

	normalize_url = lambda url:'/' if (not str(url).startswith('/')) else ''
	
	t_analytics = get_template('new/_google_analytics.html')
	t_footer = get_template('new/_footer.html')
	t_menu = get_template('new/_site_menu.html')
	_menu_id_top = "MenuBarTop"
	_menu_id_bottom = "MenuBarBottom"
	_menu_class = "MenuBarHorizontal"
	_context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({})),
		    'INNER_CONTENT':'',
		    'MENU_ID':_menu_id_bottom,
		    'MEDIA_URL':settings.MEDIA_URL,
		    'FOOTER':t_footer.render(Context({'CURRENT_YEAR':_utils.timeStampLocalTime(format=_utils.formatDate_YYYY()),'MENU':t_menu.render(Context({'MENU_CONTENT':render_menu(menutype_bottom,id=_menu_id_top,class_=_menu_class,target=_expected_target)}))})),
		    'MENU':t_menu.render(Context({'MENU_CONTENT':render_menu(menutype_top,id=_menu_id_top,class_=_menu_class,target=_expected_target)})),
		    'TITLE':'%s - %s (%s)',
		    'HEAD':content_head,
		    }
	    
	_context['INNER_CONTENT'] = ''
	sub_title = ''

	contents = content_models.Content.objects.filter(url=_expected_target)
	if (contents.count() > 0):
	    sub_title = contents[0].menu_tag
	elif (contents.count() == 0):
	    contents = content_models.Snippet.objects.filter(snippet_tag=_expected_target)
	    if (contents.count() > 0):
		sub_title = contents[0].descr
		
	if (contents.count() > 0):
	    _context['INNER_CONTENT'] = contents[0].content
	
	is_viewing_item = (url_toks[0] == 'item') if (len(url_toks) > 0) else False
	is_deleting_item = (url_toks[0] == 'delete') if (len(url_toks) > 0) else False
	
	if (_expected_target == '/'):
	    grid_name = 'table_items_grid'
	    grid_width = 800
	    grid_height = 200
	    _head = grid_head()
	    
	    _id = -1
	    
	    content = _context['INNER_CONTENT']
    
	    h = oohtml.Html()
	    h.html_simple_table([()],id=grid_name,style="display:inline;")
    
	    content += h.toHtml()
	    
	    _context['HEAD'] = _context['HEAD']+'\n'.join(_head)

	    _scripts = grid_content_items(request,grid_name,id_=_id,width=grid_width,height=grid_height)
	    _context['INNER_CONTENT'] = content+_scripts
	elif (_expected_target == '/add') or (is_viewing_item):
	    _scripts = calendar_content(request)
	    d_context = {}
	    _id = -1
	    if (is_viewing_item):
		_id = int(url_toks[-1]) if (str(url_toks[-1]).isdigit()) else -1
		_items = ToDo.objects.filter(id=_id)
		anItem = _items[0] if (_items.count() > 0) else None
		for k,v in anItem.__dict__.iteritems():
		    _v = v
		    if (k == 'duedate'):
			_v = _utils.getAsDateTimeStr(v,fmt=_utils.formatDate_MMDDYYYY_slashes())
		    elif (k == 'status'):
			_v = 'True' if (v) else 'False'
		    d_context['VALUE_%s' % (k.upper())] = _v
	    form_add_item = forms.DjangoForm(request,'add', ToDo, '/%s/submit/' % ('add' if (not is_viewing_item) else 'edit'))
	    form_add_item.use_captcha = False
	    form_add_item.datetime_field_content = get_template('new/_calendar_proxy.html')
	    form_add_item.submit_button_title = "Submit your ToDo Item."
	    form_add_item.submit_button_value = "Submit ToDo Item"
	    form_add_item.add_hidden_field('id',_id)
	    try:
		form_html = form_as_html.form_as_html(form_add_item,callback=_form_for_model,context=d_context)
	    except Exception, e:
		form_html = _utils.formattedException(details=e)
	    _extra_html = ''
	    if (is_viewing_item):
		t_extra_html = get_template('new/_delete_todo_button.html')
		_extra_html = t_extra_html.render(Context({'ID':'%d' % (_id)}))
	    _context['INNER_CONTENT'] = _context['INNER_CONTENT'] + _extra_html + form_html + _scripts
	elif (url_toks[0] in ['add','edit']) and (url_toks[-(1 if (not str(url_toks[-1]).isdigit()) else 2)] == 'submit'):
	    d_context = {}
	    _action = ''.join([t for t in _expected_target.split('/') if (len(t) > 0)])
	    form_add_item = forms.DjangoForm(request,'add', ToDo, '/%s/submit/' % (_action))
	    _form_for_model(form_add_item)
	    try:
		form_html = form_add_item.validate_and_save(request,d_context,callback=on_successful_todo,callback_beforeSave=on_before_form_save,callback_validation_failed=on_unsuccessful_todo,callback_error=on_todo_form_error)
		if (isinstance(form_html,dict)):
		    html_context = form_html
		    t_content = get_template('new/_todo_submitted.html')
		    form_html = t_content.render(Context(html_context))
		else:
		    _context['INNER_CONTENT'] = _context['INNER_CONTENT'] + form_html
	    except Exception, e:
		form_html = _utils.formattedException(details=e)
	    _context['INNER_CONTENT'] = _context['INNER_CONTENT'] + form_html
	elif (_expected_target == '/delete') or (is_deleting_item):
	    _id = int(url_toks[-1]) if (str(url_toks[-1]).isdigit()) else -1
	    _items = ToDo.objects.filter(id=_id)
	    for anItem in _items:
		anItem.delete()
	    t_content = get_template('new/_todo_deleted.html')
	    form_html = t_content.render(Context({'ID':'%d' % (_id)}))
	    _context['INNER_CONTENT'] = _context['INNER_CONTENT'] + form_html
	
	now = _utils.timeStamp(format=pages.formatTimeStr())
	_context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
	return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder='new')
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	import mimetypes
	mimetype = mimetypes.guess_type('.html')[0]
	response = HttpResponse('<br/>'.join(info_string.split('\n')), mimetype=mimetype)
	return response

