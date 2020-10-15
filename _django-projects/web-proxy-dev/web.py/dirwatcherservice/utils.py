import re
import os, sys

import ujson

from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.enum.Enum import Enum

def get_google_auth_seed():
    from vyperlogix.misc import GenPasswd
    from vyperlogix.google.auth import pyg2fa
    d = {}
    d['seed'] = GenPasswd.GenPasswdFriendlyAlphas(maxlength=16,uniquely=True)
    d['name'] = "Vyperlogix Web Services"
    d['href'] = pyg2fa.qrCodeURL(d['name'], d['seed'])
    return d

__re__ = re.compile(r".*/memcached/installers/(?P<os>windows)/(?P<product>memcached)\W(?P<platform>win)(?P<bits>[0-9]*)\W(?P<revision>[0-9]*\.[0-9]*\.[0-9]*-[0-9]*)/(?P<filename>.*)", re.MULTILINE)

def fetch_downloads_vyperlogix_com_files(regex=__re__,method=None,remote=None,use_local_json=True):
    from vyperlogix.misc import ObjectTypeName
    
    __host__= 'ftp.ord1-1.websitesettings.com'
    __port__ = 22
    
    __username__ = 'raychorn'

    from vyperlogix.crypto import Encryptors
    __password__ = Encryptors._decode('D0E5E5EBC0E2B0B0')

    __remote__ = '/downloads.vyperlogix.com/web/content' if (not remote) else remote
    
    from vyperlogix.sockets.scp.RemoteFileSystem import RemoteScp, Methods
    scp = RemoteScp(__host__,__port__,__username__,__password__,__remote__)
    
    if (method):
        scp.method = method

    __files__ = scp.fetch_directory_from_remote_host(use_local_json=use_local_json)
    
    if (not method):
        if (ObjectTypeName.typeClassName(regex).find('_sre.SRE_Pattern') > -1):
            files = [(f[0],f[-1].groupdict()) for f in [(f,regex.match(f)) for f in __files__] if (f[-1])]
        else:
            files = [f for f in scp.fetch_directory_from_remote_host()]
    else:
        files = __files__
    
    return files

if (__name__ == '__main__'):
    '''
    python -m cProfile -s cummulative utils.py
    '''
    from vyperlogix.sockets.scp.RemoteFileSystem import Methods
    files = fetch_downloads_vyperlogix_com_files(regex=None,method=Methods.recusive|Methods.testing)

    if (0):
        __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win64'
        __remote__ = '/downloads.vyperlogix.com/web/content/memcached/installers/windows/memcached-win32'
        
        files = [f for f in files if (f.startswith(__remote__))]
        
    from vyperlogix.iterators.dict import dictutils
    from vyperlogix.iterators.dict.dictutils import DictWalkOptions

    from vyperlogix.decorators.dictwalk import walk_into
    
    @walk_into(files)
    def __callback__(item):
        print item
    
    