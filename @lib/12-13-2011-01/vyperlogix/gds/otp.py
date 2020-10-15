''' 
This module provides an Otp object that can be used to get one time
pad strings.  It should be adequate for situations that don't require
high security.

You can call the module directly as a script; it will want the
number of otp strings to print out and an optional seed number.
For example, 'python otp.py 20' will print out 20 otp strings.

You may pass in a function to the constructor.  This function takes
an integer parameter (defaults to 0) and must return a string.
This string is hashed with the MD5 algorithm and the hex
representation of the hash is returned.  If you do not pass in a
string generating function, an internal function is used that is
based on the whrandom module.

Once you have constructed an Otp object, call the Get() method to
return an OTP string.  The Get() method can have an integer
parameter that is passed to the str_function() function.  For the
default function (GenerateString()), if the seed is nonzero, the
Wichmann-Hill generator is started over and initialized from the
seed.

Each call to Get generates a new random string, sends it to
md5.update(), (which appends it to its own internal copy of all the
strings it's been sent), and then a new md5 hash is gotten, which is
converted to the hex representation with 32 hex characters.

This module could be made to provide cryptographically secure
one time pads by substituting a cryptographic quality random
number generator for the whrandom object.  You can go out on
the web and search for "random number" and find some hardware
devices to do this.

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
import md5, whrandom
__version__ = "$Id: otp.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

whG = whrandom.whrandom()

def GenerateString(seed = 0):
    '''Generate a string from a four byte integer.  The string is the
    4 bytes of the integer, each converted to a character.
    '''
    global whG
    if seed:      # seed != 0 means to restart; whrandom seeds from time.
        whG.seed(seed & 0xff, 
                 (seed & 0xff00) >> 8, 
                 (seed & 0xff0000) >> 16)
    n = whG.randint(0, 2**30-1)
    str = ""
    str = str + chr((n & 0xFF000000) >> 24)
    str = str + chr((n & 0x00FF0000) >> 16)
    str = str + chr((n & 0x0000FF00) >>  8)
    str = str + chr((n & 0x000000FF) >>  0)
    return str

class Otp:
    def __init__(self, str_function = GenerateString, seed = 0):
        str_function(seed) # Initialize random number generator
        self.m = md5.new()

    def Get(self, seed=0):
        '''Return an OTP.
        '''
        self.m.update(GenerateString(seed))
        string = self.m.digest()
        str = ""
        for ix in xrange(len(string)):
            str = str + "%02X" % ord(string[ix])
        return str

if __name__ == "__main__":
    import sys
    num = 1
    seed = 0
    if len(sys.argv) < 2:
        print "Usage:  otp num_times [seed]"
        sys.exit(1)
    num = int(sys.argv[1])
    if len(sys.argv) == 3:
        seed = int(sys.argv[2])
    o = Otp(seed=seed)
    for ix in xrange(num):
        print o.Get()
