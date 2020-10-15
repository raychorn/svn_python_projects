'''
Counts lines of non-commented source code for C and C++.  Strips
out comments, then counts non-empty lines.  Prints a report to stdout.

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

import re, sys, os, getopt, string, time

start_C_comment      = re.compile("^.*(/\*.*$)")
end_C_comment        = re.compile("^(.*\*/).*$")
one_line_C_comment   = re.compile(".*(/\*.*\*/).*$")
cpp_comment          = re.compile(".*(//.*$)")

total_lines = 0

def Usage():
    print "Usage:  %s source_file1 [source_file2 ...]"
    sys.exit(1)

def RemoveCComments(lines):
    # Any comments extending over multiple lines will be replaced with
    # blank lines to maintain line numbering.
    in_comment = 0
    for ix in xrange(len(lines)):
        if in_comment:
            mo = end_C_comment.match(lines[ix])
            if mo:
                in_comment = 0
                lines[ix] = string.replace(lines[ix], mo.group(1), "")
                continue
            lines[ix] = ""
        else:
            mo = one_line_C_comment.match(lines[ix])
            if mo:
                lines[ix] = string.replace(lines[ix], mo.group(1), "")
                continue
            mo = cpp_comment.match(lines[ix])
            if mo:
                lines[ix] = string.replace(lines[ix], mo.group(1), "")
                continue
            mo = start_C_comment.match(lines[ix])
            if mo:
                in_comment = 1
                lines[ix] = string.replace(lines[ix], mo.group(1), "")
                continue

def ProcessFile(file):
    global total_lines
    try:
        ifp = open(file)
        lines = ifp.readlines()
        ifp.close()
    except:
        sys.stderr.write("Couldn't read '%s'\n" % file)
        sys.exit(1)
    RemoveCComments(lines)
    # Remove all blank lines.  We go backwards so as not to mess the
    # counter ix up.
    for ix in xrange(len(lines)-1, 0, -1):
        line = string.strip(lines[ix])
        if len(line) == 0:
            del lines[ix]
    print "%8d  %s" % (len(lines), file)
    total_lines = total_lines + len(lines)

def main():
    if len(sys.argv) < 2:
        Usage()
    for file in sys.argv[1:]:
        ProcessFile(file)
    print ""
    print "%8d  %s" % (total_lines, "Total")

if __name__ == "__main__":
    main()
