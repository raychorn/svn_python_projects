from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

import os, sys

from django.contrib.auth import get_user

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

import mimetypes
from mimetypes import guess_type

__mimetype = mimetypes.guess_type('.html')[0]
__jsonMimetype = 'application/json'
__xmlMimetype = mimetypes.guess_type('.xml')[0]
__textMimetype = 'text/plain'

_root_ = os.path.dirname(__file__)

from users.g import dict_to_json

import models

__error_symbol = 'ERROR'

def rest_handle_get_applications(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    applications = models.DjangoApplication.objects.filter(user=_user)
    applications = [] if (applications.count() == 0) else applications
    d = dict([('name',app.name) for app in applications])
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_add_application(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    from vyperlogix.win import hosts
    from vyperlogix.sockets import whois
    
    _user = get_user(request)
    name = django_utils.get_from_post(request,'name',default=None)
    servername = django_utils.get_from_post(request,'servername',default=None)
    # is the servername a domain name with more than 1 token split on '.' ?
    toks = [t for t in str(servername).split('.') if (len(t) > 0)]
    __is_domain_valid__ = None
    if (len(toks) > 1):
        __is_domain_valid__ = whois.whois_lookup_validated(servername)
    else:
        # should the domain name be maintained in the GUI as domain.vyperlogix.com OR just domain ?
        h = hosts.WindowsHosts()
        __is_domain_valid__ = h.has_domain(regex=servername)
        if (not __is_domain_valid__):
            h.add_domain_and_save(servername)
            __is_domain_valid__ = h.has_domain(regex=servername)
    # if not a real domain name then allocate it in hosts file...
    applications = models.DjangoApplication.objects.filter(user=_user).filter(name=name)
    applications = [] if (applications.count() == 0) else applications
    d = {}
    server = None
    if (len(applications) == 0):
        if (__is_domain_valid__):
            servers = models.DjangoServer.objects.filter(user=_user).filter(servername=servername)
            if (len(servers) == 0):
                server = models.DjangoServer(user=_user,servername=servername)
                server.save()
                servers = models.DjangoServer.objects.filter(user=_user).filter(servername=servername)
                server = servers[0]
        if (server):
            app = models.DjangoApplication(user=_user,name=name,server=server)
            app.save()
        applications = models.DjangoApplication.objects.filter(user=_user)
        applications = [] if (applications.count() == 0) else applications
        d = dict([('name',app.name) for app in applications])
    d['is_domain_valid'] = __is_domain_valid__
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)

def rest_handle_remove_application(request,parms,browserAnalysis,__air_id__,__apiMap__,data={}):
    _user = get_user(request)
    name = django_utils.get_from_post(request,'name',default=None)
    applications = models.DjangoApplication.objects.filter(user=_user).filter(name=name)
    for app in applications:
        app.delete()
    d = {}
    applications = models.DjangoApplication.objects.filter(user=_user)
    applications = [] if (applications.count() == 0) else applications
    d = dict([('name',app.name) for app in applications])
    json = dict_to_json(d)
    return HttpResponse(content=json,mimetype=__jsonMimetype)


