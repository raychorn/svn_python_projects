import os,sys

from vyperlogix import misc
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.hash import lists

from vyperlogix.misc import _utils
from vyperlogix.xml import XMLJSON

_get = lambda key,node:node[key] if (lists.isDict(node)) and (node.has_key(key)) else None
unlist = lambda item:item[0] if (misc.isList(item) and (len(item) > 0)) else item
get = lambda key,node:unlist(_get(key,node))
normalize = lambda fname:os.sep.join([_dvd,fname.replace('/',os.sep)])
normalize_slashes = lambda item,slash:slash.join([n for n in item.split(slash) if (len(n) > 0)])

def go_look_for_file_named(fname):
    _fname = str(fname).lower()
    for root,dirs,files in _utils.walk(_dvd):
	for f in files:
	    if (str(f).lower() == _fname):
		return os.sep.join([root,f])
    if (len(fname) > 0):
	print >> sys.stderr, 'WARNING: Cannot locate "%s".' % (fname)
    else:
	pass
    return None

def replace_node_item_using(node,key,item):
    anItem = _get(key,node)
    s = str(anItem[0] if (misc.isList(anItem)) else anItem)
    ch = s[0] if (len(s) > 0) else ''
    has_slash1 = '/' in s
    has_slash2 = os.sep in s
    has_leading_slash1 = ch == '/'
    has_leading_slash2 = ch == os.sep
    if (anItem):
	slash = '/' if (has_leading_slash1) else os.sep if (has_leading_slash2) else ''
	_item = normalize_slashes(item,os.sep).replace(os.sep,'/' if (has_slash1) else os.sep)
	_s = ''
	_v = ''
	if (misc.isList(node[key])):
	    _s = node[key][0]
	    _v = slash + _item
	    node[key][0] = _v
	else:
	    _s = node[key]
	    _v = slash + _item
	    node[key] = _v
	print >>sys.stderr, '%s -> %s' % (_s,_v)

def callback(key,node):
    if (key == 'item'):
	img = get('image',node)
	img = normalize(img) if (img) else ''
	media = get('media',node)
	media = normalize(media) if (media) else ''
	_img = go_look_for_file_named(os.path.basename(img))
	if (_img) and (str(img) != str(_img)):
	    replace_node_item_using(node,'image',_img.replace(_dvd,''))
	_media = go_look_for_file_named(os.path.basename(media))
	if (media) and (str(media) != str(_media)):
	    replace_node_item_using(node,'media',_media.replace(_dvd,''))
	if (_img) and (_media):
	    __analysis__[os.path.splitext(_media)[-1]] = _img
	    pass
	pass

if (__name__ == '__main__'):
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--source=?':'path to the folder that contains all those files.',
	    '--dvd=?':'path to the dvd.',
	    '--target=?':'file type target for this process.',
	    }
    _argsObj = Args.Args(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = _argsObj.programName
	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	    _isVerbose = False
	    
	_isDebug = False
	try:
	    if _argsObj.booleans.has_key('isDebug'):
		_isDebug = _argsObj.booleans['isDebug']
	except:
	    pass
	
	_isRecurse = False
	try:
	    if _argsObj.booleans.has_key('isRecurse'):
		_isRecurse = _argsObj.booleans['isRecurse']
	except:
	    pass
	
	_isHelp = False
	try:
	    if _argsObj.booleans.has_key('isHelp'):
		_isHelp = _argsObj.booleans['isHelp']
	except:
	    pass
	
	if (_isHelp):
	    ppArgs()
	    sys.exit()
	    
	_source = ''
	try:
	    __source = _argsObj.arguments['source'] if _argsObj.arguments.has_key('source') else _source
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_source = __source
	
	_target = ''
	try:
	    __target = _argsObj.arguments['target'] if _argsObj.arguments.has_key('target') else _target
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_target = __target
	
	_dvd = ''
	try:
	    __dvd = _argsObj.arguments['dvd'] if _argsObj.arguments.has_key('dvd') else _dvd
	except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
	_dvd = __dvd
	
	if (_isVerbose):
	    print >> sys.stderr, '_isDebug=', _isDebug
	    print >> sys.stderr, '_source=', _source
	    print >> sys.stderr, '_target=', _target
	    print >> sys.stderr, '_dvd=', _dvd
	    
	if (os.path.exists(_source)):
	    import os, sys
	    import urllib
	    import simplejson
	    from vyperlogix.misc import _utils
	    
	    __analysis__ = lists.HashedLists()
	
	    xml = _utils.readFileFrom(_source)
	    xml = xml.replace('&',urllib.quote_plus('&'))
	    print 'Reading "%s".' % (_source)
	    data = XMLJSON.xml_to_python(xml,callback=callback) # ,callback=callback

	    json = XMLJSON.python_to_json(data)
	    #json = data.asJSONSerializable()
	    data2 = simplejson.loads(json)
	    
	    import pyxslt.serialize
	    xml2 = pyxslt.serialize.toString(rootTagName='data',prettyPrintXml=True,menu=data2)

	    fname2 = os.sep.join([os.path.dirname(__file__),os.path.basename(_source)])
	    print 'Writing "%s".' % (fname2)
	    _utils.writeFileFrom(fname2,xml2)
	    print 'Done !'
	else:
	    print >> sys.stderr, 'WARNING: Double-check your options, there is something wrong with the --source=? or --cmd=?'
	