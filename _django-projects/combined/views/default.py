import os

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.conf import settings

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.django import django_utils
from vyperlogix.django import pages

from vyperlogix.misc import LazyImport

from vyperlogix.misc  import ObjectTypeName

from vyperlogix.hash import lists

from vyperlogix.lists import ListWrapper

_title = 'Vyper Logix Corp., The 21st Century Python Company'

def default(request):
    '''
    The Process:
    
    1). Determine the domain name from the request object.
    2). Load the settings for the domain name.
    3). Load the views for the domain name.
    4). Pass the request to the views for the domain name.
    '''
    tracer = []
    info_string = ''
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    
    http_host = django_utils.get_http_host(request)
    _host = http_host.split(':')[0]

    s = 'combined%s.settings' % ('.django' if (not django_utils.isProduction(django_utils._cname)) else '')
    m = LazyImport.LazyImport(s)
    m = m.__lazyimport_import
    settings._target = None
    settings.configure(**m.__dict__)
    
    r_url = settings.ROOT_URLCONF
    
    if (settings.SITES.has_key(_host)):
        aSite = settings.SITES[_host]
        s = '%s.settings' % (aSite.__name__)
        m = LazyImport.LazyImport(s)
        m = m.__lazyimport_import
        settings._target = None
        settings.configure(**m.__dict__)
        
        _path = aSite.__path__[0]
        
        if (settings.ROOT_URLCONF):
            settings.ROOT_URLCONF = r_url
        
        if (settings.INSTALLED_APPS):
            i_apps = settings.INSTALLED_APPS
            
            _apps = []
            for appname in i_apps:
                p = os.path.join(_path,appname)
                if (os.path.exists(p)):
                    appname = '%s.%s' % (aSite.__name__,appname)
                _apps.append(appname)
                
            settings.INSTALLED_APPS = tuple(_apps)

        v = '%s.views.default' % (aSite.__name__)
        m = LazyImport.LazyImport(v)
        m = m.__lazyimport_import
        
        try:
            if (callable(m.default)):
                return m.default(request)
        except Exception, _details:
            info_string = _utils.formattedException(details=_details)
    else:
        tracer.append('VyperDjango GUI goes here...')
        if (_utils.isBeingDebugged or django_utils.isBeingDebugged):
            fIO = _utils.stringIO()
            try:
                lists.prettyPrint(request.environ,title='request.environ',fOut=fIO)
            except:
                pass
            try:
                lists.prettyPrint(request.META,title='request.META',fOut=fIO)
            except:
                pass
            try:
                lists.prettyPrint(request.GET,title='request.GET',fOut=fIO)
            except:
                pass
            try:
                lists.prettyPrint(request.POST,title='request.POST',fOut=fIO)
            except:
                pass
            tracer.append('<br/>'.join(fIO.getvalue().split('\n')))
        
    return handle_404(request,context={'DEBUG_INFO':'%s<br/>%s' % ('<br/>'.join([str(item) for item in tracer]),info_string)})

def handle_404(request,context={}):
    s = pages.render_the_template(request,_title,'404_content.html',context=context,template_folder='').content.replace('&lt;br/&gt;','<br/>')
    return HttpResponseNotFound(s)

