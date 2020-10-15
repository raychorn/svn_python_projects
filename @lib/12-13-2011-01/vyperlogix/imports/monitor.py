import sys
import imp
import os

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

class ImpWrapper:
    def __init__(self, path=None, callback=None):
        '''callback(path,fullname)'''
        if path is not None and not os.path.isdir(path):
            raise ImportError
        self.path = path
        self.__callback__ = callback

    def find_module(self, fullname, path=None):
        callback_failed = (path is None)
        if (not callback_failed):
            if (callable(self.__callback__)):
                try:
                    self.__callback__(path,fullname)
                except Exception, details:
                    print 'ERROR: %s' % (str(details))
                    callback_failed = True
            else:
                callback_failed = True
            if (callback_failed):
                print '"%s" --> "%s".' % (path,fullname)
        subname = fullname.split(".")[-1]
        if subname != fullname and self.path is None:
            return None
        if self.path is None:
            path = None
        else:
            path = [self.path]
        try:
            file, filename, stuff = imp.find_module(subname, path)
        except ImportError:
            return None
        return ImpLoader(file, filename, stuff)

class ImpLoader:
    def __init__(self, file, filename, stuff):
        self.file = file
        self.filename = filename
        self.stuff = stuff

    def load_module(self, fullname):
        mod = imp.load_module(fullname, self.file, self.filename, self.stuff)
        if self.file:
            self.file.close()
        mod.__loader__ = self  # for introspection
        return mod

def hook(callback=None):
    i = ImpWrapper(callback=callback)
    sys.meta_path.append(i)
    sys.path_hooks.append(ImpWrapper)

def reporterHook(fname=None,isVerbose=False):
    import os, sys
    
    if (fname is None):
        fname = os.sep.join([os.path.dirname(sys.argv[0]),os.path.basename('%s.txt' % (sys.argv[0].split('.')[0]))])
    if (os.path.exists(fname)):
        os.remove(fname)

    def myCallback(path,fullname):
        _msg = '(%s) :: "%s" --> "%s".' % (os.path.basename(sys.argv[0]),path,fullname)
        fOut = open(fname,'a')
        try:
            print >>fOut, _msg
        finally:
            fOut.flush()
            fOut.close()
        if (isVerbose):
            print _msg
    hook(callback=myCallback)
