import os

def deleteFile(root,fname):
	os.remove(os.path.join(root, fname))

def deleteAllFilesUnder(folderName):
	try:
		for root, dirs, files in os.walk(folderName, topdown=False):
			for name in files:
				deleteFile(root, name)
			for dir in dirs:
				os.rmdir(root+os.sep+dir)
		os.removedirs(folderName)
	except:
		pass

