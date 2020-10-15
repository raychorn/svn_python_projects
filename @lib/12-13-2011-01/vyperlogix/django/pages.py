__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

import os
import time
import datetime

from vyperlogix.html import myOOHTML as oohtml

template_filename = lambda template_folder,fname:'%s%s%s' % (template_folder,os.sep if (len(template_folder) > 0) else '',fname)

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def formatMetaDateTimeStr():
    return '%a, %d %b %Y %H:%M:%S'

def get_tabs_nav_html(navigation_tabs,request=None,content=''):
    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    i = 1
    request_path = request.path if (ObjectTypeName.typeClassName(request).find('django.core.handlers.wsgi.WSGIRequest') > -1) else ''
    for tab in navigation_tabs:
	_url, _text1, _text2 = tab
	ul._tagLI(oohtml.renderAnchor('%s' % _url,_text1,target="_blank" if (_url.find('://') > -1) else "_top",rel='sb%d'%i,class_='selected' if (_url == request_path) else ''))
	i += 1
    ul._tagLI(content if (misc.isString(content)) else '')

    return h.toHtml()

def get_tabs_nav_content_html(navigation_tabs):
    h = oohtml.Html()
    i = 1
    for tab in navigation_tabs:
	_url, _text1, _text2 = tab
	div = h.tag(oohtml.oohtml.DIV, id='sb%d'%i, class_="tabcontent")
	span = div.tag(oohtml.oohtml.SPAN, class_="tabTitle")
	span.text(_text2)
	i += 1

    return h.toHtml()

def _render_the_page(request,_title,template_name,navigation_menu_type,navigation_tabs,styles_context={},context={},footer_context={},template_folder='',js=[],head=[]):
    '''
    request is the Django request.
    _title is the title for the site.
    template_name is the template filename for the body of the content, may be a partial.
    navigation_menu_type is the tabs menu type for the site navigation bar.
    navigation_tabs is the list of tabs.
    context is the Context for the main body of the site per the template_name.
    template_folder is the prefix for the folder in which the templates reside. (template_name may reside in a different folder than the rest of the templates)
    '''
    import urllib

    from vyperlogix.misc import _utils
    from vyperlogix.django import tabs
    
    now = _utils.timeStamp(format=formatTimeStr())
    _yyyy = _utils.timeStamp(format=formatYYYYStr())

    url_toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]

    h = oohtml.Html()
    try:
	for j in js:
	    h.tagSCRIPT(src=j)
    except:
	pass
    js_head = h.toHtml()

    styles_content = ''
    if (styles_context.has_key('ADDITIONAL_JS')):
	styles_content = styles_context['ADDITIONAL_JS']
    else:
	styles_context['ADDITIONAL_JS'] = styles_content
    styles_content = '%s%s' % (js_head,styles_content)
    styles_context['ADDITIONAL_JS'] = styles_content
	
    t_styles = get_template(template_filename(template_folder,'_styles.html'))
    html_styles = t_styles.render(Context(styles_context))

    t_tabs_header = get_template(template_filename(template_folder,'_tabs_header.html'))
    c = Context({'id':tabs.tab_num_from_url(url_toks[0] if (len(url_toks) > 0) else '/',navigation_tabs)})
    c.update(styles_context)
    html_tabs_header = t_tabs_header.render(c)

    head_content = ''
    try:
	for item in head:
	    head_content += item
    except:
	pass
    
    _delta = datetime.timedelta(days=365.25*20)
    _dt = datetime.datetime.fromtimestamp(time.time())
    _expires_time = _dt - _delta
    _expires_ts = time.strftime(formatMetaDateTimeStr(),_expires_time.timetuple())
    _last_modified_ts = time.strftime(formatMetaDateTimeStr(),_dt.timetuple())

    t_header = get_template(template_filename(template_folder,'_header_for_content.html'))
    c = Context({'the_title': '%s (%s)' % (_title,now),
		 'STYLES_CONTENT':html_styles,
		 'TABS_HEADER':html_tabs_header+head_content,
		 'EXPIRES_TIME':_expires_ts,
		 'LAST_MODIFIED':_last_modified_ts
		 })
    c.update(context)
    html_header = t_header.render(c)
    
    t_footer = get_template(template_filename(template_folder,'_footer_for_content.html'))
    c = Context({'current_year': _yyyy})
    c.update(footer_context)
    html_footer = t_footer.render(c)

    t_content = get_template(template_name)
    html_content = t_content.render(Context(context))
    
    t_tabs_content = get_template(template_filename(template_folder,'_tabs_content.html'))
    html_tabs_content = t_tabs_content.render(Context({'MENU_TYPE':navigation_menu_type,
						       'NAVIGATION_TABS':get_tabs_nav_html(navigation_tabs),
						       'NAVIGATION_CONTENT':get_tabs_nav_content_html(navigation_tabs)
						       }))
    
    t = get_template(template_filename(template_folder,'site_content_template.html'))
    c = Context({'current_year': _yyyy,
		 'the_title': _title,
		 'HEADER_FOR_CONTENT':html_header,
		 'FOOTER_FOR_CONTENT':html_footer,
		 'CONTENT':html_content,
		 'TABS_CONTENT':html_tabs_content
		 })
    html = t.render(c)
    return html

def render_the_page(request,_title,template_name,navigation_menu_type,navigation_tabs,styles_context={},context={},footer_context={},template_folder='',js=[],head=[]):
    '''
    request is the Django request.
    _title is the title for the site.
    template_name is the template filename for the body of the content, may be a partial.
    navigation_menu_type is the tabs menu type for the site navigation bar.
    navigation_tabs is the list of tabs.
    context is the Context for the main body of the site per the template_name.
    template_folder is the prefix for the folder in which the templates reside. (template_name may reside in a different folder than the rest of the templates)
    '''
    return HttpResponse(_render_the_page(request,_title,template_name,navigation_menu_type,navigation_tabs,styles_context=styles_context,context=context,footer_context=footer_context,template_folder=template_folder,js=js,head=head))

def _render_the_template(request,_title,template_name,context={},template_folder=''):
    t_page = get_template(template_filename(template_folder,template_name))
    html_page = t_page.render(Context(context, autoescape=False))
    return html_page

def render_the_template(request,_title,template_name,context={},template_folder=''):
    s = _render_the_template(request,_title,template_name,context=context,template_folder=template_folder)
    return HttpResponse(s,mimetype='text/html')
