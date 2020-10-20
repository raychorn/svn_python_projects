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

def findDjangoTemplateDirsIn(fname,target,callback=None):
    import re
    from vyperlogix import misc
    from vyperlogix.misc import collectFromPath
    __reFilter = '[._]svn' 
    rejecting_re = re.compile(__reFilter)
    _template_paths = collectFromPath.collectDirsFromPath(fname,rejecting_re=rejecting_re)
    try:
        _template_paths = dict([(k,v) for k,v in _template_paths.iteritems() if ( (callable(callback)) and (callback(k)) ) or (str(k).find('template') > -1)])
    except:
        pass
    td = list(target)
    for dirName in _template_paths.keys():
        td.insert(len(td),dirName)
    return tuple(list(set(td)))
