from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from vyperlogix.misc import _utils

import urllib

_title = 'Take Control of your PDF Bank Statements'

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def default(request):
    now = _utils.timeStamp(format=formatTimeStr())
    t = get_template('home.html')
    html = t.render(Context({'current_date': now, 'the_title': _title}))
    return HttpResponse(html)

def about(request):
    _yyyy = _utils.timeStamp(format=formatYYYYStr())
    t = get_template('about.html')
    html = t.render(Context({'current_year': _yyyy}))
    return HttpResponse(html)

def tabs(request):
    now = _utils.timeStamp(format=formatTimeStr())
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    t = get_template('tabs.html')
    if (len(toks) == 1):
        html = t.render(Context({'current_date': now, 'the_title': _title, 'id':0}))
    else:
        id = toks[-1] if (len(toks) == 2) else toks[1]
        id = int(id) if (str(id).isdigit()) else 0
        html = t.render(Context({'current_date': now, 'the_title': _title, 'id':id}))
    return HttpResponse(html)

