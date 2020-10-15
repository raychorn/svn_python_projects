import os, sys

from datetime import datetime
from vyperlogix.misc import _utils

from django.conf import settings

from vyperlogix.django import django_utils

from vyperlogix.misc import LazyImport

from django.db.models import loading

from vyperlogix.hash import lists

from vyperlogix.lists import ListWrapper

from vyperlogix.misc import ReportTheList

from vyperlogix.misc import ObjectTypeName

class VyperDjangoMiddleware(object):
    def __adjust_apps__(self,apps,aSite):
        i_apps = apps
        o_apps = [app for app in i_apps if (not app.startswith('django.'))] # seek to determine which apps are from django and which are not...
        _apps = list(set(i_apps) - set(o_apps))
        o_apps = ['%s.%s' % (aSite.__name__,app.split('.')[-1]) for app in o_apps]
        return tuple(_apps+o_apps)
    
    def process_request(self, request):
        url_toks = django_utils.parse_url_parms(request)
        
        http_host = request.META['HTTP_X_FORWARDED_SERVER'] if (request.META.has_key('HTTP_X_FORWARDED_SERVER')) else request.META['HTTP_HOST']
        _host = http_host.split(':')[0]
    
        s = 'combined%s.settings' % ('.django' if (not django_utils.isProduction(django_utils._cname)) else '')
        m = LazyImport.LazyImport(s)
        m = m.__lazyimport_import
        settings._target = None
        settings.configure(**m.__dict__)
        
        d = lists.HashedLists2(dict([(k,v) for k,v in m.__dict__.iteritems() if (not k.startswith('__')) and (not k.endswith('__')) and (ObjectTypeName.typeClassName(v) != 'module')]))
        if (django_utils.isBeingDebugged) and (sys.platform != 'win32'):
            fout = open('/home/raychorn/debug.txt','w')
            try:
                print >>fout, '_host is "%s".' % (_host)
                print >>fout, '%s\n' % ('='*80)
                d.prettyPrint(title=s,fOut=fout)
            finally:
                fout.flush()
                fout.close()
        
        r_url = settings.ROOT_URLCONF
        
        isAdjustingInstalledApps = False
        if (settings.SITES.has_key(_host)):
            aSite = settings.SITES[_host]
            s = '%s.settings' % (aSite.__name__)
            m = LazyImport.LazyImport(s)
            m = m.__lazyimport_import
            
            d = dict([(k,v) for k,v in m.__dict__.iteritems() if (not k.startswith('__')) and (not k.endswith('__')) and (ObjectTypeName.typeClassName(v) != 'module')])
            if (d.has_key('INSTALLED_APPS')):
                d['INSTALLED_APPS'] = self.__adjust_apps__(d['INSTALLED_APPS'],aSite)
                m.__dict__['INSTALLED_APPS'] = d['INSTALLED_APPS']
            request.session['settings'] = d

            settings._target = None
            settings.configure(**m.__dict__)
            
            d = lists.HashedLists2(dict([(k,v) for k,v in m.__dict__.iteritems() if (not k.startswith('__')) and (not k.endswith('__')) and (ObjectTypeName.typeClassName(v) != 'module')]))
            
            _path = aSite.__path__[0]
            
            x = ListWrapper.ListWrapper(sys.path)
            xi = x.findAllMatching(_path)
            if (len(xi) == 0):
                sys.path.insert(0,_path)

            isAdjustingInstalledApps = True
            settings.ROOT_URLCONF = '%s.%s' % (aSite.__name__,settings.ROOT_URLCONF.split('.')[-1])
        else:
            settings.ROOT_URLCONF = s.replace('.settings','.urls')
                
        _app_loader_errors = []
        if (settings.INSTALLED_APPS):
            loading._loaded = False
            loading._app_list = []
            loading._app_models = {}
            for app in settings.INSTALLED_APPS:
                try:
                    aModule = loading.load_app(app)
                    app_name = app.split('.')[-1]
                    if (aModule is not None) and (not loading._app_models.has_key(app_name)):
                        reload(aModule)
                except ImportError, e:
                    if (str(e).find('No module named') == -1):
                        _app_loader_errors.append(_utils.formattedException(details=e))
            loading._loaded = True

        if (sys.platform != 'win32'):
            fname = '/home/raychorn/debug/%s/debug-apps.txt' % ('_'.join(_utils.timeStampForFileName().split('_')[0:-1]))
            _utils._makeDirs(os.path.dirname(fname))
            fout = open(fname,'a')
            try:
                ts = ' '.join(_utils.timeStampLocalTime().split('T'))
                print >>fout, 'BEGIN: %s :: %s' % (ts,'='*80)
                print >>fout, '_host is "%s".' % (_host)
                print >>fout, '%s\n' % ('-'*80)
                del d['SECRET_KEY']
                del d['DATABASE_PASSWORD']
                d.prettyPrint(title=s,fOut=fout)
                if (len(_app_loader_errors) > 0):
                    ReportTheList.reportTheList(_app_loader_errors,'App Loader Errors',fOut=fout)
                print >>fout, 'END!   %s :: %s\n\n' % (ts,'='*80)
            finally:
                fout.flush()
                fout.close()
            
    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return None