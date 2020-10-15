from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from vyperlogix.misc import _utils

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

import urllib

# ============================================================================

_title = 'pyEggs™ - Vyper Logix Corp, Secure Python Eggs'

def render_static_html(request,_title,template_name,template_folder='',context={}):
    return pages._render_the_template(request,_title,template_name,context=context,template_folder=template_folder)

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    #t_analytics = get_template('_google_analytics.html')
    #_context = {'GOOGLE_ANALYTICS':t_analytics.render(Context({})),
		#'MENU_HOME_STATE':'',
		#'MENU_PRODUCTS_STATE':'',
		#'HOME_MENU_TITLE':'',
		#'MENU_ABOUT_STATE':'',
		#'ABOUT_MENU_TITLE':'',
		#'MENU_LEGAL_STATE':'',
		#'LEGAL_MENU_TITLE':'',
		#'RIGHT_SIDE_CONTENT':'',
		#'TITLE':'%s - %s (%s)'
		#}
    #sub_title = ''
    #sub_title = ''
    #if (len(url_toks) == 0):
	#inner_home_context = {'LATEST_NEWS_CONTENT':'',
			      #'LEFT_SIDE_UPPER_CONTENT':'<== HOME PAGE',
			      #}
	#_context['INNER_CONTENT'] = render_static_html(request,'','_inner_home.html',template_folder='21',context=inner_home_context)
	#_context['RIGHT_SIDE_CONTENT'] = render_static_html(request,'','_home.html','21')
	#_context['MENU_HOME_STATE'] = '_down'
	#_context['HOME_MENU_TITLE'] = 'Home'
    #elif (url_toks[0] == 'about'):
	#_context['INNER_CONTENT'] = render_static_html(request,'','_about.html',template_folder='21',context={})
	#sub_title = 'About Vyper Logix Corp'
	#_context['RIGHT_SIDE_CONTENT'] = sub_title
	#_context['MENU_ABOUT_STATE'] = '_down'
	#_context['ABOUT_MENU_TITLE'] = 'About'
    #now = _utils.timeStamp(format=pages.formatTimeStr())
    #_context['TITLE'] = _context['TITLE'] % (_title,sub_title,now)
    #return pages.render_the_template(request,'%s' % (_title),'index.html',context=_context,template_folder='21')
    return HttpResponse(t_analytics.render(Context({})))

def vyperProxy(request):
    return default(request)

# ============================================================================
#def default(request):
    #now = _utils.timeStamp(format=pages.formatTimeStr())
    #t = get_template('pyeggs-home.html')
    #html = t.render(Context({'current_date': now, 'the_title': _title}))
    #return HttpResponse(html)

#def about(request):
    #_yyyy = _utils.timeStamp(format=formatYYYYStr())
    #t = get_template('pyeggs-about.html')
    #html = t.render(Context({'current_year': _yyyy}))
    #return HttpResponse(html)

#def tabs(request):
    #now = _utils.timeStamp(format=pages.formatTimeStr())
    #toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    #t = get_template('tabs.html')
    #if (len(toks) == 1):
        #html = t.render(Context({'current_date': now, 'the_title': _title, 'id':0}))
    #else:
        #id = toks[-1] if (len(toks) == 2) else toks[1]
        #id = int(id) if (str(id).isdigit()) else 0
        #html = t.render(Context({'current_date': now, 'the_title': _title, 'id':id}))
    #return HttpResponse(html)

