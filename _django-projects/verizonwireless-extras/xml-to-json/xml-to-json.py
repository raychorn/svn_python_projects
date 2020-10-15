from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.hash import lists

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

def xml_to_json(xml,callback=None):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    po.proxy.callback = callback
    json = po.process(xml)
    
    return json

fname = r"Z:\python projects\_django-projects\@projects\verizonwireless\extras\global_nav_props\globalnav.properties.props"
props = dict([tuple([t.strip() for t in l.split('=')]) for l in _utils.readFileFrom(fname).split('\n') if (len(l) > 0) and (not l.startswith('#'))])

props = lists.HashedFuzzyLists2(props)
_props = props.insideOut()

def handle_data(data):
    from vyperlogix.xml import XML2JSon
    data = data if (not misc.isList(data)) else data[-1]
    if (data.has_key('label')) and (data.has_key('url')):
        url = urllib.unquote_plus(misc._unpack_(data['url'])).replace('&amp;','&')
        del data['url']
        data['url'] = url
        toks = ListWrapper(misc._unpack_(data['url']).split('?')[0].split('/'))
        i = toks.findFirstMatching('')
        domain = toks[i+1] if (i > -1) else ''
        _domain = domain
        domain = _props[_domain]
        if (domain == None) or (len(domain) == 0):
            domain = props[_domain]
            if (domain == None) or (len(domain) == 0):
                new_domain = str(_domain)
                new_name = new_domain.split('.')[0].lower()
                props[new_name] = new_domain
                _props[new_domain] = new_name
                domain = _props[_domain]
        data['domain'] = domain
        del data['url'][-1]
        toks[i+1] = ''
        data['url'] = '/'.join(toks[i+1:])
        pass
    pass

if (__name__ == '__main__'):
    import os, sys
    import urllib
    from vyperlogix.misc import _utils

    fname = r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\after-oct-release\LoggedOutState.xml'
    #fname = r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\after-oct-release\LoggedInState.xml'
    xml = _utils.readFileFrom(fname)
    xml = xml.replace('&',urllib.quote_plus('&'))
    print 'Reading "%s".' % (fname)
    json = xml_to_json(xml,callback=handle_data)
    toks = list(os.path.splitext(fname))
    toks[-1] = '.json'
    fname2 = ''.join(toks)
    print 'Writing "%s".' % (fname2)
    _utils.writeFileFrom(fname2,json)
    print 'DONE !'
    pass
