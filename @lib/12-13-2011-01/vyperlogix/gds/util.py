'''
Miscellaneous routines in python:

Ruler                 Return a ruler
TensRuler             10's ruler to go along with Ruler()
WindChillInDegF       Calculate wind chill given OAT & wind speed
Deg2Rad               Converts degrees to radians
Rad2Deg               Converts radians to degrees
SpellCheck            Checks that a list of words is in a dictionary
Keep                  Keep only specified characters in a string
Remove                Remove a specified set of characters from a string
ListInColumns         Produce a listing like ls
Debug                 A class that helps with debugging
Time                  Returns a string giving local time and date
AWG                   Returns wire diam in inches for AWG gauge number
NiceRound             Rounds a floating pt to nearest 1, 2, or 5.
SignificantFiguresS   Rounds to specified num of sig figures (returns string)
SignificantFigures    Rounds to specified num of sig figures (returns float)
SignMantissaExponent  Returns tuple of sign, mantissa, exponent

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

import sys
__version__ = "$Id: util.py,v 1.1 2002/08/21 12:42:53 donp Exp $"

def Ruler(size = 79, type = 1):
    '''
    Function to return a ruler string.

    Type 1 ruler:
             1         2         3         4         5         6         7
    1234567890123456789012345678901234567890123456789012345678901234567890

    Type 2 ruler:
             1         2         3         4         5         6         7
    ----+----|----+----|----+----|----+----|----+----|----+----|----+----|

    Type 3 ruler:

    ----+----|----+----|----+----|----+----|----+----|----+----|----+----|

    Type 4 ruler:
    ---------|---------|---------|---------|---------|---------|---------|
    '''
    if size < 1:
        raise "Bad data", "Ruler:  size < 1"
    str = ""
    if type == 1:
        str = TensRuler(size)
        base = "1234567890"
    elif type == 2:
        str = TensRuler(size)
        base = "----+----|"
        pass
    elif type == 3:
        base = "----+----|"
    elif type == 4:
        base = "---------|"
    else:
        raise "Bad data", "Ruler:  type not between 1 and 3"
    num_repeats = (size/10 + 2) * 10
    tmpstr = base * num_repeats
    str = str + tmpstr[:size]
    return str

def TensRuler(size):
    if size >= 10:
        str = ""
        for ix in range(1, 1 + size/10):
            str = str + "%10d" % (ix * 10)
        str = str + "\n"
    return str

def WindChillInDegF(wind_speed_in_mph, air_temp_deg_F):
    '''Wind Chill for exposed human skin, expressed as a function of 
    wind speed in Miles per Hour and temperature in degrees Fahrenheit.
    Gotten from the Snippets collection.
    '''
    import math
    if wind_speed_in_mph < 4:
        return air_temp_deg_F * 1.0
    return (((10.45 + (6.686112 * math.sqrt(1.0*wind_speed_in_mph))            - (.447041 * wind_speed_in_mph)) / 22.034 *            (air_temp_deg_F - 91.4)) + 91.4)

def Deg2Rad(degrees):
    import math
    return degrees/180.0 * math.pi

def Rad2Deg(radians):
    import math
    return radians/math.pi * 180.0

def SpellCheck(input_list, word_dictionary, case_is_not_important = 1):
    '''
    This module provides the function SpellCheck(), which takes as its
    input the list of words to spell check in input_list and the
    dictionary word_dictionary (it's a dictionary rather than a list to
    allow fast access; the dictionary values can be null strings --
    all that's important is that the key be there).  It returns any
    words in input_list that are not in word_dictionary.
    '''
    import string
    misspelled = []
    if len(input_list) == 0:
        return []
    if len(word_dictionary) == 0:
        raise "SpellCheck:  word_dictionary parameter is empty"
    for ix in xrange(len(input_list)):
        if case_is_not_important:
            word = string.lower(input_list[ix])
        if not word_dictionary.has_key(word):
            misspelled.append(word)
    return misspelled

def Keep(str, keep_chars):
    "Keep only specified characters in a string"
    strlength = len(str)
    if strlength == 0 or len(keep_chars) == 0:  
        return ""
    count = 0
    outstring = ""
    while count < strlength:
        if str[count] in keep_chars:
            outstring = outstring + str[count]
        count = count + 1
    return outstring

def Remove(str, remove_chars):
    "Remove specified characters from a string"
    strlength = len(str)
    if strlength == 0:  
        return ""
    if len(remove_chars) == 0:  
        return str
    count = 0
    outstring = ""
    while count < strlength:
        if str[count] not in remove_chars:
            outstring = outstring + str[count]
        count = count + 1
    return outstring


def ListInColumns(list, col_width, num_columns, space_betw=0, truncate=0):
    '''Returns a list of strings with the elements of list (must be 
    strings) printed in columnar format.  Elements of list that won't
    fit in a column either generate an exception if truncate is 0
    or get truncated if truncate is nonzero.  The number of spaces 
    between columns is space_betw.

    Caveat:  if there are a small number of elements in the list, you
    may not get what you expect.  For example, try a list size of 1 to
    10 with num_columns equal to 4:  for lists of 1, 2, 3, 5, 6, and 9,
    you'll get fewer than four columns.
    '''
    lines = []
    N = len(list)
    if col_width < 1 or num_columns < 1 or space_betw < 0:
        raise "Error", "invalid parameters"
    if N == 0:
        return [""]
    num_rows = N / num_columns + (N % num_columns != 0)
    for row in xrange(num_rows):
        str = ""
        for column in xrange(num_columns):
            ix = num_rows * column + row
            if 0 <= ix <= (N-1):
                if len(list[ix]) > col_width:
                    if truncate:
                        str = str + list[ix][:col_width] + " "*space_betw
                    else:
                        raise "Error", "element %d too long" % ix
                else:
                    str = str + list[ix] + " " * (col_width - len(list[ix]))                           + " " * space_betw
        lines.append(str) 
    assert(len(lines) == num_rows)
    return lines

class Debug:
    '''
    Implements a debug class that can be useful in printing debugging
    information.
    '''

    def __init__(self, fd=sys.stderr, add_nl=1, prefix=" + "):
        self.fd = fd
        self.debug_on = 1
        self.add_nl = add_nl
        self.prefix = prefix

    def Print(self, str):
        if self.debug_on:
            str = self.prefix + str
            if self.add_nl:
                str = str + "\n"
            self.fd.write(str)
        else:
            pass

    def on(self):
        self.debug_on = 1
        
    def off(self):
        self.debug_on = 0

def Time():
    import time
    return time.ctime(time.time())

def AWG(n):
    '''Returns the wire diameter in inches given the AWG gauge 
    number (Brown and Sharpe gauge).
    '''
    import math
    if n < 0 or n > 40:
        raise "AWG argument out of range"
    return 1000*(.46/math.pow(92, (n+3.)/39))

def NiceRound(X, Up=0):
    '''Rounds a floating point number up or down (default) so that
    the mantissa is 1, 2, or 5.  Returns 0.0 if the number is 0.  Taken
    from a HP200 series computer algorithm I wrote in June of 1984.
    '''
    x = float(X)
    s = "%13.11e" % abs(x)
    a = float(s[0:13])
    exp = float("1.0" + s[13:18])
    sgn = 1.0 - 2*(X < 0)
    towards_zero = 0
    if (x > 0 and not Up) or (x < 0 and Up):
        towards_zero = 1
    if towards_zero == 0:
        if a == 1:
            pass
        elif a <= 2.0:
            a = 2.0
        elif a <= 5.0:
            a = 5.0
        elif a < 10.0:
            a = 10.0
    else:
        if a == 10:
            pass
        elif a >= 5.0:
            a = 5.0
        elif a >= 2.0:
            a = 2.0
        elif a > 1.0:
            a = 1.0
    return sgn * a * exp

def SignMantissaExponent(X):
    '''Returns a tuple (sign, mantissa, exponent) of a floating point
    number.
    '''
    digits = 15
    str = ("%%.%de" % digits) % abs(float(X))
    return (1-2*(X<0), float(str[0:digits+2]), int(str[digits+3:]))

def SignificantFiguresS(value, figures=3):
    '''Returns a string representing the number value rounded to
    a specified number of significant figures.  The number is
    converted to a string, then rounded and returned as a string.
    If you want it back as a number, use float() on the string.
    '''
    if figures < 1 or figures >15:
        raise "Number of significant figures must be >= 1 and <= 15"
    sign, mantissa, exponent = SignMantissaExponent(float(value))
    fmt = "%%.%df" % (figures-1)
    str = ""
    if sign < 0:
        str = "-"
    return str + (fmt % mantissa) + ("e%+04d" % exponent)

def SignificantFigures(value, figures=3):
    '''Rounds a value to specified number of significant figures.
    This function returns a float.
    '''
    return float(SignificantFiguresS(value, figures))

def C2F(c):
    '''Converts degrees C to degrees F.
    '''
    if c <= -273.15:
        raise "Temperature too low"
    return 9./5*c + 32

def F2C(f):
    '''Converts degrees C to degrees F.
    '''
    c = (f-32.)*5/9
    if c <= -273.15:
        raise "Temperature too low"
    return c

