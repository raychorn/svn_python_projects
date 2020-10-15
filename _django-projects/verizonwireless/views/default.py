from django import http
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseRedirect
from django.conf import settings

from django.core import serializers

import os, sys

from vyperlogix.django import django_utils

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.js import minify

from vyperlogix.django import pages
from vyperlogix.html import myOOHTML as oohtml

from vyperlogix.django import django_utils

from vyperlogix.products import keys

from vyperlogix.crypto import md5
from vyperlogix.misc import GenPasswd

from models import Json,Environments,Protocols

from uuid import uuid4

from vyperlogix.enum.Enum import Enum

import urllib

_root_ = os.path.dirname(__file__)

import random
random.seed()

class MenuStates(Enum):
    logged_in = 'logged-in'
    logged_out = 'logged-out'
    loggedin = 'logged-in'
    loggedout = 'logged-out'
    
is_menu_state_logged_in = lambda e:e.value == MenuStates.logged_in.value
is_menu_state_logged_out = lambda e:e.value == MenuStates.logged_out.value

def getMenu1XML(num,isRecursive=1):
    xml = ''
    for i in xrange(0,num+1):
        ch = chr(ord('A') + i)
        choice = random.randrange(0,5)
        choice_submenu = random.randrange(0,5)
        is_using_submenu = (choice_submenu == 3) and (isRecursive < 2)
        if (choice == 3):
            xml += '<menuitem type="separator" />'
        else:
            if (is_using_submenu):
                _xml = ''
                _xml += '<menuitem label="Menu%s">' % (isRecursive)
                _xml += getMenu1XML(choice_submenu,isRecursive+1)
                _xml += '</menuitem>'
                xml += _xml
            else:
                xml += '<menuitem label="MenuItem %s-%s" data="%s%s"/>' % (isRecursive,ch,isRecursive,ch)
    return xml

def getMenuXML(context, filename='menuItems.xml'):
    fname = os.sep.join([settings.MEDIA_ROOT,os.sep.join(['xml',filename])])
    xml = _utils.readFileFrom(fname)
    xml = django_utils.render_from_string(xml,context=Context(context))
    return xml

def getMenuXML_from(fname):
    xml = ''
    if (os.path.exists(fname)):
        xml = _utils.readFileFrom(fname)
    return xml

def getData_from(fname):
    data = ''
    if (os.path.exists(fname)):
        data = _utils.readFileFrom(fname)
    return data

def xml_to_json(xml):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(xml)
    
    return json

def xml_to_python(xml):
    from vyperlogix.xml import XML2JSon
    
    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    obj = po._process(xml)
    
    return obj

def python_to_json(obj):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(obj)
    
    return json

def python_to_xml(obj):
    from vyperlogix.xml.serializer import XMLMarshal
    
    stream = _utils.stringIO()
    
    XMLMarshal.dumps(stream,obj)

    return stream.getvalue()

def dict_to_json(dct):
    json = ''
    try:
        import simplejson
        json = simplejson.dumps(dct,separators=(',\n', ':\n'))
    except:
        pass
    return json

def getMenuXMLLoggedIn():
    return getMenuXML_from(r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\after-oct-release\LoggedInState.xml')

def getMenuXMLLoggedOut():
    return getMenuXML_from(r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\after-oct-release\LoggedOutState.xml')

def getNewMenuXML():
    return getMenuXML({'head_tag':'menu', 'metadata_tag':'meta', 'data_tag':'menuitem', 'id':'id', 'label':'label', 'url':'url', 'type':'type', 'domain':'domain', 'body':'body', 'target':'target', 'hOrientation':'-2', 'vOrientation':'top'},'menuItems0.xml')

def default(request):
    url_toks = django_utils.parse_url_parms(request)
    params = _utils.get_dict_as_pairs(url_toks)

    if (url_toks == [u'rest', u'getMenuXML']):
        return HttpResponse(content=getMenuXML('menu','menuitem','meta','label','url','type','data','group'),mimetype='text/xml')
    elif (url_toks == [u'rest', u'getMenuXML2']):
        return HttpResponse(content=getMenuXML('data','data','data','label','url','type','data','group'),mimetype='text/xml')
    elif (url_toks == [u'rest', u'getMenuXML3']):
        return HttpResponse(content=getMenuXML('a','b','c','l','u','t','d','g'),mimetype='text/xml')
    elif (url_toks == [u'rest', u'getMenuXML3', 'xml']):
        return HttpResponse(content=getMenuXML('a','b','c','l','u','t','d','g'),mimetype='application/xml')
    elif (url_toks == [u'rest', u'getMenuXML3', 'json']):
        return HttpResponse(content=xml_to_json(getMenuXML('a','b','c','l','u','t','d','g')),mimetype='application/json')
    elif (url_toks == [u'rest', u'getMenuXML3', 'json', 'text']):
        return HttpResponse(content=xml_to_json(getMenuXML('a','b','c','l','u','t','d','g')))
    elif (url_toks == [u'rest', u'getMenuXML41']):
        from vyperlogix.zlib import zlibCompressor
        s = getMenuXML('menu','menuitem','meta','label','url','type','data','group')
        z = zlibCompressor.zlib_compress(s)
        return HttpResponse(content=z,mimetype='application/x-gzip')
    elif (url_toks == [u'rest', u'getMenuXML42']):
        from vyperlogix.zlib import zlibCompressor
        s = getMenuXML('a','b','c','l','u','t','d','g')
        z = zlibCompressor.zlib_compress(s)
        return HttpResponse(content=z,mimetype='application/x-gzip')
    elif (url_toks == [u'rest', u'getMenuXML', 'logged-in']):
        return HttpResponse(content=getMenuXMLLoggedIn(),mimetype='text/xml')
    elif (url_toks == [u'rest', u'getMenuXML', 'logged-in', 'json']):
        return HttpResponse(content=xml_to_json(getMenuXMLLoggedIn()),mimetype='application/json')
    elif (url_toks == [u'rest', u'getMenuXML', 'logged-out']):
        return HttpResponse(content=getMenuXMLLoggedOut(),mimetype='text/xml')
    elif (url_toks == [u'rest', u'getMenuXML', 'logged-out', 'json']):
        return HttpResponse(content=xml_to_json(getMenuXMLLoggedOut()),mimetype='application/json')
    elif (url_toks == [u'rest', u'getZLIB']):
        return HttpResponse(content=getData_from(r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\zlib-tester\_x_zlib.hex'),mimetype='text/html') # application/x-gzip
    elif (url_toks[0:3] == [u'rest', u'save', u'file']):
        success = True
        _url = ''
        try:
            from vyperlogix.products import keys
            fname = keys._decode(url_toks[-2].upper())
            _url = 'http://%s%s' % (request.META['HTTP_HOST'],fname)
            contents = keys._decode(url_toks[-1].upper())
            root = settings.MEDIA_ROOT
            root_toks = root.split(os.sep)
            fname_toks0 = fname.split('/')
            fname_toks = [t.strip() for t in fname_toks0 if (len(t.strip()) > 0)]
            i = len(root_toks)
            if (root_toks[-1] == fname_toks[0]):
                i = -1
            fpath = os.sep.join([os.sep.join(root_toks[0:i]),os.sep.join(fname_toks)])
            _utils.writeFileFrom(fpath,contents)
        except:
            success = False
        return HttpResponse(content=dict_to_json({'success':success,'url':_url}),mimetype='application/json')
    elif (url_toks[0:2] == [u'rest', u'global-nav']):
        root = settings.MEDIA_ROOT
        fpath = r'global-nav\stylesheets'
        fpath = os.sep.join([root,fpath,url_toks[-1]])
        if (os.path.exists(fpath)):
            return HttpResponse(content=getData_from(fpath),mimetype='text/html')
        return HttpResponseNotFound(content='Cannot find "%s".' % (fpath))
    elif (url_toks[0:4] == [u'rest', u'get', u'menu', u'count']):
        num = Json.objects.count()
        is_returning_json = (url_toks[-1] == 'json')
        data = {'count':num}
        if (is_returning_json):
            _content = python_to_json(data)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'delete', u'menu']):
        is_returning_json = (url_toks[-1] == 'json')
        uuid = url_toks[-2]
        menus = Json.objects.filter(uuid=uuid).all()
        status = {'success':True}
        if (len(menus) > 0):
            aMenu = menus[0]
            aMenu.delete()
        else:
            status['success'] = False
        if (is_returning_json):
            _content = python_to_json({'success':True})
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:4] == [u'rest', u'get', u'menu', u'environments']):
        is_returning_json = (url_toks[-1] == 'json')
        if (Environments.objects.count() == 0):
            fname = r"Z:\python projects\_django-projects\@projects\verizonwireless\extras\global_nav_props\globalnav.properties.props"
            envs = dict([tuple([t.strip() for t in l.split('=')]) for l in _utils.readFileFrom(fname).split('\n') if (len(l) > 0) and (not l.startswith('#'))])
            for k,v in envs.iteritems():
                env = Environments(name=k,domain=v,uuid=uuid4())
                env.save()
        envs = [{'name':anEnv.name,'domain':anEnv.domain,'uuid':anEnv.uuid} for anEnv in Environments.objects.all()]
        if (is_returning_json):
            _content = python_to_json(envs)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:4] == [u'rest', u'get', u'menu', u'protocols']):
        is_returning_json = (url_toks[-1] == 'json')
        protocols = [{'name':aProto.name,'value':aProto.value,'uuid':aProto.uuid} for aProto in Protocols.objects.all()]
        if (is_returning_json):
            _content = python_to_json(protocols)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:4] == [u'rest', u'get', u'menu', u'state']):
        is_returning_json = (url_toks[-1] == 'json')
        uuid = url_toks[-2]
        menus = Json.objects.filter(uuid=uuid).all()
        status = {'success':True}
        if (len(menus) > 0):
            aMenu = menus[0]
            status['state'] = aMenu.state
        else:
            status = {'success':False}
        if (is_returning_json):
            _content = python_to_json(status)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'get', u'menu']):
        is_returning_json = (url_toks[-1] == 'json')
        uuid = url_toks[-2]
        menus = Json.objects.filter(uuid=uuid).all()
        if (len(menus) > 0):
            aMenu = menus[0]
            _content = aMenu.json if (is_returning_json) else aMenu.xml
            _mimetype = 'application/json' if (is_returning_json) else 'text/xml'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot return the selected Menu at this time.')
    elif (url_toks[0:3] == [u'rest', u'change', u'menu']):
        is_returning_json = (url_toks[-1] == 'json')
        target = url_toks[-2]
        verb = url_toks[-3]
        uuid = url_toks[-4]
        menus = Json.objects.filter(uuid=uuid).all()
        status = {'success':False}
        if (len(menus) > 0):
            aMenu = menus[0]
            aMenu.state = MenuStates.logged_in.value if (MenuStates(target) == MenuStates.logged_in) else MenuStates.logged_out.value
            aMenu.save()
            status = {'success':True}
        if (is_returning_json):
            _content = python_to_json({'success':True})
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'rename', u'menu']):
        is_returning_json = (url_toks[-1] == 'json')
        uuid = url_toks[-2]
        name = url_toks[-3]
        menus = Json.objects.filter(uuid=uuid).all()
        status = {'success':True}
        if (len(menus) > 0):
            aMenu = menus[0]
            old_name = aMenu.name
            aMenu.name = name
            aMenu.save()
            status['uuid'] = uuid
            status['name'] = name
            _menus = Json.objects.filter(uuid=uuid).all()
            if (len(_menus) > 1):
                _menus = _menus.filter(name=old_name).all()
                if (len(_menus) > 0):
                    _aMenu = _menus[0]
                    _aMenu.delete()
        else:
            status = {'success':False}
        if (is_returning_json):
            _content = python_to_json(status)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'get', u'menus']):
        menus = [{'name':aMenu.name,'state':aMenu.state,'uuid':aMenu.uuid} for aMenu in Json.objects.order_by('name').all()]
        names = {}
        for aMenu in menus:
            names[aMenu['name']] = aMenu
        menus = [names[k] for k in misc.sort(names.keys())]
        is_returning_json = (url_toks[-1] == 'json')
        if (is_returning_json):
            _content = python_to_json(menus)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'set', u'menu']):
        is_returning_json = (url_toks[-1] == 'json')
        uuid = url_toks[-2]
        menus = Json.objects.filter(uuid=uuid).all()
        status = {'success':True}
        if (len(menus) > 0):
            aMenu = menus[0]
            aMenu.json = request.POST['data']
            aMenu.save()
        else:
            status = {'success':False}
        if (is_returning_json):
            _content = python_to_json(status)
            _mimetype = 'application/json'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot handle any option other than JSON for output at this time.')
    elif (url_toks[0:3] == [u'rest', u'new', u'menu']):
        _menu_state = MenuStates.logged_out
        if (url_toks[-2] == MenuStates.logged_in.value):
            _menu_state = MenuStates.logged_in
        is_returning_json = (url_toks[-1] == 'json')
        name = url_toks[-3]
        if (len(name) == 0):
            for n in xrange(1,1001):
                menus = Json.objects.filter(name='name%s' % (n)).all()
                if (len(menus) == 0):
                    n += 1
                    break
            name = 'menu%s' % (n)
        if (is_menu_state_logged_in(_menu_state)):
            x = getMenuXMLLoggedIn()
        else:
            x = getMenuXMLLoggedOut()
        x = x.replace('&',urllib.quote_plus('&'))
        d = xml_to_python(x)
        l = d['menu'][0][str(d['menu'][0]['datafield'][0])]
        m = d['menu'][0][str(d['menu'][0]['metafield'][0])]
        mm = lists.HashedLists2()
        for item in m:
            for k,v in item.iteritems():
                mm[k] = misc._unpack_(v)
        lst = []
        for item in l:
            _d_ = lists.HashedLists2()
            _d_[mm['label']] = urllib.unquote_plus(misc._unpack_(item[mm['label']]))
            _d_['uuid'] = str(uuid4())
            lst.append(_d_)
        _xml = getNewMenuXML()
        d_json = xml_to_python(_xml)
        l_json = d_json['menu'][0][str(d_json['menu'][0]['datafield'][0])]
        if (l_json == None):
            d_json['menu'][0][str(d_json['menu'][0]['datafield'][0])] = lst
        _json = python_to_json(d_json)
        if ( (isinstance(_json,str)) or (isinstance(_json,unicode)) ) and (len(_menu_state.value) > 0):
            aMenu = Json(name=name,json=_json,xml=_xml,state=_menu_state.value,uuid=uuid4())
            aMenu.save()
            _content = aMenu.json if (is_returning_json) else aMenu.xml
            _mimetype = 'application/json' if (is_returning_json) else 'text/xml'
            return HttpResponse(content=_content,mimetype=_mimetype)
        return HttpResponseNotFound(content='Cannot make a new Menu due to a system error.')
    
    fname = request.META['PATH_INFO']
    if (request.META['PATH_INFO'] == '/'):
        dname = os.path.join(os.path.dirname(_root_),'static','flex')
        files = [f for f in os.listdir(dname) if (os.path.splitext(f)[-1] == '.html')]
        
        if (len(files) > 0):
            fname = files[0]
    
    return HttpResponseRedirect('/static/flex%s%s'% ('/' if (not fname.startswith('/')) else '',fname))
