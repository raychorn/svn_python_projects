#!/usr/bin/env python

#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   DrPython is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   Requirements(Dependencies):  Install Python, and wxPython.
#
#   Tested On Windows, Linux, Mac OS X
#
#   Icons taken from "Klassic New Crisp Icons" by Asif Ali Rizwaan (therizwaan) from the KDE-LOOK site (some edited a bit).
#   A humble and excellent artist.
#   Oh, the python icon is taken from wxPython.
#   The basic design of the program is meant to roughly (ROUGHLY) mimick DrScheme.
#   The purpose is the same, to provide a simple IDE(integrated development environment) ideal for teaching.
#   The DrPython icon itself was based on the DrScheme icon, with a slightly edited wxpython icon inserted(note yellow tongue, googly eyes).
#
#   This program could not have been written without the wonderful work of the people behind
#   python and wxPython, in particular the Styled Text Control.  Thank you.  Hopefully this tool will be of use.

#This loverly little file
#let's people grab file attributes from the
#.lnk file format (windows shortcut).
#
#It does not require any libraries external to python.

# Adapted from the excellent perl code found in smb2web.
# (smb2web by Rolf Howarth)

import string, re

refile = re.compile('(\\\\|[A-Z]\:)(.+)', re.M)
reinvalid = re.compile('(\")|(\t)|(\n)|(\r)', re.M)

def IsFolder(text):
    return ord(text[0x18]) & 0x10

def IsNetwork(text):
    return (ord(text[0x18]) == 0x00) and (ord(text[0x14]) == 1)

def GetPrintableStrings(text):
    strings = []

    cs = ''

    for character in text:
        if character in string.printable:
            cs += character
        else:
            if cs:
                if (refile.search(cs) is not None) and (reinvalid.search(cs) is None):
                    if cs[0] != '/':
                        strings.append(cs)
            cs = ''

    return strings

def ReadLink(filename):
    f = file(filename, 'rb')
    text = f.read()
    f.close()

    return GetPrintableStrings(text)[0].replace('\\', '/')