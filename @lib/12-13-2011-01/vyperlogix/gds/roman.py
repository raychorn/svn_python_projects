'''
Provides two functions to convert back and forth between roman and
decimal numbers.

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
__version__ = "$Id: roman.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

iv = re.compile("IV")
ix = re.compile("IX")
xl = re.compile("XL")
xc = re.compile("XC")
cd = re.compile("CD")
cm = re.compile("CM")
i  = re.compile("I" )
v  = re.compile("V" )
x  = re.compile("X" )
l  = re.compile("L" )
c  = re.compile("C" )
d  = re.compile("D" )
m  = re.compile("M" )

def RomanNumeralsToDecimal(roman_string):
    import re, string
    str = string.upper(roman_string)
    exp = ""
    if iv.search(str) != None:  str = iv.sub("+4",    str)
    if ix.search(str) != None:  str = ix.sub("+9",    str)
    if xl.search(str) != None:  str = xl.sub("+40",   str)
    if xc.search(str) != None:  str = xc.sub("+90",   str)
    if cd.search(str) != None:  str = cd.sub("+400",  str)
    if cm.search(str) != None:  str = cm.sub("+900",  str)
    if  i.search(str) != None:  str =  i.sub("+1",    str)
    if  v.search(str) != None:  str =  v.sub("+5",    str)
    if  x.search(str) != None:  str =  x.sub("+10",   str)
    if  l.search(str) != None:  str =  l.sub("+50",   str)
    if  c.search(str) != None:  str =  c.sub("+100",  str)
    if  d.search(str) != None:  str =  d.sub("+500",  str)
    if  m.search(str) != None:  str =  m.sub("+1000", str)
    exec "num = " + str
    return num
    

def DecimalToRomanNumerals(base10_integer):
    '''Translated from a public domain C routine by Jim Walsh in the
    Snippets collection.
    '''
    roman = ""
    n, base10_integer = divmod(base10_integer, 1000)
    roman = "M"*n
    if base10_integer >= 900:
        roman = roman + "CM"
        base10_integer = base10_integer - 900
    while base10_integer >= 500:
        roman = roman + "D"
        base10_integer = base10_integer - 500
    if base10_integer >= 400:
        roman = roman + "CD"
        base10_integer = base10_integer - 400
    while base10_integer >= 100:
        roman = roman + "C"
        base10_integer = base10_integer - 100
    if base10_integer >= 90:
        roman = roman + "XC"
        base10_integer = base10_integer - 90
    while base10_integer >= 50:
        roman = roman + "L"
        base10_integer = base10_integer - 50
    if base10_integer >= 40:
        roman = roman + "XL"
        base10_integer = base10_integer - 40
    while base10_integer >= 10:
        roman = roman + "X"
        base10_integer = base10_integer - 10
    if base10_integer >= 9:
        roman = roman + "IX"
        base10_integer = base10_integer - 9
    while base10_integer >= 5:
        roman = roman + "V"
        base10_integer = base10_integer - 5
    if base10_integer >= 4:
        roman = roman + "IV"
        base10_integer = base10_integer - 4
    while base10_integer > 0:
        roman = roman + "I"
        base10_integer = base10_integer - 1
    return roman

if __name__ == "__main__":
    '''We'll test the conversion routines by converting from a decimal
    integer n to a Roman numeral and then back again.  If the operations
    are not the identity transformation, it's an error.
    '''
    largest_number = 5000
    for num in xrange(1,largest_number+1):
        str = DecimalToRomanNumerals(int(num))
        number = RomanNumeralsToDecimal(str)
        if number != num:
            print "Routines failed for", num
            raise "Test failure"
    print "Test passed."
