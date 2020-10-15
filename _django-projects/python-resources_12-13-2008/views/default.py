from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from vyperlogix.misc import _utils

from vyperlogix.misc import _utils

import urllib

_title = 'Your Python Resource'

def formatTimeStr():
    return '%m/%d/%Y %H:%M:%S'

def formatYYYYStr():
    return '%Y'

def default(request):
    from vyperlogix.html.flexigrid import script
    now = _utils.timeStamp(format=formatTimeStr())
    t = get_template('home.html')
    colModel = '''
{display: 'ISO', name : 'iso', width : 40, sortable : true, align: 'left'},
{display: 'Name', name : 'name', width : 180, sortable : true, align: 'left'},
{display: 'Printable Name', name : 'printable_name', width : 120, sortable : true, align: 'left'},
{display: 'ISO3', name : 'iso3', width : 130, sortable : true, align: 'left', hide: true},
{display: 'Numcode', name : 'numcode', width : 120, sortable : true, align: 'left'},
    '''
    searchitems = '''
{display: 'Name', name : 'name'},
{display: 'ISO', name : 'iso'}
    '''
    head = script.head('http://media.vyperlogix.com/flexigrid')
    js = script.script('flex1','http://%s/grid/' % (request.environ['HTTP_HOST']),'Countries',colModel,searchitems,'name','asc')
    html = t.render(Context({'current_date': now, 'the_title': _title, 'content': js, 'head': head}))
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

def crossdomain(request):
    t = get_template('crossdomain.xml')
    html = t.render(Context({}))
    return HttpResponse(html)
