def copyZipFile(fname,adjustAnalysis=None,checkTypes=None,adjustTypes=None,adjustContents=None,postProcess=None,cleanup=None,zipPrefix='',acceptable_types=[]):
    import zipfile, os, sys, tempfile, types
    from vyperlogix.misc import _utils
    from vyperlogix.zip import getZipFilesAnalysis

    def _cleanup(fname,newName):
	if (os.path.exists(fname)) and (os.path.exists(newName)):
	    targetFolder = os.path.dirname(fname)
	    targetFname = os.sep.join([targetFolder,'copy%s'%(os.path.basename(fname))])
	    _utils.copyFile(newName,targetFname)
	else:
	    print >>sys.stderr, 'WARNING: Cannot copy the Zip file from "%s" to the target-folder of "%s".' % (fname,targetFname)
	pass
    
    new_tuple = tempfile.mkstemp('.zip','new')
    os.close(new_tuple[0])
    newName = new_tuple[-1]
    os.remove(newName)
    newName = newName.split('.')[0]
    os.mkdir(newName)
    tmpFolder = os.sep.join([newName,'zip'])
    newName = os.sep.join([newName,'new-file.zip'])
    if (not os.path.exists(tmpFolder)):
	os.mkdir(tmpFolder)
    _zip = zipfile.ZipFile(fname,'r',zipfile.ZIP_DEFLATED)
    newZip = zipfile.ZipFile(newName,'w',zipfile.ZIP_STORED)
    _analysis = getZipFilesAnalysis.getZipFilesAnalysis(_zip,prefix=zipPrefix,_acceptable_types=acceptable_types)
    if (callable(adjustAnalysis)):
	try:
	    _analysis = adjustAnalysis(_analysis)
	except:
	    pass
    for f,t in _analysis.iteritems():
	bool_t = True
	if (callable(checkTypes)):
	    try:
		bool_t = checkTypes(t)
	    except:
		bool_t = True
	if (bool_t):
	    if (callable(adjustTypes)):
		try:
		    t = adjustTypes(t)
		except:
		    pass
	    for tt in t:
		_f = '.'.join([f,tt]) if (len(tt) > 0) else f
		contents = _zip.read(_f)
		if (callable(adjustContents)):
		    try:
			contents = adjustContents(tt,_f,contents,_analysis)
		    except:
			pass
		tmpFile = os.sep.join([tmpFolder,_f.replace('/',os.sep)])
		try:
		    dname = os.path.dirname(tmpFile)
		    if (not os.path.exists(dname)):
			os.makedirs(dname)
		    _utils.writeFileFrom(tmpFile,contents)
		    newZip.write(tmpFile,_f,zipfile.ZIP_DEFLATED)
		finally:
		    try:
			os.remove(tmpFile)
		    except:
			pass
    if (callable(postProcess)):
	try:
	    postProcess(tmpFolder,_zip,newZip,_analysis)
	except:
	    pass
    _zip.close()
    newZip.close()
    _utils.removeAllFilesUnder(tmpFolder)
    if (os.path.exists(tmpFolder)):
	os.remove(tmpFolder)
    if (callable(cleanup)):
	try:
	    cleanup(fname,newName)
	except:
	    pass
    else:
	try:
	    _cleanup(fname,newName)
	except:
	    pass
    if (os.path.exists(newName)):
	os.remove(newName)
    try:
	newName = os.path.dirname(newName)
	os.rmdir(newName)
    except:
	pass
    pass

