import os, sys
import re

import zipfile

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.daemon.daemon import Log
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix import oodb

from vyperlogix.hash import lists

from vyperlogix.misc import threadpool

from vyperlogix.enum.Enum import Enum

import sys

from vyperlogix import oodb
dbx_name = lambda fpath,name:oodb.dbx_name(name,fpath)

import sqlalchemy_model

from vyperlogix.classes.CooperativeClass import Cooperative

_log_path = os.path.join(os.path.dirname(sys.argv[0]),'logs')

_utils._makeDirs(_log_path)

_logFile = open(os.path.join(_log_path, '%s_%s.txt' % (os.path.basename(sys.argv[0]),_utils.timeStampLocalTime(format=_utils.formatSalesForceDateTimeStr()).replace(' ','_').replace(':','_'))),'w')
_log = EchoLog(_logFile)

begin_ts = None

_Q_ = threadpool.ThreadQueue(5)

class NodeFactory(Cooperative):
    def __init__(self):
	pass
	
    def make_node(self,_id=-1,_parent=-1,_name='',_creation_date=_utils.timeStampLocalTime(),_modification_date=_utils.timeStampLocalTime(),_is_active=False,_is_file=False,_is_url=False):
	return sqlalchemy_model.Node(id=_id,name=_name,parent=_parent,creation_date=sqlalchemy_model.default_date(_creation_date),modification_date=sqlalchemy_model.default_date(_modification_date),is_active=_is_active,is_file=_is_file,is_url=_is_url)

_is_running_local = True

conn_str = sqlalchemy_model.get_conn_str(logger=_log)
    
agent = sqlalchemy_model.get_sql_agent(conn_str,logger=_log)
    
_factory = NodeFactory()

top = r'Z:\@myFiles\@Python'

pattern = '@python'

svnFilter = '[._]svn' 
rxSVN=re.compile(svnFilter)

py26Filter = '@Python_2.6a3' 
rxPy26=re.compile(py26Filter)

filter = lambda f:(f.lower().find(pattern) > -1)

class Methods(Enum):
    none = 0
    use_mySQL = 1
    use_fast = 2

def normalize_fpath(top,fpath):
    _is_file_ = os.path.isfile(fpath)
    return (fpath.replace(top,''),_is_file_)

def root_folders(_top,_filter=None):
    files = os.listdir(_top)
    return [os.sep.join([_top,f]) for f in files if (not callable(_filter)) or ((callable(_filter)) and _filter(f))]

def process_name(cls,d_url,_rr_,_name,isInternetShortcut=False,logger=sys.stderr):
    '''
    This function CANNOT be run in the background via any kind of threading mechanism because the state of the parent
    depends on the number of records in the database.
    '''
    import os, sys
    from vyperlogix.misc import _utils

    sess = agent.new_session()
    if (sess is None):
	print >>logger, '1. LAST_ERROR :: %s' % (agent.lastError)
	return
    agent.use_session(sess)
    if (agent.session is None):
	print >>logger, '2. LAST_ERROR :: %s' % (agent.lastError)
	return
    print >>logger, 'BEGIN: Session %s' % (sess)
    try:
	s_name,_is_file_ = normalize_fpath(_rr_,_name)
	print >>logger, '\t%s' % (s_name)
	_parent = -1
	num_recs = agent.session.query(cls).count()
	nodes = s_name.split(os.sep)
	for s in nodes[0:-1]:
	    if (len(s) == 0):
		continue
	    rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=s, parent=_parent)
	    print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),s,_parent)
	    if (rec.count() == 0):
		_id = num_recs+1
		aNode = _factory.make_node(_id=_id,_parent=_parent,_name=s,_creation_date=None,_modification_date=None,_is_active=True,_is_file=False,_is_url=False)
		agent.add(aNode)
		agent.flush()
		print >>logger, '1. Commit. aNode is %s' % (str(aNode))
		print >>logger, '='*80
		print >>logger, '\n'
		_parent = _id
		num_recs += 1
	    else:
		aNode = rec.first()
		_parent = aNode.id
	if (not isInternetShortcut):
	    _id = num_recs+1
	    rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=nodes[-1], parent=_parent)
	    print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),nodes[-1],_parent)
	    if (rec.count() == 0):
		aNode = _factory.make_node(_id=_id,_parent=_parent,_name=nodes[-1],_creation_date=None,_modification_date=None,_is_active=True,_is_file=_is_file_,_is_url=False)
		agent.add(aNode)
		agent.flush()
		print >>logger, '2. Commit. aNode is %s' % (str(aNode))
		print >>logger, '='*80
		print >>logger, '\n'
	else:
	    _id = num_recs+1
	    for k,v in d_url.iteritems():
		rec = agent.session.query(cls).filter("name=:name and parent=:parent").params(name=v, parent=_parent)
		print >>logger, 'rec.count()=%s, name is "%s", parent is "%s".' % (rec.count(),v,_parent)
		if (rec.count() == 0):
		    aNode = _factory.make_node(_id=_id,_parent=_parent,_name=v,_creation_date=None,_modification_date=None,_is_active=True,_is_file=False,_is_url=True)
		    agent.add(aNode)
		    agent.flush()
		    print >>logger, '3. Commit. aNode is %s' % (str(aNode))
		    print >>logger, '='*80
		    print >>logger, '\n'
    except Exception, details:
	from vyperlogix.misc import _utils
	info_string = _utils.formattedException(details=details)
	print >>logger, info_string
    finally:
	print >>logger, 'END!  Session %s' % (sess)
	agent.destroy_session(sess)
	logger.flush()
	logger.close()
	pass

def walk_folder(top,zipPrefix=None,callback=None,zipFile=None,status_callback=None,logger=sys.stderr):
    for root, dirs, files in _utils.walk(top,rejecting_re=rxSVN):
	i2 = 1
	n2 = len(files)
	_root = root.split(os.sep)[-1]
	for f in files:
	    _f = os.sep.join([root,f])
	    pcent2 = (float(i2) / float(n2)) * 100.0
	    curr_ts = _utils.timeSeconds()
	    et_ts = curr_ts - begin_ts
	    x_et_ts2 = (float(et_ts) * 100.0) / pcent2
	    s_et_ts2 = '%-10.2f'%x_et_ts2
	    s_et_ts2 = s_et_ts2.strip()
	    if (callable(status_callback)):
		try:
		    status_callback(pcent,pcent2)
		except Exception, details:
		    info_string = _utils.formattedException(details=details)
		    print >>log, info_string
		    print >>sys.stderr, info_string
	    info_string = 'BEGIN: (%2.0f%%) (%s secs remain) "%s"' % (pcent2,s_et_ts2,_root)
	    print >>logger, info_string
	    d_parent = None
	    for name in files:
		_name = os.sep.join([root,name])
		_url = _utils.parse_InternetShortcut(_name)
		isInternetShortcut = len(_url) > 0
		if (isInternetShortcut):
		    info_string = '%s' % (_url)
		    print >>logger, info_string
		if (callable(callback)):
		    try:
			callback(root,_name,zipPrefix,zipFile,_url,isInternetShortcut=isInternetShortcut,logger=logger)
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			print >>logger, info_string
	    info_string = 'END! (%2.0f%%) (%s secs remain) "%s"' % (pcent2,s_et_ts2,_root)
	    print >>logger, info_string
	    print >>logger, '='*80
	    print >>logger, '\n'

def handle_file(root,name,zipPrefix,zipFile,_url='',isInternetShortcut=False,logger=sys.stderr):
    from vyperlogix.lists.ListWrapper import ListWrapper
    if (not isInternetShortcut):
	l = ListWrapper(name.split(os.sep))
	i = l.findFirstContaining(zipPrefix)
	srcname = ''
	if (i > -1):
	    srcname = os.sep.join(l[i:])
	try:
	    print >>logger, '%s :: %s --> %s' % (misc.funcName(),name,srcname)
	    zipFile.write(name,srcname,zipfile.ZIP_DEFLATED)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>logger, info_string
    else:
	l = ListWrapper(zipFile.filename.split(os.sep))
	i = l.findFirstContaining('zips')
	dest = ''
	if (i > -1):
	    dest = os.sep.join(l[0:i])
	links_filename = os.path.join(dest,'links','links_%s.txt' % (zipPrefix))
	_utils.makeDirs(links_filename)
	fOut = open(links_filename,'w')
	try:
	    print >>logger, '%s :: url --> %s' % (misc.funcName(),_url)
	    print >>fOut, '%s\n' % (_url)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>logger, info_string
	finally:
	    fOut.flush()
	    fOut.close()

@threadpool.threadify(_Q_)
def process_zipfile(dest,fpath,fname,logger=sys.stderr):
    zip_filename = os.path.join(dest,'zips','.'.join([fname,'zip']))
    _utils.makeDirs(zip_filename)
    if (_isUse_7z) and (os.path.exists(_7z)):
	print >>logger, '%s :: %s --> %s' % (misc.funcName(),_7z,zip_filename)
	_cmd = '%s %s "%s" "%s"' % (_7z,_7z_options,zip_filename,fpath)
	print >>logger, '%s :: command --> %s' % (misc.funcName(),_cmd)
	logger2 = Log(open(zip_filename.replace('.zip','.txt'),'w'))
	try:
	    _utils.spawnProcessWithDetails(_cmd,fOut=logger2)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>logger, info_string
	finally:
	    logger2.flush()
	    logger2.close()
    else:
	print >>logger, '%s :: OPEN ZIP --> %s' % (misc.funcName(),zip_filename)
	_Z_ = zipfile.ZipFile(zip_filename,'w',zipfile.ZIP_DEFLATED,allowZip64=True)
	try:
	    walk_folder(fpath,zipPrefix=fname,callback=handle_file,zipFile=_Z_)
	except Exception, details:
	    info_string = _utils.formattedException(details=details)
	    print >>logger, info_string
	finally:
	    print >>logger, '%s :: CLOSE ZIP --> %s' % (misc.funcName(),zip_filename)
	    _Z_.close()

def process_name_quickly(cls,d_url,top,fpath,dest=None,isInternetShortcut=False,logger=sys.stderr):
    '''
    This function CANNOT be run in the background via any kind of threading mechanism because the state of the parent
    depends on the number of records in the database.
    '''
    fname,is_file = normalize_fpath(top,fpath)
    
    fname = os.sep.join([n for n in fname.split(os.sep) if (len(n) > 0)])
    process_zipfile(dest,fpath,fname,logger=logger)
    
    print >>logger, '%s' % (misc.funcName())
    print >>logger, 'top --> %s' % (top)
    print >>logger, 'fpath --> %s' % (fpath)
    print >>logger, 'fname --> %s' % (fname)
    print >>logger, 'dest --> %s' % (dest)
    print >>logger, '='*80
    print >>logger, '\n'

def main(method,processor=process_name,status_callback=None,dest=None,log=sys.stdout):
    global begin_ts
    _files = root_folders(top)
    i = 1
    n = len(_files)
    begin_ts = _utils.timeSeconds()
    try:
	#_rr_ = os.path.dirname(top)
	_rr_ = top
	for _r_ in _files:
	    if (method == Methods.use_fast):
		if (callable(processor)):
		    try:
			processor(sqlalchemy_model.Node,{},_rr_,_r_,dest=dest,logger=log)
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			print >>log, info_string
			print >>sys.stderr, info_string
	    elif (method == Methods.use_mySQL):
		pass
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>logger, info_string
    info_string = 'DONE !!!'
    print >>log, info_string
    print >>sys.stderr, info_string

if (__name__ == '__main__'):
    from vyperlogix.misc import Args
    from vyperlogix.misc import PrettyPrint

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--mysql':'use mySQL.',
	    '--fast':'fast processor.',
	    '--threads=?':'the number of threads between 5 and 1000.',
	    '--src=?':'source for the folder scan.',
	    '--dest=?':'destination for the output files.',
	    '--use_7z':'use the 7z program when zipping.',
	    '--7z=?':'path to the 7z program.',
	    }
    _argsObj = Args.Args(args)

    _progName = _argsObj.programName
    _isHelp = False
    try:
	if _argsObj.booleans.has_key('isHelp'):
	    _isHelp = _argsObj.booleans['isHelp']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isHelp = False
	
    _isMySQL = False
    try:
	if _argsObj.booleans.has_key('isMysql'):
	    _isMySQL = _argsObj.booleans['isMysql']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isMySQL = False
    
    _isUse_7z = False
    try:
	if _argsObj.booleans.has_key('isUse_7z'):
	    _isUse_7z = _argsObj.booleans['isUse_7z']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isUse_7z = False
    
    _isFast = False
    try:
	if _argsObj.booleans.has_key('isFast'):
	    _isFast = _argsObj.booleans['isFast']
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
	_isFast = False
	
    __threads__ = 5
    try:
	__threads = _argsObj.arguments['threads'] if _argsObj.arguments.has_key('threads') else __threads__
	__threads__ = int(__threads)
    except Exception, details:
	__threads__ = 5
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _threads = __threads__
    
    if (_threads > 5) and (_threads <= 1000):
	_Q_ = threadpool.ThreadQueue(_threads)

    __dest__ = os.path.dirname(sys.argv[0])
    try:
	__dest = _argsObj.arguments['dest'] if _argsObj.arguments.has_key('dest') else __dest__
	__dest__ = __dest
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _dest = __dest__
    
    if (os.path.isfile(_dest)):
	_utils.makeDirs(_dest)
    else:
	_utils._makeDirs(_dest)

    __src__ = top
    try:
	__src = _argsObj.arguments['src'] if _argsObj.arguments.has_key('src') else __src__
	__src__ = __src
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _src = __src__
    
    __7z__ = r'C:\Program Files (x86)\7-Zip\7z.exe'
    try:
	__7z = _argsObj.arguments['7z'] if _argsObj.arguments.has_key('7z') else __7z__
	__7z__ = __7z
    except Exception, details:
	info_string = _utils.formattedException(details=details)
	print >>sys.stderr, info_string
    _7z = __7z__
    
    _7z_options = "a -r -v100k -x!.svn -tzip -y -aoa -mx9:m=Deflate64"
    
    if (_isHelp):
	ppArgs()
    
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    method = Methods.none
    processor = None
    if (_isMySQL):
	method = Methods.use_mySQL
	processor = process_name
    elif (_isFast):
	method = Methods.use_fast
	processor = process_name_quickly
	print >>_log, '\n'
    if (processor is not None):
	main(method,processor=processor,dest=_dest,log=_log)
	print >>_log, 'Waiting for threads to complete...'
	_Q_.join()
    else:
	print >>sys.stderr, '%s :: Nothing to do.' % (misc.funcName())
