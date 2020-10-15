import os
from os import stat
import sys
import lib.threadpool
import psyco
import lib.processAllFilesUnder

_isVerbose = False

_top_folder = ''

_base_folder = '\\public\\'

_target_folder = 'dss'

_svn_folder_name = '.svn'

_dos_cmd_name = 'dos.cmd'

S_IREAD = 256
S_IWRITE = 128

_pool = lib.threadpool.Pool(1000)

def explainMode(mode):
	explaination = []
	if (mode and S_IREAD):
		explaination.append('S_IREAD')
	if (mode and S_IWRITE):
		explaination.append('S_IWRITE')
	return ','.join(explaination)

def criteria(root,dirs,files,tag):
	if ( ( (len(dirs) == 0) and (len(files) == 0) ) or (root.find(_svn_folder_name) > -1) ):
		b_action_taken = False
		if (len(files) > 0):
			for f in files:
				try:
					fqName = root+os.sep+f
					os.chmod(fqName,S_IREAD|S_IWRITE)
					os.remove(fqName)
				except Exception, details:
					if (_isVerbose):
						print '(%s) :: (criteria) :: ERROR.1 (%s)' % (tag,str(details))
				b_action_taken = True
				if (_isVerbose):
					print '(%s) :: (criteria) :: os.remove(%s)' % (tag,root+os.sep+f)
		if (root.find(_svn_folder_name) > -1):
			toks = root.split(os.sep)
			while (len(toks) > 0):
				b_exiting = (toks[-1] == _svn_folder_name)
				p = os.sep.join(toks)
				try:
					os.rmdir(p)
				except:
					pass
				b_action_taken = True
				if (_isVerbose):
					print '(%s) :: (criteria) :: os.rmdir(%s)' % (tag,p)
				toks.pop()
				if (b_exiting):
					break
		if (b_action_taken == False):
			if ( (len(dirs) == 0) and (len(files) == 0) ):
				os.removedirs(root)
				b_action_taken = True
				if (_isVerbose):
					print '(%s) :: (criteria) :: os.rmdir(%s)' % (tag,root)
			if ( (b_action_taken == False) and (_isVerbose) ):
				print '(%s) :: (criteria) :: root=(%s), dirs=(%s), files=(%s)' % (tag,root,dirs,files)

def processAllFilesUnder(top,criteria):
	lib.processAllFilesUnder.processAllFilesUnder(top,criteria,tag='(1)')
	lib.processAllFilesUnder.processAllFilesUnder(top,criteria,tag='(2)')

def deleteFile(root,f):
	lib.processAllFilesUnder.deleteFile(root,f)

def deleteAction(root,dirs,files,tag):
	for f in files:
		deleteFile(root,f)
	for d in dirs:
		fq = root+os.sep+d
		if (os.path.exists(fq)):
			os.rmdir(fq)
	try:
		os.removedirs(root)
	except:
		pass

def deleteAllFilesUnder(top,criteria):
	lib.processAllFilesUnder.processAllFilesUnder(top,criteria)

def copyFileFromTo(source,dest):
	if (_isVerbose):
		print '(copyFileFromTo) :: source=(%s), dest=(%s)' % (source,dest)
	lib.processAllFilesUnder.copyOSFileFromTo(source,dest)

def copyAllFilesUnderTo(source,target,action):
	lib.processAllFilesUnder.copyAllFilesUnderTo(source,target,action)

def writeCmdFile(cmd):
	fHand = open(_dos_cmd_name,'w')
	fHand.writelines('%s\n' % cmd)
	fHand.close()

def main(top):
	print '(main) :: top=(%s)' % (top)
	processAllFilesUnder(top,criteria)
	_pool.join()
	baseFolder = top[0:top.find(_base_folder)+len(_base_folder)]
	if (baseFolder.endswith(os.sep) == False):
		baseFolder += os.sep
	fqTarget = baseFolder+_target_folder
	if (_isVerbose):
		print '(main) :: _base_folder=(%s), baseFolder=(%s), fqTarget=(%s)' % (_base_folder,baseFolder,fqTarget)
	if (os.path.exists(fqTarget)):
		deleteAllFilesUnder(fqTarget,deleteAction)
	if (os.path.exists(fqTarget) == False):
		os.mkdir(fqTarget)
	#print '(main) :: source=(%s), dest=(%s)' % (top,fqTarget)
	_cmd = 'XCOPY "%s%s*.*" "%s" /V /Y /O /S' % (top,os.sep,fqTarget+os.sep)
	print '(main) :: _cmd=(%s)' % (_cmd)
	_pool.join()
	writeCmdFile(_cmd)

if ( (len(sys.argv) == 1) or (sys.argv[1] == '--help') ):
	print '--help                      ... displays this help text.'
	print '--verbose                   ... output more stuff.'
	print '--folder=folder_name        ... top folder name.'
	print '--svn=svn_folder_name       ... svn folder name.'
	print '--base=base_folder_name     ... base folder name.'
	print '--target=target_folder_name ... target folder name.'
	print '--cmd=dos_cmd_name          ... dos command file name.'
else:
	for i in xrange(len(sys.argv)):
		bool = ( (sys.argv[i].find('--folder=') > -1) or (sys.argv[i].find('--svn=') > -1) or (sys.argv[i].find('--base=') > -1) or (sys.argv[i].find('--target=') > -1) or (sys.argv[i].find('--cmd=') > -1) )
		if (bool): 
			toks = sys.argv[i].split('=')
			if (sys.argv[i].find('--folder=') > -1):
				_top_folder = toks[1]
			elif (sys.argv[i].find('--svn=') > -1):
				_svn_folder_name = toks[1]
			elif (sys.argv[i].find('--base=') > -1):
				_base_folder = toks[1].replace(os.sep,'')
				if (_base_folder.startswith(os.sep) == False):
					_base_folder = os.sep + _base_folder
				if (_base_folder.endswith(os.sep) == False):
					_base_folder += os.sep
			elif (sys.argv[i].find('--target=') > -1):
				_target_folder = toks[1].replace(os.sep,'')
			elif (sys.argv[i].find('--cmd=') > -1):
				_dos_cmd_name = toks[1]
		elif (sys.argv[i].find('--verbose') > -1):
			_isVerbose = True
	psyco.bind(main)
	main(_top_folder)
