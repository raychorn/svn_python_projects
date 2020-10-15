import sys
import math

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.lists.ListWrapper import ListWrapper
from vyperlogix.hash import lists
from vyperlogix.misc.ReportTheList import reportTheList

import uuid

from global_nav_props.props_parser import parse_props_file

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

def xml_to_json(xml,callback=None,callbackB4=None,callbackNodeName=None):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    po.proxy.callback = callback
    po.proxy.callbackB4 = callbackB4
    po.proxy.callbackNodeName = callbackNodeName
    json = po.process(xml)
    
    return json

fname = r"C:\Documents and Settings\c0horra\My Documents\@myFiles\python-projects\verizonwireless\extras\global_nav_props\globalnav.properties.props"
props = dict([tuple([t.strip() for t in l.split('=')]) for l in _utils.readFileFrom(fname).split('\n') if (len(l) > 0) and (not l.startswith('#'))])

#myProps = parse_props_file(fname)

props = lists.HashedFuzzyLists2(props)
_props = props.insideOut()

_exceptions = ['hOrientation','vOrientation']
node_name_exceptions = ['gLinks','lob','logo','search','cart','location','locationName','coverage','localeCoverage','welcome','home','logout']

meta = lists.HashedLists2()
_meta = meta.insideOut()

c_meta = lists.HashedLists2()

d_meta = lists.HashedLists2()
d_meta['id'] = "i"
d_meta['label'] = "l"
d_meta['url'] = "u"
d_meta['type'] = "t"
d_meta['domain'] = "d"
d_meta['domain_key'] = "k"
d_meta['body'] = "b"
d_meta['target'] = "w"
d_meta['secure'] = "s"
d_meta['title'] = "e"
d_meta['uuid'] = "x"
d_meta['roles'] = "r"
d_meta['onebill'] = "o"
d_meta['alltel'] = "a"
d_meta['alltelurl'] = "c"
d_meta['hbxlink'] = "h"

_secureDefault_choices = ['0','1']
_targetDefault_choices = ['_blank','_top']

_d_meta = d_meta.insideOut()

secure_census = lists.HashedLists()
target_census = lists.HashedLists()

for k,v in _d_meta.iteritems():
    assert len(v) if (misc.isList(v)) else len([v]) == 1, 'Oops, there is something dreadfully wrong with your d_meta definitions where (%s) is concerned.' % (k)

compression_analysis = lists.HashedLists2()

_choose_ = lambda foo,bar:foo if (foo != None) else bar

def dec_to_hex(dec):
    import math
    from vyperlogix import oodb

    strip = lambda x:x[-1] if (len(x) == 2) and (x[0] == '0') else x
    
    v_dec = dec
    digits = []
    n = int(math.ceil(math.log(dec,16)))-1 if (dec > 0) else 0
    for i in xrange(n,-1,-1):
        if (i > 0):
            p = 16**i
            v = int(dec / p)
        else:
            p = 0
            v = dec
        h = oodb.dec2hex(v)
        h = strip(h)
        digits.append(h)
        dec -= p*v
    s = ''.join(digits)
    _dec = oodb.hex2dec(s)
    assert v_dec == _dec, 'Oops. something went wrong with ' + misc.funcName() + '().'
    return s

_uuids = lists.HashedLists()

d_uuids = lists.HashedLists2()

def uuid_flattener(_uuid):
    from vyperlogix import oodb
    
    x = _utils.alpha_numeric_only(_uuid)
    k = 0
    toks = []
    toks2 = []
    z = [i for i in xrange(0,len(x)+1,4)]
    zz = z[1:]
    xx = 0
    for j in zz:
        tok = x[k:j]
        toks.append(tok)
        _dec = oodb.hex2dec(tok)
        toks2.append(_dec)
        k = j
        xx += _dec
    aUUID = dec_to_hex(xx)
    aVector = _uuids[aUUID]
    if (aVector != None):
        if (len(aVector) > 10):
            print 'Blown-up with %d UUID collisions.' % (len(aVector))
            sys.exit(1)
        else:
            print 'WARNING: There was a UUID collision.'
            aUUID = uuid_flattener(str(uuid.uuid4()))
    else:
        _uuids[aUUID] = _uuid
    return aUUID

def _handle_data_(name,data):
    global _meta, _isCompressed, _secureDefault, _targetDefault, _node_count
    
    from vyperlogix.xml import XML2JSon
    data = data if (not misc.isList(data)) else data[-1]
    if (name == 'meta'):
        _isMetaChanged = False
        for k,v in data.iteritems():
            if (k not in _exceptions):
                _isMetaChanged = True
                meta[k] = misc._unpack_(v)
        if (_isMetaChanged):
            _meta = meta.insideOut()
        if (meta.has_key('domain')) and (compression_analysis[meta['domain']] == None):
            compression_analysis[meta['domain']] = lists.HashedLists()
        if (meta.has_key('domain_key')) and (compression_analysis[meta['domain_key']] == None):
            compression_analysis[meta['domain_key']] = lists.HashedLists()
    else:
        if (_isCompressing) and (not _isCompressed):
            for k,v in meta.iteritems():
                c_meta[k] = d_meta[k]
            assert len(c_meta) == len(d_meta), 'Oops, Something went wrong with the metadata compression... Check to make sure d_meta is correct.'
            _isCompressed = True
        if (data.has_key(meta['type'])) or ( (data.has_key(meta['label'])) and ( (data.has_key(meta['url'])) or (data.has_key(meta['body'])) ) ) or ( (len(data.keys()) == 1) and ( (data.has_key(meta['label'])) or (data.has_key(meta['url'])) ) ) or ( (len(data.keys()) == 2) and ( (data.has_key(meta['label'])) or (data.has_key(meta['id'])) ) ):
            if data.has_key(meta['url']):
                url = urllib.unquote_plus(misc._unpack_(data['url'])).replace('&amp;','&')
                del data[meta['url']]
                data[meta['url']] = url
                _url_ = misc._unpack_(data['url'])
                _query_ = _url_.split('?')
                toks = ListWrapper(_query_[0].split('/'))
                i = toks.findFirstMatching('')
                try:
                    domain = toks[i+1] if (i > -1) else ''
                except:
                    domain = ''
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
                data[meta['domain_key']] = domain
                data[meta['domain']] = _domain
                data[meta['secure']] = '1' if str(toks[0]).lower() == 'https:' else '0'
                del data[meta['url']][-1]
                try:
                    toks[i+1] = ''
                except:
                    pass
                data[meta['url']] = '/'.join(toks[i+1:])+('?' if (len(_query_) > 1) else '')+(_query_[-1] if (len(_query_) > 1) else '')
            if (_isCompressing):
                if (data[meta['secure']] != None):
                    try:
                        isSecure = misc._unpack_(data[meta['secure']])
                        print "data[meta['secure']]=%s, _secureDefault=%s" % (isSecure,_secureDefault)
                        if (isSecure == _secureDefault):
                            print 'Removed !\n'
                            del data[meta['secure']]
                        else:
                            print
                    except Exception, details:
                        info_string = _utils.formattedException(details=details)
                        print info_string,'\n'
                if (data[meta['target']] != None):
                    try:
                        isTarget = misc._unpack_(data[meta['target']])
                        print "data[meta['target']]=%s, _targetDefault=%s" % (isTarget,_targetDefault)
                        if (isTarget == _targetDefault):
                            print 'Removed !\n'
                            del data[meta['target']]
                        else:
                            print
                    except Exception, details:
                        info_string = _utils.formattedException(details=details)
                        print info_string,'\n'
                for k,v in data.iteritems():
                    if (c_meta.has_key(k)):
                        del data[k]
                        data[c_meta[k]] = misc._unpack_(v)
                if (data.has_key(c_meta['domain'])):
                    compression_analysis[meta['domain']][misc._unpack_(data[c_meta['domain']])] = data
                if (data.has_key(c_meta['domain_key'])):
                    compression_analysis[meta['domain_key']][misc._unpack_(data[c_meta['domain_key']])] = data
            elif data.has_key(meta['url']):
                secure_census[misc._unpack_(data[meta['secure']])] = data
                target_census[misc._unpack_(data[meta['target']])] = data
        if (not data.has_key(d_meta['uuid'])):
            aUUID = str(uuid.uuid4())
            aUUID = uuid_flattener(aUUID) if (aUUID.find('-') > -1) else aUUID
            if (_isPerformingCompressionAnalysis):
                _node_count += 1
            else:
                pass
            uuid_key = 'uuid' if (_isPerformingCompressionAnalysis) else d_meta['uuid']
            data[uuid_key] = aUUID[len(aUUID)-the_n:] if (not _isPerformingCompressionAnalysis) else aUUID
            d_uuids[misc.__unpack__(data[uuid_key])] = data

def handle_data(name,data):
    try:
        _handle_data_(name,data)
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print info_string

def _handle_metadata(data):
    menu = misc._unpack_(data['menu'])
    datafield = misc._unpack_(menu['datafield'])
    metafield = misc._unpack_(menu['metafield'])
    headerfield = misc._unpack_(menu['headerfield'])
    metadata = menu[metafield]
    if (_isCompressing):
        for aMeta in metadata:
            for k,v in aMeta.iteritems():
                if (c_meta.has_key(k)):
                    del aMeta[k]
                    aMeta[misc._unpack_(v)] = c_meta[k]
        del menu['datafield']
        menu['datafield'] = handle_nodeName(datafield)
        del menu['headerfield']
        menu['headerfield'] = handle_nodeName(headerfield)
    d_meta = lists.HashedLists2()
    for k1,v1 in compression_analysis.iteritems():
        kk = c_meta[k1]
        if (not d_meta.has_key(k1)):
            d_meta[k1] = lists.HashedLists2()
            d_meta[k1]['full->key'] = lists.HashedLists2()
            d_meta[k1]['key->full'] = lists.HashedLists2()
        for k2,v2 in v1.iteritems():
            if (not d_meta[k1]['full->key'].has_key(k2)):
                d_meta[k1]['full->key'][k2] = len(d_meta[k1]['full->key'])+1
                d_meta[k1]['key->full'] = d_meta[k1]['full->key'].insideOut()
            for anItem in v2:
                del anItem[kk]
                anItem[kk] = d_meta[k1]['full->key'][k2]
    for k,v in d_meta.iteritems():
        _menu_key = '%s_%s' % (metafield,k)
        if (not menu.has_key(_menu_key)):
            menu[_menu_key] = lists.HashedLists2()
        for kk,vv in v['key->full'].iteritems():
            misc._unpack_(menu[_menu_key])[kk] = misc._unpack_(vv)
    secureDefault = lists.HashedLists2({'secureDefault':_secureDefault})
    metadata.append(secureDefault)
    secureDefault = lists.HashedLists2({'targetDefault':_targetDefault})
    metadata.append(secureDefault)
    pass

def handle_metadata(data):
    try:
        return _handle_metadata(data)
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print info_string

def handle_nodeName(name):
    return name if (name.lower() == 'meta') else name[0] if (name not in node_name_exceptions) else name

def handle_loggedIn_data(name,data):
    try:
        print name, len(data), data.asDict() if (lists.isDict(data)) else data
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print info_string

def handle_loggedIn_b4(data):
    try:
        print len(data), data.asDict() if (lists.isDict(data)) else data
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print info_string

def handle_loggedIn_nodeName(name):
    print name
    return name

if (__name__ == '__main__'):
    import os, sys
    import urllib
    from vyperlogix.misc import _utils
    
    _node_count = 0
    
    _isCompressing = False
    _isCompressed = False
    _isPerformingCompressionAnalysis = True
    secure_census = lists.HashedLists()
    
    fname1 = r"C:\Documents and Settings\c0horra\My Documents\@myFiles\python-projects\verizonwireless\extras\global-nav-sniffer\after-oct-release+header\LoggedOutState_Header.xml"
    fname2 = r"C:\Documents and Settings\c0horra\My Documents\@myFiles\Data\logged-in-state\sample2.xml"
    fname3 = r"C:\Documents and Settings\c0horra\My Documents\@myFiles\python-projects\verizonwireless\extras\global-nav-sniffer\after-oct-release+header\LoggedInState_Header.xml"
    
    #fname = fname1
    #fname = fname2
    fname = fname3
    
    if ( (fname == fname1) or (fname == fname3) ):
        xml = _utils.readFileFrom(fname)
        xml = xml.replace('&',urllib.quote_plus('&'))
        print 'Reading "%s".' % (fname)
    
        json = xml_to_json(xml,callback=handle_data)
    
        toks = list(os.path.splitext(fname))
        toks[-1] = '-json.txt'
        fname2 = ''.join(toks)
        print 'Writing "%s".' % (fname2)
        _utils.writeFileFrom(fname2,json)
        
        _len_ = lambda item:len(item) if (item != None) else 0
        census_analysis = lambda choice1,choice2,bucket:choice1 if (_len_(bucket[choice1]) > _len_(bucket[choice2])) else choice2
    
        _secureDefault = census_analysis('0','1',secure_census)
        _targetDefault = census_analysis('_blank','_top',target_census)
    
        if (secure_census[None]):
            _x_ = secure_census[None]
            _k_ = _secureDefault
            if (_x_ is not None):
                _k_ = set(_secureDefault_choices) - set([misc._unpack_(k) for k in secure_census.keys() if (misc._unpack_(k) != 'None')])
            del secure_census[None]
            secure_census[_k_] = _x_
        
        if (target_census[None]):
            _x_ = target_census[None]
            _k_ = _targetDefault
            dk = dict([(k,len(target_census[k])) for k in target_census.keys()])
            if (_x_ is not None):
                _xx_ = [x for x in target_census.keys() if (x != 'None')][0]
                _kk_ = list(set(_targetDefault_choices) - set([_xx_]))[0]
                dk[_kk_] = len(target_census[None])
                del dk['None']
            _largest = ['',-1]
            for k,v in dk.iteritems():
                if (v > _largest[-1]):
                    _largest = [k,v]
            _k_ = _largest[0]
            target_census[_k_] = _largest[-1]
            _targetDefault = target_census.keys()[0]
        
        _isCompressing = True
        _isPerformingCompressionAnalysis = False
        
        assert _node_count == len(d_uuids), 'Oops there is something wrong with the way UUIDs are being counted.'
        the_node_count = _node_count
        the_n = int(math.ceil(math.log(the_node_count,16)))
        _node_count = 0
        d_uuids = lists.HashedLists2()
    
        json = xml_to_json(xml,callback=handle_data,callbackB4=handle_metadata,callbackNodeName=handle_nodeName)
        toks = list(os.path.splitext(fname))
        toks[-1] = '-compressed-json.txt'
        fname2 = ''.join(toks)
        print 'Writing "%s".' % (fname2)
        _utils.writeFileFrom(fname2,json)
    
        #_isCompressing = False
        #_isCompressed = False
    
        #json = xml_to_json(xml,callback=handle_data,callbackB4=handle_metadata)
        #toks = list(os.path.splitext(fname))
        #toks[-1] = '-json.txt'
        #fname2 = ''.join(toks)
        #print 'Writing "%s".' % (fname2)
        #_utils.writeFileFrom(fname2,json)
    
        assert _node_count == 0, 'Oops there is something wrong with the way UUIDs are being counted.'
        
        #if (len(_uuids) > 0):
            #_uuids.prettyPrint()
        l = ListWrapper(d_uuids.keys())
        #reportTheList(l,'UUID Values')
        n = math.ceil(math.log(len(l),16))
        ll = ListWrapper([(i[0:int(n)],i) for i in misc.copy(l)])
        d_l = lists.HashedLists(dict([(i[0],i[-1]) for i in ll]))
        x_l = [len(v) > 1 for k,v in d_l.iteritems()]
        assert any(x_l) == False, 'Oops, the compressed UUID values are corrupt and cannot be used.'
        #_d_l = d_l.insideOut()
        #for k,v in _d_l.iteritems():
            #aVector = d_uuids[k]
            #if (aVector != None):
                #del aVector['uuid']
                #aVector[d_meta['uuid']] = v
    elif (fname == fname2):
        xml = _utils.readFileFrom(fname)
        xml = xml.replace('&',urllib.quote_plus('&'))
        print 'Reading "%s".' % (fname)
    
        json = xml_to_json(xml,callback=handle_loggedIn_data,callbackB4=handle_loggedIn_b4,callbackNodeName=handle_loggedIn_nodeName)

        toks = list(os.path.splitext(fname))
        toks[-1] = '-json.txt'
        __fname = ''.join(toks)
        print 'Writing "%s".' % (__fname)
        _utils.writeFileFrom(__fname,json)
    print 'DONE !'
    pass
