'''
Provides the Bsearch class that can be used to perform a binary
search in a sorted file or a large list (if the list is not large,
you'd probably just want to use the python builtin 'in' for doing
a linear search or convert the data to a dictionary).

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
__version__ = "$Id: bsearch.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

class Bsearch:  
    '''This class implements an object that will perform binary
    searches for a key.  You can initialize it with either a
    sorted list (or a sorted tuple) or a file object.  For a file 
    object, you must give the record size and the number of records 
    in the file.  You can also specify an initial offset in the file 
    to where the first record occurs.  You also need to provide a 
    compare function that returns -1 for <, 0 for ==, and 1 for >.
    '''

    def __init__(self, data_container, compare_function, num_records=0,                  record_size=0, first_record_offset=0):
        '''data_container can be a sequence or an open file descriptor.
        '''
        self.err = "Error"
        self.container   = data_container
        self.compare_function = compare_function
        if type(data_container) == type([]) or            type(data_container) == type(()):
            self.type        = "list"
            self.num_records = len(data_container)
            if self.num_records < 1:
                raise self.err,                       "data_container is empty list"
        elif type(data_container) == type(sys.stdin):
            self.type        = "file"
            self.num_records = num_records
            self.record_size = record_size
            self.offset      = first_record_offset
            self.cmp         = compare_function
            # Make sure we can seek
            data_container.seek(self.offset)
            data_container.seek(self.offset + (num_records - 1) * record_size)
        else:
            raise self.err,                   "data_container parameter must be list or file object"

    def __get_index(self, index):
        '''Return the (index+1)th item
        '''
        if self.type == "list":
            return self.container[index]
        else:
            self.container.seek(self.offset + index*self.record_size)
            str = self.container.read(self.record_size)
            return str

    def KeyIsInContainer(self, key):
        '''Returns a tuple; the first element is 1 or 0, depending on
        whether the key is in the data_container or not.  The second
        element is the zero-based index of the key in the container.
        '''
        lower = 0
        upper = self.num_records
        while (lower < upper):
            index = (lower + upper)/2
            str = self.__get_index(index)
            cmp = self.compare_function(key, str)
            if cmp < 0:
                upper = index
            elif cmp > 0:
                lower = index + 1
            else:
                return (1, index)
        return (0, -1)
        
