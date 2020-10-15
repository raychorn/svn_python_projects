#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public Lisense)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Tab Nanny Check: returns a string on checking.

from tabnanny import *

#Copied from tabnanny by Tim Peters, then hacked to work the way I want.

import os
import tokenize

__all__ = ["check", "NannyNag", "process_tokens"]

verbose = 0
filename_only = 0

def errprint(*args):
    printstr(args)

def printstr(*args):
    result = ''
    sep = ''
    for arg in args:
        result += sep + str(arg)
        sep = ' '
    return result + '\n'

def Check(file):
    """check(file_or_dir)

    If file_or_dir is a directory and not a symbolic link, then recursively
    descend the directory tree named by file_or_dir, checking all .py files
    along the way. If file_or_dir is an ordinary Python source file, it is
    checked for whitespace related problems. The diagnostic messages are
    written to standard output using the print statement.
    """

    result = ''

    if os.path.isdir(file) and not os.path.islink(file):
        if verbose:
            result += printstr("%s: listing directory" % `file`)
        names = os.listdir(file)
        for name in names:
            fullname = os.path.join(file, name)
            if os.path.isdir(fullname) and not os.path.islink(fullname) or os.path.normcase(name[-3:]) == ".py":
                check(fullname)
        return result

    try:
        f = open(file)
    except IOError, msg:
        result += errprint("%s: I/O Error: %s" % (`file`, str(msg)))
        return result

    if verbose > 1:
        result += printstr("checking", `file`, "...")

    try:
        process_tokens(tokenize.generate_tokens(f.readline))

    except tokenize.TokenError, msg:
        result += errprint("%s: Token Error: %s" % (`file`, str(msg)))
        return result

    except NannyNag, nag:
        badline = nag.get_lineno()
        line = nag.get_line()
        if verbose:
            result += printstr("%s: *** Line %d: trouble in tab city! ***" % (`file`, badline))
            result += printstr("offending line:", `line`)
            result += printstr(nag.get_msg())
        else:
            if ' ' in file: file = '"' + file + '"'
            if filename_only: result += printstr(file)
            else: result += printstr(file, badline, `line`)
        return result

    if verbose:
        result += printstr("%s: Clean bill of health." % `file`)

    return result