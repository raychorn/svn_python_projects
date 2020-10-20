__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

from vyperlogix.classes.CooperativeClass import Cooperative

class TinyTreeMixIn(Cooperative):
    '''
    This MixIn provides the tinytree.tree with the ability to render itself as a nested Python dict {} to allow for pickling.
    
    The assumption is that all Node classes that use this MixIn will either use the properties_idiom to define properties or
    implement instance vars to define properties.
    
    Also the __init__() method must specify optional params for all of the properties that init the Node which means
    the Node instance must be capable of being initialized via the individual params rather than only via the __init__()
    method.
    '''
    __avoid__ = ['parent','children']
    def asPythonDict(self):
        '''
        Renders the node as a Python dict {} suitable for pickling.
        DO NOT USE tail-recursion optimization on this function or bad evil things will happen to the children of each node.
        '''
        node = {}
        for key in self.__dict__.keys():
            if (key not in self.__avoid__):
                property_name = key.strip('__')
                node[property_name] = self.__dict__[key]
        children = []
        for aNode in self.children:
            children.append(aNode.asPythonDict())
        node['children'] = children
        node['__module__'] = self.__module__
        return node

    def fromPythonDict(self,aDict):
        '''
        Renders the tree node from a Python dict {} taken from a pickle.
        DO NOT USE tail-recursion optimization on this function or bad evil things will happen to the children of each node.
        '''
        node = self.__class__()
        for key in self.__dict__.keys():
            if (key not in self.__avoid__):
                property_name = key.strip('__')
                self.__dict__[key] = aDict[property_name]
        if (aDict.has_key('children')):
            for aChild in aDict['children']:
                node.addChild(self.fromPythonDict(aChild))
        return node
