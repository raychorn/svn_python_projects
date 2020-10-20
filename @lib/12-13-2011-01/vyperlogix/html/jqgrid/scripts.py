from django.template import Context, loader

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

def head(url):
    toks = url.split('/')
    url = '/'.join(toks[0:-1 if (toks[-1] == '') else len(toks)])
    html='''
<link rel="stylesheet" type="text/css" media="screen" href="{{ url }}/themes/basic/grid.css" />
<link rel="stylesheet" type="text/css" media="screen" href="{{ url }}/themes/jqModal.css" />
<script src="{{ url }}/js/jquery.js" type="text/javascript"></script>
<script src="{{ url }}/js/jqModal.js" type="text/javascript"></script>
<script src="{{ url }}/js/jquery.jqGrid.js" type="text/javascript"></script>
<script src="{{ url }}/js/jqDnR.js" type="text/javascript"></script>
'''
    tplate = loader.get_template_from_string(html)
    content = tplate.render(Context({'url': url}))
    return content

def js(head):
    toks = url.split('/')
    url = '/'.join(toks[0:-1 if (toks[-1] == '') else len(toks)])
    html='''<script type="text/javascript">{{ HEAD }}</script>'''
    tplate = loader.get_template_from_string(html)
    content = tplate.render(Context({'HEAD':_head}))
    return content

def head_list(url):
    return [item for item in head(url).split('\n') if (len(item.strip()) > 0)]
