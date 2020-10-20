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

import re

_parse = lambda foo, _re:[match for match in _re.finditer(foo)]

def __parse_for_anchor_heads(toks):
    '''Returns the contents of the opening tag for an HTML anchor.'''
    _re_anchor2 = re.compile(r"""</?\w+((\s+(\w|\w[\w\-]*\w)(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>""")
    return [t[0] if (len(t) > 0) else t for t in [_parse(t.group(),_re_anchor2) for t in toks]]

def parse_for_anchors(source):
    '''Returns the matches where match.start(), match.stop() and match.group() are meaningful.'''
    _re_anchor = re.compile("<a[^>]*>(.*?)</a>")
    return _parse(aContent.content,_re_anchor)

def parse_for_anchor_heads(source):
    '''Returns the contents of the opening tag for an HTML anchor.'''
    return __parse_for_anchor_heads(parse_for_anchors(source))

def parse_for_hrefs(aTag,source):
    from vyperlogix.html.parsers.HTMLParsers import TargetedHTMLParser
    
    myParser = TargetedHTMLParser()
    myParser.targetTag(aTag)
    myParser.feed(source)
    
    if (myParser.tagCount > 0):
        return myParser.tagContents
    return []
