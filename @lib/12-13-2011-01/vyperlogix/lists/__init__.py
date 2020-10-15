__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
from vyperlogix import misc
from vyperlogix.decorators import properties_idiom
class ConsumeableList(object):
    
    def __init__(self, aList=None):
        self.__list = aList
        self.__default__ = misc.copy(aList)
        self.__items__ = misc.reverseCopy(aList)
    
    def __getitem__(self, index):
        if (len(self.__items__) <= index):
            raise AttributeError('Invalid list index given.')
        item = self.__items__.pop()
        return item
    
    def __list__():
        doc = "the list"
        def fget(self):
            return misc.reverseCopy(self.__items__)
        return locals()    
    __list__ = property(**__list__())

    def __reset__(self):
        self.__items__ = misc.reverseCopy(self.__default__)
    
    def __iter__(self):
        def iterator(items):
            for item in items:
                yield item
        return iterator(self.__list__)
    
    def __len__(self):
        return len(self.__list__)
    
