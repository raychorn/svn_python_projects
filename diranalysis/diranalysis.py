import os, sys

from vyperlogix import oodb
from vyperlogix.misc import _utils
from vyperlogix.lists import ListWrapper

__dirname__ = ''

__pattern__ = ['appdata', 'local']

__filecount = 0
__foldercount = 0

if (__name__ == '__main__'):
    l = ListWrapper.ListWrapper(_utils.appDataFolder().split(os.sep))
    f1 = l.find(__pattern__[0])
    f2 = l.find(__pattern__[-1])
    if (f1 > -1) and (f2 > -1) and (f2 > f1):
        l = l[0:(min(f1,f2))]
    dbname = os.path.splitext(__file__)[0]+'@'+_utils.timeStampForFileName()+'.dbx'
    db = oodb.PickledFastHash2(dbname)
    dirname = os.sep.join(l)
    for top, dirs, files in _utils.walk(dirname):
        for f in files:
            _fname = os.sep.join([top,f])
            db[_fname] = _fname
            __filecount += 1
            print '%s --> %s' % (__filecount,_fname)
        __foldercount += 1
    db.close()
    print 'There are %d files in %d folders.' % (__filecount,__foldercount)

