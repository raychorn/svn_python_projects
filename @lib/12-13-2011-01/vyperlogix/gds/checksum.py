'''
This routine provides a 128 bit checksum for each file given on the
command line.  It also prints the file size in bytes.  (The 'checksum'
is actually the md5 hash of the file.)  Returns 0 if all files were
processed OK; otherwise returns 1.

Note that if you pass * on the command line, the directories will be
recognized as directories and not cause a return status of 1, even
though you can't really return a hash value for a directory.

Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.
'''
import sys, re
__version__ = "$Id: checksum.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

backslashG = re.compile(r"\\")
recursiveG = 0
retvalG    = 0
sortG      = 0  # How to sort the output.  0 means no sorting, 1 means 
                # sort by field 1 (the MD5 hash), 2 by field 2 (the 
                # number of bytes in the file), 3 by file name.

def CalcMD5(filename):
    '''Returns a tuple of the MD5 hash in hex, the file size in bytes, 
    and the filename.
    '''
    import md5
    if IsDirectory(filename):
        return
    try:
        fp = open(filename, "rb")
        str = fp.read()
        bytes = len(str)
        fp.close()
        m = md5.new()
        m.update(str)
        str = m.digest()
        hexform = ""
        for ix in xrange(len(str)):
            hexform = hexform + "%02x" % ord(str[ix])
        # If filename contains backslashes, convert them to forward slashes
        filename = backslashG.sub("/", filename)
        return (hexform, bytes, filename)
    except:
        sys.stderr.write("Couldn't process file %s\n" % filename)
        retvalG = 1
        return ()

def IsDirectory(dir_name):
    'Return 1 if dir_name is a directory; otherwise return 0.'
    import os
    mask = 040000
    try:
        s = os.stat(dir_name)
    except:
        return 0
    if (mask & s[0]) == mask:
        return 1
    else:
        return 0

def Usage():
    global retvalG
    print '''Usage:  checksum [-r] [-s n] file1 [file2 ...]
Typical output:
  44A5D1B02117CA7AC44AF086ACA74B8C 116710    filename
    First  field:    MD5 hash (in hex) of file
    Second field:    Size of file in bytes
    Third  field:    File name
  -r option descends directories recursively
  -s option sorts output by nth field (use n < 0 to reverse sort order):
    0   In command line order [default]
    1   Sort by MD5 hash
    2   Sort by file size
    3   Sort by file name'''
    retvalG = 1
    sys.exit(retvalG)

def ProcessCommandLine(cmdline_args):
    import getopt
    global retvalG, sortG, recursiveG
    try:
        optlist, args = getopt.getopt(cmdline_args, "rs:")
    except getopt.error, str:
        print str
        retvalG = 1
        sys.exit(retvalG)
    if len(args) < 1:
        Usage()
    for opt in optlist:
        if opt[0] == "-s":
            sortG = int(opt[1])
            limit = 3
            if sortG < -limit or sortG > limit:
                Usage()
        if opt[0] == "-r":
            recursiveG = 1
    return args

def Sort(arg1, arg2):
    '''The comparison function used to sort two tuples by comparing
    the element indicated by sortG.  Return -1 if arg1 < arg2,
    0 if arg1 == arg2, 1 if arg1 > arg2.
    '''
    if sortG == 0:
        return 0
    ix = abs(sortG) - 1
    if sortG < 0:
        sgn = -1
    else:
        sgn = 1
    if arg1[ix] < arg2[ix]:
        return -1 * sgn
    if arg1[ix] > arg2[ix]:
        return 1 * sgn
    return 0

def ProcessDirectory(dir, results):
    '''dir is a directory, so process all files that it contains and 
    put in the results list.  Any directories found in dir result in 
    a recursive call to this function.
    '''
    import glob
    filelist = glob.glob(dir + "/*")
    for file in filelist:
        if IsDirectory(file):
            ProcessDirectory(file, results)
        else:
            results.append(CalcMD5(file))

def main():
    import glob
    if len(sys.argv) < 2:
        Usage()
    args = ProcessCommandLine(sys.argv[1:])
    files = []
    for arg in args:
        list = glob.glob(arg)
        for file in list:
            files.append(file)
    results = []
    for file in files:
        if IsDirectory(file):
            if recursiveG:
                ProcessDirectory(file, results)
        else:
            results.append(CalcMD5(file))
    if sortG:
        results.sort(Sort)
    for r in results:
        print "%s %-9d %s" % r
    return retvalG

if __name__ == "__main__":
    main()
