from vyperlogix.classes.CooperativeClass import Cooperative

import sys, os, re
import imp
import traceback
import zipfile

import logging

from vyperlogix.misc import ObjectTypeName

from vyperlogix.logging import standardLogging
from vyperlogix.daemon.daemon import CustomLog
from vyperlogix.daemon.daemon import EchoLog

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

from vyperlogix.crypto import Encryptors

_isVerbose = False

_useBeautifulSoup = True

# To-Do:
# 
# (1) Make Encrypted Egg with only source to test this process. - DONE!
# (2) Study the ZipImport code to see how source is generally imported then replicate the process possibly by sub-classing the ZipImport code.

class ZipImporterEncrypted(Cooperative):
    class RemoteImporter(Cooperative):
        def __init__(self, path):
            self.__path__ = None
            self.__context__ = ZipImporterEncrypted.context()
            if self.context.re_url_ok.match(path):
                logging.warning("%s: accepting '%s'." % (ObjectTypeName.typeName(self),path))
                self.__path__ = path
                if (not self.path.endswith("/")):
                    self.path += '/'
            else:
                logging.error("%s: rejecting non-url path item: '%s'" % (ObjectTypeName.typeName(self),path))
                raise ImportError
    
        def context():
            doc = "context"
            def fget(self):
                return self.__context__
            return locals()    
        context = property(**context())

        def path():
            doc = "path"
            def fget(self):
                return self.__path__
            def fset(self,path):
                self.__path__ = path
            return locals()    
        path = property(**path())

        def find_module(self, fullname, mpath=None):
            """try to locate the remote module, do this:
             a) try to get fullname.py from http://self.path/
             b) try to get __init__.py from http://self.path/fullname/
            """
    
            fullname = fullname.split('.')[-1]
    
            for url, path in [
             (self.path + fullname + '.py',          None),
             (self.path + fullname + '/__init__.py', self.path + fullname + '/')]:
                try:
                    source = self.get_source(url)
                except Exception, e:
                    logging.error("find_module: failed to get '%s'. (%s)" % (url, e))
                else:
                    logging.info("find_module: got '%s'." % url)
                    return ZipImporterEncrypted.RemoteLoader(url, path, source)
    
            return None
    
        def get_source(self, url):
            """Download the source from given url.
            """
            from urllib2 import urlopen
    
            src = ''
    
            key = self.context.settings.get('ssl_key')
            cert = self.context.settings.get('ssl_cert')
            proto, host, port, path = self.context.re_url_split.findall(url)[0]
            try:
                port = int(port)
            except:
                port = 443
            
            if proto == 'https' and cert:
                # handle http over ssl with client certificate
                import httplib
                
                conn = httplib.HTTPSConnection(
                    host=host,
                    port=port,
                    key_file=key,
                    cert_file=cert,
                )
                
                conn.putrequest('GET', path)
                conn.endheaders()
                response = conn.getresponse()
                if response.status != 200:
                    raise StandardError, "HTTPS Error: %d"%response.status
                src = response.read()
            else:
                # handle everything else
                src = urlopen(url).read()
            
            src = src.replace("\r\n", "\n")    
            return src
            
    class RemoteLoader(Cooperative):
        def __init__(self, url, path, source):
            self.url = url
            self.path = path
            self.source = source
            self._files = {}
    
        def load_module(self, fullname):
            """add the new module to sys.modules,
            execute its source and return it
            """
    
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
    
            mod.__file__ = "%s" % self.url
            mod.__loader__ = self
            if self.path:
                mod.__path__ = [self.path]
    
            for line in self.source.split('\n'):
                logging.info(line)
    
            logging.warning("load_module: executing %s's source..." % fullname)
    
            exec self.source in mod.__dict__
    
            mod = sys.modules[fullname]
            return mod

    class EncryptedImporter(RemoteImporter):
        def __init__(self, path):
            self.__path__ = path
            self.__context__ = ZipImporterEncrypted.context()
            logging.warning("%s: accepting '%s'." % (ObjectTypeName.typeName(self),path))
    
        def find_module(self, fullname, mpath=None):
            """try to locate the remote module, do this:
             a) try to get fullname.py from http://self.path/
             b) try to get __init__.py from http://self.path/fullname/
            """
	    _paths = []
            fn = os.sep.join(fullname.split('.'))
            toks = fn.split(os.sep)
            while (len(toks) > 0):
                _fn = os.sep.join(toks)
                if (self.path.find(_fn) > -1):
                    fn.replace(_fn,'')
		    _paths.append(os.sep.join([self.path,'__init__.py']))
                    break
                del toks[-1]
	    _paths.append(os.sep.join([self.path,'%s.py' % fn]))
            for fqPath in _paths:
                try:
                    source = self.get_source(fqPath)
                except Exception, e:
                    logging.error("find_module: failed to get '%s'. (%s)" % (fqPath, e))
                    exc_info = sys.exc_info()
                    info_string = '\n'.join(traceback.format_exception(*exc_info))
                    logging.error(info_string)
                else:
                    logging.info("find_module: got '%s'." % fqPath)
                    return ZipImporterEncrypted.RemoteLoader(fqPath, os.path.dirname(fqPath), source)
    
            return None
    
        def _decryptBlowfish(self,str):
            s = [110,111,119,105,115,116,104,101,116,105,109,101,102,111,114,97,108,108,103,111,111,100,109,101,110,116,111,99,111,109,101,116,111,116,104,101,97,105,100,111,102,116,104,101,105,114,99,111,117,110,116,114,121]
            p = ''.join([chr(ch) for ch in s])
            return blowfish.decryptData(str,p)

        def decryptSimple(self,str):
            return Encryptors.decryptSimple(str)
        
        def get_source(self, fqPath):
            """Download the source from given fqPath.
            """
            src = ''
            _encryptor_method = None
            _fqPath = os.path.splitext(fqPath)[0]
            fqPaths = [s % _fqPath for s in ['%s.py','%s.pyc','%s.pyo']]
            s = list(set([s for s in sys.path if (fqPath.startswith(s)) or (os.path.splitext(s)[-1] in ['.egg','.zip'])]))
            print '(%s.%s) :: s=%s' % (self.__class__,misc.funcName(),s)
	    _sigName = 'EGG-INFO/signature'.lower()
            for p in s:
                print '(%s.%s) :: p=%s' % (self.__class__,misc.funcName(),p)
                if (not os.path.isdir(p)) and (os.path.exists(p)):
                    _zip = zipfile.ZipFile(p,'r',zipfile.ZIP_STORED)
		    try:
			print '(%s.%s) :: fqPath=%s' % (self.__class__,misc.funcName(),fqPath)
			zz = [f.filename for f in _zip.filelist if (f.filename.lower() == _sigName)]
			print '\n'.join(zz)
			if (len(zz) > 0):
			    _zz = [os.sep.join(f.filename.split('/')) for f in _zip.filelist]
			    files = [f for f in _zz if (not f.lower().startswith('egg-info/')) and (len([ff for ff in fqPaths if (ff.find(f) > -1)]) > 0)]
			    print '(%s.%s) :: files=%s' % (self.__class__,misc.funcName(),files)
			    if (len(files) > 0):
				print 'BEGIN:'
				cName = '/'.join(files[0].split(os.sep))
				print '(%s.%s) :: cName=%s' % (self.__class__,misc.funcName(),cName)
				contents = _zip.read(cName)
				if (_encryptor_method == None):
				    signature = _zip.read(zz[0])
				    if (signature in Encryptors.Encryptors):
					x = Encryptors.Encryptors(signature)
					if (x == Encryptors.Encryptors.simple):
					    src = Encryptors.decryptSimple(contents)
				print '(%s.%s) :: src=%s' % (self.__class__,misc.funcName(),src)
				print 'END!'
		    finally:
			_zip.close()
    
            src = src.replace("\r\n", "\n")    
            return src
            
        
    def __init__(self):
        self.__re_url_ok__ = re.compile(r'^http://|^ftp://|^https://')
        self.__re_url_split__ = re.compile('^(.+):\/\/(.+?)(?::(\d+))?(\/.*)$')
        self.__settings__ = sys.__dict__.setdefault(
            'urlimport_settings',
            {'ssl_cert': '', 'ssl_key': '', 'debug': 1}
        )
        ZipImporterEncrypted.context(self)
        logging.getLogger(ObjectTypeName.typeName(self))

	# unregister the zipimporter hook just to make sure we do not confuse the system...
        sys.path_hooks = [x for x in sys.path_hooks if x.__name__ != 'zipimporter']

        # register The Hooks
	sys.path_hooks = [x for x in sys.path_hooks if x.__name__ != 'RemoteImporter']
        sys.path_hooks.append(ZipImporterEncrypted.RemoteImporter)
        
        sys.path_hooks = [x for x in sys.path_hooks if x.__name__ != 'EncryptedImporter']
        sys.path_hooks.append(ZipImporterEncrypted.EncryptedImporter)

        logging.info('sys.path_hooks=%s' % ','.join([x.__name__ for x in sys.path_hooks]))

        sys.path_importer_cache.clear()
        
        logging.info("Url importing enabled. Add urls to sys.path.")
        logging.info("Use urlimport.config(key=value) to manipulate settings:")
        
        # print settings
        self.config()
        
        logging.info("This stuff is experimental, use at your own risk. Enjoy.")
        
    @classmethod
    def context(self,instance=None):
        ZipImporterEncrypted.__context__ = instance if (instance) else ZipImporterEncrypted.__context__
        return ZipImporterEncrypted.__context__
    
    def re_url_ok():
        doc = "re_url_ok"
        def fget(self):
            return self.__re_url_ok__
        def fset(self, regex):
            self.__re_url_ok__ = regex
        return locals()    
    re_url_ok = property(**re_url_ok())

    def re_url_split():
        doc = "re_url_split"
        def fget(self):
            return self.__re_url_split__
        def fset(self, regex):
            self.__re_url_split__ = regex
        return locals()    
    re_url_split = property(**re_url_split())
    
    def settings():
        doc = "settings"
        def fget(self):
            return self.__settings__
        def fset(self, regex):
            self.__settings__ = regex
        return locals()    
    settings = property(**settings())
    
    def config(self, **kwargs):
        """config(key=value) - Set key to value.
           config()          - Display settings.
        """
        self.settings.update(kwargs)
        for k,v in (kwargs or self.settings).iteritems():
            logging.info(" "+str(k)+"="+repr(v))

if (__name__ == '__main__'):
    def safely_mkdir_logs():
        _log_path = os.path.abspath('logs')
        if (not os.path.exists(_log_path)):
            os.mkdir(_log_path)
        return _log_path

    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'displays this help text.','--verbose':'output more stuff.'}
    _argsObj = Args.Args(args)
    if (_isVerbose):
	print '_argsObj=(%s)' % str(_argsObj)

    if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
	ppArgs()
    else:
	_progName = _argsObj.programName

	_isVerbose = False
	try:
	    if _argsObj.booleans.has_key('isVerbose'):
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
	    _isVerbose = False

	ver = _utils.getFloatVersionNumber()
	if (ver >= 2.5):
	    name = _utils.getProgramName()
	    _log_path = safely_mkdir_logs()
	    logFileName = os.sep.join([_log_path,'%s.log' % (name)])
	    
	    _stdLogging = EchoLog(open(logFileName,'w'), fOut=sys.stdout)
	    _logLogging = CustomLog(_stdLogging)
    
	    standardLogging.standardLogging(logFileName,_level=logging.ERROR,console_level=logging.INFO,isVerbose=True)
	    
	    _logLogging.logging = logging # echos the log back to the standard logging...
	    logging = _logLogging # replace the default logging with our own custom logging...
	    
	    i = ZipImporterEncrypted()
	    try:
		if (_useBeautifulSoup):
		    try:
			src_url = 'http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.0.7a.py'
			sys.path += [src_url]
			import BeautifulSoup
			BeautifulSoup
		    except Exception, e:
			print 'ERROR: Cannot import from "%s" because:' % (src_url)
			print _utils.formattedException(details=e)
			print '='*80

		print 'BEGIN-BEFORE: sys.path'
		for p in sys.path:
		    print p
		print 'END-BEFORE: sys.path'
		print
    
		try:
		    iLib = sys.path.index('z:\python projects\@lib')
		    if (iLib > -1):
			del sys.path[iLib]
			print 'INFO: VyperLogix Library was removed from sys.path.'
		    else:
			iLib = len(sys.path)
		except Exception, e:
		    print 'INFO: There was no need to remove VyperLogix Library from sys.path.'
		    
		print 'BEGIN-AFTER: sys.path'
		for p in sys.path:
		    print p
		print 'END-AFTER: sys.path'
		print

		sys.path_importer_cache.clear()

		try:
		    src_url = 'http://secure-code.vyperlogix.com/'
		    sys.path.insert(iLib,src_url)
		    
		    print 'BEGIN-AFTER-URL: sys.path'
		    for p in sys.path:
			print p
		    print 'END-AFTER-URL: sys.path'
		    print
    
		    from vyperlogix.products import keys
		    
		    s = 'now is the time'
		    e = keys._encode(s)
		    p = keys._decode(e)
		    print e, p
		    assert s == p, 'Oops, cannot validate that product keys can be encoded/decoded.'
		    
		    from vyperlogix.enum import Enum
		    
		    class MyTypes(Enum.EnumLazy):
			none = 0
			one = 1
			two = 2
			
		    print MyTypes.none, MyTypes.one, MyTypes.two
		except Exception, e:
		    print 'ERROR: Cannot import from "%s" because:' % (src_url)
		    print _utils.formattedException(details=e)
		    print '='*80

		# BEGIN: This code fails...
		#sys.path += [r'Z:\python projects\pyEggs\@lib\eVyperLogixLib-1.0-py2.5.egg']
		#print '\n'.join(sys.path)
		#from e.aima import utils
		#print utils.Dict(a=1,b=2,c=3)
		# END!   This code fails...
		
	    except ImportError:
		# To import from an exotic source we leave the source out of the normal path list and then notice when we cannot do the import.
		# Perform the import by reading the source and then do an "exec" to execute the source.
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.error('ImportError :: %s' % info_string)
	    except Exception, details:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		logging.error('%s :: %s' % (details,info_string))
	else:
	    print >> sys.stderr, 'ERROR - Cannot continue unless Python 2.5.x is being used, the current version is "%s" and this is unacceptable.' % ver
	pass
