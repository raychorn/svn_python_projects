import gzip, zlib, base64

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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

def base64_encoder(s):
    return base64.encodestring(s)

def hex_encoder(s):
    from vyperlogix.products import keys
    return keys.encode(s)

def gzip_compress(s,encoder=base64_encoder):
    l = len(s)
    sio = StringIO()
    gzipper = gzip.GzipFile(mode="wb", fileobj=sio, compresslevel=9)
    gzipper.write(s)
    gzipper.flush()
    s = sio.getvalue()
    if (callable(encoder)):
        try:
            s = encoder(s)
        except:
            pass
    return s,l

def base64_decoder(s):
    return base64.decodestring(s)

def hex_decoder(s):
    from vyperlogix.products import keys
    return keys.decode(s)

def decompress_gzip(z,l,decoder=base64_decoder):
    s = z
    if (callable(decoder)):
        try:
            s = decoder(s)
        except:
            pass
    sio = StringIO(s)
    gzipper = gzip.GzipFile(mode="rb", fileobj=sio, compresslevel=9)
    s = gzipper.read(l)
    return s
