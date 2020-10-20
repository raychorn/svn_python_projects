from vyperlogix.hash import lists
from xml.dom.minidom import parse, parseString

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

d_amps = {
    '216':'Oslash',
    '217':'Ugrave',
    '214':'Ouml',
    '215':'times',
    '212':'Ocirc',
    '213':'Otilde',
    '210':'Ograve',
    '211':'Oacute',
    '8476':'real',
    '218':'Uacute',
    '219':'Ucirc',
    '9674':'loz',
    '164':'curren',
    '8260':'frasl',
    '165':'yen',
    '166':'brvbar',
    '8250':'rsaquo',
    '167':'sect',
    '160':'nbsp',
    '9830':'diams',
    '8465':'image',
    '161':'iexcl',
    '8659':'dArr',
    '8658':'rArr',
    '8712':'isin',
    '8713':'notin',
    '162':'cent',
    '8746':'cup',
    '933':'Upsilon',
    '932':'Tau',
    '931':'Sigma',
    '220':'Uuml',
    '937':'Omega',
    '936':'Psi',
    '935':'Chi',
    '918':'Zeta',
    '8220':'ldquo',
    '8221':'rdquo',
    '8222':'bdquo',
    '8744':'or',
    '8224':'dagger',
    '8225':'Dagger',
    '8226':'bull',
    '710':'circ',
    '8736':'ang',
    '8734':'infin',
    '9829':'hearts',
    '8715':'ni',
    '916':'Delta',
    '928':'Pi',
    '929':'Rho',
    '8707':'exist',
    '8706':'part',
    '8704':'forall',
    '920':'Theta',
    '921':'Iota',
    '922':'Kappa',
    '923':'Lambda',
    '924':'Mu',
    '925':'Nu',
    '926':'Xi',
    '376':'Yuml',
    '9001':'lang',
    '8472':'weierp',
    '8230':'hellip',
    '199':'Ccedil',
    '198':'AElig',
    '195':'Atilde',
    '194':'Acirc',
    '197':'Aring',
    '196':'Auml',
    '191':'iquest',
    '190':'frac34',
    '193':'Aacute',
    '192':'Agrave',
    '252':'uuml',
    '253':'yacute',
    '250':'uacute',
    '251':'ucirc',
    '8804':'le',
    '8805':'ge',
    '8969':'rceil',
    '8968':'lceil',
    '919':'Eta',
    '254':'thorn',
    '915':'Gamma',
    '914':'Beta',
    '917':'Epsilon',
    '255':'yuml',
    '8733':'prop',
    '913':'Alpha',
    '8838':'sube',
    '8206':'lrm',
    '8207':'rlm',
    '8204':'zwnj',
    '8205':'zwj',
    '8201':'thinsp',
    '245':'otilde',
    '244':'ocirc',
    '247':'divide',
    '246':'ouml',
    '241':'ntilde',
    '240':'eth',
    '243':'oacute',
    '242':'ograve',
    '249':'ugrave',
    '248':'oslash',
    '8747':'int',
    '39':'apos',
    '38':'amp',
    '8970':'lfloor',
    '8719':'prod',
    '34':'quot',
    '8800':'ne',
    '8721':'sum',
    '927':'Omicron',
    '8727':'lowast',
    '9002':'rang',
    '8501':'alefsym',
    '8218':'sbquo',
    '339':'oelig',
    '338':'OElig',
    '8971':'rfloor',
    '8211':'ndash',
    '8656':'lArr',
    '8745':'cap',
    '8212':'mdash',
    '8743':'and',
    '8217':'rsquo',
    '8216':'lsquo',
    '60':'lt',
    '8801':'equiv',
    '62':'gt',
    '179':'sup3',
    '178':'sup2',
    '177':'plusmn',
    '176':'deg',
    '175':'macr',
    '174':'reg',
    '173':'shy',
    '172':'not',
    '171':'laquo',
    '170':'ordf',
    '977':'thetasym',
    '8194':'ensp',
    '8195':'emsp',
    '8709':'empty',
    '8730':'radic',
    '978':'upsih',
    '182':'para',
    '183':'middot',
    '180':'acute',
    '181':'micro',
    '186':'ordm',
    '187':'raquo',
    '184':'cedil',
    '185':'sup1',
    '8596':'harr',
    '188':'frac14',
    '189':'frac12',
    '8592':'larr',
    '8593':'uarr',
    '402':'fnof',
    '8254':'oline',
    '8773':'cong',
    '8776':'asymp',
    '8594':'rarr',
    '168':'uml',
    '169':'copy',
    '229':'aring',
    '228':'auml',
    '227':'atilde',
    '226':'acirc',
    '225':'aacute',
    '224':'agrave',
    '223':'szlig',
    '222':'THORN',
    '221':'Yacute',
    '163':'pound',
    '964':'tau',
    '965':'upsilon',
    '966':'phi',
    '967':'chi',
    '960':'pi',
    '961':'rho',
    '962':'sigmaf',
    '963':'sigma',
    '8901':'sdot',
    '968':'psi',
    '969':'omega',
    '8660':'hArr',
    '8839':'supe',
    '8657':'uArr',
    '947':'gamma',
    '8835':'sup',
    '8834':'sub',
    '934':'Phi',
    '8364':'euro',
    '8756':'there4',
    '238':'icirc',
    '239':'iuml',
    '234':'ecirc',
    '235':'euml',
    '236':'igrave',
    '237':'iacute',
    '230':'aelig',
    '231':'ccedil',
    '232':'egrave',
    '233':'eacute',
    '959':'omicron',
    '958':'xi',
    '951':'eta',
    '950':'zeta',
    '953':'iota',
    '952':'theta',
    '955':'lambda',
    '954':'kappa',
    '957':'nu',
    '956':'mu',
    '8629':'crarr',
    '201':'Eacute',
    '200':'Egrave',
    '203':'Euml',
    '202':'Ecirc',
    '205':'Iacute',
    '204':'Igrave',
    '207':'Iuml',
    '206':'Icirc',
    '209':'Ntilde',
    '208':'ETH',
    '8853':'oplus',
    '8249':'lsaquo',
    '8242':'prime',
    '8243':'Prime',
    '8240':'permil',
    '8722':'minus',
    '8595':'darr',
    '8711':'nabla',
    '948':'delta',
    '949':'epsilon',
    '946':'beta',
    '732':'tilde',
    '982':'piv',
    '945':'alpha',
    '9827':'clubs',
    '8869':'perp',
    '8764':'sim',
    '8482':'trade',
    '353':'scaron',
    '352':'Scaron',
    '8836':'nsub',
    '9824':'spades',
    '8855':'otimes'
}

amps = ['%26','%3C','%3E']

is_any_amps = lambda t:any([t.find(ch) > -1 for ch in amps])

def is_cdata(source):
    import urllib
    t = urllib.quote_plus(source)
    return (is_any_amps(t))

def quote_plus_if_required(source):
    import urllib
    t = urllib.quote_plus(source)
    return t if (is_any_amps(t)) else source

def quote_if_required(source):
    import urllib
    t = urllib.quote(source)
    return t if (is_any_amps(t)) else source

def decodeUnicode(value):
    from vyperlogix.misc import decodeUnicode
    return decodeUnicode.decodeUnicode(str(value))

def getAttrFromNode(node,name):
    value = ''
    try:
	if (node.hasAttribute(name)):
	    value = decodeUnicode(node.getAttribute(name))
    except:
	pass
    return value

def getNodeText(node):
    from xml.dom import Node
    rc = ""
    if (node.nodeType == Node.TEXT_NODE):
	rc += node.data
    return decodeUnicode(str(rc))

def getAllNodeText(nodelist):
    rc = ""
    for node in nodelist:
	rc += getNodeText(node)
    return rc

def getAttrsFromNode(node):
    _attrs = {}
    try:
	attrs = node.attributes
	for attrName in attrs.keys():
	    _attrs[attrName] = attrs.get(attrName).nodeValue
    except:
	pass
    return _attrs

def xmlToDict(xml):
    _dict = lists.HashedLists2()
    docs = [parseString(d) for d in xml.split('\x00')]
    for doc in docs:
	_data = doc.getElementsByTagName("data")
	for d in _data:
	    _dict['data'] = getAttrsFromNode(d)
	_items = doc.getElementsByTagName("item")
	for item in _items:
	    _item = lists.HashedLists2()
	    _attrs = getAttrsFromNode(item)
	    _key = ''
	    if (_attrs.has_key('Id')):
		_key = _attrs['Id']
	    if (len(_key) > 0):
		for child in item.childNodes:
		    _attrs = getAttrsFromNode(child)
		    _text = getNodeText(child)
		    if (len(_text) == 0):
			_text = getAllNodeText(child.childNodes)
		    _item['attributes'] = _attrs
		    _item[child.nodeName] = _text
		_dict[_key] = _item
	    pass
    return _dict

import xml.dom.minidom

def xml2dict(xmlstring):
    doc = xml.dom.minidom.parseString(xmlstring)
    remove_whilespace_nodes(doc.documentElement)
    return elementtodict(doc.documentElement)

def elementtodict(parent):
    child = parent.firstChild
    if (not child):
	return None
    elif (child.nodeType == xml.dom.minidom.Node.TEXT_NODE):
	return child.nodeValue
    
    d={}
    while child is not None:
	if (child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE):
	    try:
		d[child.tagName]
	    except KeyError:
		d[child.tagName]=[]
	    d[child.tagName].append(elementtodict(child))
	child = child.nextSibling
    return lists.HashedLists2(d)

def remove_whilespace_nodes(node, unlink=True):
    remove_list = []
    for child in node.childNodes:
	if child.nodeType == xml.dom.Node.TEXT_NODE and not child.data.strip():
	    remove_list.append(child)
	elif child.hasChildNodes():
	    remove_whilespace_nodes(child, unlink)
    for node in remove_list:
	node.parentNode.removeChild(node)
	if unlink:
	    node.unlink()

def xml_to_json(xml):
    from vyperlogix.xml import XML2JSon
    
    json = ''

    po = XML2JSon.XMLConversionProxy(XML2JSon.XML2JSon())
    json = po.process(xml)
    
    return json

def python_to_xml(d):
    from xml.dom.minidom import Document
    import copy

    class dict2xml(object):
	doc     = Document()
    
	def __init__(self, structure):
	    if len(structure) == 1:
		rootName    = str(structure.keys()[0])
		self.root   = self.doc.createElement(rootName)
    
		self.doc.appendChild(self.root)
		self.build(self.root, structure[rootName])
    
	def build(self, father, structure):
	    if type(structure) == dict:
		for k in structure:
		    tag = self.doc.createElement(k)
		    father.appendChild(tag)
		    self.build(tag, structure[k])
	    
	    elif type(structure) == list:
		grandFather = father.parentNode
		tagName     = father.tagName
		grandFather.removeChild(father)
		for l in structure:
		    tag = self.doc.createElement(tagName)
		    self.build(tag, l)
		    grandFather.appendChild(tag)
		
	    else:
		data    = str(structure)
		tag     = self.doc.createTextNode(data)
		father.appendChild(tag)
	
	def asXML(self):
	    return self.doc.toprettyxml(indent="",newl="")
	    
	def asPrettyXML(self):
	    return self.doc.toprettyxml(indent="  ")
	    
	def display(self):
	    print self.asPrettyXML()
	    
    return dict2xml(d).asXML()

