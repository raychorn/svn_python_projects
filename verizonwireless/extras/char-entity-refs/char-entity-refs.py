import os, sys, re
import datetime
import random

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.html.parsers.HTMLConversion import HTMLConversion
from vyperlogix.html.parsers.HTMLConversion import HTMLConversionProxy

if (__name__ == '__main__'):
    
    from vyperlogix.lists import ListWrapper
    from vyperlogix.misc import ReportTheList
    from vyperlogix.products import keys
    
    from vyperlogix.django import django_utils
    from vyperlogix.classes.SmartObject import SmartFuzzyObject

    find_files = lambda dname,pattern:[f for f in os.listdir(dname) if (os.path.splitext(f)[-1] == '.html') and (f.lower().find(pattern.lower()) > -1)]
	
    html = ''
    dname = os.path.dirname(__file__)
    so = SmartFuzzyObject()
    try:
	files = find_files(dname,'source')
	if (len(files) > 0):
	    fname = os.path.join(dname,files[0])
	    so.fname = fname
	    html = _utils.readFileFrom(fname)
	    so.content = html
    except:
	pass
    finally:
	import BeautifulSoup
	soup = BeautifulSoup.BeautifulSoup(so.content)
	toks = list(os.path.splitext(fname))
	toks[0] += '-pretty'
	fn = ''.join(toks)
	_utils.writeFileFrom(fn,soup.prettify())

    po = HTMLConversionProxy(HTMLConversion())
    items = po.process(so.content)
    ll = ListWrapper.ListWrapper([str(n[0]) for n in items[0][0]])
    iName = ll.findFirstMatching('Name')
    iCode = ll.findFirstContaining(' (decimal)')
    d_code = lists.HashedLists2()
    d_code2 = lists.HashedLists2()
    for item in items:
	try:
	    _name = HTMLConversion.unpack(item[0][iName])
	    _code = int(HTMLConversion.parse(item[0][iCode]))
	    d_code[_name] = [str(HTMLConversion.unpack(item[0][iCode])),_code]
	    d_code2[_code] = _name
	except Exception, e:
	    #print 'ERROR: %s' % (_utils.formattedException(e))
	    pass
    s = d_code.pretty(delim='\n')
    s2 = d_code2.pretty(delim='\n')
    t = str(d_code)
    toks = list(os.path.splitext(so.fname))
    toks[-1] = '.py'
    fname = ''.join(toks)
    _utils.writeFileFrom(fname,'d='+s+'\n'+'_d='+s2)
    print 'Done !'
