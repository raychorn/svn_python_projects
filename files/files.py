import os, sys
from vyperlogix.misc import _utils

__bias__ = 'J:\\@Vyper Logix Corp\\@Projects\\PDFXporter\\@workspace_burrito\\SVNCloudPortal\\src\\'

__top__ = 'J:\\@Vyper Logix Corp\\@Projects\\PDFXporter\\@workspace_burrito\\SVNCloudPortal\\src\\assets\\images\\clouds\\Clouds Free Pictures'

__code__ = '''
[Embed (source="{{filename}}" )]
public static const {{classname}}:Class;
'''

if (__name__ == '__main__'):
    for top, dirs, files in _utils.walk(__top__):
        _files_ = [os.sep.join([top.replace(__bias__, ''), f]) for f in files]
        for f in _files_:
            className = f.split(os.sep)[-1].split('.')[0].replace('-', '_').capitalize()
            c = __code__.replace('{{filename}}', '%s').replace('{{classname}}', '%s')
            print c % (f, className)
