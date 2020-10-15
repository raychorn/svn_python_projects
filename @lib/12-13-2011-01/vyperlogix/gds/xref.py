'''
Implements the Xref function which will generate a dictionary of the
tokens separated by whitespace and punctuation in a text file.  The
contents of the dictionary are the line numbers (1-based) the tokens
appear on.

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

import re
__version__ = "$Id: xref.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

punctuation_reG = re.compile("/|\"|'|\.|\,|\?|\s|\<|\>|\[|\]|\{|\}|:|;|\||\\\\|~|`|!|@|#|\$|%|\^|&|\*|\(|\)|-|=|\+")
    

def Xref(filename, preserve_case = 0):
    import string
    global punctuation_reG, whitespaceG
    try:
        fp = open(filename, "r")
        lines = fp.readlines()
        fp.close()
    except:
        raise "Couldn't read input file \"%s\"" % filename
    # Convert all punctuation to spaces.
    for line_num in xrange(len(lines)):
        line = punctuation_reG.sub(" ", lines[line_num])
        if not preserve_case:
            lines[line_num] = string.lower(line)
        else:
            lines[line_num] = line

    # Now split lines into words and build the list of words
    dict = {}
    for line_num in xrange(len(lines)):
        if lines[line_num] == "":  continue
        words = re.split("  *", lines[line_num])
        for word in words:
            if word == "":  continue
            if not dict.has_key(word):
                dict[word] = []
            line_num_1_based = line_num + 1
            if line_num_1_based not in dict[word]:
                dict[word].append(line_num_1_based)
    return dict

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Usage:  xref file"
        sys.exit(1)
    words = Xref(sys.argv[1], 1)
    list = []
    # Find longest word
    maxlen = 0
    for key in words.keys():
        if len(key) > maxlen:
            maxlen = len(key)
    # Now print the output
    template = "%%-%ds: " % maxlen
    for key in words.keys():
        str = template % key
        for line_num in words[key]:
            s = "%d," % line_num
            str = str + s
        str = str[:len(str)-1]  # Remove last comma
        list.append(str)
    list.sort()
    for s in list:
        print s
