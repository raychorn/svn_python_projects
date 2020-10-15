def xml_to_python(xml,callback=None):
    from vyperlogix.xml import XML2JSon
    
    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon(callback=callback))
    obj = po._process(xml)
    
    return obj

def python_to_xml(obj):
    from vyperlogix.xml.serializer import XMLMarshal
    
    stream = _utils.stringIO()
    
    XMLMarshal.dump(stream,obj)

    return stream.getvalue()

def python_to_json(obj):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(obj)
    
    return json

def xml_to_json(xml):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(xml)
    
    return json

from vyperlogix import misc
from vyperlogix.hash import lists
_metadata = lists.HashedFuzzyLists2()

def callback(data):
    global _metadata
    if (misc.isList(data)):
        data = data[-1]
    if (lists.isDict(data)) and (data.has_key(_metadata['label'])) and ( (data.has_key(_metadata['url'])) or (data.has_key(_metadata['body'])) ):
        if (data.has_key(_metadata['url'])):
            del data[_metadata['url']]
            data[_metadata['url']] = '...'
    else:
        if (lists.isDict(data)):
            for k,v in data.iteritems():
                _metadata[k] = v
    return data

if (__name__ == '__main__'):
    import os, sys
    import urllib
    import simplejson
    from vyperlogix.misc import _utils

    fname = r'Z:\python projects\_django-projects\@projects\verizonwireless\extras\global-nav-sniffer\LoggedOutState.xml'
    xml = _utils.readFileFrom(fname)
    xml = xml.replace('&',urllib.quote_plus('&'))
    print 'Reading "%s".' % (fname)
    data = xml_to_python(xml) # ,callback=callback

    json = python_to_json(data)
    toks = list(os.path.splitext(fname))
    toks[-1] = '.json'
    fname2 = ''.join(toks)
    print 'Writing "%s".' % (fname2)
    _utils.writeFileFrom(fname2,json)

    #data2 = simplejson.loads(json)
    
    #import pyxslt.serialize
    #xml2 = pyxslt.serialize.toString(rootTagName='menu',prettyPrintXml=True,menu=data2)

    #toks[-1] = '2.xml'
    #fname2 = ''.join(toks)
    #print 'Writing "%s".' % (fname2)
    #_utils.writeFileFrom(fname2,xml2)

    print 'DONE !'
    pass
