from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from vyperlogix.misc import _utils

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def default(request):
    now = _utils.timeStamp(format=formatTimeStr())
    _title = 'Automate & Secure your Python Eggs'
    t = get_template('pyeggs-home.html')
    html = t.render(Context({'current_date': now, 'the_title': _title}))
    return HttpResponse(html)

def about(request):
    _yyyy = _utils.timeStamp(format=formatYYYYStr())
    t = get_template('pyeggs-about.html')
    html = t.render(Context({'current_year': _yyyy}))
    return HttpResponse(html)

