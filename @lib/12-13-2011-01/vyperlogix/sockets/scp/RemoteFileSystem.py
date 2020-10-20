__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
import os, sys

import ujson

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.enum.Enum import Enum

__json__ = os.path.abspath('./files-json.txt')

class Methods(Enum):
    recusive = 1
    nonrecusive = 2
    flat = 4
    testing = 8

class RemoteScp():
    def __init__(self,host,port,user,pwd,remote,method=Methods.flat,logPath=None):
        self.__host__ = host
        self.__port__ = port
        self.__user__ = user
        self.__pwd__ = pwd
        self.__remote_path__ = remote
        self.__method__ = method
        self.__logPath__ = logPath

    def host():
        doc = "host"
        def fget(self):
            return self.__host__
        def fset(self, host):
            self.__host__ = host
        return locals()
    host = property(**host())

    def port():
        doc = "port"
        def fget(self):
            return self.__port__
        def fset(self, port):
            self.__port__ = port
        return locals()
    port = property(**port())

    def user():
        doc = "user"
        def fget(self):
            return self.__user__
        def fset(self, user):
            self.__user__ = user
        return locals()
    user = property(**user())

    def pwd():
        doc = "pwd"
        def fget(self):
            return self.__pwd__
        def fset(self, pwd):
            self.__pwd__ = pwd
        return locals()
    pwd = property(**pwd())

    def remote():
        doc = "remote"
        def fget(self):
            return self.__remote_path__
        def fset(self, remote):
            self.__remote_path__ = pwd
        return locals()
    remote = property(**remote())

    def method():
        doc = "method"
        def fget(self):
            return self.__method__
        def fset(self, method):
            self.__method__ = method
        return locals()
    method = property(**method())

    def logPath():
        doc = "logPath"
        def fget(self):
            return self.__logPath__
        def fset(self, logPath):
            self.__logPath__ = logPath
        return locals()
    logPath = property(**logPath())

    def store_in_bucket_recursive(self,bucket={},fp=None):

        def packit(fp):
            toks = [t for t in fp.split('/') if t]
            ret = fp
            for tok in reversed(toks):
                ret = {tok: ret}
            return ret
        
        def merge(d1, d2):
            for k1,v1 in d1.iteritems():
                if not k1 in d2:
                    d2[k1] = v1
                elif misc.isDict(v1):
                    merge(v1, d2[k1])
            return d2

        if (not fp):
            paths = ['1/2/3','1/2/4','1/2/5']
        else:
            paths = [fp] if (not misc.isList(fp)) else fp
        dicts = [packit(p) for p in paths]
        merged = bucket if (misc.isDict(bucket)) else {}
        for d in dicts:
            merged = merge(merged,d)
        return merged

    def store_in_bucket(self,__namespace__,keyname,path):
        toks = [t for t in path.split('/') if (len(t) > 0)]

        lines = []
        ops = ['[toks[%s]]' % (i) for i in xrange(0,len(toks))]
        __first_time__ = (not __namespace__.has_key(keyname))
        n = (len(toks)+(1 if (__first_time__) else 0))
        for i in xrange(0,len(toks)+1):
            s = '%s%s' % (keyname,''.join(ops[0:i]))
            t = '%s%s' % (keyname,''.join(ops[0:i-1]))
            if (i == 0):
                lines.append('%s = %s' % (s,'{}'))
            else:
                if (i == (n-1)) and (__first_time__):
                    x = '"%s"'%('/'+('/'.join(toks)))
                else:
                    if (i < n):
                        x = '{} if (not %s.has_key("%s")) else %s' % (t,toks[i-1],s)
                    else:
                        x = '"%s"'%('/'+('/'.join(toks)))
                lines.append('%s = %s' % (s,x))
        if (not __first_time__):
            del lines[0]
        __namespace__['toks'] = toks
        exec('\n'.join(lines)) in __namespace__
        del __namespace__['toks']
        return __namespace__

    def fetch_file_from_remote_host(self,remote,local):
        from vyperlogix import paramiko
    
        sftp = paramiko.ParamikoSFTP(self.host,int(self.port),self.user,password=self.pwd,use_manual_auth=True,callback=None,auto_close=False,logPath=self.logPath)
    
        __remote__ = self.remote
    
        __sftp__ = sftp.getSFTPClient
        
        try:
            __sftp__.get(remote, local)
        except Exception, ex:
            print >> sys.stderr, 'ERROR: %s' % (_utils.formattedException(details=ex))
    
        sftp.close()
    
    def fetch_directory_from_remote_host(self,method=Methods.recusive,use_local_json=True,logPath=None):
        __has_json__ = os.path.exists(__json__)
        if (use_local_json) and (__has_json__):
            files = ujson.loads(_utils.readFileFrom(__json__,mode='r',noCRs=True))
        else:
            from vyperlogix import paramiko
        
            sftp = paramiko.ParamikoSFTP(self.host,int(self.port),self.user,password=self.pwd,use_manual_auth=True,callback=None,auto_close=False,logPath=self.logPath)
        
            __remote__ = self.remote
        
            __sftp__ = sftp.getSFTPClient
        
            __remotes__ = []
        
            def __sftp_isdir__(directory):
                try:
                    result = __sftp__.isdir(directory)
                except:
                    result = False
                return result
        
            def sftp_listfiles_from(directory):
                for name in __sftp__.listdir(directory):
                    full_path = '/'.join([directory, name])
                    if __sftp_isdir__(full_path):
                        for entry in sftp_listfiles_from(full_path):
                            yield entry
                    else:
                        yield full_path
    
            files = [f for f in sftp_listfiles_from(__remote__)]
            sftp.close()
    
        __method__ = None
        try:
            if (self.method.value & Methods.recusive.value):
                __method__ = self.store_in_bucket_recursive
            elif (self.method.value & Methods.nonrecusive.value):
                __method__ = self.store_in_bucket
            elif (self.method not in [Methods.testing,Methods.flat]):
                print >> sys.stderr, 'WARNING: Invalid method used for method parameter.'
                sys.exit(1)
        except:
            pass
        
        bucket = {}
        try:
            if (__method__ == self.store_in_bucket):
                for f in files:
                    bucket = __method__(bucket,'directory',f)
                    if (bucket.has_key('__builtins__')):
                        del bucket['__builtins__']
            elif (__method__ == self.store_in_bucket_recursive):
                bucket = __method__(bucket=bucket,fp=files)
            else:
                bucket = files
        except:
            bucket = files
    
        if (self.method & Methods.testing):
            fOut = open(__json__,'w')
            print >> fOut, ujson.dumps(files)
            fOut.flush()
            fOut.close()
        return bucket

import re
__re__ = re.compile(r".*/memcached/installers/(?P<os>windows)/(?P<product>memcached)\W(?P<platform>win)(?P<bits>[0-9]*)\W(?P<revision>[0-9]*\.[0-9]*\.[0-9]*-[0-9]*)/(?P<filename>.*)", re.MULTILINE)

def fetch_downloads_vyperlogix_com_files(regex=__re__):
    from vyperlogix.misc import ObjectTypeName
    
    __host__= 'ftp.ord1-1.websitesettings.com'
    __port__ = 22
    
    __username__ = 'raychorn'

    from vyperlogix.crypto import Encryptors
    __password__ = Encryptors._decode('D0E5E5EBC0E2B0B0')

    __remote__ = '/downloads.vyperlogix.com/web/content'
    
    from vyperlogix.sockets.scp.RemoteFileSystem import RemoteScp
    scp = RemoteScp(__host__,__port__,__username__,__password__,__remote__)

    if (ObjectTypeName.typeClassName(regex).find('_sre.SRE_Pattern') > -1):
        files = [(f[0],f[-1].groupdict()) for f in [(f,regex.match(f)) for f in scp.fetch_directory_from_remote_host()] if (f[-1])]
    else:
        files = [f for f in scp.fetch_directory_from_remote_host()]
    
    return files

if (__name__ == '__main__'):
    '''
    python -m cProfile -s cummulative utils.py
    '''
    files = fetch_downloads_vyperlogix_com_files(regex=None)

    __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win64'
    __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win32'
    
    files = [f for f in files if (f.startswith(__remote__))]
    
    __host__= 'ftp.ord1-1.websitesettings.com'
    __port__ = 22
    
    __username__ = 'raychorn'

    from vyperlogix.crypto import Encryptors
    __password__ = Encryptors._decode('D0E5E5EBC0E2B0B0')

    __command_short__ = '/downloads.vyperlogix.com/web/content'
    scp = RemoteScp(__host__,__port__,__username__,__password__,__command_short__)

    __local__ = 'J:/@9'
    for f in files:
        print f
        scp.fetch_file_from_remote_host(f,__local__)
        
    if (1):
        sys.exit(1)
    
    __host__= 'ftp.ord1-1.websitesettings.com'
    __port__ = 22
    
    __username__ = 'raychorn'

    from vyperlogix.crypto import Encryptors
    __password__ = Encryptors._decode('D0E5E5EBC0E2B0B0')

    __command_short__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows'
    __command_long__ = '/'
    
    scp = RemoteScp(__host__,__port__,__username__,__password__,__command_short__)

    bucket = scp.fetch_directory_from_remote_host()
    
    if (scp.method != Methods.flat):
        from vyperlogix.iterators.dict import dictutils
        f = dictutils.flatten(bucket,delim='/')

    print ujson.dumps(bucket)
    
    