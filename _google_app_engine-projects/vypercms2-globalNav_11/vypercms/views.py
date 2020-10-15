from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, update_object
from django.template import RequestContext, TemplateDoesNotExist
from google.appengine.ext import db
from mimetypes import guess_type
from myapp.forms import PersonForm
from myapp.models import Contract, File, Person
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
from django.contrib.auth.decorators import login_required

from django.contrib.sites.models import Site

from django.template import loader
from django.template import Context

from models import StyleSheet, Title, Head, Template, Page, Domain

import mimetypes

from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

__content__ = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"><title>VyperCMS v2.0 ERROR</title></head><body>{{ content }}</body></html>'''

__content0__ = '''
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
    dir="ltr"
    xml:lang="en"
    lang="en">
  <head>
    <title>{{ title }}</title>
    <style type="text/css">
        {{ css }}
    </style>
  </head>
  {{ content }}
</html>
'''

__mimetype = mimetypes.guess_type('.html')[0]

@login_required
def admin(request,args):
    try:
        s_response = ''
        __error__ = ''

        parms = django_utils.parse_url_parms(request)
        isRestGetMenuCount = (len(parms) > 0) and (parms[0:4] == [u'rest', u'get', u'menu', u'count'])

        if (isRestGetMenuCount):
            s_response = restGetMenuCount(request,parms)
        else:
            __error__ = 'INVALID Request [@/%s]' % (str('/'.join(parms)))
            s_response = '<font color="red">'+__error__+'</font>'
        t = loader.get_template_from_string(__content__)
        c = {'content':s_response}
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=__mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)

def get_pages_by_url(u):
    return Page.all().filter('url',unicode(u))

__development__ = ['localhost:9000']

def default(request):
    try:
        s_response = ''
        __error__ = ''

        parms = django_utils.parse_url_parms(request)
        url = '/%s' % (str('/'.join(parms)))
        pages = get_pages_by_url(url)

	current_site = str(Site.objects.get_current())
	current_site = current_site.replace('.appspot','').replace('.com','').lower()

        isTweets = (len(parms) > 0) and (parms[0:2] == [u'vypertwitz', u'tweet']) # /vypertwitz/tweet/
        
        if (pages.count() > 0):
            aPage = pages[0]
            t = loader.get_template_from_string(__content0__)
            c = {'title':aPage.title.name,'css':aPage.css.content,'content':aPage.template.content}
        elif (url == '/'):
            return render_to_response(request, 'main.html')
        elif (isTweets):
            from vypertwitz.views import default as vypertwitz_default
            return vypertwitz_default(request)
        else:
	    from urllib import quote
            try:
                if (parms[0] == 'free-4u'):
                    _data = {}
                    if (request.GET.has_key('message')):
                        _data['url'] = 'http://free-4u.appspot.com/free-4u/activation.html?message=%s' % (quote(request.GET['message']))
		    try:
			return render_to_response(request, 'platforms/free-4u.html',data=_data)
		    except TemplateDoesNotExist, e:
			return render_to_response(request, 'main.html')
                return render_to_response(request, url[1:] if (url.startswith('/')) else url)
            except TemplateDoesNotExist, e:
                try:
                    return render_to_response(request, url)
                except TemplateDoesNotExist, e:
                    cname = request.META['HTTP_HOST']
                    if (django_utils._is_(request,__development__)):
                        return render_to_response(request, '404.html', {'details':'<p>This page shows-up for when running in development otherwise the home page shows-up.</p>'+'<BR/>'.join(_utils.formattedException(details=e).split('\n')),'HTTP_HOST':cname})
                    return render_to_response(request, 'main.html')
        content = t.render(Context(c,autoescape=False))
        return HttpResponse(content,mimetype=__mimetype)
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        mimetype = mimetypes.guess_type('.html')[0]
        return HttpResponse('<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n'))), mimetype=mimetype)
