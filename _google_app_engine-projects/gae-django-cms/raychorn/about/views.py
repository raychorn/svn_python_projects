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

from google.appengine.api import memcache

from django.conf import settings

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.django import django_utils

from vyperlogix.classes.SmartObject import SmartObject

import logging

import mimetypes

__mimetype = mimetypes.guess_type('.html')[0]

__num_images = 33
__image_Pattern = '%sof%s.png'
__image_URI = '/static/images/about/'
__image_descr_Pattern = '%s of %s'

__27_of_33 = '''
'''

__32_of_33 = '''
'''

__image_descr = {'27 of 33':__27_of_33,'32 of 33':__32_of_33}

def populate_images():
    __images = []
    aMemKey = "AboutVyperBlog_populate_images11"
    aMemToken = memcache.get(aMemKey)
    if aMemToken is not None:
        __images = aMemToken
    else:
        for n in xrange(1,__num_images+1):
            descr = __image_descr_Pattern%(n,__num_images)
            notes = __image_descr[descr] if (__image_descr.has_key(descr)) else ''
            notes = notes.strip()
            __images.append({'image':''.join([__image_URI,__image_Pattern%(n,__num_images)]),'num':n,'descr':descr,'notes':notes,'showPayPal':__image_descr.has_key(descr)})
        try:
            aMemToken = __images
            memcache.add(aMemKey, aMemToken, 60*60*24)
        except Exception, e:
            info_string = _utils.formattedException(details=e)
            logging.error('%s.save.ERROR --> %s' % (aMemKey,info_string))
    return __images

def default(request):
    parms = django_utils.parse_url_parms(request)
    url = '/%s' % (str('/'.join(parms)))
    
    pages = lambda i,maxI:[SmartObject(dict([('num',n),('isCurrent',n==i),('displayable',n+1)])) for n in xrange(min(i-5,maxI-10),max(i+10,maxI)) if (n > 0) and (n <= maxI)][0:10]
    
    isAboutPage = (url == '/about')
    
    qryObj = django_utils.queryObject(request)
    browserAnalysis = django_utils.get_browser_analysis(request,parms,any([isAboutPage]))
    try:
        s_response = ''
        __error__ = ''

        if (isAboutPage):
            iPage = django_utils._int(qryObj.num)
            iPage = iPage if (iPage) else 0
            images = populate_images()
            max_imageNum = len(images)-1
            pageNums = pages(iPage,max_imageNum)
            response = render_to_response(request, 'about.html', data={'HTTP_USER_AGENT':request.META['HTTP_USER_AGENT'],'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal,'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'anImage':images[iPage],'firstPage':0,'lastPage':max_imageNum,'iPage':iPage+1,'numPages':len(images),'prevPageNum':iPage-1,'nextPageNum':iPage+1,'isFirstPage':(iPage == 0),'notFirstPage':(iPage > 0),'isLastPage':(iPage == max_imageNum),'notLastPage':(iPage < max_imageNum),'pageNums':pageNums,'url':'%s/'%(url)})
            django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
            return response
        return HttpResponseRedirect('/')
        
    except Exception, e:
        info_string = _utils.formattedException(details=e)
        logging.warning(info_string)
        _content = '<font color="red"><small>%s</small></font>'%('<br/>'.join(info_string.split('\n')))
        response = render_to_response(request, 'main.html', data={'HTTP_USER_AGENT':request.META['HTTP_USER_AGENT'],'browserName':browserAnalysis.browserName,'browserVersion':browserAnalysis.browserVersion,'isRunningLocal':browserAnalysis.isRunningLocal,'isJavaScriptOptimized':browserAnalysis.isJavaScriptOptimized,'isUsingUnsupportedBrowser':browserAnalysis.isUsingUnsupportedBrowser,'isUsingMSIE':browserAnalysis.isUsingMSIE,'isBrowserWebKit':browserAnalysis.isBrowserWebKit,'isUsingAndroid':browserAnalysis.isUsingAndroid,'qryObj':qryObj,'content':_content})
        django_utils.give_response_session_id_using(request,response,settings.APP_SESSION_KEY);
        return response
