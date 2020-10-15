from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName

_exceptions = ['hOrientation','vOrientation']

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

def xml_to_json(xml,callback=None,callback_preprocess=None,callback_before_json=None):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    po.proxy.callback = callback
    po.proxy.callback_preprocess = callback_preprocess
    po.proxy.callback_before_json = callback_before_json
    json = po.process(xml)
    
    return json

fname = r"Z:\python projects\_django-projects\@projects\verizonwireless\extras\global_nav_props\globalnav.properties.props"
props = dict([tuple([t.strip() for t in l.split('=')]) for l in _utils.readFileFrom(fname).split('\n') if (len(l) > 0) and (not l.startswith('#'))])

props = lists.HashedLists2(props)
_props = props.insideOut()

_metadata = lists.HashedLists2()

compressed_metadata = lists.HashedLists2()
_compressed_metadata = {}

_datafield = ''
datafield_compression = lists.HashedLists2()
_datafield_compression = {}

def compress_symbol(symbol,callback=lambda s:False):
    i = 0
    ck = symbol[i]
    while (i <= len(symbol)-1) and (callback(ck)):
        if (callback(ck)):
            i += 1
            ck = symbol[i]
    return ck

def handle_data(data):
    global _isCompressed, _compressed_metadata
    from vyperlogix.xml import XML2JSon
    data = data if (not misc.isList(data)) else data[-1]
    if (data.has_key('label')) and (data.has_key('url')):
        if (_isCompressing) and (not _isCompressed):
            for k,v in _metadata.iteritems():
                if (k not in _exceptions):
                    func = lambda ck:compressed_metadata.has_key(ck) or (_datafield_compression.has_key(ck))
                    ck = compress_symbol(v,callback=func)
                    compressed_metadata[ck] = v
            _isCompressed = True
            _compressed_metadata = compressed_metadata.insideOut()
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
        data['domain_key'] = domain
        data['domain'] = _domain
        del data['url'][-1]
        toks[i+1] = ''
        data['url'] = '/'.join(toks[i+1:])
        if (_isCompressing) and (len(_compressed_metadata) > 0):
            for k,v in data.iteritems():
                if (_compressed_metadata.has_key(k)):
                    del data[k]
                    data[_compressed_metadata[k]] = misc._unpack_(v)
                elif (datafield_compression.has_key(k)):
                    del data[k]
                    data[datafield_compression[k]] = misc._unpack_(v)
                else:
                    print '(???) ==> (%s)' % (k)
            pass
    else:
        if (_isCompressing):
            for k,v in data.iteritems():
                _metadata[k] = misc._unpack_(v)
    pass

def handle_metadata_compression(d):
    menu = misc._unpack_(d['menu'])
    metafield = misc._unpack_(menu['metafield'])
    datafield = misc._unpack_(menu['datafield'])
    meta = misc._unpack_(menu[metafield])
    data = misc._unpack_(menu[datafield])
    if (data == None) and (menu.has_key('menuitem')):
        data = misc._unpack_(menu['menuitem'])
        del menu['menuitem']
        menu[datafield] = data
    for aMeta in meta:
        for k,v in aMeta.iteritems():
            if (k not in _exceptions):
                replacement = _compressed_metadata[misc._unpack_(v)]
                if (replacement):
                    del aMeta[k]
                    aMeta[k] = replacement

def handle_top_node(top_node):
    global _datafield, _datafield_compression
    try:
        _datafield = [k for k in top_node.attributes.keys() if (k == 'datafield')][0]
    except:
        _datafield = ''
    x = top_node.attributes[_datafield]
    c_datafield = compress_symbol(x.value)
    datafield_compression[x.value] = c_datafield
    x.value = c_datafield
    _datafield_compression = datafield_compression.insideOut()
    pass

if (__name__ == '__main__'):
    import os, sys
    import urllib
    from vyperlogix.misc import _utils
    
    _isCompressing = False
    _isCompressed = False

    fname = r"Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\after-oct-release\LoggedOutState.xml"
    xml = _utils.readFileFrom(fname)
    xml = xml.replace('&',urllib.quote_plus('&'))
    print 'Reading "%s".' % (fname)
    json = xml_to_json(xml,callback=handle_data)
    toks = list(os.path.splitext(fname))
    toks[-1] = '.json'
    fname2 = ''.join(toks)
    print 'Writing "%s".' % (fname2)
    _utils.writeFileFrom(fname2,json)

    _isCompressing = True

    json = xml_to_json(xml,callback=handle_data,callback_preprocess=handle_top_node,callback_before_json=handle_metadata_compression)
    toks = list(os.path.splitext(fname))
    toks[-1] = '-compressed.json'
    fname2 = ''.join(toks)
    print 'Writing "%s".' % (fname2)
    _utils.writeFileFrom(fname2,json)
    
    print 'DONE !'
    pass
