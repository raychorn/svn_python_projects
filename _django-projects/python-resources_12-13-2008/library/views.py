from models import Library
from models import Country
from django.http import HttpResponse
from django.template import Context, loader
from django.http import Http404

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix import oodb

import sys
import traceback
import urllib
import uuid

_title = 'Vyper Logix Catalog&trade;'

def index(request):
    '''
    '''
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    tplate = loader.get_template('catalog.html')
    if (len(toks) == 1):
        html = tplate.render(Context({'title': _title}))
    elif (toks[-1] == 'left'):
        tplate = loader.get_template('catalogNodes.js')
        node_js = tplate.render(Context({'ICONPATH': "ICONPATH = 'http://media.vyperlogix.com/treemenu/'"}))

        tplate = loader.get_template('catalogLeftFrame.html')
        html = tplate.render(Context({'title': _title, 'nodes':'<script>\n%s\n</script>' % (node_js)}))
    elif (toks[-1] == 'right'):
        tplate = loader.get_template('catalogRightFrame.html')
        html = tplate.render(Context({'title': _title}))
    elif (toks[-1] == 'js'):
        tplate = loader.get_template('catalogNodes.js')
        html = tplate.render(Context({'title': _title}))
    else:
        tplate = loader.get_template('error.html')
        html = tplate.render(Context({'error': 'Unknown template request.'}))
    return HttpResponse(html)

def _catalog(request):
    '''
    '''
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    tplate = loader.get_template('catalogFrameless.html')

    _tplate = loader.get_template('catalogFramelessNodes.js')
    node_js = _tplate.render(Context({'ICONPATH': "ICONPATH = 'http://media.vyperlogix.com/treemenu/'"}))

    html = tplate.render(Context({'title': _title, 'pic':'%s' % (toks[-1].split('=')[-1] if len(toks) == 2 else ''), 'nodes':'<script>\n%s\n</script>' % (node_js)}))
    return HttpResponse(html)

def catalog(request):
    '''
    '''
    toks = [urllib.unquote_plus(t) for t in request.path.split('/') if (len(t) > 0)]
    tplate = loader.get_template('catalogHome.html')

    html = tplate.render(Context({'title': _title, 'nodes':'', 'content':''}))
    return HttpResponse(html)

def grid(request):
    from vyperlogix.html.flexigrid.grid_handler import grid_handler
    return HttpResponse(grid_handler(request,Country,lambda r:[r.iso, r.name, r.printable_name, r.iso3, r.numcode]))
