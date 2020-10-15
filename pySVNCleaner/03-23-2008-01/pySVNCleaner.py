from vyperlogix import google
from vyperlogix import oodb
import datetime
import os
import sys
import stat
from vyperlogix import _utils
from vyperlogix import Args
from vyperlogix import PrettyPrint

_isVerbose = False

def deleteFile(root,fname):
	f = os.sep.join([root, fname])
	os.chmod(f,stat.S_IWRITE)
	os.remove(f)
	
def deleteFiles(root):
	fnames = os.listdir(root)
	for f in fnames:
		if (_isVerbose):
			print 'deleteFile(%s, %s)' % (root, f)
		else:
			deleteFile(root, f)

def cleanFolders(p,s):
	try:
		p = p.replace('/',os.sep)
		for root, dirs, files in os.walk(p, topdown=False):
			for name in files:
				if (name.find(s) > -1):
					if (_isVerbose):
						print 'deleteFile(%s, %s)' % (root, name)
					else:
						deleteFile(root, name)
			for dir in dirs:
				if (dir.startswith(s)):
					if (_isVerbose):
						print 'os.removedirs(%s)' % (os.sep.join([root,dir]))
					else:
						f = os.sep.join([root,dir])
						deleteFiles(f)
						os.removedirs(f)
			if (root.find(os.sep+s+os.sep) > -1):
				if (_isVerbose):
					print 'os.rmdir(%s)' % (root)
				else:
					deleteFiles(root)
					os.rmdir(root)
	except Exception, details:
		print 'ERROR due to "%s".' % str(details)

def main():
	global _isVerbose
	
	args = {'--help':'displays this help text.','--verbose':'output more stuff.','--path=path_spec':'specify the path for the top of the folder tree.','--prefix=prefix_spec':'specify the prefix, usually ".svn" or "_svn" or whatever patches your specific needs.'}
	_argsObj = Args.Args(args)
	print >>sys.stderr, '_argsObj=(%s)' % str(_argsObj)
    
	if ( (len(sys.argv) == 1) or (sys.argv[-1] == args.keys()[0]) ):
		pArgs = [(k,args[k]) for k in args.keys()]
		pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
		pPretty.pprint()
    
	try:
		_isVerbose = _argsObj.booleans['isVerbose']
	except:
		_isVerbose = False
	
	_path = ''
	try:
		_path = _argsObj.arguments['path']
	except:
		pass
	
	_prefix = '.svn'
	try:
		_prefix = _argsObj.arguments['prefix']
	except:
		pass
	
	if (len(_path) > 0) and (len(_prefix) > 0):
		print 'Processing %s and all children removing files beginning with "%s" in a %s manner.' % (_path,_prefix,'verbose' if _isVerbose else 'quiet')
		cleanFolders(_path,_prefix)
	else:
		print "Seems as though you didn't specify a path spec for the top of the folder tree for which you want to remove all that SVN crap along with a prefix to tell the system what files belong to the set of SVN crap."
    
if (__name__ == '__main__'):
	from vyperlogix import _psyco
	_psyco.importPsycoIfPossible()
	if (_utils.getVersionNumber() >= 251):
		main()
	else:
		print 'You seem to be using the wrong version of Python, try using 2.5.1 or later rather than "%s".' % sys.version.split()[0]
