'''
Stack class

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
__version__ = "$Id: stack.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

class stack:
    '''List-based implementation of a stack class.  The stack elements
    can be any object, sequence, number, etc.
    
    The methods are:
        push(object)      Push an object onto the stack
        pop()             Remove the top of stack and return it
        is_empty()        Return nonzero if stack is empty
        num_elements()    Number of elements on stack
        dump_stack()      Print stack to stdout, 1 line per element
    '''
    def __init__(self):
        self.stack = []

    def push(self, object):
        self.stack.append(object)

    def pop(self):
        if len(self.stack) == 0:
            raise "Error", "stack is empty"
        obj = self.stack[-1]
        del self.stack[-1]
        return obj

    def is_empty(self):
        if len(self.stack) == 0:
            return 1
        return 0

    def num_elements(self):
        return len(self.stack)

    def dump_stack(self):
        print "Top of stack is last element in list (number 1)"
        n = len(self.stack)
        fmt = "  %%%dd  %%s" % len(`n + 1`)
        for ix in xrange(n):
            print fmt % (n - ix, self.stack[ix])


if __name__ == "__main__":
    list1 = [1.2, "3.4"]
    s = stack()
    error = "Error"
    if s.num_elements() != 0:  raise error
    s.push("Hi")
    s.push(4)
    s.push(list1)
    if s.is_empty():  raise error
    el = s.pop()
    if el != list1:  raise error
    del el
    el = s.pop()
    if el != 4:  raise error
    del el
    el = s.pop()
    if el != "Hi":  raise error
    if not s.is_empty():  raise error
