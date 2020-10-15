'''
Counts the number of lines in the input file.  The input file is assumbed
to be text, but it doesn't have to be.

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

import sys, glob
__version__ = "$Id: lc.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

def count_lines(files):
    retval = 0
    for file in sys.argv[1:]:
        if not IsFile(file):  continue
        try:
            fp = open(file, "rb")
            lines = fp.readlines()
            fp.close()
            print "%-8d  %s" % (len(lines), file)
        except:
            sys.stderr.write("Couldn't read \"%s\"\n" % file)
            retval = 1
    return retval

def IsFile(file_name):
    '''Return 1 if file_name is a file; otherwise return 0.
    '''
    import os
    try:
        s = os.stat(file_name)
        return ((0100000 & s[0]) == 0100000)
    except:
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage:  lc file1 [file2...]"
        sys.exit(1)
    sys.exit(count_lines(sys.argv[1:]))

