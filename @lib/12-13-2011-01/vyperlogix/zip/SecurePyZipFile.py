import zipfile
import os, re
from distutils import util

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

class SecurePyZipFile(zipfile.ZipFile):
    """Class to create ZIP archives with Python library files and packages."""

    __rx__ = re.compile('[.]svn')
    __isSourceless__ = True
    
    def explainCompression(self,val):
        if (val == zipfile.ZIP_DEFLATED):
            return 'ZIP_DEFLATED'
        elif (val == zipfile.ZIP_STORED):
            return 'ZIP_STORED'
        return 'UNKNOWN'

    def __explainSourceless__(self):
        if (self.isSourceless):
            return 'Sourceless'
        return 'not Sourceless'

    def __repr__(self):
        return '%s :: File name is "%s" and compression is "%s" and is "%s".' % (str(self.__class__),self.filename,self.explainCompression(self.compression),self.explainSourceless)
    
    def writepy(self, paths=[]):
        """Add all files from paths to the ZIP archive.
        paths is a list of paths each of which specifies a pathname.
        """
        from vyperlogix import misc
        for top in paths if (misc.isList(paths)) else [paths]:
            try:
                for root, dirs, files in os.walk(top):
                    if (self.rx.search(root) == None):
                        print '='*80
                        print 'files=%s' % files
                        py_files = [os.path.join(root,f) for f in files if f.endswith('.py' if not self.isSourceless else '.pyo')]
                        print '-'*80
                        print 'py_files=%s' % py_files
                        util.byte_compile(py_files,optimize=2,force=1)
                        for f in py_files:
                            print 'ZIP Adding (%s) to (%s)' % (f,self.filename)
                            f_base = f.replace('.pyo','.pyc').replace(top,'')
                            _f_base = f_base.split(os.sep)[-1]
                            self.write(f,f_base)
                        print '='*80
            except Exception, details:
                print 'Error in ZIP processing. (%s)' % (str(details))

    def get_rx(self):
        '''The Regex for svn files.'''
        return self.__rx__

    def set_rx(self,rx):
        '''The Regex for svn files.'''
        if isinstance(rx,re):
            self.__rx__ = rx
        else:
            print 'WARNING :: This function requires the rx parm to be of type "re" not "%s".' % type(rx)
            
    def get_isSourceless(self):
        return self.__isSourceless__
        
    def set_isSourceless(self,isSourceless):
        if isinstance(isSourceless,bool):
            self.__isSourceless__ = isSourceless
        else:
            print 'WARNING :: This function requires the isSourceless parm to be of type "bool" not "%s".' % type(isSourceless)
            
    def get_explainSourceless(self):
        return self.__explainSourceless__()
            
    rx = property(get_rx,set_rx)
    isSourceless = property(get_isSourceless,set_isSourceless)
    explainSourceless = property(get_explainSourceless)
