'''
This script lets you treat the lines of a text file as a set.  You can
then take the intersection, union, and difference of a set of lines.  
The difference operator only operates on the first two files and returns
the set of elements in the first file that are not in the second file.

The syntax is 

    fset.py [-w] op file1 file2 [file3 ...]

where op is the operation:

    d[ifference]
    i[ntersection]
    u[nion]

The output is sent to stdout and is sorted.

The -w option means to ignore leading and trailing whitespace when
comparing elements.

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

debug = 0

import os, string, sys, getopt
__version__ = "$Id: fset.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

ignore_whitespace = 0
op = [ "difference", "intersection", "union" ]

def Debug(str):
    if debug:
        print "+ " + str

def GetFile(filename):
    '''Returns a dictionary with the text file's lines as the keys.
    '''
    try:
        ifp = open(filename)
        lines = ifp.readlines()
        ifp.close()
    except:
        print "Couldn't read '%s'" % filename
        sys.exit(1)
    dict = {}
    for line in lines:
        if ignore_whitespace:
            dict[string.strip(line)] = line
        else:
            dict[line] = line
    return dict

def Intersection(dict1, dict2):
    d1 = dict2
    d2 = dict1
    if len(dict1.keys()) > len(dict2.keys()):
        d1 = dict2
        d2 = dict1
    # Now d1's size will be <= d2
    result = {}
    for key in d1.keys():
        if d2.has_key(key):
            result[key] = d1[key]
    return result

def Union(dict1, dict2):
    result = {}
    for key in dict1.keys():
        result[key] = dict1[key]
    for key in dict2.keys():
        result[key] = dict2[key]
    return result

def Difference(dict1, dict2):
    '''Get the intersection of the two sets.  Then delete any element
    in dict1 that is in the intersection.
    '''
    intersection = Intersection(dict1, dict2)
    for key in intersection.keys():
        if dict1.has_key(key):
            del dict1[key]
    return dict1.copy()

def Usage():
    print '''Usage:  fset.py [-w] op file1 file2 [file3 ...]
  where op is the operation:
      d[ifference]     Lines in first file that are not in second.
      i[ntersection]   Lines that are common to all files.
      u[nion]          Lines that are in any of the files.

  Performs operations on the lines of a file as if they were members of
  a set.  -w means to ignore leading and trailing whitespace.'''
    sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w")
    except getopt.error, str:
        print "getopt error:  %s\n" % str
        sys.exit(1)
    for opt in opts:
        if opt[0] == "-w":
            global ignore_whitespace
            ignore_whitespace = 1
            Debug("Ignoring whitespace")
    if len(args) < 3:
        Usage()
    Debug("args are " + `args`)
    # Get the operation
    operation = args[0]
    first_letter = operation[0]
    if op[0][0] == first_letter:
        fn = Difference
        Debug("op is difference")
    elif op[1][0] == first_letter:
        fn = Intersection
        Debug("op is intersection")
    else:
        fn = Union
        Debug("op is union")
    # Iterate on the files on the command line
    if fn == Difference:
        result = Difference(GetFile(args[1]), GetFile(args[2]))
    else:
        result = GetFile(args[1])
        Debug("Got result for file %s:" % args[1])
        Debug("%s" % `result`)
        for file in args[2:]:
            next_file = GetFile(file)
            Debug("Got result for file %s" % file)
            Debug("%s" % `next_file`)
            result = fn(result, next_file)
    # Print results
    values = result.values()
    if ignore_whitespace:
        for ix in xrange(len(values)):
            value = values[ix]
            values[ix] = string.strip(value) + "\n"
    values.sort()
    for value in values:
        print value,  # Remember lines still have their newlines

main()
