import re
import os, sys
import time
import logging
from StringIO import StringIO

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedLists

import json

__ignoring__ = ['.git']

__keywords__ = ['dashboardname']

__regexs__ = [re.compile(r"\s*%s\s*" % (k), flags=re.I) for k in __keywords__]
#__regexs__ = [re.compile(r"\s*%s\.\s*" % (k), flags=re.I) for k in __keywords__]

data = {}
__files__ = []

ioBuf = StringIO()

__re_words__ = re.compile("\W", re.UNICODE) #.split(s)

get_index = lambda d:d.get('index',{})

def read_file(fpath,keywords=[],read_contents=False):
    __index__ = HashedLists(fromDict={}, caseless=True)
    io = StringIO()
    if (os.path.exists(fpath) and os.path.isfile(fpath)):
	fn = open(fpath,mode='r')
	try:
	    lnum = 0
	    kwords = [k[0:4].lower() for k in keywords]
	    for l in fn:
		_l_ = str(l).rstrip()
		results = [w for w in __re_words__.split(_l_) if (w[0:4].lower() in kwords)]
		for r in results:
		    __index__[r] = lnum
		if (read_contents):
		    print >> io, _l_
		lnum += 1
	except Exception, ex:
	    logging.exception(ex.message)
	fn.close()
    content = io.getvalue().rstrip() if (read_contents) else fpath
    return {'content':content, 'index':json.dumps(__index__.asDict())}

def initialize(fpath,keywords=[]):
    logging.info('initialize.1 fpath=%s' % (fpath))
    
    for top,dirs,files in os.walk(fpath):
	if (len(files) > 0) and (all([top.find(t) == -1 for t in __ignoring__])):
	    logging.debug('%s has %s files.' % (top,len(files)))
	    _files = [os.sep.join([top,f]) for f in files if (not f.startswith('.'))]
	    for f in _files:
		__files__.append(f)
    
    outName = 'dashboard_templates.py'
    print >> ioBuf, '# %s\n' % (outName)
    #print >> ioBuf, '__index__ = {}\n'
    print >> ioBuf, '__templates__ = {}\n'
    for f in __files__:
	vector = read_file(f,keywords=keywords)
	# modify the content using the vector...
	print >> ioBuf, "__templates__['%s'] = {}" % (f)
	print >> ioBuf, "__templates__['%s']['content'] = '%s'" % (f,vector.get('content',''))
	print >> ioBuf, "__templates__['%s']['index'] = %s" % (f,vector.get('index',"{}"))
    fOut = open(outName,mode='w')
    try:
	print >> fOut, ioBuf.getvalue()
    except:
	pass
    finally:
	fOut.flush()
	fOut.close()
    return

does_directory_exist = lambda fname:(fname and os.path.exists(fname) and os.path.isdir(fname))

def replace_all(source,replacement=None,patterns=[]):
    if (misc.isStringValid(source) and misc.isStringValid(replacement) and misc.isIterable(patterns)):
	for r in patterns:
	    toks = r.search(source)
	    while (toks):
		try:
		    if (toks):
			token = source[toks.start():toks.end()]
			extra_token = _utils.non_alpha_numeric_only(replacement)
			if (misc.is_camel_case(token)):
			    replacement = str(replacement).capitalize()
			source = source[0:toks.start()] + replacement + extra_token + source[toks.end():]
			toks = r.search(source[toks.end():])
		    else:
			break
		except:
		    break
    return source

def write_content(source,dest,output=None,bias=None,dashboard_name=None,testing=True,keywords=[],regexs=[]):
    if (os.path.exists(source) and os.path.isfile(source)):
	if (dest):
	    is_bias_valid = does_directory_exist(bias)
	    if (not output) and (is_bias_valid):
		if (bias.endswith(os.sep)):
		    bias = bias[0:-1]
		toks = bias.split(os.sep)
		dname = toks.pop()
		dname = '%s-%s' % (dname,dashboard_name)
		output = os.sep.join(toks+[dname])
		if (not testing):
		    while (1):
			if (not os.path.exists(output)):
			    os.makedirs(output)
			    break
			elif (os.path.isfile(output)):
			    os.remove(output)
			else:
			    break
	    if (testing and output) or (does_directory_exist(output)):
		if (is_bias_valid):
		    try:
			basename = str(source).replace(bias,'')
			s = os.sep if (not basename.startswith(os.sep)) else ''
			output = ''.join([output,basename])
			output = replace_all(output, replacement=dashboard_name, patterns=regexs)
			if (testing):
			    logging.info('*** source=%s' % (source))
			    logging.info('*** output=%s' % (output))
			if (not testing):
			    f_source = open(source)
			    f_output = open(output, mode='w')
			else:
			    print 'BEGIN: %s' % ('-'*40)
			for line in f_source:
			    new_line = replace_all(line, replacement=dashboard_name, patterns=regexs)
			    if (testing):
				print new_line
			    else:
				print >> f_output, new_line
			if (not testing):
			    f_output.flush()
			    f_output.close()
			    f_source.close()
			else:
			    print 'END!!! %s\n' % ('-'*40)
		    except Exception, ex:
			logging.debug('EXCEPTION: %s' % (ex))
		else:
		    logging.warning('Cannot write content into directory "%s" due to missing or invalid bias so this is a programming logic error.' % (output))
	    else:
		logging.warning('%s write content into directory "%s"%s%s.' % ('Did not' if (testing) else 'Cannot ',output,' because -o has an invalid or missing value' if (not output) else ' due to some other UNKNOWN reason',' because using -t test mode' if (testing) else ' due to maybe you wanted to use test mode but forgot to use the -t option'))
	else:
	    logging.warning('Cannot write content into "%s".' % (dest))
    else:
	logging.warning('Cannot read content from "%s".' % (source))

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    program_name = __name__ if (__name__ != '__main__') else os.path.splitext(os.path.basename(sys.argv[0]))[0]
    LOG_FILENAME = './%s.log' % (program_name)
    logger = logging.getLogger(program_name)
    handler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler) 
    print 'Logging to "%s".' % (handler.baseFilename)
    
    ch = logging.StreamHandler()
    ch_format = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(ch_format)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    
    logging.getLogger().setLevel(logging.DEBUG)

    if (len(sys.argv) == 1):
	sys.argv.insert(len(sys.argv), '-h')
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-i", "--init", action="store", type="string", help="initialize the dashboard source files.", dest="input")
    parser.add_option("-n", "--name", action="store", type="string", help="dashboard name.", dest="name")
    parser.add_option("-o", "--out", action="store", type="string", help="output directory.", dest="output")
    parser.add_option('-t', '--test', dest='testmode', help="test mode - does everything but make a dashboard.", action="store_true")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    
    options, args = parser.parse_args()
    
    ___isVerbose____ = False
    if (options.verbose):
	_isVerbose = True
	
    __testmode__ = False
    if (options.testmode):
	__testmode__ = True
	    
    __default_dashboardname__ = __dashboardname__ = 'DashboardName'
    if (options.name):
	__dashboardname__ = options.name
    else:
	print >> sys.stderr, 'WARNING: Using the default dashboard name.'
	
    __has_dashboard_name_changed__ = (__dashboardname__ != __default_dashboardname__)
	
    __inputpath__ = None
    if (options.input):
	__inputpath__ = options.input
    else:
	print >> sys.stderr, 'WARNING: Nothing to use for initialization.'
	    
    __output__ = None
    if (options.output):
	__output__ = options.output
    #elif (__testmode__):
	#print >> sys.stderr, 'WARNING: Please specify -o (output) even when using -t.'
    #else:
	#print >> sys.stderr, 'WARNING: Please specify -o (output) or nothing happens.'
	#sys.exit(1)

    #if (__testmode__) and (__output__):
	#print >> sys.stderr, 'WARNING: Cannot specify both -t and -o at the same time because this is just confusion; you want to test and output together ?!?  Get a grip !'
		
    if (os.path.exists(__inputpath__) and os.path.isdir(__inputpath__)):
	initialize(__inputpath__,keywords=__keywords__)
    if (__has_dashboard_name_changed__):
	try:
	    import dashboard_templates
	    dt = dashboard_templates.__templates__
	    for k,v in dt.iteritems():
		v['__bias__'] = []
		v['fname'] = k.split(os.sep)
	    while (1):
		try:
		    if (len(v['fname']) > 0):
			t = v['fname'][0]
			has = True
			for k,v in dt.iteritems():
			    if (v['fname'][0] != t):
				has = False
				break
			if (has):
			    for k,v in dt.iteritems():
				v['fname'] = v['fname'][1:]
				v['__bias__'].append(t)
			else:
			    break
		    else:
			break
		except:
		    break
	    has = True
	    first = None
	    joined = False
	    for k,v in dt.iteritems():
		if (misc.isIterable(v['__bias__'])):
		    v['__bias__'] = os.sep.join(v['__bias__'])
		if (misc.isIterable(v['fname'])):
		    v['fname'] = os.sep.join(v['fname'])
		    joined = True
		if (not first):
		    first = v['__bias__']
		    if (not joined):
			v['fname'] = os.sep.join(v['fname'])
		elif (first != v['__bias__']):
		    has = False
		    logging.warning('Problem with bias in dashbaord_templates... Check your logic.')
		    break
	    has_files = False
	    if (has): #  and __testmode__
		# generate the dashboard...  show which filenames will change then which files will change.
		for k,v in dt.iteritems():
		    toks = v['fname'].split(os.sep)
		    if (any([t in __keywords__ for t in toks])):
			for kw in __keywords__:
			    k = k.replace(kw,__dashboardname__)
			#if (__testmode__):
			has_files = True
			print '-'*30
			print '--> %s' % (k)
			print '*** %s' % (v)
			c = v.get('content',None)
			if (c):
			    write_content(c, k, bias=first, dashboard_name=__dashboardname__, testing=__testmode__, keywords=__keywords__, regexs=__regexs__)
			else:
			    logging.warning('Cannot write content into "%s" from missing content source file.' % (k))
			print '-'*30
			print
		    indx = get_index(v)
		    if (len(indx) > 0):
			if (__testmode__):
			    print '!!! indx=%s' % (indx)
		pass
	    if (not has_files):
		logging.warning('Did not create any files due to possibly incorrect or invalid template.  Please correct this issue and try again.')
	    else:
		logging.error('Seems like you are not using a valid template.  Please make the required changes and rerun.')
	except ImportError, ex:
	    logging.exception(ex)
	pass
    else:
	logging.warning('Nothing more to do since no -n option was given.')
    sys.exit(1)

