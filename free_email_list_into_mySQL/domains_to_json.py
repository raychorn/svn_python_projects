import os, sys

from vyperlogix.misc import _utils

__freehost_domains_filename = r"Z:\python projects\free_email_list_into_mySQL\freeemailhost__c.xml"

def python_to_json(obj):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(obj)
    
    return json

def xml_to_python(xml):
    from vyperlogix.xml import XML2JSon
    
    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    obj = po._process(xml)
    
    return obj

def domains():
    xml = _utils.readFileFrom(__freehost_domains_filename,noCRs=True)
    obj = xml_to_python(xml)
    json = python_to_json(obj)
    return json

if (__name__ == '__main__'):
    json = domains()
    t = list(os.path.splitext(os.path.basename(__freehost_domains_filename)))
    t[-1] = '.json'
    fname = os.sep.join([os.path.dirname(__freehost_domains_filename),''.join(t)])
    _utils.writeFileFrom(fname,json)
