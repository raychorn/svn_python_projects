'''
Tool to compare shell environment variable settings

This tool will compare two files A and B containing the output of a 'set'
shell command and produce four groupings:
    
    * Those environment variables in A but not in B
    * Those environment variables in B but not in A
    * Those environment variables that are common and equal
    * Those environment variables that are common but unequal

However, it will give incorrect results when an environment variable
contains
an embedded newline; IFS is a variable that typically does this.  But it
will print the offending line to stderr to alert you that some comparisons
may not be correct.

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

import sys, string, re

# The two files
A = ""
B = ""

bash_func = re.compile("^.*=\(\)$")

def Usage():
    '''Check the command line; if OK, parse.  If not, give usage message
    and exit.
    '''
    if len(sys.argv) != 3:
        print '''Usage:  %s  A  B
  Compares two files A and B containing the output of a shell 'set' 
  command and reports:

    * Those environment variables in A but not in B
    * Those environment variables in B but not in A
    * Those environment variables that are common and equal
    * Those environment variables that are common but unequal''' %     sys.argv[0]
        sys.exit(1)
    global A, B
    A = sys.argv[1]
    B = sys.argv[2]

def Compare(dictA, dictB):
    common_equal   = {}
    common_unequal = {}
    only_in_A      = {}
    only_in_B      = {}
    all_keys       = {}
    for key in dictA.keys() + dictB.keys():
        all_keys[key] = 0
    for key in all_keys.keys():
        if dictA.has_key(key):
            if dictB.has_key(key):
                if dictA[key] == dictB[key]:
                    common_equal[key] = 0
                else:
                    common_unequal[key] = 0
            else:
                only_in_A[key] = 0
        else:
            only_in_B[key] = 0
    # Print report
    if len(common_equal) > 0:
        print "Common and equal variables:"
        PrintKeys(common_equal)
    if len(common_unequal) > 0:
        print "Common and unequal variables:"
        PrintKeys(common_unequal)
    if len(only_in_A) > 0:
        print "Only in file %s:" % A
        PrintKeys(only_in_A)
    if len(only_in_B) > 0:
        print "Only in file %s:" % B
        PrintKeys(only_in_B)

def PrintKeys(dict):
    keys = dict.keys()
    keys.sort()
    for key in keys:
        print " ", key

def BuildDict(file):
    stream = open(file)
    lines = stream.readlines()
    stream.close()
    dict = {}
    lineno = 0
    for line in lines:
        lineno = lineno + 1
        line = string.strip(line)
        if line == "":
            continue
        pos = string.find(line, "=")
        if pos == -1:
            sys.stderr.write("Bad line %d of file %s\n" % (lineno, file))
            continue
        if bash_func.match(line) and            line != "DIRSTACK=()" and            line != "GROUPS=()":
            print "matched", line
            # First line of a bash function listing; we're done
            break
        name  = line[:pos]
        value = line[pos+1:]
        assert(not dict.has_key(name))
        dict[name] = value
    return dict

def main():
    Usage()
    dictA = BuildDict(A)
    dictB = BuildDict(B)
    Compare(dictA, dictB)
    sys.exit(0)

main()
