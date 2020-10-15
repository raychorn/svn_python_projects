# Copyright 2005, 2006 Kevin Shuk and Magma Design Automation
# Copyright 2007, 2008, 2009 Kevin Shuk and Canonical Limited
# All rights reserved
#
#This file is part of pyax.
#
#pyax is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
#
#pyax is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyax.  If not, see <http://www.gnu.org/licenses/>.
"""Module to convert numbers from one base to another """
import string

BASE2  = string.digits[:2]
BINARY = BASE2

BASE8  = string.octdigits
OCTAL = BASE8

BASE10 = string.digits
DECIMAL = BASE10

BASE16 = string.digits + string.ascii_uppercase[:6]
HEX = BASE16

def baseconvert(number, fromdigits, todigits):
    """convert a number from one base to another

    @param number: the number for which we wish to change the base
    @param fromdigits: digit domain that number is in
    @param todigits: digit domain we wish the number to be in
    """
    
    if str(number)[0]=='-':
        number = str(number)[1:]
        neg = True
    else:
        neg = False

    # make an integer out of the number
    x=long(0)
    for digit in str(number):
       x = x*len(fromdigits) + fromdigits.index(digit)
    
    # create the result in base 'len(todigits)'
    res=''
    while x>0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x /= len(todigits)
    if len(res) == 0:
        res = 0
    if neg:
        res = "-%s" %res
    return res
