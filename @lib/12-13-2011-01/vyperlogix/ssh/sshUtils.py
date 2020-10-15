"""
SSH support for win32 development to spoof accessing server based Linux resources.
"""

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import os
import sys
import traceback

from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc.ObjectTypeName import __typeName as ObjectTypeName__typeName
from vyperlogix.misc import _utils
from vyperlogix import misc

try:
    import paramiko
except ImportError, details:
    print 'WARNING due to "%s".' % str(details)

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
from vyperlogix.hash import lists
    
def calcXferRate(xfer_rate):
    xfer_factor = 1
    xfer_rate_calc = xfer_rate/1024
    xfer_rate_fmt = '%s KB/sec' % ('%-4.2f' % xfer_rate_calc).strip()
    if (xfer_rate_calc > 1024):
	xfer_factor = 1024
	xfer_rate_calc = xfer_rate/(1024*xfer_factor)
	xfer_rate_fmt = '%s MB/sec' % ('%-4.2f' % xfer_rate_calc).strip()
    return lists.HashedLists2({'xfer_rate':xfer_rate,'xfer_factor':xfer_factor,'xfer_rate_fmt':xfer_rate_fmt})

def giveXferStatus(iBytes,iTotal,xfer_rate,secs):
    if (iTotal > 0) and (xfer_rate > 0):
	xfer_rate_calc = calcXferRate(xfer_rate)
	print '(%2.2f%%) %s %s of %s in %4.2f seconds.' % ((float(iBytes)/float(iTotal))*100.0,xfer_rate_calc['xfer_rate_fmt'],iBytes,iTotal,((iTotal-iBytes)/(xfer_rate*xfer_rate_calc['xfer_factor'])))

class SSHConnection(Cooperative):
    def __init__(self,hostname='',port=22,username='',password='',isLazy=False):
	self.__lastError__ = StringIO()
	self.__hostname__ = hostname
	self.__port__ = port
	self.__username__ = username
	self.__password__ = password
	self.__transport__ = None
	self.__sftp__ = None
        self.__sep__ = '/'
	if (not isLazy):
	    self.ssh_connect_client()
	pass
    
    def __repr__(self):
	c = ObjectTypeName__typeName(self)
	return '%s(hostname="%s",port=%s,username="%s",password="...")' % (c,self.hostname,self.port,self.username)

    def __str__(self):
	return '%s@%s:%s' % (self.username,self.hostname,self.port)

    def sep():
        doc = "seperator for host file names"
        def fget(self):
            return self.__sep__
        return locals()
    sep = property(**sep())
    
    def transport():
        doc = "transport"
        def fget(self):
            return self.__transport__
        return locals()
    transport = property(**transport())
    
    def sftp():
        doc = "sftp"
        def fget(self):
	    if (self.__sftp__ is None):
		self.ssh_connect_client()
            return self.__sftp__
        return locals()
    sftp = property(**sftp())
    
    def hostname():
        doc = "hostname"
        def fget(self):
            return self.__hostname__
        def fset(self, hostname):
            self.__hostname__ = hostname
        return locals()
    hostname = property(**hostname())
    
    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        def fset(self, port):
            self.__port__ = port
        return locals()
    port = property(**port())

    def username():
        doc = "username"
        def fget(self):
            return self.__username__
        def fset(self, username):
            self.__username__ = username
        return locals()
    username = property(**username())

    def password():
        doc = "password"
        def fget(self):
            return self.__password__
        def fset(self, password):
            self.__password__ = password
        return locals()
    password = property(**password())

    def lastError():
	doc = "lastError message - use getvalue() to retrieve the message"
	def fget(self):
	    return self.__lastError__
	return locals()
    lastError = property(**lastError())

    def lastErrorMessage():
	doc = "lastError message"
	def fget(self):
	    return self.__lastError__.getvalue()
	return locals()
    lastErrorMessage = property(**lastErrorMessage())

    def ssh_connect_transport(self):
	""" Make an SSH connection with the server to mimic certain functions only for win32 platform to facilitate development.
	"""
	# get host key, if we know one
	hostkeytype = None
	hostkey = None
	try:
	    host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
	except IOError:
	    try:
		host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
	    except IOError:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		print >>self.lastError, '\n%s :: Cannot open host keys file, Reason: %s' % (ObjectTypeName.objectSignature(self),info_string)
		host_keys = {}
	if host_keys.has_key(self.hostname):
	    hostkeytype = host_keys[self.hostname].keys()[0]
	    hostkey = host_keys[self.hostname][hostkeytype]
	else:
	    print "%s :: Host key not found. Please create key manually using: ssh %s" % (misc.funcName(),self.hostname)
	# now, connect and use paramiko Transport to negotiate SSH2 across the connection
	try:
	    t = paramiko.Transport((self.hostname, self.port))
	    t.connect(username=self.username, password=self.password, hostkey=hostkey)
	except Exception, e:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>self.lastError, '\n%s :: Cannot open connection to %s:%s using username of "%s", Reason: %s' % (ObjectTypeName.objectSignature(self),self.hostname,self.port,self.username,info_string)
	    return None
	return t

    def ssh_connect_client(self):
	""" connect and use paramiko Transport to negotiate SSH2 across the connection
	"""
	self.__sftp__ = None
	if (self.transport is None):
	    self.__transport__ = self.ssh_connect_transport()
	if (self.__transport__ is not None):
	    try:
		self.__sftp__ = paramiko.SFTPClient.from_transport(self.transport)
	    except Exception, e:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		print >>self.lastError, '\n%s :: Cannot open client connection to %s:%s using username of "%s", Reason: %s' % (ObjectTypeName.objectSignature(self),self.hostname,self.port,self.username,info_string)
		try:
		    if (self.sftp is not None):
			ssh_close()
		except:
		    pass
		return None
	else:
	    return None
    
	return self.sftp

    def ssh_close(self):
	"""Close the previously opened client connection as obtained by ssh_connect_client()"""
	try:
	    self.sftp.close()
	    self.__sftp__ = None
	except:
	    pass
	try:
	    self.transport.close()
	    self.__transport__ = None
	except:
	    pass
	return

    def __ssh_listdir(self,dir_path):
	""" Perform directoy list against an SSH accessible server.
	"""
	if ((dir_path == None) or (dir_path == '')): 
	    dir_path = '.'
	try:
	    dirlist = self.sftp.listdir(dir_path)
	except:
	    return None
	return dirlist

    def listdir(self,pathName):
	"""
	Return a list containing the names of the entries in the given path. The list is in arbitrary order. It does not include the special entries '.' and '..' even if they are present in the folder. This method is meant to mirror os.listdir as closely as possible. For a list of full SFTPAttributes  objects, see listdir_attr.
	
	Parameters:
	    * path (str) - path to list (defaults to '.')
	
	Returns: list of str
	    list of filenames 	
	"""
	return self.__ssh_listdir(pathName)

    def normalize(self,dir_path):
	"""
	Return the normalized path (on the server) of a given path. This can be used to quickly resolve symbolic links or determine what the server is considering to be the "current folder" (by passing '.' as path).
	
	Parameters:
	    * path (str) - path to be normalized
	
	Returns: str
	    normalized form of the given path
	    
	Raises:
	    * IOError - if the path can't be resolved on the server
	"""
	if ((dir_path == None) or (dir_path == '')): 
	    dir_path = '.'
	try:
	    return self.sftp.normalize(dir_path)
	except:
	    return None
	return None

    def chdir(self,dir_path):
	"""
	Change the "current directory" of this SFTP session. Since SFTP doesn't really have the concept of a current working directory, this is emulated by paramiko. Once you use this method to set a working directory, all operations on this SFTPClient object will be relative to that path.
	
	Parameters:
	    * path (str) - new current working directory
	
	Raises:
	    * IOError - if the requested path doesn't exist on the server
	"""
	try:
	    return self.sftp.chdir(dir_path)
	except:
	    return None
	return None

    def chmod(self,path,mode):
	"""
	Change the mode (permissions) of a file. The permissions are unix-style and identical to those used by python's os.chmod function.
	
	Parameters:
	    * path (str) - path of the file to change the permissions of
	    * mode (int) - new permissions
	"""
	try:
	    return self.sftp.chmod(path,mode)
	except:
	    return None
	return None

    def chown(self,path,uid,gid):
	"""
	Change the owner (uid) and group (gid) of a file. As with python's os.chown function, you must pass both arguments, so if you only want to change one, use stat first to retrieve the current owner and group.
	
	Parameters:
	    * path (str) - path of the file to change the owner and group of
	    * uid (int) - new owner's uid
	    * gid (int) - new group id
	"""
	try:
	    return self.sftp.chown(path,uid,gid)
	except:
	    return None
	return None

    def close(self):
	"""
	Close the SFTP session and its underlying channel.
	"""
	return self.ssh_close()

    def get_channel(self):
	"""
	Return the underlying Channel object for this SFTP session. This might be useful for doing things like setting a timeout on the channel.
	
	Returns: Channel
	    the SSH channel 
	"""
	try:
	    return self.sftp.get_channel()
	except:
	    return None
	return None

    def getcwd(self):
	"""
	Return the "current working directory" for this SFTP session, as emulated by paramiko. If no directory has been set with chdir, this method will return None.
	
	Returns: str
	    the current working directory on the server, or None 	
	"""
	try:
	    f = self.sftp.getcwd()
	    return f if (f is not None) else self.home()
	except:
	    return None
	return None

    def listdir_attr(self,dir_path):
	"""
	Return a list containing SFTPAttributes objects corresponding to files in the given path. The list is in arbitrary order. It does not include the special entries '.' and '..' even if they are present in the folder.
	
	The returned SFTPAttributes objects will each have an additional field: longname, which may contain a formatted string of the file's attributes, in unix format. The content of this string will probably depend on the SFTP server implementation.
	
	Parameters:
	    * path (str) - path to list (defaults to '.')
	
	Returns: list of SFTPAttributes
	    list of attributes 	
	"""
	try:
	    return self.sftp.listdir_attr(dir_path)
	except:
	    return None
	return None

    def stat(self,dir_path):
	"""
	Retrieve information about a file on the remote system. The return value is an object whose attributes correspond to the attributes of python's stat structure as returned by os.stat, except that it contains fewer fields. An SFTP server may return as much or as little info as it wants, so the results may vary from server to server.
	
	Unlike a python stat object, the result may not be accessed as a tuple. This is mostly due to the author's slack factor.
	
	The fields supported are: st_mode, st_size, st_uid, st_gid, st_atime, and st_mtime.
	
	Parameters:
	
	    * path (str) - the filename to stat
	
	Returns: SFTPAttributes
	    an object containing attributes about the given file 	
	"""
	try:
	    return self.sftp.stat(dir_path)
	except:
	    return None
	return None
    
    def lstat(self,dir_path):
	"""
	Retrieve information about a file on the remote system, without following symbolic links (shortcuts). This otherwise behaves exactly the same as stat.
	
	Parameters:
	    * path (str) - the filename to stat
	
	Returns: SFTPAttributes
	    an object containing attributes about the given file 	
	"""
	try:
	    return self.sftp.lstat(dir_path)
	except:
	    return None
	return None
    
    def mkdir(self,dir_path,file_mode=0777):
	"""
	Create a folder (directory) named path with numeric mode mode. The default mode is 0777 (octal). On some systems, mode is ignored. Where it is used, the current umask value is first masked out.
	
	Parameters:
	    * path (str) - name of the folder to create
	    * mode (int) - permissions (posix-style) for the newly-created folder
	"""
	try:
	    return self.sftp.mkdir(dir_path,file_mode)
	except:
	    return None
	return None
    
    def file(self,filename,mode='r',bufsize=-1):
	"""
	Open a file on the remote server. The arguments are the same as for python's built-in file (aka open). A file-like object is returned, which closely mimics the behavior of a normal python file object.
	
	The mode indicates how the file is to be opened: 'r' for reading, 'w' for writing (truncating an existing file), 'a' for appending, 'r+' for reading/writing, 'w+' for reading/writing (truncating an existing file), 'a+' for reading/appending. The python 'b' flag is ignored, since SSH treats all files as binary. The 'U' flag is supported in a compatible way.
	
	Since 1.5.2, an 'x' flag indicates that the operation should only succeed if the file was created and did not previously exist. This has no direct mapping to python's file flags, but is commonly known as the O_EXCL flag in posix.
	
	The file will be buffered in standard python style by default, but can be altered with the bufsize parameter. 0 turns off buffering, 1 uses line buffering, and any number greater than 1 (>1) uses that specific buffer size.
	
	Parameters:
	    * filename (str) - name of the file to open
	    * mode (str) - mode (python-style) to open in
	    * bufsize (int) - desired buffering (-1 = default buffer size)
	
	Returns: SFTPFile
	    a file object representing the open file
	    
	Raises:
	    * IOError - if the file could not be opened.
	"""
	try:
	    return self.sftp.file(filename,mode,bufsize)
	except:
	    return None
	return None
    
    def open(self,filename,mode='r',bufsize=-1):
	"""
	Open a file on the remote server. The arguments are the same as for python's built-in file (aka open). A file-like object is returned, which closely mimics the behavior of a normal python file object.
	
	The mode indicates how the file is to be opened: 'r' for reading, 'w' for writing (truncating an existing file), 'a' for appending, 'r+' for reading/writing, 'w+' for reading/writing (truncating an existing file), 'a+' for reading/appending. The python 'b' flag is ignored, since SSH treats all files as binary. The 'U' flag is supported in a compatible way.
	
	Since 1.5.2, an 'x' flag indicates that the operation should only succeed if the file was created and did not previously exist. This has no direct mapping to python's file flags, but is commonly known as the O_EXCL flag in posix.
	
	The file will be buffered in standard python style by default, but can be altered with the bufsize parameter. 0 turns off buffering, 1 uses line buffering, and any number greater than 1 (>1) uses that specific buffer size.
	
	Parameters:
	    * filename (str) - name of the file to open
	    * mode (str) - mode (python-style) to open in
	    * bufsize (int) - desired buffering (-1 = default buffer size)
	
	Returns: SFTPFile
	    a file object representing the open file
	    
	Raises:
	    * IOError - if the file could not be opened.
	"""
	try:
	    return self.sftp.open(filename,mode,bufsize)
	except:
	    return None
	return None
    
    def get(self,remotepath,localpath,callback=None):
	"""
	Copy a remote file (remotepath) from the SFTP server to the local host as localpath. Any exception raised by operations will be passed through. This method is primarily provided as a convenience.
	
	Parameters:
	    * remotepath (str) - the remote file to copy
	    * localpath (str) - the destination path on the local host
	    * callback (function(int, int)) - optional callback function that accepts the bytes transferred so far and the total bytes to be transferred (since 1.7.4)
	"""
	try:
	    return self.sftp.get(remotepath,localpath,callback=None)
	except:
	    return None
	return None
    
    def put(self,localpath,remotepath,callback=None):
	"""
	Copy a local file (localpath) to the SFTP server as remotepath. Any exception raised by operations will be passed through. This method is primarily provided as a convenience.
	
	The SFTP operations use pipelining for speed.
	
	Parameters:
	    * localpath (str) - the local file to copy
	    * remotepath (str) - the destination path on the SFTP server
	    * callback (function(int iBytes, int iTotal, float xfer_rate, int elapsed_secs)) - optional callback function that accepts the bytes transferred so far and the total bytes to be transferred (since 1.7.4)
	
	Returns: SFTPAttributes
	    an object containing attributes about the given file (since 1.7.4) 	
	"""
	import time
	from vyperlogix.misc import _utils
	
	_begin_ts = time.time()
	_callback_ = None
	def _callback(iBytes,iTotal):
	    if (callable(_callback_)):
		et = time.time() - _begin_ts
		if (et == 0):
		    et = 0.00000000001
		xfer = iBytes / et
		try:
		    _callback_(iBytes,iTotal,xfer,et)
		except Exception, details:
		    print >>sys.stderr, '%s' % str(details)
	
	try:
	    if (not callable(callback)):
		callback = None
	    else:
		try:
		    callback(0,0,0,0)
		except Exception, details:
		    print >>sys.stderr, '%s :: Cannot use the callback because it has the following problem: "%s".' % (ObjectTypeName.objectSignature(self),str(details))
		    callback = None
	    if (callback is not None):
		_callback_ = callback
	    result = self.sftp.put(localpath,remotepath,_callback)
	    _end_ts = time.time()
	    _iTotal = result.st_size
	    xfer = _iTotal / (_end_ts - _begin_ts)
	    return [result,xfer]
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
	    return None
	return None
    
    def readlink(self,dir_path):
	"""
	Return the target of a symbolic link (shortcut). You can use symlink to create these. The result may be either an absolute or relative pathname.
	
	Parameters:
	    * path (str) - path of the symbolic link file
	
	Returns: str
	    target path 	
	"""
	try:
	    return self.sftp.readlink(dir_path)
	except:
	    return None
	return None
    
    def remove(self,dir_path):
	"""
	Remove the file at the given path. This only works on files; for removing folders (directories), use rmdir.
	
	Parameters:
	    * path (str) - path (absolute or relative) of the file to remove
	
	Raises:
	    * IOError - if the path refers to a folder (directory)
	"""
	try:
	    return self.sftp.remove(dir_path)
	except:
	    return None
	return None
    
    def rename(self,old_name,new_name):
	"""
	Rename a file or folder from oldpath to newpath.
	
	Parameters:
	    * oldpath (str) - existing name of the file or folder
	    * newpath (str) - new name for the file or folder
	
	Raises:
	    * IOError - if newpath is a folder, or something else goes wrong
	"""
	try:
	    return self.sftp.rename(old_name,new_name)
	except:
	    return None
	return None
    
    def rmdir(self,fname):
	"""
	Remove the folder named path.
	
	Parameters:
	    * path (str) - name of the folder to remove
	"""
	try:
	    return self.sftp.rmdir(fname)
	except:
	    return None
	return None
    
    def symlink(self,source,dest):
	"""
	Create a symbolic link (shortcut) of the source path at destination.
	
	Parameters:
	    * source (str) - path of the original file
	    * dest (str) - path of the newly created symlink
	"""
	try:
	    return self.sftp.symlink(source,dest)
	except:
	    return None
	return None
    
    def truncate(self,fname,fsize):
	"""
	Change the size of the file specified by path. This usually extends or shrinks the size of the file, just like the truncate() method on python file objects.
	
	Parameters:
	    * path (str) - path of the file to modify
	    * size (int or long) - the new size of the file
	"""
	try:
	    return self.sftp.truncate(fname,fsize)
	except:
	    return None
	return None
    
    def unlink(self,fname):
	"""
	Remove the file at the given path. This only works on files; for removing folders (directories), use rmdir.
	
	Parameters:
	    * path (str) - path (absolute or relative) of the file to remove
	
	Raises:
	    * IOError - if the path refers to a folder (directory)
	"""
	try:
	    return self.sftp.unlink(fname)
	except:
	    return None
	return None
    
    def utime(self,fname,times):
	""" 
	Set the access and modified times of the file specified by path. If times is None, then the file's access and modified times are set to the current time. Otherwise, times must be a 2-tuple of numbers, of the form (atime, mtime), which is used to set the access and modified times, respectively. This bizarre API is mimicked from python for the sake of consistency -- I apologize.

	Parameters:
	    * path (str) - path of the file to modify
	    * times (tuple(int)) - None or a tuple of (access time, modified time) in standard internet epoch time (seconds since 01 January 1970 GMT)
	"""
	try:
	    return self.sftp.utime(fname,times)
	except:
	    return None
	return None

    def home(self):
        """ home folder for current user """
        f = self.normalize(self.getcwd())
        toks = f.split(self.sep)
        t = toks[0:3]
        return self.sep.join(t)

    def isdir(self, pathName):
        """Test whether a remote path is a directory"""
        import stat
        try:
            st = self.stat(pathName)
            return False if (st == None) else stat.S_ISDIR(st.st_mode)
        except os.error:
            return False
        return False

    def islink(self, pathName):
        """Test whether a path is a symbolic link"""
        import stat
        try:
            st = self.lstat(pathName)
        except (os.error, AttributeError):
            return False
        return stat.S_ISLNK(st.st_mode)

    def walk(self, top, topdown=True, onerror=None):
        """Remote Directory tree generator.
    
        For each directory in the remote directory tree rooted at top (including top
        itself, but excluding '.' and '..'), yields a 3-tuple
    
            dirpath, dirnames, filenames
    
        dirpath is a string, the path to the directory.  dirnames is a list of
        the names of the subdirectories in dirpath (excluding '.' and '..').
        filenames is a list of the names of the non-directory files in dirpath.
        Note that the names in the lists are just names, with no path components.
        To get a full path (which begins with top) to a file or directory in
        dirpath, do os.path.join(dirpath, name).
    
        If optional arg 'topdown' is true or not specified, the triple for a
        directory is generated before the triples for any of its subdirectories
        (directories are generated top down).  If topdown is false, the triple
        for a directory is generated after the triples for all of its
        subdirectories (directories are generated bottom up).
    
        When topdown is true, the caller can modify the dirnames list in-place
        (e.g., via del or slice assignment), and walk will only recurse into the
        subdirectories whose names remain in dirnames; this can be used to prune
        the search, or to impose a specific order of visiting.  Modifying
        dirnames when topdown is false is ineffective, since the directories in
        dirnames have already been generated by the time dirnames itself is
        generated.
    
        By default errors from the os.listdir() call are ignored.  If
        optional arg 'onerror' is specified, it should be a function; it
        will be called with one argument, an os.error instance.  It can
        report the error to continue with the walk, or raise the exception
        to abort the walk.  Note that the filename is available as the
        filename attribute of the exception object.
    
        Caution:  if you pass a relative pathname for top, don't change the
        current working directory between resumptions of walk.  walk never
        changes the current directory, and assumes that the client doesn't
        either.
    
        Example:
    
        from os.path import join, getsize
        for root, dirs, files in walk('python/Lib/email'):
            print root, "consumes",
            print sum([getsize(join(root, name)) for name in files]),
            print "bytes in", len(files), "non-directory files"
            if 'CVS' in dirs:
                dirs.remove('CVS')  # don't visit CVS directories
        """
    
        from posixpath import join
    
        # We may not have read permission for top, in which case we can't
        # get a list of the files the directory contains.  os.path.walk
        # always suppressed the exception then, rather than blow up for a
        # minor reason when (say) a thousand readable directories are still
        # left to visit.  That logic is copied here.
        try:
            # Note that listdir and error are globals in this module due
            # to earlier import-*.
            names = self.listdir(top)
        except error, err:
            if (callable(onerror)):
                try:
                    onerror(err)
                except:
                    pass
            return
    
        dirs, nondirs = [], []
	if (names is not None):
	    for name in names:
		if self.isdir(join(top, name)):
		    dirs.append(name)
		else:
		    nondirs.append(name)
	
	    if topdown:
		yield top, dirs, nondirs
	    for name in dirs:
		path = join(top, name)
		if not self.islink(path):
		    for x in self.walk(path, topdown, onerror):
			yield x
	    if not topdown:
		yield top, dirs, nondirs
	else:
	    print '(%s) :: Possibly no files found at "%s".' % (ObjectTypeName.objectSignature(self),top)
    
    def searchForFolderNamed(self,fname,top='/'):
        """ Search for a folder of a specific name """
        for root, dirs, files in self.walk(top, topdown=True):
            if (fname in dirs):
                return self.sep.join([root,fname])
        return ''

    def exists(self,pathName):
        """ Perform os.path.exists().
        """
	return self.stat(pathName) != None
    
    def chmod_tree(self, path, mode, mask):
	'''Chmod the tree at path (Chmod recursively on a whole subtree)'''
	import stat
	def visit(arg, dirname, names):
	    mode, mask = arg
	    for name in names:
		fullname = self.sep.join([dirname, name])
		if not self.islink(fullname):
		    new_mode = (self.stat(fullname)[stat.ST_MODE] & ~mask) | mode
		    self.chmod(fullname, new_mode)
	self.walk(path, visit, (mode, mask))
    
    def fileSize(self,fname):
	if (self.exists(fname)):
	    st = self.stat(fname)
	    return st.st_size
	return -1

    def rmtree(self, path, ignore_errors=False, onerror=None):
	"""Recursively delete a directory tree.
    
	If ignore_errors is set, errors are ignored; otherwise, if onerror
	is set, it is called to handle the error with arguments (func,
	path, exc_info) where func is os.listdir, os.remove, or os.rmdir;
	path is the argument to that function that caused it to fail; and
	exc_info is a tuple returned by sys.exc_info().  If ignore_errors
	is false and onerror is None, an exception is raised.
    
	"""
	import sys, stat
	if ignore_errors:
	    def onerror(*args):
		pass
	elif onerror is None:
	    def onerror(*args):
		raise
	names = []
	try:
	    names = self.listdir(path)
	except os.error, err:
	    onerror(self.listdir, path, sys.exc_info())
	for name in names:
	    fullname = self.sep.join([path, name])
	    try:
		mode = self.lstat(fullname).st_mode
	    except os.error:
		mode = 0
	    if stat.S_ISDIR(mode):
		self.rmtree(fullname, ignore_errors, onerror)
	    else:
		try:
		    self.remove(fullname)
		except os.error, err:
		    onerror(self.remove, fullname, sys.exc_info())
	try:
	    self.rmdir(path)
	except os.error:
	    onerror(self.rmdir, path, sys.exc_info())
	    
    def safe_rmtree(dirname, retry=0):
	'''Remove the tree at DIRNAME (For clearing away read-only directories)'''
	import os, sys, time
	def rmtree(dirname):
	    self.chmod_tree(dirname, 0666, 0666)
	    self.rmtree(dirname)
    
	if not self.exists(dirname):
	    return
    
	if retry:
	    for delay in (0.5, 1, 2, 4):
		try:
		    self.rmtree(dirname)
		    break
		except:
		    time.sleep(delay)
	    else:
		self.rmtree(dirname)
	else:
	    self.rmtree(dirname)

def sftp_to_host(hostname,username,password,source,dest,isSilent=False):
    try:
	ssh = SSHConnection(hostname=hostname,username=username,password=password)
    except:
	exc_info = sys.exc_info()
	info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	print >>sys.stderr, info_string
    if (not isSilent):
	print 'ssh.transport = %s' % (ssh.transport)
    if (ssh.transport):
	results = [0,-1]
	try:
	    if (not isSilent):
		print 'ssh.isdir(%s)=%s' % (dest,ssh.isdir(dest))
	    if (ssh.isdir(dest)):
		dest = ssh.sep.join([dest,os.path.basename(source)])
	    if (not isSilent):
		print 'dest=%s' % (dest)
		print 'ssh.exists(%s)=%s' % (dest,ssh.exists(dest))
	    if (ssh.exists(dest)):
		if (not isSilent):
		    print 'ssh.remove(%s)' % (dest)
		ssh.remove(dest)
	    if (not isSilent):
		print 'SFTP "%s" to host as "%s".' % (source,dest)
	    results = ssh.put(source, dest, callback=giveXferStatus if (not isSilent) else None)
	except:
	    exc_info = sys.exc_info()
	    info_string = _utils.asMessage('\n'.join(traceback.format_exception(*exc_info)))
	    print >>sys.stderr, info_string
	finally:
	    xfer_rate_calc = lists.HashedLists2() if (results is None) else calcXferRate(results[-1])
	    if (not isSilent):
		print 'SFTP Done, %s, Closing Connection.' % (xfer_rate_calc['xfer_rate_fmt'])
	    ssh.close()
    else:
	print >>sys.stderr, 'Unable to get a connection with the server using "%s".' % ('%s,%s,%s' % (hostname,username,password))

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
