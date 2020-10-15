'''
This module provides a function that constructs a list containing
the sizes of directories under a specified directory.

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

import os
__version__ = "$Id: space.py,v 1.4 2002/08/21 12:41:49 donp Exp $"

listG = []

def GetTotalFileSize(dummy_param, directory, list_of_files):
    '''Given a list of files and the directory they're in, add the
    total size and directory name to the global list listG.
    '''
    global listG
    currdir = os.getcwd()
    os.chdir(directory)
    total_size = 0
    if len(list_of_files) != 0:
        for file in list_of_files:
            if file == ".." or file == ".":  continue
            size = os.stat(file)[6]
            total_size = total_size + size
    listG.append([total_size, directory])
    os.chdir(currdir)

def GetSize(directory):
    '''Returns a list of the form [ [a, b], [c, d], ... ] where
    a, c, ... are the number of total bytes in the directory and
    b, d, ... are the directory names.  The indicated directory 
    is recursively descended and the results are sorted by directory 
    size with the largest directory at the beginning of the list.
    '''
    import os
    global listG
    listG = []
    os.path.walk(directory, GetTotalFileSize, "")
    listG.sort()
    listG.reverse()

def ShowBiggestDirectories(directory):
    import string
    GetSize(directory)
    # Get total number of bytes
    total_size = 0L
    for dir in listG:
        total_size = total_size + dir[0]
    if total_size != 0:
        print "For directory '%s':    " % directory,
        print "[total space = %.1f MB]" % (total_size / 1e6)
        print "   %     MB   Directory"
        print "------ -----  " + "-" * 50
        not_shown_count = 0
        for dir in listG:
            percent = 100.0 * dir[0] / total_size
            dir[1] = string.replace(dir[1], "\\\\", "/")
            if percent >= 0.1:
                print "%6.1f %5d  %s" % (percent, int(dir[0]/1e6), dir[1])
            else:
                not_shown_count = not_shown_count + 1
        if not_shown_count > 0:
            if not_shown_count > 1:
                print "            [%d directories not shown]" % not_shown_count
            else:
                print "            [%d directory not shown]" % not_shown_count

if __name__ == '__main__':
    import sys
    name = sys.argv[0]
    sys.argv = sys.argv[1:]
    if len(sys.argv) == 0:
        sys.argv.append(".")
    ShowBiggestDirectories(sys.argv[0])
