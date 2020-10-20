from vyperlogix.enum import Enum

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

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

if __name__ == '__main__':
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__

    def _test():
    
        class Color(Enum):
            red = 1
            green = 2
            blue = 3
    
        print 'Color=(%s)' % str(Color)
        print '\n'
        print 'BEGIN: Iterate over the Enumeration:'
        for e in Color:
            print '\te=(%s)' % str(e)
        print 'END! Iterate over the Enumeration:\n'
            
        print 'Color.red=(%s), int(Color.red)=(%s)' % (Color.red,int(Color.red))
        print 'dir(Color)=(%s)' % str(dir(Color))
        print 'Color(1)=(%s)' % Color(1)
        try:
            print 'Color.orange=(%s)' % (Color.orange)
        except:
            print 'There is no Color.orange.'
        try:
            print 'Color(4)=(%s)' % (Color(4))
        except Exception, details:
            print 'There is no Color(4) due to "%s".' % str(details)
        x = 'Color.%s' % 'red'
        try:
            print '%s=(%s)' % (x,eval(x))
        except:
            print "There is no Color('red')."
    
        print 'Color.red == Color.red=(%s)' % Color.red == Color.red
        print 'Color.red == Color.blue=(%s)' % Color.red == Color.blue
        print 'Color.red == 1=(%s)' % (Color.red == 1)
        print 'Color.red == 2=(%s)' % (Color.red == 2)
    
        class ExtendedColor(Color):
            white = 0
            orange = 4
            yellow = 5
            purple = 6
            black = 7
    
        print 'ExtendedColor.orange=(%s)' % ExtendedColor.orange
        print 'ExtendedColor.red=(%s)' % ExtendedColor.red
    
        print 'Color.red == ExtendedColor.red=(%s)' % (Color.red == ExtendedColor.red)
    
        class OtherColor(Enum):
            white = 4
            blue = 5
    
        class MergedColor(Color, OtherColor):
            pass
    
        print 'MergedColor.red=(%s)' % MergedColor.red
        print 'MergedColor.white=(%s)' % MergedColor.white
    
        print 'Color=(%s)' % Color
        print 'ExtendedColor=(%s)' % ExtendedColor
        print 'OtherColor=(%s)' % OtherColor
        print 'MergedColor=(%s)' % MergedColor

    _test()
