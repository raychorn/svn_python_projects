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

from string import ascii_letters, digits, punctuation

from vyperlogix.misc import _utils

def __bufferToHex__(buffer, start, count):
    accumulator = ''
    for item in xrange(count):
        try:
            accumulator += '%02X' % ord(buffer[start + item]) + ' '
        except IndexError:
            break
    return accumulator

def __bufferToAscii__(buffer, start, count):
    accumulator = ''
    _good_chars_ = ascii_letters + digits + punctuation + ' '
    _signal_break = False
    for item in xrange(count):
        try:
            char = chr(ord(buffer[start + item]))
        except IndexError:
            _signal_break = True
        if (char in _good_chars_):
            accumulator += char
        else:
            accumulator += '.'
        if (_signal_break):
            break
    return accumulator

def dumps(data,size=20,io=None,ascii_only=False):
    io = _utils.stringIO() if (io is None) else io
    index = 0
    
    bytesRead = len(data)
    while index < bytesRead:
        if (not ascii_only):
            print >> io, '%s' % (__bufferToHex__(data, index, size))
        print >> io, '|%s|' % (__bufferToAscii__(data, index, size))
        
        index += size
        if bytesRead - index < size:
            size = bytesRead - index
    return io
