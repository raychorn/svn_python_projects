import os
import sys

import logging
from logging import handlers

import imp
if (hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")):
    import zipfile
    import pkg_resources

    my_file = pkg_resources.resource_stream('__main__',sys.executable)
    print '%s' % (my_file)

    import tempfile
    __vyperlogix__ = tempfile.NamedTemporaryFile().name

    zip = zipfile.ZipFile(my_file)
    data = zip.read("vyperlogix_2_7.zip")
    file = open(__vyperlogix__, 'wb')
    file.write(data)
    file.flush()
    file.close()
    __vyperlogix__ = file.name
    print '__vyperlogix__ --> "%s".' % (__vyperlogix__)

    import zipextimporter
    zipextimporter.install()
    sys.path.insert(0, __vyperlogix__)

    print 'BEGIN:'
    for f in sys.path:
        print f
    print 'END !!'

from vyperlogix import misc

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

LOG_FILENAME = './windows-temporary-file-cleaner.log'

logger = logging.getLogger('windows-temporary-file-cleaner')
handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.INFO)

from vyperlogix.misc import _utils

__folders__ = ['C:/Temp', 'C:/Users/*/AppData/Local/Temp', 'C:/Windows/Temp']

def clean_temporary_files():
    for f in __folders__:
        if (f.find('*') > -1):
            ff = f.replace(os.sep,'/')
            while (ff.find('**') > -1):
                ff = ff.replace('**','*')
            toks = ff.split('*')
            # iterate the users...
            for top,dirs,files in _utils.walk(toks[0]):
                for d in dirs:
                    fpath = os.sep.join([top,d,toks[-1]]).replace(os.sep,'/').replace('//','/')
                    if (os.path.exists(fpath)) and (os.path.isdir(fpath)):
			for f in [os.sep.join([fpath,n]).replace(os.sep,'/') for n in os.listdir(fpath)]:
			    try:
				logger.info('Removing "%s".' % (f))
				_utils.removeAllFilesUnder(f)
			    except WindowsError:
				pass
			    pass
        else:
            for top,dirs,files in _utils.walk(f):
                for d in dirs:
                    fpath = os.sep.join([top,d])
                    if (os.path.exists(fpath)) and (os.path.isdir(fpath)):
			logger.info('Removing "%s".' % (fpath))
                        _utils.removeAllFilesUnder(fpath)

if (__name__ == '__main__'):
    def ppArgs():
        pArgs = [(k,args[k]) for k in args.keys()]
        pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
        pPretty.pprint()

    args = {'--help':'show some help.',
            '--verbose':'output more stuff.',
            '--debug':'debug some stuff.',
            '--folders=?':'list of additional folders to process.',
            }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
        ppArgs()
    else:
        _progName = __args__.programName

        _isVerbose = __args__.get_var('isVerbose',bool,False)
        _isDebug = __args__.get_var('isDebug',bool,False)
        _isHelp = __args__.get_var('isHelp',bool,False)

	_folders = __args__.get_var('folders',Args._str_,'')
	if (_isVerbose):
	    print >>sys.stdout, 'DEBUG: _folders=%s' % (_folders)
	_folders = _folders.split(',')

        if (_isHelp):
            ppArgs()
            sys.exit()

	for f in _folders:
	    if (os.path.exists(f)):
		__folders__.append(f)
	__folders__ = list(set(__folders__))
        clean_temporary_files()
