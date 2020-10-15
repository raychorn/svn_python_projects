'''
Implements a class that allows you to create arbitrarily long 
bitfields.  The bits are numbered from 0 to N-1, where N is the
size of the bitfield.

The methods are:
    is_set()            Return 1 if specified bit is set
    is_clear()          Return 1 if specified bit is clear
    set_bit()           Set a specified bit
    clear_bit()         Clear a specified bit
    set_bit_range()     Set a range of bits to one
    clear_bit_range()   Set a range of bits to zero
    set_to_zeros()      Set all the bits to zero
    set_to_ones()       Set all the bits to one
    num_bytes_used()    How many bytes the representation takes

The implementation uses a list of strings for the bitfields.  You
can choose the size of the strings in the list.

Here are some creation times of larger bitfields on a laptop PC
(approx. 800 MHz Pentium machine with 256 MB RAM and Windows 2000):

    size = 10^6 bits, creation time = 0.04 sec
    size = 10^7 bits, creation time = 0.37 sec
    size = 10^8 bits, creation time = 4.16 sec
    size = 10^9 bits, creation time = 42.2 sec

Here are some creation times for a 166 MHz Pentium with 32
MB of RAM running Windows NT 4.0 (second column is ratio to
above laptop times):

    size = 10^6 bits, creation time = 0.05 sec
    size = 10^7 bits, creation time = 0.5 sec       1.3
    size = 10^8 bits, creation time = 7.2 sec       1.7
    size = 10^9 bits, creation time = 327 sec       7

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
__version__ = "$Id: bitfield.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

class bitfield:
    '''Lets you define arbitrary bit fields.   All bit fields can be 
    initialized to all zeros or all ones.  If you choose to use a
    large bit field, the most time consuming tasks are creation of
    and changing a large range.

    A list of strings is used to implement the bit field.  Each character
    in a string represents 8 bits and each list element represents
    self.num_rows * 8 bits.  You can specify the number of bits in each 
    row if you like (list element 0 is row 1, list element 1 is row 2, 
    etc.).
    '''

    def __init__(self, num_bits, init_with_ones = 0, num_bits_in_row = 64*8):
        self.errorstr = "Error"
        self.num_bits = long(num_bits)  # Allows ints, longs, floats
        if self.num_bits < 1:
            raise self.errorstr, "number_of_bits must be > 0"
        if type(num_bits_in_row) != type(1) or num_bits_in_row < 8:
            raise self.errorstr, "num_bits_in_row must be an integer >= 8"
        if num_bits_in_row % 8 != 0:
            raise self.errorstr, "num_bits_in_row must be divisible by 8"
        self.num_bits_in_row = num_bits_in_row
        self.num_bytes_in_row = int(num_bits_in_row / 8)
        self.num_rows = int(self.num_bits / num_bits_in_row +             (self.num_bits % num_bits_in_row != 0))
        self.dot = 0    # Set to != 0 for '.' and '|' representation.
        self.bitstr = []
        self.zero = chr(0)   * int(self.num_bits_in_row / 8)
        self.one  = chr(255) * int(self.num_bits_in_row / 8)
        if init_with_ones:
            for ix in xrange(self.num_rows):
                self.bitstr.append(self.one)
        else:
            for ix in xrange(self.num_rows):
                self.bitstr.append(self.zero)

    def __get_index(self, bit_position):
        '''Return a tuple; the first element is which row the bit is in,
        the next element is which byte, and the next is which bit in 
        that byte.
        '''
        self.__within_range(bit_position)
        row, bit_in_row = divmod(bit_position, self.num_bits_in_row)
        byte_in_row, bit_in_byte = divmod(bit_in_row, 8)
        return (row, byte_in_row, bit_in_byte)

    def is_set(self, bit_position):
        row, byte, bit = self.__get_index(bit_position)
        return not(not(ord(self.bitstr[row][byte]) & (1 << bit)))

    def is_clear(self, bit_position):
        return not self.is_set(bit_position)

    def set_bit(self, bit_position):
        self.__set_bit(bit_position, 1)

    def clear_bit(self, bit_position):
        self.__set_bit(bit_position, 0)

    def __set_bit(self, bit_position, value):
        row, byte, bit = self.__get_index(bit_position)
        s = self.bitstr
        assert(value == 0 or value == 1)
        if value == 1:
            new_byte = chr(ord(s[row][byte]) | (1 << bit))
        else:
            new_byte = chr(ord(s[row][byte]) & ( ~ (1 << bit)))
        if byte == 0:
            if len(s[row]) > 1:
                s[row] = new_byte + s[row][1:]
            else:
                s[row] = new_byte
        elif byte == self.num_bytes_in_row - 1:
            s[row] = s[row][:-1] + new_byte
        else:
            s[row] = s[row][:byte] + new_byte + s[row][byte+1:]
        assert(len(s[row]) == self.num_bytes_in_row)

    def set_bit_range(self, start, finish):
        '''These two functions are inefficient for a setting or
        clearing a large number of bits, but, boy, were they
        easy to write. :)
        '''
        if start > finish:
            raise self.errorstr, "start must be less than finish"
        for bit_position in xrange(start, finish+1):
            self.__set_bit(bit_position, 1)

    def clear_bit_range(self, start, finish):
        for bit_position in xrange(start, finish+1):
            self.__set_bit(bit_position, 0)

    def set_to_zeros(self):
        self.bitstr = []
        for ix in xrange(self.num_rows):
            self.bitstr.append(self.zero)

    def set_to_ones(self):
        self.bitstr = []
        for ix in xrange(self.num_rows):
            self.bitstr.append(self.one)

    def __within_range(self, bit_position):
        if type(bit_position) != type(1) or            bit_position < 0              or            bit_position > self.num_bits - 1:
            raise self.errorstr, "bit position must be >= 0 and <= %d" %                 (self.num_bits - 1)
    
    def __repr__(self):
        '''Returns binary representation with LSB to right.  Set self.dot
        to nonzero to use an alternative form from 1's and 0's that's 
        sometimes easier to read.
        '''
        str = ""
        on  = '1'
        off = '0'
        if self.dot:
            on  = '|'
            off = '.'
        for ix in xrange(self.num_bits-1, -1, -1):
            if self.is_set(ix):
                str = str + on
            else:
                str = str + off
        return str

    def num_bytes_used(self):
        tmp = self.num_bytes_in_row * self.num_rows
        try:
            retval = int(tmp)
        except:
            retval = tmp
        return retval

    def __cmp__(self, o):
        "Implements ==, != only"
        if type(o) != type(self):
            raise self.errorstr, "object is not a bitfield"
        if o.num_bits != self.num_bits:
            return 1
        match = 0
        for ix in xrange(self.num_rows):
            if o.bitstr[ix] != self.bitstr[ix]:
                match = 1
                break
        return match


def Test(size):
    import time
    start = time.time()
    err = "Test failed for size %d" % size
    a = bitfield(size)
    b = bitfield(size, init_with_ones = 0)
    o = bitfield(size, init_with_ones = 1)
    b.set_bit(size-1)
    if not b.is_set(size-1): raise err
    b.clear_bit(size-1)
    if not b.is_clear(size-1): raise err
    b.set_bit(size-2)
    if not b.is_set(size-2): raise err
    b.clear_bit(size-2)
    if not b.is_clear(size-2): raise err
    b.set_bit(0)
    if not b.is_set(0): raise err
    b.clear_bit(0)
    if not b.is_clear(0): raise err
    b.set_bit(1)
    if not b.is_set(1): raise err
    b.clear_bit(1)
    if not b.is_clear(1): raise err
    if a != b: raise err
    b.set_to_ones()
    if b != o: raise err
    b.set_to_zeros()
    if a != b: raise err
    finish = time.time()
    print "Size %.1e time = %.2f sec" % (size, finish-start)

if __name__ == "__main__":
    # Test the class.
    for size in [2, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]:
        Test(int(size))

