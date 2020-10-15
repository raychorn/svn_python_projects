from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

from django.shortcuts import render_to_response

from g import __context__

import re
import json

from vyperlogix import misc

from django.contrib.auth.models import AnonymousUser

from models import JsonData

get_user = lambda r:r.session.get('__user__', AnonymousUser) if (r and misc.isDict(r.session)) else AnonymousUser

def default(request):
    context = __context__(request)
    current_user = get_user(request)
    context['IS_NOT_LOGGED_IN'] = current_user is AnonymousUser
    return render_to_response('main.html', context, content_type="text/html")

def data(request):
    context = __context__(request)
    current_user = get_user(request)
    context['IS_NOT_LOGGED_IN'] = current_user is AnonymousUser
    context['current_user'] = current_user
    items = JsonData.objects.order_by('statename').all()
    has_database = len(items) > 0
    context['action'] = '/createdata/' if (not has_database) else ''
    context['HAS_DATABASE'] = has_database
    context['debug'] = 'has_database=%s' % (has_database)
    context['items'] = items
    context['HAS_ITEM'] = False
    return render_to_response('data.html', context, content_type="text/html")

def not_yet_implemented(request):
    return render_to_response('not-yet-implemented.html', __context__(request), content_type="text/html")

def acceptable_use_policy(request):
    return render_to_response('acceptable-use-policy.html', __context__(request), content_type="text/html")

def contact(request):
    return render_to_response('contact.html', __context__(request), content_type="text/html")

def terms(request):
    return render_to_response('terms-of-use.html', __context__(request), content_type="text/html")

def create_data(request):
    from g import states, fetch_data_for
    items = JsonData.objects.all()
    for item in items:
        item.delete()
    for statename in states:
        __json__ = fetch_data_for(statename)
        item = JsonData()
        item.statename = statename
        if (misc.isString(__json__)):
            item.data = json.dumps(json.loads(__json__),indent=4)
        else:
            item.data = json.dumps(__json__,indent=4)
        item.save()
    return HttpResponseRedirect('/data/')

def fetch_data(request,statename):
    context = __context__(request)
    current_user = get_user(request)
    context['IS_NOT_LOGGED_IN'] = current_user is AnonymousUser
    context['current_user'] = current_user
    items = JsonData.objects.all()
    has_database = len(items) > 0
    context['action'] = '/createdata/' if (not has_database) else ''
    context['HAS_DATABASE'] = has_database
    context['debug'] = 'statename=%s' % (statename)
    context['items'] = None
    found_item = False
    for item in items:
        if (item.statename == statename):
            found_item = True
            item = json.dumps(json.loads(item.data),indent=4)
            #item = item.data
            break
    if (not found_item):
        item = None
    context['item'] = item
    context['HAS_ITEM'] = found_item
    return render_to_response('data.html', context, content_type="text/html")

def unittests(request):
    context = __context__(request)
    current_user = get_user(request)
    context['IS_NOT_LOGGED_IN'] = current_user is AnonymousUser
    return render_to_response('unittests.html', __context__(request), content_type="text/html")
