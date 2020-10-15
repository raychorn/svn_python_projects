'''
PyOoHtml - Python Object Oriented HTML (version 0.0.b - 2008.06.21)
'The future is reusable'


Public domain (P) 2008 Davide Rognoni

DAVIDE ROGNONI DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS, IN NO EVENT SHALL DAVIDE ROGNONI BE LIABLE FOR
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.

E-mail: davide.rognoni@gmail.com
"PyOoHtml Free Services" on http://pyoohtml.appspot.com/


NEWS
----
Add HIDDEN, IMG, IFRAME
New text2(...)
Fixed tagPRE(...) --> t.html(...) --> t.text2(...)
Fixed the others tagXXX(...)


FILES LIST
----------
pyoohtml.py
static/test.css
static/test.js


DEPENDENCES
-----------
Python 2.5.1


TUTORIAL
--------
See the main code:
python pyoohtml.py

See the generated file "test.html" (This Page Is Valid HTML 4.0 Transitional!)
'''

import re

from vyperlogix import misc

# generic const
DOCTYPE_40_TRANSITIONAL = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">'

# tags
A = 'a'
BODY = 'body'
BR = 'br'
DIV = 'div'
FORM = 'form'
H1 = 'h1'
H2 = 'h2'
H3 = 'h3'
HEAD = 'head'
HTML = 'html'
HR = 'hr'
IFRAME = 'iframe'
IMG = 'img'
INPUT = 'input'
LI = 'li'
META = 'meta'
OL = 'ol'
OPTION = 'option'
P = 'p'
PRE = 'pre'
SCRIPT = 'script'
SELECT = 'select'
SPAN = 'span'
STYLE = 'style'
TABLE = 'table'
TEXTAREA = 'textarea'
TD = 'td'
TH = 'th'
TITLE = 'title'
TR = 'tr'
UL = 'ul'

# properties and attributes
ALL = 'all'
AUTHOR = 'author'
BUTTON = 'button'
CHECKBOX = 'checkbox'
CHECKED = 'checked'
CONTENT_TYPE = 'content-type'
DESCRIPTION = 'description'
DISABLED = 'disabled'
FILE = 'file'
HIDDEN = 'hidden'
KEYWORDS = 'keywords'
MULTIPART_FORM_DATA = 'multipart/form-data'
MULTIPLE = 'multiple'
POST = 'post'
RADIO = 'radio'
READONLY = 'readonly'
ROBOTS = 'robots'
SELECTED = 'selected'
SUBMIT = 'submit'
TEXT = 'text'
TEXT_CSS = 'text/css'
TEXT_HTML_CHARSET_ISO_8859_1 = "text/html; charset=iso-8859-1"
TEXT_JAVASCRIPT = 'text/javascript'

class Html:
    '''Base element: tag or text'''
    def __init__(self):
        self.txt = None # if text is not None
        self.name = None # if tag is not None
        self.inline = False # if True: <table><tr><td>text</td></tr></table>
        self.open = False # if True: <input readonly type="text" name="input1" value="1">
        self.properties = [] # example: readonly
        self.attributes = {} # example: id="content"
        self.elements = [] # tag or text

    def tag(self, _name, *properties, **attributes):
        '''Makes a new tag, appends to parent and returns it'''
        h = Html()
        h.name = _name
        h.properties = properties
        h.attributes = attributes
        self.elements.append(h)
        return h

    def tagIn(self, _name, *properties, **attributes):
        '''inline tag, example: <table><tr><td>text</td></tr></table>'''
        h = self.tag(_name, *properties, **attributes)
        h.inline = True
        return h

    def tagOp(self, _name, *properties, **attributes):
        '''open tag, example: <input type="text" name="input1" value="1">'''
        h = self.tag(_name, *properties, **attributes)
        h.open = True
        return h

    def text(self, txt):
        '''Makes a new text and appends to parent'''
        h = Html()
        h.txt = txt
        self.elements.append(h)

    def text2(self, txt):
        '''Makes a new formatted text and appends to parent'''
        h = Html()
        h.txt = txt
        if txt:
            h.txt = str(txt).replace('<', '&lt;')
        self.elements.append(h)

    def html(self,txt):
        '''Makes a new formatted text and appends to parent
		Example: [b bold] [a link, http://python.org] [i italic] [u underline] [code code]'''
        h = Html()
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('\n', '<br>')
        h.txt = re.sub('\[(\w+)\s+(.+?)]', self.__html, txt)
        self.elements.append(h)

    def __html(self, match):
        tag = match.group(1)
        attributes = ''
        text = match.group(2)
        if tag == 'a':
            text = text.split(',', 1)
            attributes = ' href="%s"' % (text[1].strip())
            text = text[0].strip()
        return "<%s%s>%s</%s>" % (tag, attributes, text, tag)

    def toHtml(self):
        '''Makes html text and return it'''
        return self.__toHtml(0, self.elements)

    def __toHtml(self, level, elements):
        tabs = '\t'*level
        out = ''
        for e in elements:
            if e.txt != None:
                out += '%s' % (e.txt)
            else:
                if not e.inline:
                    out += "\n%s" % (tabs)
                if e.open:
                    out += '<%s%s%s>' % (e.name, self.__toProperties(e.properties),
                                         self.__toAttributes(e.attributes))
                else:
                    out += '<%s%s%s>%s</%s>' % (e.name, self.__toProperties(e.properties),
                                                self.__toAttributes(e.attributes), self.__toHtml(level+1, e.elements), e.name)
        return out

    def __toAttributes(self, a):
        s = ""
        for k in a:
            s += ' %s="%s"' % (self.__replaceKey(k), a[k])
        return s

    def __toProperties(self, p):
        s = ""
        for i in p:
            s += ' %s' % (i)
        return s

    # from "class_" to "class"
    # from "http_equiv" to http-equiv
    def __replaceKey(self, k):
        k = k.rstrip('_')
        k = k.replace('_','-')
        return k

    def tagA(self, _text, **attributes):
        t = self.tag(A, **attributes)
        t.text2(_text)
        return t

    def tagH1(self, _text, **attributes):
        t = self.tag(H1, **attributes)
        t.text2(_text)
        return t

    def tagH2(self, _text, **attributes):
        t = self.tag(H2, **attributes)
        t.text2(_text)
        return t

    def tagH3(self, _text, **attributes):
        t = self.tag(H3, **attributes)
        t.text2(_text)
        return t

    def tag_H1(self, _text, **attributes):
        t = self.tag(H1, **attributes)
        t.text(_text)
        return t

    def tag_H2(self, _text, **attributes):
        t = self.tag(H2, **attributes)
        t.text(_text)
        return t

    def tag_H3(self, _text, **attributes):
        t = self.tag(H3, **attributes)
        t.text(_text)
        return t

    def tagLI(self, _text, **attributes):
        t = self.tag(LI, **attributes)
        t.text2(_text)
        return t

    def tagOPTION(self, _text, *properties, **attributes):
        t = self.tag(OPTION, *properties, **attributes)
        t.text2(_text)
        return t

    def tagPRE(self, _text, **attributes):
        t = self.tag(PRE, **attributes)
        t.text2(_text)
        return t

    def tagSELECT(self, options, _value, *properties, **attributes):
        select = self.tag(SELECT, *properties, **attributes)
        for o in options:
            if self.__isSelected(o[0], _value):
                select.tagOPTION(o[1], SELECTED, value=o[0])
            else:
                select.tagOPTION(o[1], value=o[0])

    def __isSelected(self, value, values):
        if (misc.isList(values)):
            for v in values:
                if value == v:
                    return True
        elif (value == values):
                return True
        return False

    def tagSCRIPT(self, _text='', **attributes):
        attributes['type'] = TEXT_JAVASCRIPT
        t = self.tag(SCRIPT, **attributes)
        t.text(_text)
        return t

    def tagSPAN(self, _text, **attributes):
        t = self.tag(SPAN, **attributes)
        t.text2(_text)
        return t

    def tagSTYLE(self, _text, **attributes):
        attributes['type'] = TEXT_CSS
        t = self.tag(STYLE, **attributes)
        t.text(_text)
        return t

    def tagTABLE(self, _rows, **attributes):
        table = self.tag(TABLE, **attributes)
        tr = table.tag(TR)
        for c in _rows[0]:
            tr.tagTH(c)
        for r in _rows[1:]:
            tr = table.tag(TR)
            for c in r:
                tr.tagTD(c)

    def tagTH(self, _text, **attributes):
        t = self.tag(TH, **attributes)
        t.text2(_text)
        return t

    def tagTITLE(self, _text, **attributes):
        t = self.tag(TITLE, **attributes)
        t.text2(_text)
        return t

    def tagTEXTAREA(self, _text, *properties, **attributes):
        t = self.tag(TEXTAREA, *properties, **attributes)
        t.text(_text)
        return t

    def metas(self, *metas):
        for m in metas:
            self.tagOp(META, name=m[0], content=m[1])

    def scripts(self, *scripts):
        for s in scripts:
            self.tagSCRIPT(src=s)

if  __name__ == '__main__':
    h = Html()
    h.text(DOCTYPE_40_TRANSITIONAL)

    html = h.tag(HTML)
    head = html.tag(HEAD)
    head.tagOp(META, http_equiv=CONTENT_TYPE, content=TEXT_HTML_CHARSET_ISO_8859_1)
    head.metas(
        (AUTHOR, "Davide Rognoni"),
        (KEYWORDS, "Python, Object, Oriented, HTML"),
        (DESCRIPTION, "Python Object Oriented HTML - 'The future is reusable'"),
        (ROBOTS, ALL))
    head.tagTITLE("This is the title")
    head.scripts("static/test.js", "static/test2.js")
    head.tagSCRIPT("function test() {jsTest()}")
    head.tagSTYLE('@import "static/test.css";')

    body = html.tag(BODY)
    idContent = body.tag(DIV, id="content", style="background-color: yellow")
    idContent.text("This is")
    idContent.tagOp(BR)
    idContent.text("the content")
    idContent.tagH1("This is the title")

    a = idContent.tag(A, href="javascript:test()")
    a.text("Alert")
    idContent.text("|")
    a = idContent.tagIn(A, href="javascript:test()")
    idContent.text(" |")
    a.text("Alert2")
    a = idContent.tagA("Alert3", href="javascript:test()")
    idContent.tagOp(HR)

    idContent.tagTABLE((
        ("Col 1","Col 2"),
        ("1.1","1.2"),
        ("2.1","2.2")), border="1")

    form = idContent.tag(FORM, action="test.html")
    form.tagOp(INPUT, READONLY, type=TEXT, name="input1", value="1")
    form.tagOp(INPUT, DISABLED, type=TEXT, name="input2", value="2")
    form.tagOp(INPUT, CHECKED, type=CHECKBOX, name="input3", value="yes")
    form.tagOp(INPUT, CHECKED, type=RADIO, name="input4", value="yes")

    options = (
        ("a","option a"),
        ("b","option b"),
        ("c","option c"))
    form.tagSELECT(options, "b", name="input5")
    form.tagSELECT(options, ("a","c"), MULTIPLE, name="input6", size="3")

    form.tagTEXTAREA("hello", name="input7", cols="8", rows="2")
    form.tagOp(INPUT, type=FILE, name="input8")
    form.tagOp(INPUT, type=SUBMIT)

    p = idContent.tag(P)
    p.text("This is a new paragraph")
    p = idContent.tag(P)
    p.html("""This is a <new> paragraph
with [b bold] [a link, javascript:alert('link')] [i italic] [u underline] [code code]""")

    p.tagSPAN("span", class_= "colored")

    idContent.tagPRE("""\
function test() {
                     alert("<Hello>");
}""")

    ul = idContent.tag(UL)
    ul.tagLI("One")
    li = ul.tagLI("Two")
    ol = li.tag(OL)
    ol.tagLI("Two A")
    ol.tagLI("Two B")
    ul.tagLI("Three")

    # save on file
    f = file("test.html", "w")
    f.write(h.toHtml())
    f.close()
