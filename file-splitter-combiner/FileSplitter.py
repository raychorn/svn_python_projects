""" FileSplitter - Simple Python file split/concat module.

    What it does
    -==========-
    
    1. Split a text/binary file into equal sized chunks
       and save them separately. 

    2. Concat existing chunks and recreate
       original file.

    Author: Anand Pillai
    Copyright : None, (Public Domain)
"""

import os, sys
import glob
import re

#from vyperlogix.misc import threadpool
#_Q1_ = threadpool.ThreadQueue(1000)

from vyperlogix.misc import _utils
from vyperlogix.misc import _psyco

_number_format__ = '-\d+_\d+'

_id_re = re.compile(r".*-(?P<num>\d+)_(?P<total>\d+)")

class FileSplitterException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def usage():
    return """\nUsage: FileSplitter.py -i <inputfile> -o <outputfilepath> -n <chunksize> [option]\n
    Options:\n
    -s, --split  Split file into chunks
    -j, --join   Join chunks back to file.
    """

#@threadpool.threadify(_Q1_)  # memory issues since the files can be larger than the available RAM - nice idea but... may not work...
def write_chunk(fname,bytes):
    print 'Writing file:',fname
    try:
        chunkf = file(fname, 'wb')
        chunkf.write(bytes)
    except (OSError, IOError), e:
        info_string = _utils.formattedException(details=e)
        print >>sys.syderr, info_string
    finally:
        chunkf.close()

class FileSplitter:
    """ File splitter class """

    def __init__(self):

        # cache filename
        self.__filename = ''
        self.__outputpath = ''
        # number of equal sized chunks
        self.__numchunks = 5
        # Size of each chunk
        self.__chunksize = 0
        # Optional postfix string for the chunk filename
        self.__postfix = ''
        # Program name
        self.__progname = "FileSplitter.py"
        # Action
        self.__action = 0 # split

    def parseOptions(self, args):

        import getopt

        try:
            optlist, arglist = getopt.getopt(args, 'sji:o:n:', ["split=", "join="])
        except getopt.GetoptError, e:
            print e
            return None

        for option, value in optlist:
            if option.lower() in ('-i', ):
                self.__filename = value
            elif option.lower() in ('-o', ):
                self.__outputpath = value
            elif option.lower() in ('-n', ):
                self.__numchunks = int(value)
            elif option.lower() in ('-s', '--split'):
                self.__action = 0 # split
                #self.__outputpath = os.path.dirname(self.__filename)
            elif option.lower() in ('-j', '--join'):
                self.__action = 1 # combine

        if not self.__filename:
            sys.exit("Error: filename not given")
        
    def do_work(self):
        if self.__action==0:
            self.split()
        elif self.__action==1:
            self.combine()
        else:
            return None
        
    def split(self):
        """ Split the file and save chunks
        to separate files """

        print 'Splitting file', self.__filename
        print 'Number of chunks', self.__numchunks, '\n'
        
        try:
            f = open(self.__filename, 'rb')
        except (OSError, IOError), e:
            raise FileSplitterException, str(e)

        fname = (os.path.split(self.__filename))[1]
        bname = os.sep.join([self.__outputpath,os.path.basename(fname)])
        # Get the file size
        fsize = os.path.getsize(self.__filename)
        # Get size of each chunk
        self.__chunksize = int(float(fsize)/float(self.__numchunks))
        
        self.__postfix = '_%s' % (self.__numchunks)

        chunksz = self.__chunksize
        total_bytes = 0

        for x in xrange(self.__numchunks):
            chunkfilename = bname + '-' + str(x+1) + self.__postfix

            # if reading the last section, calculate correct
            # chunk size.
            if x == self.__numchunks - 1:
                chunksz = fsize - total_bytes

            try:
                data = f.read(chunksz)
                total_bytes += len(data)
                write_chunk(chunkfilename,data)
            except (OSError, IOError), e:
                info_string = _utils.formattedException(details=e)
                print >>sys.syderr, info_string
                continue
            except EOFError, e:
                info_string = _utils.formattedException(details=e)
                print >>sys.syderr, info_string
                break

        print 'Done.'

    def sort_index(self, f1, f2):

        toks = _id_re.match(f1)
        index1 = toks.groups()[0]
        toks = _id_re.match(f2)
        index2 = toks.groups()[0]
        
        if index1 != -1 and index2 != -1:
            i1 = int(index1)
            i2 = int(index2)
            return i1 - i2
        
    def combine(self):
        """ Combine existing chunks to recreate the file.
        The chunks must be present in the cwd. The new file
        will be written to cwd. """

        print 'Creating file', self.__outputpath
        
        bname = self.__outputpath
        bname2 = os.path.basename(bname)
        
        # bugfix: if file contains characters like +,.,[]
        # properly escape them, otherwise re will fail to match.
        for a, b in zip(['+', '.', '[', ']','$', '(', ')'], ['\+','\.','\[','\]','\$', '\(', '\)']):
            bname2 = bname2.replace(a, b)
            
        chunkre = re.compile(bname2 + _number_format__)
        
        chunkfiles = []
        fname = os.sep.join([self.__filename,'*.*'])
        for f in glob.glob(fname):
            print f
            if chunkre.match(os.path.basename(f)):
                chunkfiles.append(f)

        print 'Number of chunks', len(chunkfiles), '\n'
        chunkfiles.sort(self.sort_index)

        for f in chunkfiles:
            try:
                print 'Appending chunk', os.path.join(".", f)
                data = open(f, 'rb').read()
                try:
                    f = open(bname, 'ab')
                    f.write(data)
                except (OSError, IOError, EOFError), e:
                    raise FileSplitterException, str(e)
                finally:
                    f.close()
            except (OSError, IOError, EOFError), e:
                info_string = _utils.formattedException(details=e)
                print >>sys.syderr, info_string
                continue

        print 'Wrote file', bname

def main():
    import sys

    if len(sys.argv)<2:
        sys.exit(usage())
        
    fsp = FileSplitter()
    fsp.parseOptions(sys.argv[1:])
    _psyco.importPsycoIfPossible(func=fsp.do_work)
    fsp.do_work()

if __name__=="__main__":
    main()
