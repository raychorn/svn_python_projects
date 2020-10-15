import sys

from vyperlogix import misc 

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

class PrettyPrint:
    def __init__(self,title,items,orient,delim=' '):
        '''orient of True means '''
        self.lines = []
        if (not misc.isString(title)):
            print >>sys.stderr, '(PrettyPrint).ERROR :: title cannot be "%s", it must however be a string instance.' % str(title)
        else:
            if (not misc.isList(items)):
                print >>sys.stderr, '(PrettyPrint).ERROR :: items cannot be "%s", it must however be a list instance.' % str(items)
            else:
                if (not isinstance(orient,bool)):
                    print >>sys.stderr, '(PrettyPrint).ERROR :: orient cannot be "%s", it must however be a bool instance.' % str(orient)
                else:
                    if (not misc.isString(delim)):
                        print >>sys.stderr, '(PrettyPrint).ERROR :: delim cannot be "%s", it must however be a string instance.' % str(delim)
                    else:
                        self.title = title
                        self.items = items
                        print title
                        n = 0
                        for p in items:
                            if (misc.isList(p)):
                                n = max(n,len(p))
                        stats = []
                        for i in xrange(len(items)):
                            stats.append(0)
                        for i in xrange(len(items)):
                            p = items[i]
                            if (misc.isList(p)):
                                for ii in xrange(len(p)):
                                    stats[i] = max(stats[i],len(p[ii])+len(delim))
                        self.lines = []
                        for i in xrange(len(items)):
                            p = items[i]
                            if (misc.isList(p)):
                                aLine = []
                                for ii in xrange(len(p)):
                                    if (not orient):
                                        s = '%s%s' % (' '*(stats[ii]-len(p[ii])),p[ii])
                                    else:
                                        s = '%s%s' % (p[ii],' '*(stats[ii]-len(p[ii])))
                                    if (ii == (len(p)-1)):
                                        s = s.rstrip()
                                    aLine.append(s)
                                self.lines.append(delim.join(aLine))
                            else:
                                self.lines.append(str(p))

    def pprint(self):
        print '\n'.join(self.lines)

    def __repr__(self):
        return 'PrettyPrint for "%s"' % (self.title)
