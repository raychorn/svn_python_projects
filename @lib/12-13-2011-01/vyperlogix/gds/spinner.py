'''
Implements a text spinner.  Prints to stdout.

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
__version__ = "$Id: spinner.py,v 1.4 2002/08/21 12:41:49 donp Exp $"

class Spinner:
    def __init__(self, type=0):
        if type == 0:
            self.char = ['.', 'o', 'O', 'o']
        else:
            self.char = ['|', '/', '-', '\\', '-']
        self.len  = len(self.char)
        self.curr = 0

    def Print(self):
        self.curr = (self.curr + 1) % self.len
        str = self.char[self.curr]
        sys.stdout.write("\b \b%s" % str)

    def Done(self):
        sys.stdout.write("\b \b")

if __name__ == "__main__":
    import time
    num_times  = 50
    delay_time = 0.08 # seconds

    print "Demo of type=0 spinner:"
    s = Spinner(type=0)
    for jx in xrange(num_times):
        s.Print()
        time.sleep(delay_time)
    s.Done()

    print "Demo of type=1 spinner:"
    s = Spinner(type=1)
    for jx in xrange(num_times):
        s.Print()
        time.sleep(delay_time)
    s.Done()
