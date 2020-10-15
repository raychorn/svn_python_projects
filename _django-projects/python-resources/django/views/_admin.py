from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import sys

from vyperlogix.misc import _utils

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

import urllib

try:
    from settings import _navigation_tabs
except ImportError:
    from resources.settings import _navigation_tabs

try:
    from settings import _navigation_menu_type
except ImportError:
    from resources.settings import _navigation_menu_type
    
try:
    from settings import MEDIA_ROOT
except ImportError:
    from resources.settings import MEDIA_ROOT

try:
    from settings import MEDIA_URL
except ImportError:
    from resources.settings import MEDIA_URL

try:
    from settings import _title
except ImportError:
    from resources.settings import _title

try:
    from settings import conn_str
except ImportError:
    from resources.settings import conn_str

def _admin(request):
    from models import Node

    items = Node.objects.all()
    
    if (len(items) == 0):
        aNode = Node(id='-1', name='Top', parent=-1, creation_date=_utils.today_localtime(),modification_date=_utils.today_localtime(),is_active=True,is_file=False,is_url=False)
        aNode.save()
        i = aNode.id
    
    items = Node.objects.all()

    h = oohtml.Html()
    ul = h.tag(oohtml.oohtml.UL)
    for item in items:
        ul._tagLI(item.name)
    content = h.toHtml()
    
    c = {'ADMIN_CONTENT': content}
    return pages.render_the_page(request,'%s' % (_title),'_admin.html',_navigation_menu_type,_navigation_tabs,context=c)

