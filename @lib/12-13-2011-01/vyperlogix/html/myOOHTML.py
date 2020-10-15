__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import oohtml

from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.decorators import deprecated

from vyperlogix import misc

table_header_attributes = {}

LINK = 'link'
U = 'u'
LABEL = 'label'
NOBR = 'nobr'
B = 'b'
CENTER = 'center'

class Html(oohtml.Html, Cooperative):
    def __toHtml(self, level, elements):
        tabs = ''*level
        out = ''
        for e in elements:
            if e.txt != None:
                out += '%s' % (e.txt)
            else:
                if not e.inline:
                    out += "%s" % (tabs)
                if e.open:
                    out += '<%s%s%s/>' % (e.name, self.__toProperties(e.properties), self.__toAttributes(e.attributes))
                else:
                    out += '<%s%s%s>%s</%s>' % (e.name, self.__toProperties(e.properties), self.__toAttributes(e.attributes), self.__toHtml(level+1, e.elements), e.name)
        return out

    def tag(self, _name, *properties, **attributes):
        '''Makes a new tag, appends to parent and returns it'''
        h = Html()
        h.name = _name
        h.properties = properties
        h.attributes = attributes
        self.elements.append(h)
        return h

    def text(self, txt):
        '''Makes a new text and appends to parent'''
        h = Html()
        h.txt = txt
        self.elements.append(h)

    def text2(self, txt):
        '''Makes a new formatted text and appends to parent'''
        h = Html()
        h.txt = txt
        if txt:
            h.txt = str(txt).replace('<', '&lt;')
        self.elements.append(h)

    def tagHR(self, **attributes):
	t = self.tagOp(oohtml.HR, **attributes)
	return t

    def tagDIV(self, _text, **attributes):
	t = self.tag(oohtml.DIV, **attributes)
	t.text(_text)
	return t
		
    def tagBUTTON(self, _text, **attributes):
	t = self.tag(oohtml.BUTTON, **attributes)
	t.text(_text)
	return t
		
    def tagFORM(self, **attributes):
	t = self.tag(oohtml.FORM, enctype="multipart/form-data", method="post", **attributes)
	return t
    
    def tag_FORM(self, **attributes):
	t = self.tag(oohtml.FORM, **attributes)
	return t
    
    def tagRADIO(self, name, value, caption, isCHECKED=False, **attributes):
	if (isCHECKED):
	    self.tagOp(oohtml.INPUT, oohtml.CHECKED, type=oohtml.RADIO, name=name, value=value)
	else:
	    self.tagOp(oohtml.INPUT, type=oohtml.RADIO, name=name, value=value)
	span = self.tagSPAN('')
	span.text('&nbsp;%s&nbsp;' % (caption))
		
    def tagP(self, _text, **attributes):
	t = self.tag(oohtml.P, **attributes)
	t.text(_text)
	return t
		
    def tagIFRAME(self, **attributes):
	t = self.tag(oohtml.IFRAME, **attributes)
	return t
		
    def tagUL(self, **attributes):
	t = self.tag(oohtml.UL, **attributes)
        return t

    def tagOL(self, **attributes):
	t = self.tag(oohtml.OL, **attributes)
        return t

    def tag_A(self, _text, **attributes):
        t = self.tag(oohtml.A, **attributes)
        t.text(_text)
        return t

    def tag_LI(self, _text, **attributes):
        t = self.tag(oohtml.LI, **attributes)
        t.text(_text)
        return t

    def tagU(self, _text, **attributes):
	t = self.tag(U, **attributes)
	t.text(_text)
	return t
		
    def tagINPUT(self, *properties, **attributes):
        '''example: <input type="text" name="input1" value="1">'''
	t = self.tagOp(oohtml.INPUT, *properties, **attributes)
	return t
		
    def tagSPAN(self, _text, **attributes):
        t = self.tag(oohtml.SPAN, **attributes)
        t.text(_text)
        return t

    def tag_SPAN(self, _text, **attributes):
        t = self.tag(oohtml.SPAN, **attributes)
        t.text2(_text)
        return t

    def tagSUBMIT(self, _title, **attributes):
	t = self.tagOp(oohtml.INPUT, name="submit", type="submit", title=_title, **attributes)
	return t
		
    def tagLABEL(self, _name, _text, *properties, **attributes):
        t = self.tag(LABEL,for_=_name,*properties,**attributes)
	t.text(_text)
	return t
		
    def tagNOBR(self,*properties,**attributes):
        t = self.tag(NOBR,*properties,**attributes)
	return t
		
    def tagB(self, _text, **attributes):
	t = self.tag(B, **attributes)
	t.text(_text)
	return t
		
    def tagCenter(self, _text, **attributes):
	t = self.tag(CENTER, **attributes)
	t.text(_text)
	return t
		
    def tagTD(self, _text, **attributes):
	t = self.tag(oohtml.TD, **attributes)
	t.text(_text)
	return t

    def _tagSPAN(self, _text, **attributes):
        t = self.tag(oohtml.SPAN, **attributes)
        t.text(_text)
        return t
    
    def _tagLI(self, _text, **attributes):
	t = self.tag(oohtml.LI, **attributes)
	t.text(_text)
	return t
		
    def _tagLI(self, _text, **attributes):
        t = self.tag(oohtml.LI, **attributes)
        t.text(_text)
        return t

    def _tagH3(self, _text, **attributes):
        t = self.tag(oohtml.H3, **attributes)
        t.text(_text)
        return t

    def tagBR(self, *properties, **attributes):
	t = self.tagOp(oohtml.BR, *properties, **attributes)
	return t
		
    def tagLINK(self, **attributes):
	t = self.tagOp(LINK, **attributes)
	return t
		
    def _tagLI_(self, _text, attributes):
	t = self.tag(oohtml.LI)
	t.text(_text)
	if (isinstance(attributes,dict)):
	    t.attributes = attributes
	return t
		
    def html(self,txt):
        '''Makes a new formatted text and appends to parent
            Example: [b bold] [a link, http://python.org] [i italic] [u underline] [code code]'''
        h = Html()
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('\n', '<br>')
        h.txt = re.sub('\[(\w+)\s+(.+?)]', self.__html, txt)
        self.elements.append(h)

    @deprecated.deprecated
    def tag_TABLE(self, _rows, **attributes):
        '''This function has been replaced by html_table()'''
        return self.html_table(_rows, **attributes)

    def html_table(self, _rows, **attributes):
        table = self.tag(oohtml.TABLE, **attributes)
        tr = table.tag(oohtml.TR)
        for c in _rows[0]:
            tr.table_td(c,bgColor='silver',align='left')
        for r in _rows[1:]:
            tr = table.tag(oohtml.TR)
            if (isinstance(r,list)):
                for c in r:
                    tr.table_td(c,**attributes)
            else:
                tr.table_td(r,**attributes)

    def html_simple_table(self, _rows, **attributes):
	'''_rows consists of tuples each tuple can specify attributes for each table td tag.'''
        table = self.tag(oohtml.TABLE, **attributes)
        for r in _rows:
	    tr = table.tag(oohtml.TR)
            if (isinstance(r,list)) or (isinstance(r,tuple)):
                for c in r:
		    if (isinstance(c,tuple)):
			d = {}
			toks = [t.split('=') for t in c[-1].replace('"','').split(';')]
			for t in toks:
			    if (len(t) == 2):
				d[t[0]] = t[-1]
			tr._table_td(c[0],d)
		    else:
			tr.table_td(c)
            else:
                tr.table_td(r)

    def table_td(self, _text, **attributes):
        t = self.tag(oohtml.TD, **attributes)
        t.text(_text)
        return t

    def _table_td(self, _text, attributes):
        t = self.tag(oohtml.TD)
        t.text(_text)
	t.attributes = attributes
        return t

    def tag_IMG(self, *properties, **attributes):
        t = self.tagOp(oohtml.IMG, *properties, **attributes)
        return t
    
class HtmlCycler(Html):
    def __init__(self):
	super(HtmlCycler, self).__init__()
	self.__use_cycler = False # make this True to allow the cycler to function otherwise it will not...
	self.__cycle_count = 0 # allows attributes to be cycled from node to node based on the number of items
	self.__cycle_func = HtmlCycler.shaded_class_cycler_function()
	self.__table_header_attrs = {'bgColor':'silver','align':'center'}
	self.__table_cell_attrs = {}

    @classmethod
    def shaded_class_cycler_function(self):
	'''This is the cycle function that emits the required attributes for the shaded class.'''
	return lambda count:{'class':'shaded' if (not (count % 2)) else ''}
    
    @classmethod
    def shaded_class_cycler_function2(self):
	'''This is the cycle function that emits the required attributes for the shaded class.'''
	return lambda count:{'style':'background-color:#efefef;' if (not (count % 2)) else ''}
    
    @classmethod
    def shaded_class_cycler_function3(self):
	'''This is the cycle function that emits the required attributes for the shaded class.'''
	return lambda count:{'bgcolor':'#efefef' if (not (count % 2)) else ''}
    
    def cycle_count():
        doc = "cycle_count"
        def fget(self):
            return self.__cycle_count
        def fset(self, cycle_count):
            self.__cycle_count = cycle_count
        return locals()
    cycle_count = property(**cycle_count())

    def cycle_func():
        doc = "cycle_func"
        def fget(self):
            return self.__cycle_func
        def fset(self, cycle_func):
            self.__cycle_func = cycle_func
        return locals()
    cycle_func = property(**cycle_func())

    def use_cycler():
        doc = "use_cycler"
        def fget(self):
            return self.__use_cycler
        def fset(self, use_cycler):
            self.__use_cycler = use_cycler if (isinstance(use_cycler,bool)) else False
	    if (self.__use_cycler):
		self.__cycle_func = HtmlCycler.shaded_class_cycler_function()
        return locals()
    use_cycler = property(**use_cycler())
    
    def table_header_attrs():
        doc = "table_header_attrs"
        def fget(self):
            return self.__table_header_attrs
        def fset(self, table_header_attrs):
            self.__table_header_attrs = table_header_attrs
        return locals()
    table_header_attrs = property(**table_header_attrs())
    
    def table_cell_attrs():
        doc = "table_cell_attrs"
        def fget(self):
            return self.__table_cell_attrs
        def fset(self, table_cell_attrs):
            self.__table_cell_attrs = table_cell_attrs
        return locals()
    table_cell_attrs = property(**table_cell_attrs())
    
    def tag(self, _name, *properties, **attributes):
        '''Makes a new tag, appends to parent and returns it'''
        h = HtmlCycler()
        h.name = _name
        h.properties = properties
        h.attributes = attributes
        self.elements.append(h)
        return h

    def __apply_attributes_to__(self,t,attributes={}):
	if (len(attributes) == 0) and (self.use_cycler) and (callable(self.cycle_func)):
	    attrs = self.cycle_func(self.cycle_count)
	    self.cycle_count += 1
	    if (isinstance(attrs,dict)):
		t.attributes = attrs

    def tagLI(self, _text, **attributes):
	'''This method does not allow HTML to be embedded in this text of the element.'''
	t = self.tag(oohtml.LI, **attributes)
	t.text2(_text)
	self.__apply_attributes_to__(t,attributes)
	return t
		
    def _tagLI(self, _text, **attributes):
	'''This method does allow HTML to be embedded in this text of the element.'''
	t = self.tag(oohtml.LI, **attributes)
	t.text(_text)
	self.__apply_attributes_to__(t,attributes)
	return t
		
    def html_simple_table(self, _rows, **attributes):
	'''_rows consists of tuples each tuple can specify attributes for each table td tag.'''
        table = self.tag(oohtml.TABLE, **attributes)
        tr = table.tag(oohtml.TR)
        for r in _rows:
            tr = table.tag(oohtml.TR)
	    self.__apply_attributes_to__(tr)
            if (isinstance(r,list)):
                for c in r:
		    if (isinstance(c,tuple)):
			d = {}
			toks = [t.split('=') for t in c[-1].replace('"','').split(';')]
			for t in toks:
			    if (len(t) == 2):
				d[t[0]] = t[-1]
			tr._table_td(c[0],d)
		    else:
			tr.table_td(c)
            else:
                tr.table_td(r)
		
    def html_simple_table_with_header(self, _rows, **attributes):
	'''_rows consists of tuples each tuple can specify attributes for each table td tag.'''
        table = self.tag(oohtml.TABLE, **attributes)
        tr = table.tag(oohtml.TR)
	for c in _rows[0]:
	    tr.table_td(c,**self.table_header_attrs)
        for r in _rows[1:]:
            tr = table.tag(oohtml.TR)
	    self.__apply_attributes_to__(tr)
            if (isinstance(r,list)):
                for c in r:
		    if (isinstance(c,tuple)):
			d = {}
			toks = [t.split('=') for t in c[-1].replace('"','').split(';')]
			for t in toks:
			    if (len(t) == 2):
				d[t[0]] = t[-1]
			tr._table_td(c[0],d,**self.table_cell_attrs)
		    else:
			tr.table_td(c,**self.table_cell_attrs)
            else:
                tr.table_td(r,**self.table_cell_attrs)
		
def renderAnchor(url,text,class_=None,title=None,target="_blank",rel=None,onClick=None):
    h = Html()
    h_html = h.tag(oohtml.HTML)
    h_body = h_html.tag(oohtml.BODY)
    h_Content = h_body.tag(oohtml.DIV)
    d = {}
    if (misc.isString(rel)):
	d['rel'] = rel
    if (misc.isString(onClick)):
	d['onClick'] = onClick
    if (misc.isString(class_)):
	d['class_'] = class_
    if (misc.isString(target)):
	d['target'] = target
    if (misc.isString(title)):
	d['title'] = title
    a = h_Content.tag(oohtml.A, href="%s" % (url), **d)
    a.text(text)
    return h_Content.toHtml().replace('<br>','').replace('<BR>','').replace('<Br>','').replace('<bR>','').replace('\n','').replace('\t','')

def _renderAnchor(url,text,class_=None,title=None,rel=None,onClick=None):
    h = Html()
    h_html = h.tag(oohtml.HTML)
    h_body = h_html.tag(oohtml.BODY)
    h_Content = h_body.tag(oohtml.DIV)
    d = {}
    if (misc.isString(rel)):
	d['rel'] = rel
    if (misc.isString(onClick)):
	d['onClick'] = onClick
    if (misc.isString(class_)):
	d['class_'] = class_
    if (misc.isString(title)):
	d['title'] = title
    a = h_Content.tag(oohtml.A, href="%s" % (url), **d)
    a.text(text)
    return h_Content.toHtml().replace('<br>','').replace('<BR>','').replace('<Br>','').replace('<bR>','').replace('\n','').replace('\t','')

def renderButton(value,title=None,onClick=None):
    h = Html()
    h_html = h.tag(oohtml.HTML)
    h_body = h_html.tag(oohtml.BODY)
    h_Content = h_body.tag(oohtml.DIV)
    d = {}
    if (misc.isString(onClick)):
	d['onClick'] = onClick
    if (misc.isString(title)):
	d['title'] = title
    value = value if (misc.isString(value)) else 'BUTTON'
    h_Content.tagINPUT(value=value,type_='button', **d)
    return h_Content.toHtml()

def render_Button(id=None,src=None,title=None,onClick=None):
    h = Html()
    h_html = h.tag(oohtml.HTML)
    h_body = h_html.tag(oohtml.BODY)
    h_Content = h_body.tag(oohtml.DIV)
    d = {}
    if (misc.isString(onClick)):
	d['onClick'] = onClick
    if (misc.isString(title)):
	d['title'] = title
    if (misc.isString(id)):
	d['id'] = id
    d['type'] = 'button'
    btn = h_Content.tag(oohtml.BUTTON, **d)
    btn.tag_IMG(src=src,border=0)
    return h_Content.toHtml()

def table_td(parent, _text, **attributes):
    t = parent.tag(oohtml.TD, **attributes)
    t.text(_text)
    return t

def html_table(parent, _rows, **attributes):
    table = parent.tag(oohtml.TABLE, **attributes)
    tr = table.tag(oohtml.TR)
    for c in _rows[0]:
        tr.table_td(c,bgColor='silver',align='left')
    for r in _rows[1:]:
        tr = table.tag(oohtml.TR)
        for c in r:
            table_td(tr,c,**attributes)
    return table.toHtml().replace('\n','').replace('\t','')

def renderTable(row0,dict_obj,**attributes):
    from vyperlogix.hash import lists
    h = Html()
    h_html = h.tag(oohtml.HTML)
    h_body = h_html.tag(oohtml.BODY)
    h_Content = h_body.tag(oohtml.DIV)
    _rows = [['','']] if (not isinstance(row0,list)) and (not isinstance(row0,tuple)) else [list(row0)]
    if (lists.isDict(dict_obj)):
        for k,v in dict_obj.iteritems():
            _rows.append([k,str(v) if (v is not None) and (len(str(v)) > 0) else '&nbsp;'])
    h_Content.html_table(_rows,**attributes)
    return h_Content.toHtml().replace('\n','').replace('\t','')

def render_table_from_list(aList,text_id=None,num_wide=6,**attributes):
    items = []
    h = Html()
    if (isinstance(aList,list)):
        _items = []
        for item in aList:
	    if (text_id is not None):
		_items.append(item[text_id])
	    else:
		_items.append(item)
            if (len(_items) == num_wide):
                items.append(_items)
                _items = []
	for item in _items:
	    items.append(item)
    h.html_simple_table(items,**attributes)
    return h.toHtml()

def tag_IMG(*properties, **attributes):
    h = Html()
    h.tag_IMG(*properties, **attributes)
    return h.toHtml()

def tag_INPUT(*properties, **attributes):
    h = Html()
    h.tagINPUT(*properties, **attributes)
    return h.toHtml()

def tag_BUTTON(_text, **attributes):
    h = Html()
    h.tagBUTTON(_text, **attributes)
    return h.toHtml()

def tag_LINK(_href):
    h = Html()
    h.tagLINK(rel="stylesheet", href=_href, type="text/css")
    return h.toHtml()

def render_styles(_text):
    h = Html()
    h.tagSTYLE(_text, type="text/css")
    return h.toHtml()

def render_U(_text):
    h = Html()
    h.tagU(_text)
    return h.toHtml()

def render_BR():
    h = Html()
    h.tagBR()
    return h.toHtml()

def render_CENTER(_text):
    h = Html()
    h.tagCenter(_text)
    return h.toHtml()

def render_scripts(_text):
    h = Html()
    h.tagSCRIPT(_text, type="text/javascript")
    return h.toHtml()

def render_DIV(*properties, **attributes):
    h = Html()
    h.tagDIV(*properties, **attributes)
    return h.toHtml()

def render_IMG(*properties, **attributes):
    h = Html()
    h.tag_IMG(*properties, **attributes)
    return h.toHtml()

def render_H3(*properties, **attributes):
    h = Html()
    h.tagH3(*properties, **attributes)
    return h.toHtml()

def _render_H3(*properties, **attributes):
    h = Html()
    h._tagH3(*properties, **attributes)
    return h.toHtml()

def renderSPAN(*properties, **attributes):
    '''text is not escaped'''
    h = Html()
    h.tagSPAN(*properties, **attributes)
    return h.toHtml()

def render_SPAN(*properties, **attributes):
    h = Html()
    h.tag_SPAN(*properties, **attributes)
    return h.toHtml()

def render_P(*properties, **attributes):
    h = Html()
    h.tagP(*properties, **attributes)
    return h.toHtml()

def render_IFRAME(*properties, **attributes):
    h = Html()
    h.tagIFRAME(*properties, **attributes)
    return h.toHtml()

def render_select_content(aList,tag=None,id=None,name=None,text_id=None,value_id=None,defaultChoose=False,onChange=None,selected=None):
    from vyperlogix.misc import ObjectTypeName
    from vyperlogix.classes.SmartObject import SmartObject
    h = Html() if (tag is None) else tag
    if (ObjectTypeName.typeClassName(aList).find('QuerySet') > -1):
	aList = [SmartObject(aList[i].__dict__) for i in xrange(0,aList.count())]
    if (isinstance(aList,list)):
        options = []
	if (defaultChoose):
	    options.append(('',"Choose..."))
	try:
	    options += [(item[value_id],item[text_id]) for item in aList]
	except:
	    pass # don't cry about this just skip over it...
        options = tuple(options)
        h.tagSELECT(options, (selected if (selected) else ''), id=id, name=name, onchange=onChange)
    return h.toHtml()
