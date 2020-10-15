'''
This module implements a class Set using lists.  Using lists
allows the Set class to be general, but it can be inefficient
for sets with large numbers of elements.  If you need speed,
consider using the setf.py implementation, which uses dictionaries
to store set elements.  It's fast, but the tradeoff is that
you can only store hashable objects, which appear to me to be
numbers and strings.

Both set.py and setf.py have the identical set of class methods
and attributes.

The class is named Set in both cases.  If you import the class with
a statement like 'import Set from set', you can change to the
other implementation by just changing it to 'import Set from setf'.

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

__version__ = "$Id: set.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

class Set:
    '''Class that implements a set.  The supported methods are:
        
        add_to_set(element)
            Adds the element to the set.  Element can be a list, tuple,
            dictionary, string, number, or set.  If it is a list, tuple, 
            dictionary, or set and self.decompose is true, it is broken 
            into its component parts and those are stored in the set 
            (otherwise element is just added to the set).
        delete_from_set(element)
            Deletes the element from the set.  Element can be a list, 
            tuple, dictionary, string, number, or a set.  If it is a
            list, tuple, dictionary, or set and self.decompose is true,
            element is broken into its component parts and each part is
            deleted from the set.  An exception will occur if one of 
            the elements is not in the set and self.harsh is true.  
        intersection(other_set)
            Returns a set that is the intersection of self and other_set.
        union(other_set)
            Returns a set that is the union of self and other_set.
        difference(other_set)
            Returns a set that consists of all elements in self that are
            not in other_set.
        is_in_set(element)
            Returns 1 if element is in the set, 0 if not.
        is_empty_set()
            Returns 1 if the set is empty.
        is_subset_of(other_set)
            Returns 1 if self is a subset of other_set; otherwise returns 0.
        is_proper_subset_of(other_set)
            Returns 1 if self is a proper subset of other_set; otherwise 
            returns 0.
        list()
            Returns a list of the elements of the set.
        __len__()
            Returns the number of elements in the set.
        __getitem__(element)
            Returns 1 if element is in set, 0 if not.
        __and__(other_set)
        __mul__(other_set)
        __rmul__(other_set)
            Same as intersection method.
        __or__(other_set)
        __add__(other_set)
        __radd__(other_set)
            Same as union method.
        __repr__
            Returns a string representation of the set.
        __sub__
            Same as difference() method.
        __cmp__(other_set)
            Returns 0 if self and other_set have the same member elements,
            otherwise returns 1.
        __repr__()
            Returns a string representation of the Set object.

    Because of the supported methods, you may use sets in the following
    ways; assumes r, s, and t are set objects:
        
        t = r + s      Union
        t = r | s      Union
        t = r * s      Intersection
        t = r & s      Intersection
        t = r - s      Difference
        r == s         Equality
        r != s         Non-equality
        s["a"]         Returns 1 if the string "a" is in set.

    You can pass in a dictionary, list, or tuple and it will be
    converted to a set.  If you pass in a dictionary, the keys are
    the set elements (the values are ignored).

    Attributes & parameters:

        sorted         Set to true to sort the set before printing or
                       returning as a list.  Default is false.

        harsh          If true, causes an exception to be thrown if you 
                       try to delete an element not in the list.  Defaults
                       to true.

        decompose      (Parameter to constructor)  Set this to true
                       if you want the value parameter decomposed into
                       its components and those components then make
                       up the set.  If the decompose parameter is false, 
                       the value parameter becomes the one and only 
                       element of the set.  Default is true.

        version        The class version string (it's maintained with
                       RCS).

    '''

    def __init__(self, value=None, decompose=1, harsh=1, sorted=0):
        self.set       = []
        self.sorted    = sorted
        self.harsh     = harsh
        self.decompose = decompose
        self.version   = "$Id: set.py,v 1.3 2002/08/21 12:41:49 donp Exp $"
        if value != None:
            if (type(value) == type([]) or type(value) == type(()) or                 type(value) == type({}) or type(value) == type(self))                 and decompose:
                if type(value) == type({}):
                    set_list = value.keys()
                elif type(value) == type(()):
                    set_list = list(value)
                elif type(value) == type(self):
                    set_list = value.list()
                else:
                    set_list = value
                self.set = set_list
            else:
                self.set.append(value)
                
    def add_to_set(self, object):
        if (type(object) == type([]) or type(object) == type(()) or             type(object) == type({}) or type(object) == type(self))             and self.decompose:
            if type(object) == type({}):
                set_list = object.keys()
            elif type(object) == type(()):
                set_list = list(object)
            elif type(object) == type(self):
                set_list = object.list()
            else:
                set_list = object
            self.set = self.set + set_list
        else:
            self.set.append(object)

    def delete_from_set(self, object):
        items_to_delete = []
        if (type(object) == type([]) or type(object) == type(()) or             type(object) == type({}) or type(object) == type(self))             and self.decompose:
            if type(object) == type({}):
                items_to_delete = object.keys()
            elif type(object) == type(()):
                items_to_delete = list(object)
            elif type(object) == type(self):
                items_to_delete = object.list()
            else:
                items_to_delete = object
        else:
            items_to_delete = [object]
        for item in items_to_delete:
            if item in self.set:
                ix = self.set.index(item)
                del self.set[ix]
            else:
                if self.harsh:
                    raise "Error", "item '%s' not in set" % `item`

    def intersection(self, other_set):
        self.__check_if_is_a_set(other_set)
        new_set = []
        if len(self.set) > len(other_set.set):
            iter_set = self.set[:]
            smaller_set = other_set.set
        else:
            iter_set = other_set.set[:]
            smaller_set = self.set
        for element in iter_set:
            if element in smaller_set:
                new_set.append(element)
        return Set(new_set, decompose=1)

    def union(self, other_set):                             
        self.__check_if_is_a_set(other_set)
        if len(self.set) > len(other_set.set):
            new_set = self.set[:]
            iter_set = self.set[:]
            smaller_set = other_set.set
        else:
            new_set = other_set.set[:]
            iter_set = other_set.set[:]
            smaller_set = self.set
        for element in smaller_set:
            if element not in iter_set:
                new_set.append(element)
        return Set(new_set, decompose=1)                         

    def difference(self, other_set):
        '''Returns a set that consists of all elements in self that are
        not in other_set.
        '''
        self.__check_if_is_a_set(other_set)
        new_set = self.set[:]
        for element in other_set.set:
            try:
                ix = new_set.index(element)
                del new_set[ix]
            except:
                pass
        return Set(new_set, decompose=1)

    def is_in_set(self, element):
        return self.__getitem__(element)

    def is_empty_set(self):
        return not len(self.set)

    def is_subset_of(self, other_set):
        '''Return 1 if self is a subset of other_set, otherwise 
        return 0.  This is based on the theorem that if A is a 
        subset of B, then (A union B) = B and (A intersection B) = A.  
        Here, we get the intersection of self and other_set and see 
        if it is equal to other_set.
        '''
        self.__check_if_is_a_set(other_set)
        return self.__cmp__(self.intersection(other_set)) == 0

    def is_proper_subset_of(self, other_set):
        '''Return 1 if self is a proper subset of other_set, otherwise 
        return 0.
        '''
        return self.is_subset_of(other_set) and                (len(self.set) != len(other_set.set))

    def list(self):
        s = self.set[:]
        if self.sorted:
            s.sort()
        return s

    def __check_if_is_a_set(self, other_set):
        if type(other_set) != type(self):
            raise "Error", "other_set must be a set object"

    def __len__(self):
        return len(self.set)

    def __getitem__(self, element):
        '''If element is in set, return 1; otherwise return 0.
        '''
        try:
            ix = self.set.index(element)
            return 1
        except:
            return 0

    def __and__(self, other_set):
        return self.intersection(other_set)

    def __mul__(self, other_set):
        return self.intersection(other_set)

    def __rmul__(self, other_set):
        return self.intersection(other_set)

    def __or__(self, other_set):
        return self.union(other_set)

    def __add__(self, other_set):
        return self.union(other_set)

    def __radd__(self, other_set):
        return self.union(other_set)

    def __sub__(self, other_set):
        return self.difference(other_set)

    def __cmp__(self, other_set):
        '''Returns 0 if self.set is equal to other; otherwise returns 1.
        '''
        if type(other_set) != type(self) or            len(other_set.set) != len(self.set):
            return 1
        for element in other_set.set:
            if element not in other_set.set:
                return 1
        return 0

    def __repr__(self):
        s = self.set[:]
        if self.sorted:
            s.sort()
        str = `s`
        str = "<" + str[1:]
        return str[:-1] + ">"

if __name__ == "__main__":
    # Test the Set class
    from testset import Test
    Test(N=5, use_list_implementation=1)
