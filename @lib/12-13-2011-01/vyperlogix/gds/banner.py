'''
This module contains the function Banner() which can be used to print
a banner message like the UNIX banner(1) function.

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

# The array letters contains the information on how to print each
# character between 32 and 126, inclusive.  There are 8 bytes for
# each character and each byte represents one line of the font.  The
# high byte of the first number is the first line of 8 bits, the
# next byte is the next line, and so on.  I got these numbers by
# writing a little script that analyzed the output of somebody's
# banner program...

letters = [
        [ 0x00000000, 0x00000000 ], [ 0x30303030, 0x30003000 ],
        [ 0x6c6c6c00, 0x00000000 ], [ 0x6c6cfe6c, 0xfe6c6c00 ],
        [ 0x187e407e, 0x027e1800 ], [ 0xc2c60c18, 0x3066c600 ],
        [ 0x3828387b, 0xd6cc7700 ], [ 0x60204000, 0x00000000 ],
        [ 0x1c70c0c0, 0xc0701c00 ], [ 0x701c0606, 0x061c7000 ],
        [ 0x006c38fe, 0x386c0000 ], [ 0x303030fc, 0x30303000 ],
        [ 0x00000000, 0x00602040 ], [ 0x0000007c, 0x00000000 ],
        [ 0x00000000, 0x00060600 ], [ 0x02060c18, 0x3060c000 ],
        [ 0x7cc6ced6, 0xe6c67c00 ], [ 0x10703030, 0x30307800 ],
        [ 0x78cc0c18, 0x3062fe00 ], [ 0x78cc0c38, 0x0ccc7800 ],
        [ 0x0c1c6ccc, 0xfe0c1e00 ], [ 0x7e40407c, 0x06c67c00 ],
        [ 0x3c64c0fc, 0xc6c67c00 ], [ 0xfe860c18, 0x18181800 ],
        [ 0x3c66663c, 0x66663c00 ], [ 0x7cc6c67e, 0x064c7800 ],
        [ 0x00006060, 0x00606000 ], [ 0x00006060, 0x00602040 ],
        [ 0x183060c0, 0x60301800 ], [ 0x00007c00, 0x7c000000 ],
        [ 0xc0603018, 0x3060c000 ], [ 0x78cc8c1c, 0x30003000 ],
        [ 0x3c46c2ce, 0xcc407800 ], [ 0x183c6666, 0x7e666600 ],
        [ 0xfc66667c, 0x6666fc00 ], [ 0x3c66c0c0, 0xc2663c00 ],
        [ 0xfc666666, 0x6666fc00 ], [ 0xfe626878, 0x6862fe00 ],
        [ 0xfe626878, 0x6860f000 ], [ 0x3c64c0c0, 0xce663a00 ],
        [ 0xccccccfc, 0xcccccc00 ], [ 0x3c181818, 0x18183c00 ],
        [ 0x3c181818, 0x98d87000 ], [ 0xe6666c78, 0x6c66e600 ],
        [ 0xf0606060, 0x6066fe00 ], [ 0xc6eefed6, 0xc6c6c600 ],
        [ 0xc6e6f6de, 0xcec6c600 ], [ 0x7cc6c6c6, 0xc6c67c00 ],
        [ 0xfc66667c, 0x6060f000 ], [ 0x7cc6c6c6, 0xc6c67c06 ],
        [ 0xfc66667c, 0x6c66e600 ], [ 0x7ec2c07c, 0x0686fc00 ],
        [ 0x7e5a1818, 0x18183c00 ], [ 0x66666666, 0x66663c00 ],
        [ 0xc6c6c66c, 0x6c381000 ], [ 0xc6c6c6d6, 0xfeeec600 ],
        [ 0xee6c3810, 0x386cee00 ], [ 0xc3663c18, 0x18183c00 ],
        [ 0xfe860c18, 0x3062fe00 ], [ 0x7c606060, 0x60607c00 ],
        [ 0xc0603018, 0x0c060200 ], [ 0x3e060606, 0x06063e00 ],
        [ 0x10386cc6, 0x00000000 ], [ 0x00000000, 0x00007c00 ],
        [ 0x0c080400, 0x00000000 ], [ 0x00007c04, 0xfc8cfa00 ],
        [ 0xe060607c, 0x6666fc00 ], [ 0x00007cc6, 0xc0c67c00 ],
        [ 0x1c0c0c7c, 0xcccc7a00 ], [ 0x00007cc2, 0xfec07c00 ],
        [ 0x386c60f8, 0x6060f000 ], [ 0x00007bc6, 0xc67e047c ],
        [ 0xe060606e, 0x7666e700 ], [ 0x18003818, 0x18183c00 ],
        [ 0x18003c18, 0x1818d870 ], [ 0xe060666c, 0x706ce600 ],
        [ 0x38181818, 0x18183c00 ], [ 0x0000ecd6, 0xd6c6e700 ],
        [ 0x00006e76, 0x66666600 ], [ 0x00003c66, 0x66663c00 ],
        [ 0x0000dc66, 0x667c60f0 ], [ 0x000076cc, 0xcc7c0c1e ],
        [ 0x0000dc76, 0x6060f000 ], [ 0x0000fec0, 0xfe06fe00 ],
        [ 0x10307c30, 0x30361c00 ], [ 0x0000cecc, 0xcccc7600 ],
        [ 0x00006666, 0x663c1800 ], [ 0x0000c6d6, 0xd6fe6c00 ],
        [ 0x0000c66c, 0x386cc600 ], [ 0x0000c6c6, 0xc67e0478 ],
        [ 0x0000fc98, 0x3064fc00 ], [ 0x0c181830, 0x18180c00 ],
        [ 0x10101000, 0x10101000 ], [ 0x60303018, 0x30306000 ],
        [ 0x66980000, 0x00000000 ]
    ]


def Banner(string, char_to_use):
    '''Prints the string using the character given in char_to_use.
    Example:  Banner("Example", "l") produces

         lll                                            
          ll                                            
          ll      lllll   ll lll  ll lll  lllll  ll lll 
          lllll       l   lll ll  lll ll ll    l  lll ll
          ll  ll llllll   ll  ll  ll  ll lllllll  ll    
          ll  ll l   ll   ll  ll  ll  ll ll       ll    
         llllll  lllll l  ll  ll  ll  ll  lllll  llll   
    '''
    global letters
    out = [ [], [], [], [], [], [], [], [] ]  # 8 lines of data
    for ltr in range(len(string)):
        char = string[ltr]
        if ord(char) < 32 or ord(char) > 126:
            char = " "
        ix = ord(char)-32
        bytes = []
        lines = letters[ix][0]
        #print "Lines = 0x%08x" % lines
        out[0].append(((lines & (0xff << 24)) >> 24) & 0xff)
        out[1].append(((lines & (0xff << 16)) >> 16) & 0xff)
        out[2].append(((lines & (0xff <<  8)) >>  8) & 0xff)
        out[3].append(lines & 0xff)
        lines = letters[ix][1]
        #print "Lines = 0x%08x" % lines
        out[4].append(((lines & (0xff << 24)) >> 24) & 0xff)
        out[5].append(((lines & (0xff << 16)) >> 16) & 0xff)
        out[6].append(((lines & (0xff <<  8)) >>  8) & 0xff)
        out[7].append(lines & 0xff)
    for element in out:
        for byte in element:
            PrintByteLine(byte, char_to_use)
        sys.stdout.write("\n")
    sys.stdout.write("\n")

def PrintByteLine(byte, char_to_use):
    for ix in range(8):
        if byte & (1 << (8 - ix)):
            sys.stdout.write("%s" % char_to_use)
        else:
            sys.stdout.write(" ")

def Example():
    '''Prints the word 'banner' to stdout with each ASCII character 
    from 33 to 255.  Interesting values are:

        /   H  L  M  _  l  159  178  179  206  216  219  220 228  251
    '''
    for ix in xrange(33, 256):
        print ix
        banner.Banner("banner", chr(ix))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print "Usage:  banner <string>"
        sys.exit(1)
    Banner(sys.argv[1], "X")
