from vyperlogix.enum import Enum
from vyperlogix.misc import _utils

class PathCollectionOptions(Enum.Enum):
    collect_files = 1
    collect_dirs = 2

def _collectFromPath(fpath,option=PathCollectionOptions.collect_files,rejecting_re=None):
    '''See the PathCollectionOptions for the details.'''
    import os
    import logging
    from vyperlogix.hash import lists
    d_files = lists.HashedLists2()
    if (os.path.exists(fpath)):
	for root, dirs, files in _utils.walk(fpath, topdown=True, rejecting_re=rejecting_re):
	    if (option.value == PathCollectionOptions.collect_files.value):
		for f in files:
		    _fname = os.sep.join([root,f])
		    d_files[_fname] = _fname
	    elif (option.value == PathCollectionOptions.collect_dirs.value):
		d_files[root] = dirs
    return d_files

def collectFilesFromPath(fpath,rejecting_re=None):
    return _collectFromPath(fpath,PathCollectionOptions.collect_files,rejecting_re=rejecting_re)

def collectDirsFromPath(fpath,rejecting_re=None):
    return _collectFromPath(fpath,PathCollectionOptions.collect_dirs,rejecting_re=rejecting_re)

