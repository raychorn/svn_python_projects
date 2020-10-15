import os
import sys
from vyperlogix import utils

__pathName = 'data'

__fileNames = {}

__source_files_key = 'source_files'
__data_files_key = 'data_files'

def fileNames():
	return __fileNames

def isPackagesFile(fname):
	return ( (fname.find(__const_packages_symbol) > -1) and (fname.find(__const_unknown_packages_symbol) == -1) )

def isPublisherFile(fname):
	return (fname.find(__const_publishers_symbol) > -1)

def isUnknownPackagesFile(fname):
	return (fname.find(__const_unknown_packages_symbol) > -1)

def sourceFiles(matching=None):
	if (__fileNames.has_key(__source_files_key)):
		return __fileNames[__source_files_key] if matching == None else [f for f in __fileNames[__source_files_key] if f.find(matching) > -1]
	return []

def dataFiles():
	if (__fileNames.has_key(__data_files_key)):
		return __fileNames[__data_files_key]
	else:
		path = os.sep.join([os.path.abspath(os.curdir),__pathName])
		return [f for f in os.listdir(path) if (not os.path.isdir(os.sep.join([path,f])))]
	return []

def pathName():
	return __pathName

def __init__():
	path = os.path.abspath(os.curdir)
	__fileNames[__source_files_key] = [f for f in os.listdir(path) if f.startswith('#') and f.endswith('.txt') and utils.fileSize(os.sep.join([path,f])) < 10000000]
	print '(__init__) :: __fileNames[__source_files_key]=(%s)' % str(__fileNames[__source_files_key])
	if (not os.path.exists(__pathName)):
		os.mkdir(__pathName)

if (__name__ != '__main__'):
	if (len(__fileNames) == 0):
		__init__()
