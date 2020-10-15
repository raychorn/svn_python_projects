__license__ = "Python"
__copyright__ = "Copyright (C) 2007, Stephen Zabel, Jay Parlar"
__author__ = "Stephen Zabel - sjzabel@gmail.com"
__contributors__ = "Jay Parlar - parlar@gmail.com"

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, get_host

SSL = 'SSL'

def is_secure(request):
    if (request.META.has_key('HTTP_X_FORWARDED_SSL')):
        return (request.META['HTTP_X_FORWARDED_SSL'] == 'on')
    elif (request.META.has_key('SERVER_PORT')):
        return request.META['SERVER_PORT'] == 443
    return False

class SSLRedirect:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False

        if not secure == is_secure(request):
            return self._redirect(request, secure)

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"
        newurl = "%s://%s%s" % (protocol,get_host(request),request.get_full_path())
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError, \
"""Django can't perform a SSL redirect while maintaining POST data.
Please structure your views so that redirects only occur during GETs."""

        return HttpResponsePermanentRedirect(newurl)