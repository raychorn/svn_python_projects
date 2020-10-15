'''
This module defines the Tree() function.  This function will return 
a list of strings that represent the directory tree for the directory
passed into the function.  The calling syntax is:

    Tree(dir, indent, leading_char)

The variable indent controls how much each subdirectory is indented
on each line.  The variable leading_char sets the leading character
in the list; '|' might not be a bad choice.

If you call the module as a script, it will print the tree to stdout
for the directory you pass in on the command line (defaults to '.').

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

__version__ = "$Id: tree.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

def visit(list, dirname, names):
    list.append(dirname)

def Tree(dir, indent=4, leading_char=" "):
    import os, string, re
    list = []
    dir_list = []
    os.path.walk(dir, visit, list)
    list.sort()
    head = re.compile("^" + dir)
    indent_str = leading_char +  " " * (indent - 1)
    for directory in list: 
        if directory == ".":
            continue
        y = string.replace(directory, "\\", "/")
        y = head.sub("", y)
        fields = string.split(y, "/")
        count = len(fields) - 1
        if dir == "/":
            count = count + 1
        if fields[-1]:
            str = indent_str * count + fields[-1]
            dir_list.append(str)
    return [dir] + dir_list

if __name__ == "__main__":
    import sys
    dir_to_process = "."
    if len(sys.argv) == 2:
        dir_to_process = sys.argv[1]
    leading_char = "|"
    for dir in Tree(dir_to_process, leading_char=leading_char):
        print dir

