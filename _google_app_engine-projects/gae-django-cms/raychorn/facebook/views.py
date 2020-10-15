# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from google.appengine.ext import db
from mimetypes import guess_type
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

from facebook.models import FacebookUser

from django.conf import settings

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

import mimetypes

__mimetype = mimetypes.guess_type('.html')[0]

def default(request):
    parms = django_utils.parse_url_parms(request)
    url = '/%s' % (str('/'.join(parms)))

    isFaceBookPage = (url == '/facebook')

    qryObj = django_utils.queryObject(request)
    browserAnalysis = django_utils.get_browser_analysis(request,parms,any([isFaceBookPage]))

    try:
        s_response = ''
        __error__ = ''

        if (request.session.has_key('facebookUser_id')):
            _uid_ = request.session['facebookUser_id']
            users = [aUser for aUser in FacebookUser.all() if (aUser.id == _uid_)]
            if (len(users) > 0):
                if (isFaceBookPage):
                    response = render_to_response(request, 'facebook.html')
                    django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
                    return response
        return HttpResponseRedirect('/')
        
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n')))
        response = render_to_response(request, 'facebook.html', data={'HTTP_USER_AGENT':request.META['HTTP_USER_AGENT'],'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal,'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response
