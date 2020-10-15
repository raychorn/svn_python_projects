#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public Lisense)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#Keywords

import keyword, string
import wx.stc
from drProperty import *

def GetKeyWords(number):
    if number == 0:
        return string.join(keyword.kwlist)
    elif number == 1:
        return "".join(GetCPPKeywords())
    elif number == 2:
        return "".join(GetHTMLKeyWords())
    return ""

def GetLexer(number):
    if number == 0:
        return wx.stc.STC_LEX_PYTHON
    elif number == 1:
        return wx.stc.STC_LEX_CPP
    elif number == 2:
        return wx.stc.STC_LEX_HTML
    return wx.stc.STC_LEX_NULL

def GetCPPKeywords():
    return ["asm ", "auto ", "bool ", "break ", "case ", "catch ", "char ", "class ", "const ", "const_cast ", "continue ", "default ", "delete ", "do ", "double ", "dynamic_cast ", "else ", "enum ", "explicit ", "export ", "extern ", "false ", "float ", "for ", "friend ", "goto ", "if ", "inline ", "int ", "long ", "mutable ", "namespace ", "new ", "operator ", "private ", "protected ", "public ", "register ", "reinterpret_cast ", "return ", "short ", "signed ", "sizeof ", "static ", "static_cast ", "struct ", "switch ", "template ", "this ", "throw ", "true ", "try ", "typedef ", "typeid ", "typename ", "union ", "unsigned ", "using ", "virtual ", "void ", "volatile ", "wchar_t ", "whileasm ", "auto ", "bool ", "break ", "case ", "catch ", "char ", "class ", "const ", "const_cast ", "continue ", "default ", "delete ", "do ", "double ", "dynamic_cast ", "else ", "enum ", "explicit ", "export ", "extern ", "false ", "float ", "for ", "friend ", "goto ", "if ", "inline ", "int ", "long ", "mutable ", "namespace ", "new ", "operator ", "private ", "protected ", "public ", "register ", "reinterpret_cast ", "return ", "short ", "signed ", "sizeof ", "static ", "static_cast ", "struct ", "switch ", "template ", "this ", "throw ", "true ", "try ", "typedef ", "typeid ", "typename ", "union ", "unsigned ", "using ", "virtual ", "void ", "volatile ", "wchar_t ", "while "]

def GetHTMLKeyWords():
    return ["a ", "abbr ", "acronym ", "address ", "applet ", "area ", "b ", "base ", "basefont ", "bdo ", "big ", "blockquote ", "body ", "br ", "button ", "caption ", "center ", "cite ", "code ", "col ", "colgroup ", "dd ", "del ", "dfn ", "dir ", "div ", "dl ", "dt ", "em ", "fieldset ", "font ", "form ", "frame ", "frameset ", "h1 ", "h2 ", "h3 ", "h4 ", "h5 ", "h6 ", "head ", "hr ", "html ", "i ", "iframe ", "img ", "input ", "ins ", "isindex ", "kbd ", "label ", "legend ", "li ", "link ", "map ", "menu ", "meta ", "noframes ", "noscript ", "object ", "ol ", "optgroup ", "option ", "p ", "param ", "pre ", "q ", "s ", "samp ", "script ", "select ", "small ", "span ", "strike ", "strong ", "style ", "sub ", "sup ", "table ", "tbody ", "td ", "textarea ", "tfoot ", "th ", "thead ", "title ", "tr ", "tt ", "u ", "ul ", "var ", "xml ", "xmlns ", "abbr ", "accept-charset ", "accept ", "accesskey ", "action ", "align ", "alink ", "alt ", "archive ", "axis ", "background ", "bgcolor ", "border ", "cellpadding ", "cellspacing ", "char ", "charoff ", "charset ", "checked ", "cite ", "class ", "classid ", "clear ", "codebase ", "codetype ", "color ", "cols ", "colspan ", "compact ", "content ", "coords ", "data ", "datafld ", "dataformatas ", "datapagesize ", "datasrc ", "datetime ", "declare ", "defer ", "dir ", "disabled ", "enctype ", "event ", "face ", "for ", "frame ", "frameborder ", "headers ", "height ", "href ", "hreflang ", "hspace ", "http-equiv ", "id ", "ismap ", "label ", "lang ", "language ", "leftmargin ", "link ", "longdesc ", "marginwidth ", "marginheight ", "maxlength ", "media ", "method ", "multiple ", "name ", "nohref ", "noresize ", "noshade ", "nowrap ", "object ", "onblur ", "onchange ", "onclick ", "ondblclick ", "onfocus ", "onkeydown ", "onkeypress ", "onkeyup ", "onload ", "onmousedown ", "onmousemove ", "onmouseover ", "onmouseout ", "onmouseup ", "onreset ", "onselect ", "onsubmit ", "onunload ", "profile ", "prompt ", "readonly ", "rel ", "rev ", "rows ", "rowspan ", "rules ", "scheme ", "scope ", "selected ", "shape ", "size ", "span ", "src ", "standby ", "start ", "style ", "summary ", "tabindex ", "target ", "text ", "title ", "topmargin ", "type ", "usemap ", "valign ", "value ", "valuetype ", "version ", "vlink ", "vspace ", "width ", "text ", "password ", "checkbox ", "radio ", "submit ", "reset ", "file ", "hidden ", "image ", "public ", "!doctype ", "dtml-var ", "dtml-if ", "dtml-unless ", "dtml-in ", "dtml-with ", "dtml-let ", "dtml-call ", "dtml-raise ", "dtml-try ", "dtml-comment ", "dtml-tree "]

def SetSTCStyles(frame, stc, number):
    if number == 0:
        stc.StyleSetSpec(wx.stc.STC_P_CHARACTER, frame.prefs.txtDocumentStyleDictionary[4])
        stc.StyleSetSpec(wx.stc.STC_P_CLASSNAME, frame.prefs.txtDocumentStyleDictionary[5])
        stc.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, frame.prefs.txtDocumentStyleDictionary[7])
        stc.StyleSetSpec(wx.stc.STC_P_DEFNAME, frame.prefs.txtDocumentStyleDictionary[8])
        stc.StyleSetSpec(wx.stc.STC_P_WORD, frame.prefs.txtDocumentStyleDictionary[9])
        stc.StyleSetSpec(wx.stc.STC_P_NUMBER, frame.prefs.txtDocumentStyleDictionary[10])
        stc.StyleSetSpec(wx.stc.STC_P_OPERATOR, frame.prefs.txtDocumentStyleDictionary[11])
        stc.StyleSetSpec(wx.stc.STC_P_STRING, frame.prefs.txtDocumentStyleDictionary[12])
        stc.StyleSetSpec(wx.stc.STC_P_STRINGEOL, frame.prefs.txtDocumentStyleDictionary[13])
        stc.StyleSetSpec(wx.stc.STC_P_TRIPLE, frame.prefs.txtDocumentStyleDictionary[14])
        stc.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, frame.prefs.txtDocumentStyleDictionary[14])
        stc.SetSelForeground(1, getStyleProperty("fore", frame.prefs.txtDocumentStyleDictionary[16]))
        stc.SetSelBackground(1, getStyleProperty("back", frame.prefs.txtDocumentStyleDictionary[16]))
    elif number == 1:
        stc.StyleSetSpec(wx.stc.STC_C_CHARACTER, frame.prefs.txtDocumentStyleDictionary[4])
        stc.StyleSetSpec(wx.stc.STC_C_PREPROCESSOR, frame.prefs.txtDocumentStyleDictionary[5])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENT, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENTLINE, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENTLINEDOC, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENTDOCKEYWORD, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENTDOCKEYWORDERROR, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_COMMENTDOC, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_C_VERBATIM, frame.prefs.txtDocumentStyleDictionary[7])
        stc.StyleSetSpec(wx.stc.STC_C_WORD, frame.prefs.txtDocumentStyleDictionary[8])
        stc.StyleSetSpec(wx.stc.STC_C_WORD2, frame.prefs.txtDocumentStyleDictionary[8])
        stc.StyleSetSpec(wx.stc.STC_C_IDENTIFIER, frame.prefs.txtDocumentStyleDictionary[9])
        stc.StyleSetSpec(wx.stc.STC_C_NUMBER, frame.prefs.txtDocumentStyleDictionary[10])
        stc.StyleSetSpec(wx.stc.STC_C_OPERATOR, frame.prefs.txtDocumentStyleDictionary[11])
        stc.StyleSetSpec(wx.stc.STC_C_STRING, frame.prefs.txtDocumentStyleDictionary[12])
        stc.StyleSetSpec(wx.stc.STC_C_STRINGEOL, frame.prefs.txtDocumentStyleDictionary[13])
        stc.StyleSetSpec(wx.stc.STC_C_GLOBALCLASS, frame.prefs.txtDocumentStyleDictionary[14])
        stc.StyleSetSpec(wx.stc.STC_C_REGEX, frame.prefs.txtDocumentStyleDictionary[15])
        stc.StyleSetSpec(wx.stc.STC_C_UUID, frame.prefs.txtDocumentStyleDictionary[16])
        stc.SetSelForeground(1, getStyleProperty("fore", frame.prefs.txtDocumentStyleDictionary[18]))
        stc.SetSelBackground(1, getStyleProperty("back", frame.prefs.txtDocumentStyleDictionary[18]))
    elif number == 2:
        stc.StyleSetSpec(wx.stc.STC_H_TAG, frame.prefs.txtDocumentStyleDictionary[4])
        stc.StyleSetSpec(wx.stc.STC_H_TAGUNKNOWN, frame.prefs.txtDocumentStyleDictionary[5])
        stc.StyleSetSpec(wx.stc.STC_H_ATTRIBUTE, frame.prefs.txtDocumentStyleDictionary[6])
        stc.StyleSetSpec(wx.stc.STC_H_ATTRIBUTEUNKNOWN, frame.prefs.txtDocumentStyleDictionary[7])
        stc.StyleSetSpec(wx.stc.STC_H_NUMBER, frame.prefs.txtDocumentStyleDictionary[8])
        stc.StyleSetSpec(wx.stc.STC_H_DOUBLESTRING, frame.prefs.txtDocumentStyleDictionary[9])
        stc.StyleSetSpec(wx.stc.STC_H_SINGLESTRING, frame.prefs.txtDocumentStyleDictionary[10])
        stc.StyleSetSpec(wx.stc.STC_H_OTHER, frame.prefs.txtDocumentStyleDictionary[10])
        stc.StyleSetSpec(wx.stc.STC_H_COMMENT, frame.prefs.txtDocumentStyleDictionary[11])
        stc.StyleSetSpec(wx.stc.STC_H_XCCOMMENT, frame.prefs.txtDocumentStyleDictionary[11])
        stc.StyleSetSpec(wx.stc.STC_H_ENTITY, frame.prefs.txtDocumentStyleDictionary[12])
        stc.StyleSetSpec(wx.stc.STC_H_TAGEND, frame.prefs.txtDocumentStyleDictionary[13])
        stc.StyleSetSpec(wx.stc.STC_H_XMLSTART, frame.prefs.txtDocumentStyleDictionary[14])
        stc.StyleSetSpec(wx.stc.STC_H_XMLEND, frame.prefs.txtDocumentStyleDictionary[15])
        stc.StyleSetSpec(wx.stc.STC_H_SCRIPT, frame.prefs.txtDocumentStyleDictionary[16])
        stc.StyleSetSpec(wx.stc.STC_H_ASP, frame.prefs.txtDocumentStyleDictionary[16])
        stc.StyleSetSpec(wx.stc.STC_H_ASPAT, frame.prefs.txtDocumentStyleDictionary[16])
        stc.StyleSetSpec(wx.stc.STC_H_VALUE, frame.prefs.txtDocumentStyleDictionary[17])
        stc.StyleSetSpec(wx.stc.STC_H_QUESTION, frame.prefs.txtDocumentStyleDictionary[17])
        stc.SetSelForeground(1, getStyleProperty("fore", frame.prefs.txtDocumentStyleDictionary[19]))
        stc.SetSelBackground(1, getStyleProperty("back", frame.prefs.txtDocumentStyleDictionary[19]))