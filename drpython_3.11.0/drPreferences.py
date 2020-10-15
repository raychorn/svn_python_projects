#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
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

#Preferences

#LongLineCol from Chris McDonough
#Changed name from longlinecol to doclonglinecol

#The idea for using a dictionary for reading/writing preferences
#ame from submitted code by limodou that was never incorporated
#into DrPython.  (It used an array of preferences,
#and called modified versions of drPrefsFile functions using
#setattr and getattr to read and write preferences).

import os.path, re
import wx

rekey = re.compile('(?<=\[).*(?=\])')

def _getkey(target):
    return int(rekey.search(target).group())

def _stringify(x):
    return (x, '')

def GetPreferencesDictionary():
    #Each item in the Dictionary:
    #(Key, Array)
    #Each item in the Array:
    #(Preference, Preferences File String, Function)
    #Function: 0: (GetPref, Not an Integer,), 1: (GetPref, Integer), 2: (ExtractPref, Not an Integer).
    return {'General': [('rememberwindowsizeandposition', 'remember.window.size.and.position', 1),
('rememberdialogsizesandpositions', 'remember.dialog.sizes.and.positions', 1),
('rememberpanelsizes', 'remember.panel.sizes', 1),
('autodetectencoding', 'auto.detect.encoding', 1),
('defaultencoding', 'default.encoding', 2),
('saveonrun', 'save.on.run', 1),
('checksyntaxonsave', 'check.syntax.on.save', 1),
('checksyntaxextensions', 'check.syntax.extensions', 0),
('promptonsaveall', 'prompt.on.save.all', 1),
('doubleclicktoclosetab', 'double.click.to.close.tab', 1),
('iconsize', 'icon.size', 1),
('recentfileslimit', 'max.recent.files', 1),
('vieweol', 'view.eol', 1),
('checkeol', 'check.line.ending.type', 1),
('checkindentation', 'check.indentation.type', 1),
('pythonargs', 'python.arguments', 2),
('defaultdirectory', 'default.directory', 2),
('enablefeedback', 'enable.feedback', 1),
('alwayspromptonexit', 'always.prompt.on.exit', 1),
('backupfileonsave', 'backup.file.on.save', 1)],
'File Types': [('extensions[0]', 'filetypes.extensions.python', 0),
('extensions[1]', 'filetypes.extensions.cpp', 0),
('extensions[2]', 'filetypes.extensions.html', 0),
('extensions[3]', 'filetypes.extensions.text', 0),
('docfolding[0]', 'filetypes.docfolding.python', 1),
('docfolding[1]', 'filetypes.docfolding.cpp', 1),
('docfolding[2]', 'filetypes.docfolding.html', 1),
('docfolding[3]', 'filetypes.docfolding.text', 1),
('doctabwidth[0]', 'filetypes.doctabwidth.python', 1),
('doctabwidth[1]', 'filetypes.doctabwidth.cpp', 1),
('doctabwidth[2]', 'filetypes.doctabwidth.html', 1),
('doctabwidth[3]', 'filetypes.doctabwidth.text', 1),
('docusetabs[0]', 'filetypes.docusetabs.python', 1),
('docusetabs[1]', 'filetypes.docusetabs.cpp', 1),
('docusetabs[2]', 'filetypes.docusetabs.html', 1),
('docusetabs[3]', 'filetypes.docusetabs.text', 1),
('docuseintellibackspace[0]', 'filetypes.docuseintellibackspace.python', 1),
('docuseintellibackspace[1]', 'filetypes.docuseintellibackspace.cpp', 1),
('docuseintellibackspace[2]', 'filetypes.docuseintellibackspace.html', 1),
('docuseintellibackspace[3]', 'filetypes.docuseintellibackspace.text', 1),
('docremovetrailingwhitespace[0]', 'filetypes.docremovetrailingwhitespace.python', 1),
('docremovetrailingwhitespace[1]', 'filetypes.docremovetrailingwhitespace.cpp', 1),
('docremovetrailingwhitespace[2]', 'filetypes.docremovetrailingwhitespace.html', 1),
('docremovetrailingwhitespace[3]', 'filetypes.docremovetrailingwhitespace.text', 1),
('doceolmode[0]', 'filetypes.doceolmode.python', 1),
('doceolmode[1]', 'filetypes.doceolmode.cpp', 1),
('doceolmode[2]', 'filetypes.doceolmode.html', 1),
('doceolmode[3]', 'filetypes.doceolmode.text', 1),
('doccommentstring[0]', 'filetypes.doccommentstring.python', 0),
('doccommentstring[1]', 'filetypes.doccommentstring.cpp', 0),
('doccommentstring[2]', 'filetypes.doccommentstring.html', 0),
('doccommentstring[3]', 'filetypes.doccommentstring.text', 0),
('docwordwrap[0]', 'filetypes.docwordwrap.python', 1),
('docwordwrap[1]', 'filetypes.docwordwrap.cpp', 1),
('docwordwrap[2]', 'filetypes.docwordwrap.html', 1),
('docwordwrap[3]', 'filetypes.docwordwrap.text', 1)],
'File Dialog': [('constantwildcard', 'constant.wildcard', 0),
('wildcard', 'wildcard', 0),
('windowsshortcutreplacetable', 'windows.shortcut.replace.table', 0),
('defaultextension', 'default.extension', 1),
('usewxfiledialog', 'use.wx.filedialog', 1)],
'Drag and Drop': [('draganddropmode', 'drag.and.drop.mode', 1),
('draganddroptextmode', 'drag.and.drop.text.mode', 1)],
'Document': [('docshowlinenumbers', 'doc.show.line.numbers', 1),
('docautoindent', 'doc.autoindent', 1),
('docautoreload', 'doc.autoreload', 1),
('docupdateindentation', 'doc.update.indentation', 1),
('docparenthesismatching', 'doc.parenthesis.matching', 1),
('docusefileindentation', 'doc.use.file.indentation', 1),
('docwhitespaceisvisible', 'doc.whitespace.is.visible.on.startup', 1),
('dochighlightcurrentline', 'doc.highlight.current.line', 1),
('doccaretwidth', 'doc.caret.width', 1),
('doccommentmode', 'doc.comment.mode', 1),
('docusestyles', 'doc.use.styles', 1),
('docuseindentationguides', 'doc.use.indentation.guides', 1),
('doclonglinecol', 'doc.long.line.col', 1),
('docscrollextrapage', 'doc.scroll.extra.page', 1),
('docdefaultsyntaxhighlighting', 'doc.default.syntax.highlighting', 1),
('doconlyusedefaultsyntaxhighlighting', 'doc.only.use.default.syntax.highlighting', 1),
('PythonStyleDictionary[0]', 'doc.style.normal', 0),
('PythonStyleDictionary[1]', 'doc.style.linenumber', 0),
('PythonStyleDictionary[2]', 'doc.style.brace.match', 0),
('PythonStyleDictionary[3]', 'doc.style.brace.nomatch', 0),
('PythonStyleDictionary[4]', 'doc.style.character', 0),
('PythonStyleDictionary[5]', 'doc.style.class', 0),
('PythonStyleDictionary[6]', 'doc.style.comment', 0),
('PythonStyleDictionary[7]', 'doc.style.comment.block', 0),
('PythonStyleDictionary[8]', 'doc.style.definition', 0),
('PythonStyleDictionary[9]', 'doc.style.keyword', 0),
('PythonStyleDictionary[10]', 'doc.style.number', 0),
('PythonStyleDictionary[11]', 'doc.style.operator', 0),
('PythonStyleDictionary[12]', 'doc.style.string', 0),
('PythonStyleDictionary[13]', 'doc.style.string.eol', 0),
('PythonStyleDictionary[14]', 'doc.style.triple.string', 0),
('PythonStyleDictionary[15]', 'doc.style.caret', 0),
('PythonStyleDictionary[16]', 'doc.style.selection', 0),
('PythonStyleDictionary[17]', 'doc.style.folding', 0),
('PythonStyleDictionary[18]', 'doc.style.longlinecol', 0),
('PythonStyleDictionary[19]', 'doc.style.current.line', 0),
('PythonStyleDictionary[20]', 'doc.style.indentation.guide', 0),
('CPPStyleDictionary[0]', 'doc.cstyle.normal', 0),
('CPPStyleDictionary[1]', 'doc.cstyle.linenumber', 0),
('CPPStyleDictionary[2]', 'doc.cstyle.brace.match', 0),
('CPPStyleDictionary[3]', 'doc.cstyle.brace.nomatch', 0),
('CPPStyleDictionary[4]', 'doc.cstyle.character', 0),
('CPPStyleDictionary[5]', 'doc.cstyle.preprocessor', 0),
('CPPStyleDictionary[6]', 'doc.cstyle.comment', 0),
('CPPStyleDictionary[7]', 'doc.cstyle.verbatim', 0),
('CPPStyleDictionary[8]', 'doc.cstyle.keyword', 0),
('CPPStyleDictionary[9]', 'doc.cstyle.c.identifier', 0),
('CPPStyleDictionary[10]', 'doc.cstyle.number', 0),
('CPPStyleDictionary[11]', 'doc.cstyle.operator', 0),
('CPPStyleDictionary[12]', 'doc.cstyle.string', 0),
('CPPStyleDictionary[13]', 'doc.cstyle.string.eol', 0),
('CPPStyleDictionary[14]', 'doc.cstyle.globalclass', 0),
('CPPStyleDictionary[15]', 'doc.cstyle.regex', 0),
('CPPStyleDictionary[16]', 'doc.cstyle.uuid', 0),
('CPPStyleDictionary[17]', 'doc.cstyle.caret', 0),
('CPPStyleDictionary[18]', 'doc.cstyle.selection', 0),
('CPPStyleDictionary[19]', 'doc.cstyle.folding', 0),
('CPPStyleDictionary[20]', 'doc.cstyle.longlinecol', 0),
('CPPStyleDictionary[21]', 'doc.cstyle.current.line', 0),
('HTMLStyleDictionary[0]', 'doc.htmlstyle.normal', 0),
('HTMLStyleDictionary[1]', 'doc.htmlstyle.linenumber', 0),
('HTMLStyleDictionary[2]', 'doc.htmlstyle.brace.match', 0),
('HTMLStyleDictionary[3]', 'doc.htmlstyle.brace.nomatch', 0),
('HTMLStyleDictionary[4]', 'doc.htmlstyle.tag', 0),
('HTMLStyleDictionary[5]', 'doc.htmlstyle.unknown.tag', 0),
('HTMLStyleDictionary[6]', 'doc.htmlstyle.attribute', 0),
('HTMLStyleDictionary[7]', 'doc.htmlstyle.unknown.attribute', 0),
('HTMLStyleDictionary[8]', 'doc.htmlstyle.number', 0),
('HTMLStyleDictionary[9]', 'doc.htmlstyle.string', 0),
('HTMLStyleDictionary[10]', 'doc.htmlstyle.character', 0),
('HTMLStyleDictionary[11]', 'doc.htmlstyle.comment', 0),
('HTMLStyleDictionary[12]', 'doc.htmlstyle.entity', 0),
('HTMLStyleDictionary[13]', 'doc.htmlstyle.tag.end', 0),
('HTMLStyleDictionary[14]', 'doc.htmlstyle.xml.start', 0),
('HTMLStyleDictionary[15]', 'doc.htmlstyle.xml.end', 0),
('HTMLStyleDictionary[16]', 'doc.htmlstyle.script', 0),
('HTMLStyleDictionary[17]', 'doc.htmlstyle.value', 0),
('HTMLStyleDictionary[18]', 'doc.htmlstyle.caret', 0),
('HTMLStyleDictionary[19]', 'doc.htmlstyle.selection', 0),
('HTMLStyleDictionary[20]', 'doc.htmlstyle.folding', 0),
('HTMLStyleDictionary[21]', 'doc.htmlstyle.longlinecol', 0),
('HTMLStyleDictionary[22]', 'doc.htmlstyle.current.line', 0)],
'Prompt': [('promptisvisible', 'prompt.is.visible.on.startup', 1),
('promptmarginwidth', 'prompt.margin.width', 1),
('promptsize', 'prompt.size', 1),
('prompttabwidth', 'prompt.tabwidth', 1),
('prompteolmode', 'prompt.eolmode', 1),
('promptusetabs', 'prompt.use.tabs', 1),
('promptwordwrap', 'prompt.wordwrap', 1),
('promptwhitespaceisvisible', 'prompt.whitespace.is.visible.on.startup', 1),
('promptcaretwidth', 'prompt.caret.width', 1),
('promptusestyles', 'prompt.use.styles', 1),
('promptscrollextrapage', 'prompt.scroll.extra.page', 1),
('promptstartupscript', 'prompt.startup.script', 0),
('txtPromptStyleDictionary[0]', 'prompt.style.normal', 0),
('txtPromptStyleDictionary[1]', 'prompt.style.linenumber', 0),
('txtPromptStyleDictionary[2]', 'prompt.style.brace.match', 0),
('txtPromptStyleDictionary[3]', 'prompt.style.brace.nomatch', 0),
('txtPromptStyleDictionary[4]', 'prompt.style.character', 0),
('txtPromptStyleDictionary[5]', 'prompt.style.class', 0),
('txtPromptStyleDictionary[6]', 'prompt.style.comment', 0),
('txtPromptStyleDictionary[7]', 'prompt.style.comment.block', 0),
('txtPromptStyleDictionary[8]', 'prompt.style.definition', 0),
('txtPromptStyleDictionary[9]', 'prompt.style.keyword', 0),
('txtPromptStyleDictionary[10]', 'prompt.style.number', 0),
('txtPromptStyleDictionary[11]', 'prompt.style.operator', 0),
('txtPromptStyleDictionary[12]', 'prompt.style.string', 0),
('txtPromptStyleDictionary[13]', 'prompt.style.string.eol', 0),
('txtPromptStyleDictionary[14]', 'prompt.style.triple.string', 0),
('txtPromptStyleDictionary[15]', 'prompt.style.caret', 0),
('txtPromptStyleDictionary[16]', 'prompt.style.selection', 0)],
'Side Panels': [('sidepanelleftsize', 'side.panel.left.size', 1),
('sidepanelrightsize', 'side.panel.right.size', 1),
('sidepaneltopsize', 'side.panel.top.size', 1)],
'Find/Replace': [('findreplaceregularexpression', 'find.replace.regular.expression', 1),
('findreplacematchcase', 'find.replace.match.case', 1),
('findreplacefindbackwards', 'find.replace.find.backwards', 1),
('findreplacewholeword', 'find.replace.whole.word', 1),
('findreplaceinselection', 'find.replace.in.selection', 1),
('findreplacefromcursor', 'find.replace.from.cursor', 1),
('findreplacepromptonreplace', 'find.replace.prompt.on.replace', 1),
('findreplaceautowrap', 'find.replace.auto.wrap', 1),
('findreplaceundercursor', 'find.replace.prompt.under.cursor', 1)],
'Source Browser': [('sourcebrowserpanel', 'sourcebrowser.panel', 1),
('sourcebrowsersize', 'sourcebrowser.size', 1),
('sourcebrowserisvisible', 'sourcebrowser.is.visible', 1),
('sourcebrowsercloseonactivate', 'sourcebrowser.close.on.activate', 1),
('sourcebrowserissorted', 'sourcebrowser.is.sorted', 1),
('sourcebrowserautorefreshonsave', 'sourcebrowser.auto.refresh.on.save', 1),
('sourcebrowserautorefresh', 'sourcebrowser.auto.refresh', 1),
('sourcebrowseruseimages', 'sourcebrowser.use.images', 1),
('sourcebrowserstyle', 'sourcebrowser.style', 0)],
'Bookmarks': [('bookmarksstyle', 'bookmarks.style', 0)],
'Plugins': [('pluginsdirectory', 'plugins.directory', 2)],
'DrScript': [('drscriptsdirectory', 'drscripts.directory', 2),
('drscriptstyle', 'drscript.style', 0),
('drscriptloadexamples', 'drscript.load.examples', 1)],
'Printing': [('printdoclinenumbers', 'print.doc.linenumbers', 1),
('printpromptlinenumbers', 'print.prompt.linenumbers', 1),
('printtabwidth', 'print.tab.width', 1)],
'Documentation': [('documentationbrowser', 'documentation.browser', 0),
('documentationpythonlocation', 'documentation.python.location', 0),
('documentationwxwidgetslocation', 'documentation.wx.widgets.location', 0),
('documentationrehowtolocation', 'documentation.rehowto.location', 0)]}


class drPreferences:

    def __init__(self, platform_is_windows, programdirectory = ""):
        self.platform_is_windows = platform_is_windows
        self.programdirectory = programdirectory
        #General Settings
        self.rememberwindowsizeandposition = 1
        self.rememberdialogsizesandpositions = 1
        self.rememberpanelsizes = 1
        self.autodetectencoding = 1
        self.defaultencoding = 'latin-1'
        self.saveonrun = 1
        self.checksyntaxonsave = 1
        self.checksyntaxextensions = ''
        self.promptonsaveall = 1
        self.doubleclicktoclosetab = 0
        self.iconsize = 16
        self.recentfileslimit = 10
        self.checkindentation = 0
        self.vieweol = 1
        self.checkeol = 1
        self.pythonargs = ""
        self.defaultdirectory = programdirectory
        self.enablefeedback = 1
        self.alwayspromptonexit = 0
        self.backupfileonsave = 1
        self.save = 0

        #File Dialog
        self.usewxfiledialog = 0
        self.defaultextension = 1
        self.constantwildcard = '*.lnk'
        #self.windowsshortcutreplacetable = 'C:,/mnt/win_c#'
        #@ = replace with lowercase match & = replace with exact match
        self.windowsshortcutreplacetable = '[A-Z],/mnt/win_@#'
        if self.platform_is_windows:
            self.wildcard = "Python Source (*.pyw *.py)|*.pyw;*.py|C/C++ Source (*.c *.cc *.cpp *.cxx *.h *.hh *.hpp *.hxx)|*.c;*.cc;*.cpp;*.cxx;*.h;*.hh;*.hpp;*.hxx|HTML Files (*.htm *.html *.shtm *.shtml *.xml)|*.htm;*.html;*.shtm;*.shtml;*.xml|Backup Files (*.bak)|*.bak|Plain Text (*.txt *.dat *.log)|*.txt;*.dat;*.log|All Files (*)|*"
        else:
            self.wildcard = "Python Source (*.py *.pyw)|*.py;*.pyw|C/C++ Source (*.c *.cc *.cpp *.cxx *.h *.hh *.hpp *.hxx)|*.c;*.cc;*.cpp;*.cxx;*.h;*.hh;*.hpp;*.hxx|HTML Files (*.htm *.html *.shtm *.shtml *.xml)|*.htm;*.html;*.shtm;*.shtml;*.xml|Backup Files (*.bak)|*.bak|Plain Text (*.txt *.dat *.log)|*.txt;*.dat;*.log|All Files (*)|*"

        #Drag and Drop
        self.draganddropmode = 2
        self.draganddroptextmode = 0

        #File Types
        self.extensions = {0: 'py,pyw', 1: 'c,cc,cpp,cxx,h,hh,hpp,hxx', 2: 'htm,shtm,html,shtml,xml', 3: 'txt,dat,log'}
        self.docfolding = {0: 1, 1: 0, 2: 0, 3: 0}
        self.doctabwidth = {0: 4, 1: 4, 2: 4, 3: 4}
        self.docusetabs = {0: 0, 1: 0, 2: 0, 3: 0}
        self.docuseintellibackspace = {0: 1, 1: 1, 2: 1, 3: 1}
        self.docremovetrailingwhitespace = {0: 0, 1: 0, 2: 0, 3: 0}
        self.doceolmode = {0: 0, 1: 0, 2: 0, 3: 0}
        self.doccommentstring = {0: '#', 1: '//', 2: '', 3: '#'}
        self.docwordwrap = {0: 0, 1: 0, 2: 0, 3: 0}

        #Document Settings
        self.docshowlinenumbers = 1
        self.docautoindent = 2
        self.docautoreload = 1
        self.docupdateindentation = 0
        self.docparenthesismatching = 1
        self.docusefileindentation = 1
        self.docwhitespaceisvisible = 0
        self.dochighlightcurrentline = 1
        self.doccaretwidth = 1
        self.doccommentmode = 0
        self.docusestyles = 1
        self.docuseindentationguides = 1
        self.doclonglinecol = 0
        self.docscrollextrapage = 0
        self.docdefaultsyntaxhighlighting = 0
        self.doconlyusedefaultsyntaxhighlighting = 0

        self.PythonStyleDictionary = dict(map(_stringify, range(21)))
        self.CPPStyleDictionary = dict(map(_stringify, range(22)))
        self.HTMLStyleDictionary = dict(map(_stringify, range(23)))

        if self.platform_is_windows:
            defaultfont0="Courier" #monospaced
            defaultfont1="MS Sans Serif" #proportional
        else:
            defaultfont0="Courier 10 Pitch" #monospaced
            defaultfont1="Sans" #proportional
        
        #check if those fonts exists, else use system default
        FontList = wx.FontEnumerator().GetFacenames()
        defaultfont = wx.GetApp().GetTopWindow().GetFont().GetFaceName()
        if defaultfont0 not in FontList:
            defaultfont0=defaultfont
        if defaultfont1 not in FontList:
            defaultfont1=defaultfont
        
        self.PythonStyleDictionary[0] = "fore:#000000,back:#FFFFFF,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[1] = "fore:#000000,back:#82AEE3,size:10,face:%s" %defaultfont1
        self.PythonStyleDictionary[2] = "fore:#FF6400,back:#98D3FF,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[3] = "fore:#FF0000,back:#FFFF00,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[4] = "fore:#007f08,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[5] = "fore:#b200ac,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[6] = "fore:#7F7F7F,back:#FFFFFF,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[7] = "fore:#0B5400,back:#BAE8D5,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[8] = "fore:#e80300,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[9] = "fore:#FF0000,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[10] = "fore:#0027c4,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[11] = "fore:#FF0071,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[12] = "fore:#007f08,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[13] = "fore:#007f08,back:#ffffff,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[14] = "fore:#7B8184,back:#FFFFFF,size:10,face:%s" %defaultfont0
        self.PythonStyleDictionary[15] = "#000000"
        self.PythonStyleDictionary[16] = "fore:#000000,back:#FF7900"
        self.PythonStyleDictionary[17] = "fore:#000000,back:#82AEE3"
        self.PythonStyleDictionary[18] = "#82AEE3"
        self.PythonStyleDictionary[19] = "#98D3FF"
        self.PythonStyleDictionary[20] = "#AAAAAA"

        self.CPPStyleDictionary[0] = "fore:#000000,back:#FFFFFF,size:12,face:%s" %defaultfont0
        self.CPPStyleDictionary[1] = "fore:#000000,back:#82AEE3,size:12,face:%s" %defaultfont0
        self.CPPStyleDictionary[2] = "fore:#FF6400,back:#98D3FF,bold"
        self.CPPStyleDictionary[3] = "fore:#FF0000,back:#FFFF00,bold"
        self.CPPStyleDictionary[4] = "fore:#007f08,back:#ffffff"
        self.CPPStyleDictionary[5] = "fore:#228D63,back:#ffffff,bold"
        self.CPPStyleDictionary[6] = "fore:#2D3D9E,back:#DFDFEB,bold"
        self.CPPStyleDictionary[7] = "fore:#e80300,back:#ffffff"
        self.CPPStyleDictionary[8] = "fore:#000000,back:#ffffff,bold"
        self.CPPStyleDictionary[9] = "fore:#000000,back:#ffffff"
        self.CPPStyleDictionary[10] = "fore:#2050C6,back:#ffffff,"
        self.CPPStyleDictionary[11] = "fore:#003D22,back:#ffffff"
        self.CPPStyleDictionary[12] = "fore:#008500,back:#FFFFFF"
        self.CPPStyleDictionary[13] = "fore:#008500,back:#FFFFFF"
        self.CPPStyleDictionary[14] = "fore:#000000,back:#FFFFFF"
        self.CPPStyleDictionary[15] = "fore:#338144,back:#5FFFFF,bold"
        self.CPPStyleDictionary[16] = "fore:#330044,back:#5FFFFF"
        self.CPPStyleDictionary[17] = "#000000"
        self.CPPStyleDictionary[18] = "fore:#000000,back:#FF7900"
        self.CPPStyleDictionary[19] = "fore:#000000,back:#82AEE3"
        self.CPPStyleDictionary[20] = "#82AEE3"
        self.CPPStyleDictionary[21] = "#98D3FF"

        self.HTMLStyleDictionary[0] = "fore:#000000,back:#FFFFFF,size:12,face:%s" %defaultfont0
        self.HTMLStyleDictionary[1] = "fore:#000000,back:#82AEE3,size:12,face:%s" %defaultfont0
        self.HTMLStyleDictionary[2] = "fore:#FF6400,back:#98D3FF,bold"
        self.HTMLStyleDictionary[3] = "fore:#FF0000,back:#FFFF00,bold"
        self.HTMLStyleDictionary[4] = "fore:#000000,back:#ffffff,bold"
        self.HTMLStyleDictionary[5] = "fore:#0000FF,back:#FFFFFF,bold"
        self.HTMLStyleDictionary[6] = "fore:#2D3D9E,back:#DFDFEB,bold"
        self.HTMLStyleDictionary[7] = "fore:#FF0000,back:#ffff00,bold"
        self.HTMLStyleDictionary[8] = "fore:#0000FF,back:#ffffff"
        self.HTMLStyleDictionary[9] = "fore:#003100,back:#ffffff"
        self.HTMLStyleDictionary[10] = "fore:#204D71,back:#ffffff,bold"
        self.HTMLStyleDictionary[11] = "fore:#2D3D9E,back:#DFDFEB,bold"
        self.HTMLStyleDictionary[12] = "fore:#7B8184,back:#FFFFFF,bold"
        self.HTMLStyleDictionary[13] = "fore:#000000,back:#FFF7C2,bold"
        self.HTMLStyleDictionary[14] = "fore:#000081,back:#FFE48D,bold"
        self.HTMLStyleDictionary[15] = "fore:#006E00,back:#FFE48D,bold"
        self.HTMLStyleDictionary[16] = "fore:#00812A,back:#CEF0FF,bold"
        self.HTMLStyleDictionary[17] = "fore:#000000,back:#C2FFE8,bold"
        self.HTMLStyleDictionary[18] = "#000000"
        self.HTMLStyleDictionary[19] = "fore:#000000,back:#FF7900"
        self.HTMLStyleDictionary[20] = "fore:#000000,back:#82AEE3"
        self.HTMLStyleDictionary[21] = "#82AEE3"
        self.HTMLStyleDictionary[22] = "#98D3FF"

        self.txtDocumentStyleDictionary = self.PythonStyleDictionary

        #Prompt Settings
        self.promptisvisible = 0
        self.promptmarginwidth = 0
        self.prompttabwidth = 4
        self.promptsize = 50
        self.prompteolmode = 0
        self.promptusetabs = 1
        self.promptwordwrap = 1
        self.promptwhitespaceisvisible = 0
        self.promptcaretwidth = 1
        self.promptusestyles = 1
        self.promptscrollextrapage = 0
        self.promptstartupscript = 'import sys, os, wx'
        self.txtPromptStyleDictionary = dict(map(_stringify, range(17)))

        # lm - changing default prompt style for increased readability

        #normal
        self.txtPromptStyleDictionary[0] = "fore:#000000,back:#FFFFFF,size:8,face:%s" %defaultfont1
        # line number (margin)
        self.txtPromptStyleDictionary[1] = "fore:#000000,back:#82AEE3,size:8"
        # brace selected (match)
        self.txtPromptStyleDictionary[2] = "fore:#000000,back:#FFFFFF"
        # brace selected (no match)
        self.txtPromptStyleDictionary[3] = "fore:#000000,back:#FFFFFF"
        # character (single quoted string)
        self.txtPromptStyleDictionary[4] = "fore:#000000,back:#FFFFFF"
        #class name
        self.txtPromptStyleDictionary[5] = "fore:#000000,back:#FFFFFF"
        #comment
        self.txtPromptStyleDictionary[6] = "fore:#000000,back:#FFFFFF"
        #comment block
        self.txtPromptStyleDictionary[7] = "fore:#000000,back:#FFFFFF"
        #function name
        self.txtPromptStyleDictionary[8] = "fore:#000000,back:#FFFFFF"
        #keyword
        self.txtPromptStyleDictionary[9] = "fore:#000000,back:#FFFFFF"
        #number
        self.txtPromptStyleDictionary[10] = "fore:#000000,back:#FFFFFF"
        #operator
        self.txtPromptStyleDictionary[11] = "fore:#000000,back:#FFFFFF"
        #string
        self.txtPromptStyleDictionary[12] = "fore:#000000,back:#FFFFFF"
        #string eol
        self.txtPromptStyleDictionary[13] = "fore:#000000,back:#FFFFFF"
        #triple quoted string
        self.txtPromptStyleDictionary[14] = "fore:#000000,back:#FFFFFF"
        #caret foreground
        self.txtPromptStyleDictionary[15] = "#000000"
        #selection
        self.txtPromptStyleDictionary[16] = "fore:#000000,back:#FF7900"

        # /lm
        #Side Panel Settings
        self.sidepanelleftsize = 30
        self.sidepanelrightsize = 30
        self.sidepaneltopsize = 30

        #Find/Replace Settings
        self.findreplaceregularexpression = 0
        self.findreplacematchcase = 0
        self.findreplacefindbackwards = 0
        self.findreplacewholeword = 0
        self.findreplaceinselection = 0
        self.findreplacefromcursor = 1
        self.findreplacepromptonreplace = 1
        self.findreplaceautowrap = 0
        self.findreplaceundercursor = 1

        #Source Browser Settings
        self.sourcebrowserpanel = 0
        self.sourcebrowsersize = 25
        self.sourcebrowserisvisible = 1
        self.sourcebrowsercloseonactivate = 0
        self.sourcebrowserissorted = 0
        self.sourcebrowserautorefreshonsave = 1
        self.sourcebrowserautorefresh = 0
        self.sourcebrowseruseimages = 0
        self.sourcebrowserstyle = "fore:#FF0000,back:#FFFFFF,size:10,face:%s" %defaultfont1

        #Bookmarks Settings
        self.bookmarksstyle = "fore:#000000,back:#FFFFFF,size:12,face:%s,bold" %defaultfont1
        preferencesdirectory = wx.GetApp().GetTopWindow().preferencesdirectory
        
        #Plugins Settings
        self.pluginsdirectory = os.path.join(preferencesdirectory, 'drplugins').replace ('\\', "/")

        #DrScript Settings
        self.drscriptsdirectory = os.path.join(preferencesdirectory, 'drscripts').replace ('\\', "/")
        
        self.drscriptstyle = "fore:#000000,back:#FFFFFF,size:12,face:%s,bold" %defaultfont1
        self.drscriptloadexamples = 1

        #Printing Settings
        self.printdoclinenumbers = 1
        self.printpromptlinenumbers = 0
        self.printtabwidth = 4

        #Documentation Settings
        self.documentationbrowser = "mozilla"
        if self.platform_is_windows:
            self.documentationbrowser = "<os.startfile>"
        self.documentationpythonlocation = "http://www.python.org/doc/current/"
        self.documentationwxwidgetslocation = "http://www.wxwidgets.org/docs.htm"
        self.documentationrehowtolocation = "http://www.amk.ca/python/howto/regex/"

    def __getitem__(self, key):
        k = key.find('[')
        if k > -1:
            return self.__dict__[key[:k]][_getkey(key)]
        else:
            return self.__dict__[key]

    def __setitem__(self, key, value):
        k = key.find('[')
        if k > -1:
            self.__dict__[key[:k]][_getkey(key)] = value
        else:
            self.__dict__[key] = value

    def reset(self):
        self.__init__(self.platform_is_windows, self.programdirectory)

    def resetjust(self, target):
        defaults = drPreferences(self.platform_is_windows, self.programdirectory)

        prefsdictionary = GetPreferencesDictionary()
        if prefsdictionary.has_key(target):
            for Preference in prefsdictionary[target]:
                self[Preference[0]] = defaults[Preference[0]]

    def Copy(self, target):
        self.platform_is_windows = target.platform_is_windows
        self.programdirectory = target.programdirectory

        prefsdictionary = GetPreferencesDictionary()
        for Entry in prefsdictionary:
            for Preference in prefsdictionary[Entry]:
                self[Preference[0]] = target[Preference[0]]