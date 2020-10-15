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
from collections import defaultdict

# see https://gist.github.com/2012250
tree = lambda: defaultdict(tree)

def walk(d):
    '''
    Walk a tree (nested dicts).

    For each 'path', or dict, in the tree, returns a 3-tuple containing:
    (path, sub-dicts, values)

    where:
    * path is the path to the dict
    * sub-dicts is a tuple of (key,dict) pairs for each sub-dict in this dict
    * values is a tuple of (key,value) pairs for each (non-dict) item in this dict
    '''
    # nested dict keys
    nested_keys = tuple(k for k in d.keys() if isinstance(d[k],dict))
    # key/value pairs for non-dicts
    items = tuple((k,d[k]) for k in d.keys() if k not in nested_keys)

    # return path, key/sub-dict pairs, and key/value pairs
    yield ('/', [(k,d[k]) for k in nested_keys], items)

    # recurse each subdict
    for k in nested_keys:
        for res in walk(d[k]):
            # for each result, stick key in path and pass on
            res = ('/%s' % k + res[0], res[1], res[2])
            yield res

if (__name__ == '__main__'):
    # use fancy tree to store arbitrary nested paths/values
    import simplejson as json

    mem = tree()
    
    root = mem['SomeRootDirectory']
    root['foo.txt'] = None
    root['bar.txt'] = None
    root['Stories']['Horror']['rickscott.txt'] = None
    root['Stories']['Horror']['Trash']['notscary.txt'] = None
    root['Stories']['Cyberpunk']
    root['Poems']['doyoureadme.txt'] = None
    
    # convert to json string
    s = json.dumps(mem, indent=2)
    
    #print mem
    print s
    print
    
    # json.loads converts to nested dicts, need to walk them
    for (path, dicts, items) in walk(json.loads(s)):
        # this will print every path
        print '[%s]' % path
        for key,val in items:
            # this will print every key,value pair (skips empty paths)
            print '%s = %s' % (path+key,val)
        print
    