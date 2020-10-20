import codecs,sys

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

'''
Works well for latin-1 and utf-8 but not so much when utf-16-le is used in place of latin-1.
'''

# Convert Unicode -> UTF-8
(e,d,sr,sw) = codecs.lookup('utf-8')
unicode_to_utf8 = sw(sys.stdout)

# Convert utf-16-le -> Unicode during .write
(encode_latin1,decode_latin1,sr_latin1,sw_latin1) = codecs.lookup('latin-1')
class StreamRewriter(codecs.StreamWriter):

    def write(self,object):

        """ Writes the object's contents encoded to self.stream
            and returns the number of bytes written.
        """
        data,consumed = decode_latin1(object,self.errors)
        self.stream.write(data)
        return len(data)
