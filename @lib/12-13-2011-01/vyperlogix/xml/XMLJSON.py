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

def _python_to_json(obj):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(obj)
    
    return json

def python_to_json(d,seps=(',\n', ':\n')):
    try:
        import simplejson
        json = simplejson.dumps(d,separators=seps)
    except:
        json = _python_to_json(d)
    return json

def xml_to_json(xml):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(xml)
    
    return json

