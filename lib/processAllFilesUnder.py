import os

def deleteFile(root,fname):
	os.remove(os.path.join(root, fname))

def processAllFilesUnder(top,action=None,tag=''):
	try:
		for root, dirs, files in os.walk(top, topdown=False):
			if (str(action.__class__).find("'function'") > -1):
				try:
					action(root,dirs,files,tag)
				except Exception, details:
					print '(processAllFilesUnder) :: ERROR.2 :: (%s).' % (str(details))
	except Exception, details:
		print '(processAllFilesUnder) :: ERROR.1 :: (%s).' % (str(details))

def copyFile(fpath,tpath):
	# this copies files one byte at a time however the OS level copy function would be better to use...
	try:
		fHandSource = open(fpath,'rb')
		fHandDest = open(tpath,'wb')
		[fHandDest.write(ch) for l in fHandSource for ch in l]
		fHandDest.close()
		fHandSource.close()
	except:
		pass

def copyOSFileFromTo(source,dest):
	try:
		print 'CMD /K XCOPY "%s" "%s" /V' % (source,dest)
		#os.system()
	except:
		pass

def copyAllFilesUnderTo(source,target,action=None):
	try:
		for root, dirs, files in os.walk(source, topdown=True):
			for f in files:
				mask = root.replace(source,'')
				srcFName = root+os.sep+f
				dstFName = target+os.sep+mask+os.sep+f
				if (str(action.__class__).find("'function'") > -1):
					try:
						action(srcFName,dstFName)
					except Exception, details:
						print '(copyAllFilesUnderTo) :: ERROR.2 :: (%s).' % (str(details))
				else:
					copyOSFileFromTo(srcFName,dstFName)
	except Exception, details:
		print '(copyAllFilesUnderTo) :: ERROR.1 :: (%s).' % (str(details))
