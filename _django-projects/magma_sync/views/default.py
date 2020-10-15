from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from vyperlogix.misc import _utils

import os, sys

from vyperlogix.django import django_utils

_title = 'MagmaSync'

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

now = _utils.getAsDateTimeStr(_utils.today_localtime(),fmt=formatTimeStr())

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)
    fOut = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'%s_logger.txt' % (_title)),'a')
    print >>fOut, '%s :: %s' % (now,url_toks)
    fOut.flush()
    fOut.close()
    t = get_template('home.html')
    html = t.render(Context({'current_date': now, 'the_title': _title}))
    return HttpResponse(html)

def handle_404(request):
    return HttpResponseNotFound('<h1>404</h1>')

