#   Programmer: Daniel Pozmanter
#   E-mail: drpython@bluebottle.com
#   Note: You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   DrPython is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# drpython

#   Requirements(Dependencies):  Install Python, and wxPython.
#
#   Tested On Windows, Linux, Mac OS X
#
#   Icons taken from "Klassic New Crisp Icons" by Asif Ali Rizwaan (therizwaan) from the KDE-LOOK site (some edited a bit).
#   A humble and excellent artist.
#   Oh, the python icon is taken from wxPython.
#   The basic design of the program is meant to roughly (ROUGHLY) mimick DrScheme.
#   The purpose is the same, to provide a simple IDE(integrated development environment) ideal for teaching.
#   The DrPython icon itself was based on the DrScheme icon, with a slightly edited wxpython icon inserted(note yellow tongue, googly eyes).
#
#   This program could not have been written without the wonderful work of the people behind
#   python and wxPython, in particular the Styled Text Control.  Thank you.  Hopefully this tool will be of use.
#
#   Replaced all rstrip('\n') with rstrip(), thanks Christof Ecker: (drpython.py and DrPrefs.py).
#

#franz: stat is not used
from __future__ import with_statement
import sys, os, shutil, re, string, traceback
#import wxversion
#wxversion.select('2.8')
import wx, wx.stc
import  wx.lib.dialogs
import drScrolledMessageDialog
import drHtmlBrowser
from drNotebook import *
from drText import DrText
from drPrompt import DrPrompt
from drPrinter import DrPrinter
from drFindReplaceDialog import drFindReplaceDialog
from drBookmarksMenu import drBookmarksMenu
from drScriptMenu import drScriptMenu
from drPluginMenu import drPluginConfigureMenu, drPluginIndexMenu, drPluginAboutMenu, drPluginHelpMenu, drPluginPreferencesMenu
import drGetBlockInfo
import drSourceBrowserGoTo
import drFileDialog
import drPrefsFile
from drPreferences import drPreferences
import drShortcutsFile
import drShortcuts
import drToolBarFile
import drTabNanny
from drSourceBrowser import drSourceBrowserPanel
import drEncoding
from drStyleDialog import drSeparatorDialog
from drSingleChoiceDialog import drSingleChoiceDialog
from drMenu import drMenu
from drFileHistory import *
import pydoc
import tempfile
import time
import warnings

DRPY_VER = "3.11.3"

logdir = os.path.expanduser("~").replace("\\", "/")
if sys.platform == "win32":
    if os.environ.has_key("APPDATA"):
        logdir = os.environ["APPDATA"].replace("\\", "/")
    if not os.path.exists(logdir):
        logdir = '/'
if not logdir.endswith('/'):
    logdir += '/'

err_file = logdir + 'drpython.err'
out_file = logdir + 'drpython.out'
firsterr_file = logdir + 'drpythonfirst.err'


class drObject(wx.Object):
    """Acts basically as a thin layer over `wx.Object` with just a method to
    check for the existance of a given attribute.

    :deprecated: Because it has just one method which is itself deprecated.
    """
    def __init__(self):
        warnings.warn('`drObject` is deprecated.', DeprecationWarning, 2)

    def VariableExists(self, varname):
        """Checks if this object  has an attribute named `varname`.

        :deprecated: The test can be accomplished with the builtin function
            `hasattr()`.  Smuggling this class into the inheritance chain is
            way too complicated for such a simple task.
        """
        warnings.warn('`VariableExists()` is deprecated.'
                      ' Use `hasattr()` instead.', DeprecationWarning, 2)
        return hasattr(self, varname)


class DrFrame(wx.Frame):
    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (680, 480), name="DrPython")
        #self.ignoreevents = False

        self.disableeventhandling = False

        try:
            self.preferencesdirectory = os.path.expanduser(
                get_option_value('--preferencesbasepath')
            )
            self.invokeuserpreferencespath = True
        except KeyError:
            self.preferencesdirectory = ''
            self.invokeuserpreferencespath = False
        else:
            if not os.path.exists(self.preferencesdirectory):
                wx.MessageBox('Preferences Directory: %r does not exist!'
                              % self.preferencesdirectory,
                              'Creating Directory!',
                              wx.ICON_INFORMATION)
                os.makedirs(self.preferencesdirectory)

        self.InitializeConstants()

        self.viewinpaneltarget = 0

        self.lastprogargs = ""

        #: Simple object for attaching attributes in scripts to.
        self.DrScript = type('Object', (object,), dict())()

        self.Printer = DrPrinter(self)

        #Regex Line Endings:
        self.relewin = re.compile('\r\n', re.M)
        self.releunix = re.compile('[^\r]\n', re.M)
        self.relemac = re.compile('\re[^\n]', re.M)

        self.FormatMacReTarget = re.compile('((?<!\r)\n)|(\r\n)', re.M)
        self.FormatUnixReTarget = re.compile('(\r\n)|(\r(?!\n))', re.M)
        self.FormatWinReTarget = re.compile('((?<!\r)\n)|(\r(?!\n))', re.M)

        self.rechecksyntax = re.compile('line \d+', re.M)

        #Find/Replace

        self.FindHistory = []
        self.ReplaceHistory = []

        self.FindInFilesHistory = []
        self.ReplaceInFilesHistory = []

        self.FindOptions = []
        self.ReplaceOptions = []

        #Used for current directory with open/save
        self.ddirectory = ""

        self.stcshortcutlist = drShortcutsFile.GetSTCShortcutList()

        self.programdirectory = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

        #Preferences


        self.prefs = drPreferences(self, self.PLATFORM_IS_WIN, self.programdirectory)
        self.prefsfile = self.preferencesdirectory + "/preferences.dat"

        self.LoadPreferences()

        #Set and check all relevant directories
        self.SetDrPythonDirectories()

        #File Types
        self.setupfiletypeextensions()

        WindowWidth = 640
        WindowHeight = 480
        wasMaximized = 0
        if self.prefs.rememberwindowsizeandposition:
            if os.path.exists(self.datdirectory + "/drpython.sizeandposition.dat"):
                try:
                    f = open(self.datdirectory + "/drpython.sizeandposition.dat", 'r')
                    text = f.read()
                    if text:
                        values = map(int, text.split('\n'))
                        if len (values) == 5:
                            WindowWidth, WindowHeight, WindowX, WindowY, wasMaximized = values
                            self.SetSize((WindowWidth, WindowHeight))
                            self.Move(wx.Point(WindowX, WindowY))
                            if wasMaximized == 1:
                                wx.CallAfter(self.Maximize)
                    f.close()
                except:
                    self.ShowMessage('Error Loading Window Size.  The file "%s" may be corrupt.' % self.preferencesdirectory +
                                     "/drpython.sizeandposition.dat", 'Error')

        #Default position is for "General" preferences.
        self.prefdialogposition = 0

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.BitmapFromImage(wx.Image(self.bitmapdirectory + "/drpython.png", wx.BITMAP_TYPE_PNG)))
        self.SetIcon(icon)

        self.txtDocumentArray = []
        self.txtPromptArray = []

        self.mainpanel = drMainPanel(self, -1)

        self.mainpanel.RememberPanelSizes()

        self.SourceBrowser = None
        self.Debugger = None

        #Colour:
        self.SetBackgroundColour(self.mainpanel.GetBackgroundColour())

        self.documentnotebook = drDocNotebook(self.mainpanel.document, -1)
        self.promptnotebook = drPromptNotebook(self.mainpanel.prompt, -1)

        self.documentnotebook.AddPage(drPanel(self.documentnotebook, self.ID_APP), "Untitled 1")
        self.promptnotebook.AddPage(drPanel(self.promptnotebook, self.ID_APP), "Prompt")

        self.currentpage = self.documentnotebook.GetPage(0)
        self.currentprompt = self.promptnotebook.GetPage(0)

        self.txtDocument = DrText(self.currentpage, self.ID_DOCUMENT_BASE, self)
        self.currentpage.SetSTC(self.txtDocument)
        self.txtPrompt = DrPrompt(self.currentprompt, self.ID_PROMPT_BASE, self)
        self.currentprompt.SetSTC(self.txtPrompt)

        self.txtDocument.SetTargetPosition(0)
        self.txtDocument.untitlednumber = 1

        self.documentnotebook.SetPageImage(0, 0)
        self.promptnotebook.SetPageImage(0, 2)

        #Pop Up Menu

        self.popupmenulist = []

        self.LoadPopUpFile()

        #Position in the Arrays Below:
        self.docPosition = 0
        self.promptPosition = 0

        self.txtDocumentArray.append(self.txtDocument)
        self.txtPromptArray.append(self.txtPrompt)
        self.lastprogargsArray = [self.lastprogargs]

        #Shortcuts

        self.STCShortcuts = drShortcutsFile.GetDefaultSTCShortcuts()
        self.STCShortcutNames = drShortcutsFile.GetSTCShortcutList()
        self.STCShortcutsArgumentArray = drShortcuts.GetSTCCommandList()

        self.Shortcuts, self.ShortcutsIgnoreString = drShortcutsFile.GetDefaultShortcuts()
        self.ShortcutNames = drShortcutsFile.GetShortcutList()

        self.ShortcutsActionArray = []
        self.ShortcutsArgumentsArray = []

        #DrScript Shortcuts

        self.DrScriptShortcuts = []
        self.DrScriptShortcutNames = []

        #Plugins
        self.LoadedPlugins = []
        self.PluginModules = []

        #Plugin Events

        self.EVT_DRPY_DOCUMENT_CHANGED = 0
        self.EVT_DRPY_FILE_OPENING = 1
        self.EVT_DRPY_FILE_OPENED = 2
        self.EVT_DRPY_FILE_SAVING = 3
        self.EVT_DRPY_FILE_SAVED = 4
        self.EVT_DRPY_FILE_CLOSING = 5
        self.EVT_DRPY_FILE_CLOSED = 6
        self.EVT_DRPY_NEW = 7
        self.EVT_DRPY_NEW_PROMPT = 8
        self.EVT_DRPY_PROMPT_GOTO = 9
        self.EVT_DRPY_SETTEXT_START = 10
        self.EVT_DRPY_SETTEXT_END = 11
        self.EVT_DRPY_DRTEXT_ONKEY_DOWN_START = 12
        self.EVT_DRPY_DRTEXT_ONCHAR_START = 13




        #Plugin Arrays:

        self.drpyevents = []

        self.PluginShortcutsLoadedArray = []

        self.PluginShortcutFunctionNames = []
        self.PluginShortcutFunctions = []

        self.PluginShortcutNames = []
        self.PluginShortcuts = []
        self.PluginAction = []

        self.PluginPopUpMenuNames = []
        self.PluginPopUpMenuLabels = []
        self.PluginPopUpMenuFunctions = []

        self.PluginToolBarLabels = []
        self.PluginToolBarIconFiles16 = []
        self.PluginToolBarIconFiles24 = []
        self.PluginToolBarFunctions = []

        #Load Shortcuts

        self.STCUseDefault = 1
        self.ShortcutsUseDefault = 1

        self.LoadShortcuts()

        #Shortcuts
        drShortcuts.SetSTCShortcuts(self.txtPrompt, self.STCShortcuts, self.STCUseDefault)
        self.STCShortcuts = drShortcuts.SetSTCShortcuts(self.txtDocument, self.STCShortcuts, self.STCUseDefault)
        self.Shortcuts, self.ShortcutsActionArray, self.ShortcutsArgumentsArray = drShortcuts.SetShortcuts(self, self.Shortcuts, self.ShortcutNames, self.ShortcutsUseDefault)

        #Sizer
        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        #ugly workaround: in gtk, if a messagebox is shown, an activate app event is delivered, but only on gtk, not on windows
        #if someone want to do some actions based on this event, it is annoying
        self.ignore_activate_app_event = False

        # TODO: Replace `self.GetNewId()` by `wx.GetNewId()` when all literal
        #   IDs are removed from the source code.
        self.recentfiles = DrFileHistory(self.prefs.recentfileslimit,
                                         self.GetNewId())
        self.LoadRecentFiles()

        self.retrailingwhitespace = re.compile('(?<=\S)[ \t]+$', re.MULTILINE)

        #Compile Regular Expressions for Open Import:
        self.reimport = re.compile('^\s*?import\s+?.*?$', re.M)
        self.refromimport = re.compile('^\s*?from\s+?.*?import.*?$', re.M)

        #edited by drpython
        if self.prefs.defaultdirectory:
            self.ddirectory = self.prefs.defaultdirectory
        else:
            #add limodou 2004/04/17
            #if defaultdirectory is empty, then use the last recently file's dir
            if self.recentfiles:
                self.ddirectory = os.path.dirname(self.recentfiles[0])
            #end limodou
            else:
                self.ddirectory = self.programdirectory

        try:
            os.chdir(self.ddirectory)
        except:
            self.ShowMessage('Error Changing to Default Directory: "%s"' % (self.ddirectory), 'Preferences Error')
            self.ddirectory = self.programdirectory
            os.chdir(self.ddirectory)

        #AB: Removed: it will be called in CreateMenus
        #self.drscriptmenu = drScriptMenu(self)

        self.txtDocument.OnModified(None)

        #DrScript Shortcuts
        #AB: Removed: it will be called in CreateMenus
        #self.DrScriptShortcutsAction = self.drscriptmenu.OnScript

        self.hasToolBar = False

                #Status Bar

        self.CreateStatusBar()

        self.GetStatusBar().SetFieldsCount(4)

        #First field is hidden, to absorb wxMenuHighlight events from the menu and toolbar.
        self.GetStatusBar().SetStatusWidths([-0, -10, -10, -10])

        self.CreateMenus()
        #Sizer

        self.bSizer.Add(self.mainpanel, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(self.bSizer)



        self.UpdateMenuAndToolbar()

        self.Bind(wx.EVT_MENU,  self.OnNew, id=self.ID_NEW)
        self.Bind(wx.EVT_MENU,  self.OnOpen, id=self.ID_OPEN)
        self.Bind(wx.EVT_MENU,  self.OnOpenImportedModule, id=self.ID_OPEN_IMPORTED_MODULE)

        self.Bind(wx.EVT_MENU,  self.OnClose, id=self.ID_CLOSE)
        self.Bind(wx.EVT_MENU,  self.OnCloseAllDocuments, id=self.ID_CLOSE_ALL)
        self.Bind(wx.EVT_MENU,  self.OnCloseAllOtherDocuments, id=self.ID_CLOSE_ALL_OTHER_DOCUMENTS)

        self.Bind(wx.EVT_MENU,  self.OnReload, id=self.ID_RELOAD)
        self.Bind(wx.EVT_MENU,  self.OnRestoreFromBackup, id=self.ID_RESTORE_FROM_BACKUP)
        self.Bind(wx.EVT_MENU,  self.OnClearRecent, id=self.ID_CLEAR_RECENT)
        self.Bind(wx.EVT_MENU,  self.OnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_MENU,  self.OnSaveAs, id=self.ID_SAVE_AS)
        self.Bind(wx.EVT_MENU,  self.OnSaveCopy, id=self.ID_SAVE_COPY)
        self.Bind(wx.EVT_MENU,  self.OnSaveAll, id=self.ID_SAVE_ALL)
        self.Bind(wx.EVT_MENU,  self.OnSavePrompt, id=self.ID_SAVE_PROMPT)
        self.Bind(wx.EVT_MENU,  self.OnPrintSetup, id=self.ID_PRINT_SETUP)
        self.Bind(wx.EVT_MENU,  self.OnPrint, id=self.ID_PRINT)
        self.Bind(wx.EVT_MENU,  self.OnPrintPrompt, id=self.ID_PRINTPROMPT)
        self.Bind(wx.EVT_MENU,  self.OnExit, id=self.ID_EXIT)

        self.Bind(wx.EVT_MENU,  self.OnMenuFind, id=self.ID_FIND)
        self.Bind(wx.EVT_MENU,  self.OnMenuFindNext, id=self.ID_FIND_NEXT)
        self.Bind(wx.EVT_MENU,  self.OnMenuFindPrevious, id=self.ID_FIND_PREVIOUS)
        self.Bind(wx.EVT_MENU,  self.OnMenuReplace, id=self.ID_REPLACE)

        self.Bind(wx.EVT_MENU,  self.OnInsertSeparator, id=self.ID_INSERT_SEPARATOR)
        self.Bind(wx.EVT_MENU,  self.OnInsertRegEx, id=self.ID_INSERT_REGEX)

        self.Bind(wx.EVT_MENU,  self.OnSelectAll, id=self.ID_SELECT_ALL)

        self.Bind(wx.EVT_MENU,  self.OnCommentRegion, id=self.ID_COMMENT_REGION)
        self.Bind(wx.EVT_MENU,  self.OnUnCommentRegion, id=self.ID_UNCOMMENT_REGION)

        self.Bind(wx.EVT_MENU,  self.OnIndentRegion, id=self.ID_INDENT_REGION)
        self.Bind(wx.EVT_MENU,  self.OnDedentRegion, id=self.ID_DEDENT_REGION)

        self.Bind(wx.EVT_MENU,  self.OnCheckIndentation, id=self.ID_CHECK_INDENTATION)
        self.Bind(wx.EVT_MENU,  self.OnCleanUpTabs, id=self.ID_CLEAN_UP_TABS)
        self.Bind(wx.EVT_MENU,  self.OnCleanUpSpaces, id=self.ID_CLEAN_UP_SPACES)

        self.Bind(wx.EVT_MENU,  self.OnFormatUnixMode, id=self.ID_UNIXMODE)
        self.Bind(wx.EVT_MENU,  self.OnFormatWinMode, id=self.ID_WINMODE)
        self.Bind(wx.EVT_MENU,  self.OnFormatMacMode, id=self.ID_MACMODE)

        self.Bind(wx.EVT_MENU,  self.OnFindAndComplete, id=self.ID_FIND_AND_COMPLETE)

        self.Bind(wx.EVT_MENU,  self.OnUppercase, id=self.ID_UPPERCASE)
        self.Bind(wx.EVT_MENU,  self.OnLowercase, id=self.ID_LOWERCASE)
        self.Bind(wx.EVT_MENU,  self.OnUndo, id=self.ID_UNDO)
        self.Bind(wx.EVT_MENU,  self.OnRedo, id=self.ID_REDO)

        self.Bind(wx.EVT_MENU,  self.OnGoTo, id=self.ID_GOTO)

        self.Bind(wx.EVT_MENU,  self.OnGoToBlockStart, id=self.ID_GOTO_BLOCK_START)
        self.Bind(wx.EVT_MENU,  self.OnGoToBlockEnd, id=self.ID_GOTO_BLOCK_END)
        self.Bind(wx.EVT_MENU,  self.OnGoToClassStart, id=self.ID_GOTO_CLASS_START)
        self.Bind(wx.EVT_MENU,  self.OnGoToClassEnd, id=self.ID_GOTO_CLASS_END)
        self.Bind(wx.EVT_MENU,  self.OnGoToDefStart, id=self.ID_GOTO_DEF_START)
        self.Bind(wx.EVT_MENU,  self.OnGoToDefEnd, id=self.ID_GOTO_DEF_END)

        self.Bind(wx.EVT_MENU,  self.OnSourceBrowserGoTo, id=self.ID_SOURCEBROWSER_GOTO)

        self.Bind(wx.EVT_MENU,  self.OnZoomIn, id=self.ID_ZOOM_IN)
        self.Bind(wx.EVT_MENU,  self.OnZoomOut, id=self.ID_ZOOM_OUT)

        self.Bind(wx.EVT_MENU,  self.OnSyntaxHighlightingPython, id=self.ID_HIGHLIGHT_PYTHON)
        self.Bind(wx.EVT_MENU,  self.OnSyntaxHighlightingCPP, id=self.ID_HIGHLIGHT_CPP)
        self.Bind(wx.EVT_MENU,  self.OnSyntaxHighlightingHTML, id=self.ID_HIGHLIGHT_HTML)
        self.Bind(wx.EVT_MENU,  self.OnSyntaxHighlightingText, id=self.ID_HIGHLIGHT_PLAIN_TEXT)

        self.Bind(wx.EVT_MENU,  self.OnToggleFold, id=self.ID_TOGGLE_FOLD)
        self.Bind(wx.EVT_MENU,  self.OnFoldAll, id=self.ID_FOLD_ALL)
        self.Bind(wx.EVT_MENU,  self.OnExpandAll, id=self.ID_EXPAND_ALL)

        self.Bind(wx.EVT_MENU,  self.OnViewInLeftPanel, id=self.ID_VIEW_IN_LEFT_PANEL)
        self.Bind(wx.EVT_MENU,  self.OnViewInRightPanel, id=self.ID_VIEW_IN_RIGHT_PANEL)
        self.Bind(wx.EVT_MENU,  self.OnViewInTopPanel, id=self.ID_VIEW_IN_TOP_PANEL)

        self.Bind(wx.EVT_MENU,  self.OnToggleSourceBrowser, id=self.ID_TOGGLE_SOURCEBROWSER)
        self.Bind(wx.EVT_MENU,  self.OnToggleViewWhiteSpace, id=self.ID_TOGGLE_VIEWWHITESPACE)
        self.Bind(wx.EVT_MENU,  self.OnTogglePrompt, id=self.ID_TOGGLE_PROMPT)

        self.Bind(wx.EVT_MENU,  self.OnRun, id=self.ID_RUN)
        self.Bind(wx.EVT_MENU,  self.OnSetArgs, id=self.ID_SET_ARGS)
        self.Bind(wx.EVT_MENU,  self.OnPython, id=self.ID_PYTHON)
        self.Bind(wx.EVT_MENU,  self.OnEnd, id=self.ID_END)
        self.Bind(wx.EVT_MENU,  self.OnCheckSyntax, id=self.ID_CHECK_SYNTAX)
        self.Bind(wx.EVT_MENU,  self.OnClosePrompt, id=self.ID_CLOSE_PROMPT)

        self.Bind(wx.EVT_MENU,  self.OnPrefs, id=self.ID_PREFS)
        self.Bind(wx.EVT_MENU,  self.OnCustomizeShortcuts, id=self.ID_SHORTCUTS)
        self.Bind(wx.EVT_MENU,  self.OnCustomizePopUpMenu, id=self.ID_POPUP)
        self.Bind(wx.EVT_MENU,  self.OnCustomizeToolBar, id=self.ID_CUSTOMIZE_TOOLBAR)
        self.Bind(wx.EVT_MENU,  self.OnEditBookmarks, id=self.ID_EDIT_BOOKMARKS)
        self.Bind(wx.EVT_MENU,  self.OnEditScriptMenu, id=self.ID_EDIT_SCRIPT_MENU)
        self.Bind(wx.EVT_MENU,  self.OnEditPlugin, id=self.ID_EDIT_PLUGIN)

        self.Bind(wx.EVT_MENU,  self.OnViewAbout, id=self.ID_ABOUT)
        self.Bind(wx.EVT_MENU,  self.OnViewHelp, id=self.ID_HELP)
        self.Bind(wx.EVT_MENU,  self.OnViewPythonDocs, id=self.ID_PYTHON_DOCS)
        self.Bind(wx.EVT_MENU,  self.OnViewWxWidgetsDocs, id=self.ID_WXWIDGETS_DOCS)
        self.Bind(wx.EVT_MENU,  self.OnViewREHowtoDocs, id=self.ID_REHOWTO_DOCS)
        self.Bind(wx.EVT_MENU,  self.OnOpenWidgetInspector, id=self.ID_INSPECT_TOOL)

        self.Bind(wx.EVT_MENU, self.DoBuiltIn, id=self.ID_COPY)
        self.Bind(wx.EVT_MENU, self.DoBuiltIn, id=self.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.DoBuiltIn, id=self.ID_CUT)
        self.Bind(wx.EVT_MENU, self.DoBuiltIn, id=self.ID_DELETE)

        self.Bind(wx.EVT_MENU, self.OnSelectDocumentNext, id=self.ID_NEXT_DOCUMENT)
        self.Bind(wx.EVT_MENU, self.OnSelectDocumentPrevious, id=self.ID_PREVIOUS_DOCUMENT)
        self.Bind(wx.EVT_MENU, self.OnSelectDocumentFirst, id=self.ID_FIRST_DOCUMENT)
        self.Bind(wx.EVT_MENU, self.OnSelectDocumentLast, id=self.ID_LAST_DOCUMENT)

        # add import all button
        self.Bind(wx.EVT_TOOL, self.OnImportAll, id=self.ID_IMPORT_ALL)
        # end import all
        # add pydoc menu items
        self.Bind(wx.EVT_MENU, self.OnPyDocAll, id=self.ID_PYDOC_ALL)
        self.Bind(wx.EVT_MENU, self.OnPyDocCurrent, id=self.ID_PYDOC_CURR)
        self.Bind(wx.EVT_MENU, self.OnViewPyDoc, id=self.ID_VIEW_PYDOC)
        #end pydoc

        self.txtDocument.SetupPrefsDocument()

        self.txtDocument.OnPositionChanged(None)

        self.txtPrompt.SetReadOnly(1)

        self.txtPrompt.SetupPrefsPrompt()

        #Load SourceBrowser:
        if self.prefs.sourcebrowserisvisible:
            wx.CallAfter (self.ShowSourceBrowser)

        self.Bind(wx.EVT_END_PROCESS,  self.OnProcessEnded, id=-1)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_CLOSE, self.OnCloseW)

        self.LoadPlugins()

        #Filenames to open from the commandline
        for f in sys.argv[1:]:
            if not os.path.exists(f):
                if self.Ask('"' + f + '" Does not exist.  Create?', 'File Does Not Exist'):
                    try:
                        fh = open(f, 'wb')
                        fh.close()
                    except:
                        self.ShowMessage('Error Creating "' + f + '"')
                        continue
                else:
                  continue
            self.OpenOrSwitchToFile(f)
        self.txtDocument.SetFocus()

        self.AddKeyEvent(self.CheckKey, wx.WXK_UP)
        self.AddKeyEvent(self.CheckKey, wx.WXK_DOWN)
        self.AddKeyEvent(self.CheckKey, wx.WXK_RETURN) #needed for AutoComp like FindAndComplete

    def Append_Menu(self, menu, id, s, LaunchesDialog = False, AmpersandAt = -1, absolutelabel=''):
        label = s
        item = wx.MenuItem(menu, id, label, label)
        menuiconfile = self.bitmapdirectory + "/16/" + s + ".png"
        if os.path.exists(menuiconfile):
            #try:
            img = wx.Image(menuiconfile, wx.BITMAP_TYPE_PNG)
            bmp = wx.BitmapFromImage(img)
            #except?
        #else:
            #bmp = wx.EmptyBitmap(16, 16) #width the same, background colour frame colour, so alignment is assured
            item.SetBitmap(bmp)
        #item.SetBitmap(bmp)
        menu.AppendItem(item)

    def AddKeyEvent(self, function, Keycode, Control=0, Shift=0, Alt=0, Meta=0):
        if Keycode == -1:
            return

        shortcut = drShortcuts.BuildShortcutString(Keycode, Control, Shift, Alt, Meta)

        self.PluginShortcutNames.append('Plugin')
        self.PluginShortcuts.append(shortcut)
        self.PluginAction.append(function)

    def AddPluginFunction(self, plugin, label, function):
        self.AddPluginShortcutFunction(plugin, label, function)
        self.AddPluginPopUpMenuFunction(plugin, label, function)
        self.AddPluginToolBarFunction(label, function)

    #todo: comment out? the function don't seem to be used anywhere
    def AddPluginIcon(self, name, location16, location24):
        ctbfile = self.datdirectory + "/toolbar.custom.icons.dat"
        if not os.path.exists(ctbfile):
            f = open(ctbfile, 'w')
            f.write('\n')
            f.close()
        f = open(ctbfile, 'r')
        lines = f.read().split('\n')
        f.close()
        name = "<Plugin>:" + name
        f = open(self.datdirectory + "/toolbar.custom.icons.dat", 'w')
        for line in lines:
            if line:
                currentname = drPrefsFile.ExtractPreferenceFromText(line, "Name")
                if currentname != name:
                    f.write(line + '\n')
        f.write("<Name>" + name + "</Name><16>" + location16 + "</16><24>" + \
        location24 + "</24>\n")
        f.close()

    #todo: comment out? the function don't seem to be used anywhere
    def AddPluginShortcutFunction(self, plugin, label, function):
        self.PluginShortcutFunctionNames.append(plugin + ":" + label)
        self.PluginShortcutFunctions.append(function)

    def AddPluginPopUpMenuFunction(self, plugin, label, function):
        self.PluginPopUpMenuNames.append(plugin)
        self.PluginPopUpMenuLabels.append(label)
        self.PluginPopUpMenuFunctions.append(function)

    def AddPluginToolBarFunction(self, label, function):
        self.PluginToolBarLabels.append("<Plugin>:"+label)
        self.PluginToolBarFunctions.append(function)

    def Ask(self, question, title='DrPython'):
        answer = wx.MessageBox(question, title, wx.YES_NO | wx.ICON_QUESTION)
        return (answer == wx.YES)

    def AskExitingDrPython(self):
        if self.Ask('Would you like to quit DrPython?'):
            sys.exit()

    def checkiffileisCPP(self, filename):
        return self.refiletypeiscpp.search(filename) is not None

    def checkiffileisHTML(self, filename):
        return self.refiletypeishtml.search(filename) is not None

    def checkiffileisPlainText(self, filename):
        return self.refiletypeistxt.search(filename) is not None

    def checkiffileisPython(self, filename):
        return self.refiletypeispy.search(filename) is not None

    def CheckKey(self,event):
        if self.GetActiveSTC().AutoCompActive():
            event.Skip()
            return 1
        return 0

    def CheckSyntax(self, docnumber=-1):
        if docnumber == -1:
            docnumber = self.docPosition
        fn = self.txtDocumentArray[docnumber].GetFilename()
        if not self.txtDocumentArray[docnumber].filename:
            self.ShowMessage('Cannot Run Check on "%s"' % fn, 'Cannot Check Untitled File')
            return False
        #Check Syntax First
        try:
            #begin patch Knut Gerwens, DrPython 164, Dec. 2006.
            #there was former a problem using unicode version of wxPython with encoding cookie
            encoding = self.txtDocumentArray[docnumber].GetEncoding()
            ctext = drEncoding.DecodeText(self, self.txtDocumentArray[docnumber].GetText(), encoding)
            ctext = ctext.replace('\r\n', '\n').replace('\r', '\n')
            compile(ctext, fn, 'exec')
            #end patch Knut Gerwens, DrPython 164, Dec. 2006.
        except Exception, e:
            excstr = str(e)
            result = self.rechecksyntax.search(excstr)
            if result is not None:
                num = result.group()[5:].strip()
                try:
                    n = int(num) - 1
                    self.setDocumentTo(docnumber)
                    self.txtDocument.ScrollToLine(n)
                    self.txtDocument.GotoLine(n)
                    self.ShowMessage('compile:\n' + excstr)
                    self.txtDocument.SetSTCFocus(True)
                    self.txtDocument.SetFocus()
                    #Stop the function here if something is found.
                    return False
                except:
                    self.ShowMessage('Line Number Error:\n\n'+excstr, 'SyntaxError')
            else:
                self.ShowMessage('No Line Number Found:\n\n' + excstr, 'Syntax Error')

        #Now Check Indentation
        result = drTabNanny.Check(fn)
        results = result.split()
        if len(results) > 1:
            num = results[1]
            try:
                n = int(num) - 1
                self.setDocumentTo(docnumber)
                self.txtDocument.ScrollToLine(n)
                self.txtDocument.GotoLine(n)
                self.ShowMessage('tabnanny:\n' + result)
                self.txtDocument.SetSTCFocus(True)
                self.txtDocument.SetFocus()
                return False
            except:
                self.ShowMessage('Line Number Error:\n\n'+result, 'TabNanny Trouble')

        return True

    def CreateRecentFileMenu(self):
        result = wx.Menu()
        self.recentfiles.UseMenu(result)
        self.recentfiles.AddFilesToMenu()
        id_base = self.recentfiles.IdBase
        self.Bind(wx.EVT_MENU_RANGE,
                  self.OnOpenRecentFile,
                  id=id_base,
                  id2=id_base + self.recentfiles.MaxFiles)
        return result

    def DestroyDocument(self):
        self.txtDocumentArray.pop(self.docPosition)
        self.lastprogargsArray.pop(self.docPosition)

    def DestroyToolBar(self):
        if self.toolbar is not None:
            x = 0
            toolbarsize = len(self.ToolBarIdList)
            while x < toolbarsize:
                if self.ToolBarIdList[x] == -300:
                    self.toolbar.DeleteToolByPos(0)
                else:
                    self.toolbar.DeleteTool(self.ToolBarIdList[x])
                x = x + 1
            self.toolbar.Destroy()
            self.toolbar = None

    def DoBuiltIn(self, event):
        objid = event.GetId()

        if self.txtPrompt.GetSTCFocus():
            stc = self.txtPrompt
        else:
            stc = self.txtDocument

        if objid == self.ID_COPY:
            stc.CmdKeyExecute(wx.stc.STC_CMD_COPY)
        elif objid == self.ID_PASTE:
            stc.Paste()
        elif objid == self.ID_CUT:
            stc.CmdKeyExecute(wx.stc.STC_CMD_CUT)
        elif objid == self.ID_DELETE:
            stc.CmdKeyExecute(wx.stc.STC_CMD_CLEAR)

    def DrMessageBox(self, msg, title, style):
        self.ignore_activate_app_event = True
        answer = wx.MessageBox(msg, title, style)
        self.ignore_activate_app_event = False
        return answer

    def dynamicdrscript(self, event):
        self.drscriptmenu.OnDynamicScript(event)

    def EditPlugin(self, plugin):
        pluginfile = os.path.join(self.pluginsdirectory, plugin) + ".py"

        #Patch From Franz, Check for already open.
        #(Slightly edited by Dan, if ... in replaces try ... except.
        self.OpenOrSwitchToFile(pluginfile)

    def Execute(self, command, statustext = ''):
        if not statustext:
            statustext = "Running Command"
        self.runcommand(command, statustext, command)

    def ExecutePython(self):
        self.txtPrompt.pythonintepreter = 1
        self.ExecuteWithPython('', 'Running Python Interpreter', '-i', 'Python')
        i = self.promptPosition
        try:
            wx.Yield()
        except:
            pass
        #workaround by Dunderhead.
        if self.PLATFORM_IS_WIN:
            self.txtPromptArray[i]._waitforoutput('>>>')
        #self.txtPromptArray[i]._waitforoutput('>>>')
        self.txtPromptArray[i].ExecuteCommands(self.prefs.promptstartupscript)

    def ExecuteWithPython(self, command = '', statustext = '', pythonargs='', pagetext='Python'):
        commandstring = string.join([' -u', pythonargs, self.prefs.pythonargs, command], ' ').rstrip()
        if self.PLATFORM_IS_WIN:
            self.runcommand((self.pythexecw + commandstring), statustext, pagetext)
        else:
            self.runcommand((self.pythexec + commandstring), statustext, pagetext)

    def GetActiveSTC(self):
        if self.txtPrompt.GetSTCFocus():
            return self.txtPrompt
        else:
            return self.txtDocument

    def GetAlreadyOpen(self):
        def _get_filename(x):
            return x.filename.lower()
        return map(_get_filename, self.txtDocumentArray)

    def getfileextensionstring(self, index):
        thelist = self.prefs.extensions[index].split(',')

        thestring = ''

        for t in thelist:
            thestring += '(\.' + t.strip() + '$)|'

        return thestring[:-1]

    def GetFileName(self):
        return self.txtDocument.filename

    def getmenulabel(self, label, LaunchesDialog=False, AmpersandAt=-1, absolutelabel=''):

        shortcuttext = ''

        if label in self.ShortcutNames:
            i = self.ShortcutNames.index(label)
            shortcuttext = drShortcuts.GetShortcutLabel(self.Shortcuts[i])
        elif label in self.STCShortcutNames:
            i = self.STCShortcutNames.index(label)
            shortcuttext = drShortcuts.GetShortcutLabel(self.STCShortcuts[i])

        if absolutelabel:
            label = absolutelabel

        else:

            if (AmpersandAt > -1) and (AmpersandAt < len(label)):
                label = label[:AmpersandAt] + '&' + label[AmpersandAt:]

            if LaunchesDialog:
                label += '...'

        if len(shortcuttext) > 1:
            return label + '\t' + shortcuttext
        return label

    def GetNewId(self):
        return 10000 + wx.NewId()

    #Begin Backwards Compatibility
    def GetPluginDirectory(self):
        return self.pluginsdirectory

    def GetPluginsDirectory(self):
        return self.GetPluginDirectory()
    #End Backwards Compatibility

    def GetPluginLabels(self, filename, doNotAppend = False):
        try:
            f = open(filename, 'r')
            text = f.read()
            f.close()
        except:
            self.ShowMessage('File error with: "' + filename + '".', "ERROR")
            return []

        rePopUpMenu = re.compile(r'^\s*?DrFrame\.AddPluginFunction\(.*\)', re.MULTILINE)

        allPopUps = rePopUpMenu.findall(text)

        PopUpArray = []

        for s in allPopUps:
            #From the Left most '('
            start = s.find('(')
            #To the Right most ')'
            end = s.rfind(')')

            if (start > -1) and (end > -1):
                s = s[start+1:end]
                i = s.find(',')
                e = i + 1 + s[i+1:].find(',')
                arglabel = s[i+1:e].strip().strip('"')
                if doNotAppend:
                    PopUpArray.append(arglabel)
                else:
                    PopUpArray.append("<Plugin>:"+arglabel)

        return PopUpArray

    def GetPluginMenuLabel(self, plugin, functionlabel, menulabel=''):
        shortcuttext = ''

        searchlabel = plugin + ':' + functionlabel

        if searchlabel in self.PluginShortcutNames:
            i = self.PluginShortcutNames.index(searchlabel)
            shortcuttext = drShortcuts.GetShortcutLabel(self.PluginShortcuts[i])

        if not menulabel:
            menulabel = functionlabel

        if len(shortcuttext) > 1:
            return menulabel + '\t' + shortcuttext

        return menulabel

    def GetPreference(self, pref, key=None):
        if key is not None:
            return self.prefs[pref][key]
        else:
            return self.prefs[pref]

    def WriteUserPreferencesDirectoryFile(self):
        if not self.invokeuserpreferencespath:
            f = open(self.preferencesdirectoryfile, 'w')
            f.write(self.preferencesdirectory)
            f.close()

    def InitializeConstants(self):
        #Constant messages for file format checking.
        self.FFMESSAGE = ["Unix Mode ('\\n')", "DOS/Windows Mode ('\\r\\n')", "Mac Mode ('\\r')"]
        self.TABMESSAGE = ['Spaces', 'Mixed', 'Tabs', 'None']

        self.ID_DOCUMENT_BASE = 50
        self.ID_PROMPT_BASE = 340

        #Application ID Constants
        self.ID_APP = 101
        self.ID_NEW = 102
        self.ID_OPEN = 103
        self.ID_OPEN_IMPORTED_MODULE = 1000
        self.ID_OPEN_RECENT = 104
        self.ID_RELOAD = 105
        self.ID_RESTORE_FROM_BACKUP = 1051
        self.ID_CLOSE = 106
        self.ID_CLOSE_ALL = 6061
        self.ID_CLOSE_ALL_OTHER_DOCUMENTS = 6062
        self.ID_CLEAR_RECENT = 107
        self.ID_SAVE = 108
        self.ID_SAVE_AS = 109
        self.ID_SAVE_COPY = 1092
        self.ID_SAVE_ALL = 1098
        self.ID_SAVE_PROMPT = 1091
        self.ID_PRINT_SETUP = 1010
        self.ID_PRINT = 1011
        self.ID_PRINTPROMPT = 1012
        self.ID_EXIT = 1014
        # define import all id
        self.ID_IMPORT_ALL = self.GetNewId()

        # end import all

        # define pydoc ids
        self.ID_PYDOC_ALL = 1016
        self.ID_PYDOC_CURR = 1017
        self.ID_VIEW_PYDOC = 1018
        # end pydoc

        self.ID_INSPECT_TOOL = 1019

        self.ID_NEXT_DOCUMENT = 801
        self.ID_PREVIOUS_DOCUMENT = 802
        self.ID_FIRST_DOCUMENT = 803
        self.ID_LAST_DOCUMENT = 804
        self.ID_DOCUMENT_NAVIGATION_MENU = 810
        self.ID_DOCUMENTS_BASE = 8000
        self.ID_DOCUMENTS_MENU_BASE = 7950

        self.ID_COPY = 850
        self.ID_PASTE = 851
        self.ID_CUT = 852
        self.ID_DELETE = 853

        self.ID_FIND = 111
        self.ID_FIND_NEXT = 112
        self.ID_FIND_PREVIOUS = 1122
        self.ID_REPLACE = 113
        self.ID_GOTO = 115
        self.ID_GOTO_MENU = 1150
        self.ID_GOTO_BLOCK_START = 1151
        self.ID_GOTO_BLOCK_END = 1152
        self.ID_GOTO_CLASS_START = 1153
        self.ID_GOTO_CLASS_END = 1154
        self.ID_GOTO_DEF_START = 1155
        self.ID_GOTO_DEF_END = 1156

        self.ID_SOURCEBROWSER_GOTO = 1157

        self.ID_SELECT_ALL = 1161

        self.ID_INSERT_REGEX = 1163

        self.ID_INSERT_SEPARATOR = 1164

        self.ID_COMMENT = 1116
        self.ID_COMMENT_REGION = 116
        self.ID_UNCOMMENT_REGION = 117

        self.ID_WHITESPACE = 1118
        self.ID_INDENT_REGION = 118
        self.ID_DEDENT_REGION = 119
        self.ID_CHECK_INDENTATION = 1650

        self.ID_CLEAN_UP_TABS = 1670
        self.ID_CLEAN_UP_SPACES = 1671

        self.ID_FORMATMENU = 2000
        self.ID_UNIXMODE = 2001
        self.ID_WINMODE = 2002
        self.ID_MACMODE = 2003

        self.ID_FIND_AND_COMPLETE = 2071

        self.ID_CASE = 1191
        self.ID_UPPERCASE = 1192
        self.ID_LOWERCASE = 1193

        self.ID_UNDO = 1111
        self.ID_REDO = 1112

        self.ID_ZOOM_IN = 161
        self.ID_ZOOM_OUT = 162
        self.ID_FOLDING = 1610
        self.ID_TOGGLE_FOLD = 1613
        self.ID_FOLD_ALL = 1611
        self.ID_EXPAND_ALL = 1612
        self.ID_TOGGLE_SOURCEBROWSER = 163
        self.ID_TOGGLE_VIEWWHITESPACE = 164
        self.ID_TOGGLE_PROMPT = 165

        self.ID_VIEW_IN_PANEL = 170
        self.ID_VIEW_IN_LEFT_PANEL = 171
        self.ID_VIEW_IN_RIGHT_PANEL = 172
        self.ID_VIEW_IN_TOP_PANEL = 173

        self.ID_VIEW_IN_PANEL_BASE = 1700

        self.ID_HIGHLIGHT = 580

        self.ID_HIGHLIGHT_PYTHON = 585
        self.ID_HIGHLIGHT_CPP = 586
        self.ID_HIGHLIGHT_HTML = 587
        self.ID_HIGHLIGHT_PLAIN_TEXT = 589

        self.ID_RUN = 121
        self.ID_SET_ARGS = 122
        self.ID_PYTHON = 123
        self.ID_END = 125
        self.ID_CLOSE_PROMPT = 1250
        self.ID_CHECK_SYNTAX = 126

        self.ID_PREFS = 131
        self.ID_SHORTCUTS = 133
        self.ID_POPUP = 134
        self.ID_CUSTOMIZE_TOOLBAR = 135

        self.ID_CONFIGURE_PLUGINS = 4005
        self.ID_LOAD_PLUGIN = 4050
        self.ID_PLUGIN_HELP = 4051
        self.ID_PLUGIN_PREFS = 4052
        self.ID_PLUGIN_ABOUT = 4053
        self.ID_EDIT_PLUGIN = 4054

        self.ID_EDIT_BOOKMARKS = 301
        self.ID_EDIT_SCRIPT_MENU = 3004

        self.ID_ABOUT = 140
        self.ID_HELP = 141
        self.ID_PYTHON_DOCS = 142
        self.ID_WXWIDGETS_DOCS = 143
        self.ID_REHOWTO_DOCS = 144

        self.ID_OTHER = 9000

        self.ID_RECENT_SESSIONS_BASE = 8330

        self.ID_SCRIPT_BASE = 7500

        #STC Shortcut List:

        self.STCCOMMANDLIST = drShortcuts.GetSTCCommandList()

        #System constants

        self.PLATFORM_IS_WIN = wx.Platform == '__WXMSW__' # (sys.platform == "win32") or #wx.PLATFORM_WINDOWS or wx.PLATFORM_WINDOWS
        self.PLATFORM_IS_GTK = wx.Platform == '__WXGTK__'
        self.PLATFORM_IS_MAC = wx.Platform == '__WXMAC__'

        self.PLATFORM_OTHER = False
        if not self.PLATFORM_IS_WIN and not self.PLATFORM_IS_GTK and not self.PLATFORM_IS_MAC:
            self.PLATFORM_OTHER = True

        #Thanks to Mark Rees.
        #Thanks to Guillermo Fernandez.
        #Thanks Bjorn Breid

        #Preferences Directory Initial Setup:

        self.userhomedirectory = wx.StandardPaths.Get().GetUserConfigDir().replace('\\', '/')
        if not self.preferencesdirectory:

            self.preferencesdirectory = self.userhomedirectory

            self.preferencesdirectoryprefix = "/.drpython"
            if self.PLATFORM_IS_WIN:
                self.preferencesdirectoryprefix = "/drpython"
            self.preferencesdirectory += self.preferencesdirectoryprefix
            self.preferencesdirectoryfile = self.preferencesdirectory + "/userpreferencesdirectory.dat"

            if not os.path.exists(self.preferencesdirectory):
                os.mkdir(self.preferencesdirectory)

            if not os.path.exists(self.preferencesdirectoryfile):
                self.WriteUserPreferencesDirectoryFile()

            f = open(self.preferencesdirectoryfile, 'r')
            pth = f.read()
            f.close()

            if os.path.exists (pth):
                self.preferencesdirectory = pth
            else:
                wx.MessageBox("Changing Userpreferences directory to default:\n '%s'" % \
                    self.preferencesdirectory,
                    "Userpreferences Directory not found:",
                    wx.ICON_EXCLAMATION)
                self.WriteUserPreferencesDirectoryFile()

        #backwards compatibility todo remove that later
        self.homedirectory = os.path.expanduser('~')

        if self.PLATFORM_IS_WIN:
            self.pythexec = sys.prefix.replace("\\", "/") + "/python.exe"
            self.pythexecw = sys.prefix.replace("\\", "/") + "/pythonw.exe"
        else:
            self.pythexec = sys.executable

    def InitializePlugin(self, plugin, ShowDialog = True):
        #Check to see if the plugin is already loaded:
        if plugin in self.LoadedPlugins:
            if ShowDialog:
                self.ShowMessage(('"' + plugin + '" has already been loaded.\nDrPython will not reload this plugin.'), "Plugin Already Loaded")
            return

        #Load the Plugin
        pluginfile = os.path.join (self.pluginsdirectory, plugin + ".py")
        self.LoadedPlugins.append(plugin)
        try:
            exec(compile("import " + plugin, pluginfile, 'exec'))
            exec(compile(plugin + ".Plugin(self)", pluginfile, 'exec'))
            exec(compile('self.PluginModules.append('+plugin+')', pluginfile, 'exec'))
        except:
            self.ShowMessage("Error with: " + plugin + "\nDrPython will not load this plugin.", "Plugin Error")

        #Menus
        self.pluginsaboutmenu.AddItem(plugin)
        self.pluginshelpmenu.AddItem(plugin)
        self.pluginsprefsmenu.AddItem(plugin)

    def LoadPlugins(self, plugins_file = ""):
        #todo remove this? is this used? franz 22.03.2007:
        if plugins_file:
            pluginsfile = plugins_file
        else:
            #end todo remove this? is this used? franz 22.03.2007:
            pluginsfile = self.preferencesdirectory  + "/default.idx"
        if os.path.exists(pluginsfile):
            try:
                f = open(pluginsfile, 'rU')
                pluginstoload = [x.strip() for x in f]
                f.close()

                for plugin in pluginstoload:
                    if plugin:
                        self.InitializePlugin(plugin)
            except:
                self.ShowMessage(("Error with: " + pluginsfile + "\nDrPython will not load plugins."), "Plugins Error")
        else:
            try:
                f = open(pluginsfile, 'wb')
                #f.write('\n')
                f.close()
            except:
                self.ShowMessage('Error Ceating Default Index for Plugins.\n\nPlugins may not work correctly.', 'Plugins Error')

    def LoadPluginShortcuts(self, plugin):
        if plugin in self.PluginShortcutsLoadedArray:
            return
        self.PluginShortcutsLoadedArray.append(plugin)

        shortcutfile = os.path.join (self.pluginsshortcutsdirectory, plugin + ".shortcuts.dat")
        if not os.path.exists(shortcutfile):
            return
        try:
            shortcuts, names, ignorestring = drShortcutsFile.ReadShortcuts(shortcutfile, 0)
            x = 0
            l = len(shortcuts)
            while x < l:
                shortcut = shortcuts[x]
                try:
                    i = self.PluginShortcutFunctionNames.index(plugin + ":" + names[x])
                    self.PluginAction.append(self.PluginShortcutFunctions[i])
                    self.PluginShortcutNames.append(plugin + ":" + names[x])
                    self.PluginShortcuts.append(shortcut)
                except:
                    pass
                x += 1
        except:
            self.ShowMessage(("Error with: " + plugin + "\nDrPython will not load shortcuts for this plugin."), "Plugin Shortcuts Error")


    def LoadPopUpFile(self):
        #check for preferences file in user userpreferencesdirectory
        popupfile = self.datdirectory + "/popupmenu.dat"

        if os.path.exists(popupfile):
            try:
                f = open(popupfile, 'r')
                line = f.readline()
                while len(line) > 0:
                    self.popupmenulist.append(line.rstrip())
                    line = f.readline()
                f.close()
            except:
                self.ShowMessage("Error with: " + popupfile + "\nDrPython will use the program defaults.", "Pop Up Menu Error")


    def SetDrPythonDirectories(self):

        #bitmaps code directory
        self.bitmapdirectory = self.programdirectory + "/bitmaps"
        if not os.path.exists(self.bitmapdirectory):
            self.ShowMessage("Bitmap Directory (" + self.bitmapdirectory + ") does Not Exist.", "DrPython Fatal Error")
            sys.exit(1)

        #for backward compatibility (can be removed in the future).
        self.userpreferencesdirectory = self.preferencesdirectory


        #plugins code directory
        if not os.path.exists(self.prefs.pluginsdirectory):
            os.mkdir(self.prefs.pluginsdirectory)

        self.pluginsdirectory = self.prefs.pluginsdirectory
        sys.path.append(self.pluginsdirectory)

        #drscripts code directory
        if not os.path.exists(self.prefs.drscriptsdirectory):
            os.mkdir(self.prefs.drscriptsdirectory)
        self.drscriptsdirectory = self.prefs.drscriptsdirectory

        #dat directory
        self.datdirectory = os.path.join(self.preferencesdirectory, 'dat')
        if not os.path.exists(self.datdirectory):
            os.mkdir(self.datdirectory)

        #shortcuts directory
        self.shortcutsdirectory = os.path.join(self.preferencesdirectory, 'shortcuts')
        if not os.path.exists(self.shortcutsdirectory):
            os.mkdir(self.shortcutsdirectory)

        #plugins directory
        self.pluginsbasepreferencesdir = os.path.join(self.preferencesdirectory, '.plugins')
        if not os.path.exists(self.pluginsbasepreferencesdir):
            os.mkdir(self.pluginsbasepreferencesdir)

        #plugins preferences directory
        self.pluginspreferencesdirectory = os.path.join(self.pluginsbasepreferencesdir, 'preferences')
        if not os.path.exists(self.pluginspreferencesdirectory):
            os.mkdir(self.pluginspreferencesdirectory)

        #plugins shortcuts directory
        self.pluginsshortcutsdirectory = os.path.join(self.pluginsbasepreferencesdir, 'shortcuts')
        if not os.path.exists(self.pluginsshortcutsdirectory):
            os.mkdir(self.pluginsshortcutsdirectory)

        #plugins dat directory
        self.pluginsdatdirectory = os.path.join(self.pluginsbasepreferencesdir, 'dat')
        if not os.path.exists(self.pluginsdatdirectory):
            os.mkdir(self.pluginsdatdirectory)

    def LoadPreferences(self):
        #check for preferences file in user userpreferencesdirectory
        if os.path.exists(self.prefsfile):
            try:
                drPrefsFile.ReadPreferences(self.prefs, self.prefsfile)
            except:
                self.ShowMessage(("Error with: " + self.prefsfile + "\nDrPython will load the program defaults."), "Preferences Error")
                self.prefs.reset()
                drPrefsFile.WritePreferences(self.prefs, self.prefsfile)
        else:
            drPrefsFile.WritePreferences(self.prefs, self.prefsfile)
        wx.GetApp().debugmodus = self.prefs.debugmodus
        # already restted
        if self.prefs.defaultencoding:
            reload(sys)  #this is needed because of wine and linux
            sys.setdefaultencoding(self.prefs.defaultencoding)
            wx.SetDefaultPyEncoding(self.prefs.defaultencoding)

    def LoadRecentFiles(self):
        filename = self.datdirectory + "/recent_files.log"
        if not os.path.exists(filename):
            try:
                open(filename, 'w').close()
            except IOError:
                if self.prefs.debugmodus:
                    self.ShowMessage(
                        "Error Creating: %r\n"
                        "Maybe you don't have right access or harddisk is full" % filename,
                        "Recent Files Error"
                    )
                    self.AskExitingDrPython()

        try:
            self.recentfiles.LoadFromFile(filename)
        except IOError:
            self.ShowMessage("Error Reading: " + filename, "Recent Files Error")
            self.AskExitingDrPython()

    def LoadShortcuts(self, UseDefault = False):
        #Load STC Shortcuts
        stcshortcutsfile = self.shortcutsdirectory + "/stcshortcuts.dat"
        if os.path.exists(stcshortcutsfile) and (not UseDefault):
            try:
                self.STCShortcuts, self.STCShortcutNames, t = drShortcutsFile.ReadSTCShortcuts(stcshortcutsfile)
                self.STCUseDefault = 0
            except:
                self.ShowMessage(("Error with: " + stcshortcutsfile + "\nDrPython will not load STC shortcuts."),
                                  "STC Shortcuts Error")

        #check for shortcuts file in user userpreferencesdirectory
        shortcutsfile = self.shortcutsdirectory + "/shortcuts.dat"
        if os.path.exists(shortcutsfile) and (not UseDefault):
            try:
                self.Shortcuts, self.ShortcutNames, self.ShortcutsIgnoreString = drShortcutsFile.ReadShortcuts(shortcutsfile)
                self.ShortcutsUseDefault = 0
            except:
                self.ShowMessage(("Error with: " + shortcutsfile + "\nDrPython will load the program defaults."),
                                  "Shortcuts Error")
                self.LoadShortcuts(True)

        #Load DrScript Shortcuts
        drscriptsshortcutsfile = self.shortcutsdirectory + "/drscript.shortcuts.dat"
        if os.path.exists(drscriptsshortcutsfile) and (not UseDefault):
            try:
                self.DrScriptShortcuts, self.DrScriptShortcutNames, t = drShortcutsFile.ReadShortcuts(drscriptsshortcutsfile, 0)
            except:
                self.ShowMessage("Error with: " + drscriptsshortcutsfile + "\nDrPython will not load DrScript shortcuts.",
                                  "DrScript Shortcuts Error")
            namelen = len (self.DrScriptShortcutNames)
            shortcutslen = len(self.DrScriptShortcuts)
            if namelen != shortcutslen:
                self.ShowMessage("'drscript.shortcuts.dat' (%d Entries) and 'drscript.dat' (%d Entries) file are out of sync." % (shortcutslen, namelen),
                                  "DrScript Shortcuts Error")

    def OnActivate(self, event):
        if self.prefs.docautoreload:
            x = 0
            for Document in self.txtDocumentArray:
                if Document.filename:
                    #Get Stat Info:
                    if os.path.exists(Document.filename): #bug 2010127 reported by by Luca Falavigna - dktrkranz, thanks
                        current_mtime = int(os.stat(Document.filename).st_mtime)

                        #Check Stat Info:
                        if Document.mtime > -1:
                            if current_mtime != Document.mtime:
                                if self.Ask('"%s" has been modified by an outside source.  Would you like to reload?' % (Document.filename), "Reload File?"):
                                    self.setDocumentTo(x)
                                    self.OpenFile(Document.filename, False)
                                else:
                                    Document.mtime = current_mtime
                x += 1
        self.txtDocument.SetFocus()

    def OnDeActivate(self, event):
        if self.txtDocument.AutoCompActive():
           self.txtDocument.AutoCompCancel()
        if self.txtDocument.CallTipActive():
           self.txtDocument.CallTipCancel()
        event.Skip()

    def OnCheckIndentation(self, event):
        wx.BeginBusyCursor()
        result = self.txtDocument.CheckIndentation()
        if result == 2:
            msg = "No indentation was found in this document."
        elif result == -1:
            msg = "This document uses spaces for indentation."
        elif result == 1:
            msg = "This document uses tabs for indentation."
        elif result == 0:
            msg = "This document is mixed.  It uses tabs and spaces for indentation."
        wx.EndBusyCursor()
        self.ShowMessage(msg, "Check Indentation Results")

    def OnCheckSyntax(self, event):
        if self.CheckSyntax(self.docPosition):
            if self.prefs.enablefeedback:
                self.ShowMessage(self.txtDocument.GetFilename() + '\nPassed Syntax Check', 'Syntax Check Ok')
            else:
                self.SetStatusText('Passed Syntax Check', 2)

    def OnCleanUpSpaces(self, event):
        d = wx.TextEntryDialog(self, "Replace a tab with how many spaces?:", "Replace Tabs With Spaces", str(self.prefs.doctabwidth[self.txtDocument.filetype]))
        answer = d.ShowModal()
        value = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            wx.BeginBusyCursor()
            wx.Yield()
            try:
                x = int(value)
            except:
                self.ShowMessage("You must enter an integer (number, eg 1,2,128)", "DrPython")
                wx.EndBusyCursor()
                return
            if (x > -1) and (x <= 128):
                self.txtDocument.SetToSpaces(x)
            else:
                self.ShowMessage("That number seems WAY too high.  Just what are you doing, replacing  a tab with more than 128 spaces?", "DrPython Foolish Error")
                wx.EndBusyCursor()
                return
            self.txtDocument.OnModified(None)
            wx.EndBusyCursor()

    def OnCleanUpTabs(self, event):
        d = wx.TextEntryDialog(self, "Number of spaces to replace with a tab:", "Replace Spaces With Tabs", str(self.prefs.doctabwidth[self.txtDocument.filetype]))
        answer = d.ShowModal()
        value = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            wx.BeginBusyCursor()
            wx.Yield()
            try:
                x = int(value)
            except:
                self.ShowMessage("You must enter an integer (number, eg 1,2,128)", "DrPython")
                wx.EndBusyCursor()
                return
            if (x > -1) and (x <= 128):
                self.txtDocument.SetToTabs(x)
            else:
                self.ShowMessage("That number seems WAY too high.  Just what are you doing, replacing more than 128 spaces with a tab?", "DrPython Foolish Error")
                wx.EndBusyCursor()
                return
            self.txtDocument.OnModified(None)
            wx.EndBusyCursor()

    def OnClearRecent(self, event):
        if self.Ask("This will clear all recent files.\nAre you sure you want to do this?", "DrPython"):
            self.recentfiles.Clear()
            self.WriteRecentFiles()

    def OnClose(self, event):
        self.PPost(self.EVT_DRPY_FILE_CLOSING)
        if self.txtDocument.GetModify():
            #prompt saving filename limodou 2004/04/19
            answer = wx.MessageBox('Would you like to save "%s"?' % self.txtDocument.GetFilename(), "DrPython", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            #end limodou
            if answer == wx.YES:
                if not self.OnSave(event):
                    return
            elif answer == wx.CANCEL:
                return

        #franz: oldpos is not used
        #11/24: :) It is now!  (Adding Franz's BugFix, ironically enough).
        oldpos = self.docPosition
        oldfinder = self.txtDocumentArray[oldpos].Finder
        if len(self.txtDocumentArray) > 1:
            self.DestroyDocument()
            #Update txtDocument.targetPosition
            x = 0
            l = len(self.txtDocumentArray)
            while x < l:
                self.txtDocumentArray[x].targetPosition = x
                x = x + 1
            self.documentnotebook.DeletePage(self.docPosition)
            if self.docPosition > 0:
                self.docPosition -= 1
            elif len(self.txtDocumentArray) > 1:
                if self.docPosition > 0:
                    self.docPosition += 1
            if self.docPosition < len(self.txtDocumentArray) -1:
                self.setDocumentTo(oldpos)
            else:
                self.setDocumentTo(self.docPosition, 1)
            #11/24:
            #if oldpos > self.docPosition:
            if self.txtDocument.Finder:
                self.txtDocument.Finder.Copy(oldfinder)
        else:
            #Clear the current document:
            self.txtDocument.SetText("")
            self.txtDocument.filename = ""
            self.txtDocument.mtime = -1
            self.txtDocument.EmptyUndoBuffer()
            self.txtDocument.SetSavePoint()
            self.UpdateMenuAndToolbar()
            #The set size stuff ensures that wx.widgets repaints the tab.
            x, y = self.GetSizeTuple()
            self.SetSize((x-1, y-1))
            self.SetSize((x, y))
            self.txtDocument.untitlednumber = 1

        self.txtDocument.IsActive = True
        self.txtDocument.OnModified(None)
        self.documentnotebook.OnPageChanged(None)
        self.reloaddocumentsmenu()
        if self.SourceBrowser is not None:
            self.SourceBrowser.Browse()

        self.txtDocument.SetupLineNumbersMargin()

        self.PPost(self.EVT_DRPY_FILE_CLOSED)

    # Feb. 17 05 - Adding import all function

    def OnImportAll(self, event):
        """When the Import All button is clicked, get the path of each open file,
        and append it to sys.path, then import each file into the interpreter
        (via ExecuteCommands)"""

        if self.txtPrompt.pythonintepreter == 0:
            self.ExecutePython()
        self.promptSaveAll()
        x = len(self.txtDocumentArray) - 1
        while x > -1:
            filePath = self.getFilePath(self.txtDocumentArray[x].GetFilename())
            self.txtPrompt.ExecuteCommands("sys.path.append(\"" + filePath[0] + "\")")
            self.txtPrompt.ExecuteCommands("import " + filePath[1])
            x = x - 1


    def getFilePath(self, path):
        """Takes a path including a file name, and returns a tuple
        containing the path (minus file name), and just the file name."""
        if path.find("\\") == -1:
            return (path[:path.rfind("/") + 1], path[path.rfind("/") +1:path.rfind(".")])
        else:
            return (path[:path.rfind("\\") + 1], path[path.rfind("\\") + 1:path.rfind(".")])

    # End Feb. 17 05 import all changes.

    # Feb. 17 05 - Adding pydoc functions
    def OnPyDocAll(self, event):
        """When the generate pydoc for all files item is selected, get the path of each open file,
        and append it to sys.path, then document each file (via pydoc.writedoc))"""

        self.promptSaveAll()

        # specify output directory to save html files to
        dir = self.promptDir("Select output directory:")
        if dir:
            cwd = os.getcwd()
            os.chdir(dir)

            # grab output of pydoc commands in a temp file
            oldstdout = sys.stdout
            fd, tempname = tempfile.mkstemp()
            temp = open(tempname, 'w')

            # go through each open file, documenting
            for x in range(len(self.txtDocumentArray)):
                filePath = self.getFilePath(self.txtDocumentArray[x].GetFilename())
                sys.path.append(filePath[0])
                # create html doc
                sys.stdout = temp
                pydoc.writedoc(str(filePath[1]))
            sys.stdout = oldstdout
            temp.close()
            temp = open(tempname, 'r')
            msg = temp.read()
            temp.close()
            os.chdir(cwd)
            # pop up a message to say it generated the file
            wx.MessageBox('PyDoc: \n'+msg+'\nLocation: '+dir, 'PyDoc', wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox ("Please specify a valid directory!", "PyDoc All", wx.ICON_INFORMATION)

    def OnPyDocCurrent(self, event):
        """When the generate pydoc for current file item is selected, get the path of the current file,
        and append it to sys.path, then document it (via pydoc.writedoc))"""

        self.promptSaveCurrent()

        # specify output directory to save html files to
        dir = self.promptDir("Specify output directory:")
        if dir:
            cwd = os.getcwd()
            os.chdir(dir)

            # grab output of pydoc commands in a temp file
            oldstdout = sys.stdout
            fd, tempname = tempfile.mkstemp()
            temp = open(tempname, 'w')

            filePath = self.getFilePath(self.txtDocument.GetFilename())
            sys.path.append(filePath[0])
            # grab output of commands in a temp file
            oldstdout = sys.stdout
            sys.stdout = temp
            # create html file documenting python module
            pydoc.writedoc(str(filePath[1]))
            #pydoc.writedoc(filePath[1].encode (self.prefs.defaultencoding))
            sys.stdout = oldstdout
            temp.close()
            temp = open(tempname, 'r')
            msg = temp.read()
            temp.close()
            # pop up a message to say it generated the file
            os.chdir(cwd)
            wx.MessageBox('PyDoc: '+msg+'Location: '+dir, 'PyDoc', wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox ("Please specify a valid directory!", "PyDoc Current File", wx.ICON_INFORMATION)

    def OnViewPyDoc(self, event):
        """ Pop up PoyDoc view window, which allows the user to view pydoc in a browser for all
        files on the path"""

        self.promptSaveAll()

        if self.txtPrompt.pythonintepreter == 0:
            self.ExecutePython()
        self.txtPrompt.ExecuteCommands("import pydoc")
        for x in range(len(self.txtDocumentArray)):
            filePath = self.getFilePath(self.txtDocumentArray[x].GetFilename())
            self.txtPrompt.ExecuteCommands("sys.path.append(\"" + filePath[0] + "\")")

        # pydoc gui doesn't close from within drpython, display a message to
        # tell the user to close it with the end button
        self.txtPrompt.AddText('\n***Press the red "End" button on the DrPython toolbar (or CTRL+D) to stop***\n')
        self.txtPrompt.ExecuteCommands("pydoc.gui()")

    # End Feb. 17 05 pydoc changes.

    def OnCloseAllDocuments(self, event):
        x = len(self.txtDocumentArray) - 1
        while x > -1:
            self.setDocumentTo(x, True)
            if self.txtDocument.GetModify():
                #prompt saving filename limodou 2004/04/19
                if self.Ask('Would you like to save "%s"?' % self.txtDocument.GetFilename(), "DrPython"):
                #end limodou
                    self.OnSave(event)
            self.OnClose(event)
            x = x - 1

    def OnCloseAllOtherDocuments(self, event):
        if not self.txtDocument.filename:
            self.ShowMessage("Sorry, does not work when an untitled file is selected.", "DrPython Error")
            return
        farray = map(lambda document: document.filename, self.txtDocumentArray)
        try:
            i = farray.index(self.txtDocument.filename)
        except:
            #franz: (Updated Namespace)
            self.ShowMessage("Something went wrong trying to close all other tabs.", "DrPython Error")
            return

        x = len(farray) - 1
        while x > -1:
            if x != i:
                self.setDocumentTo(x, True)
                if self.txtDocument.GetModify():
                    #prompt saveing filename limodou 2004/04/19
                    if self.Ask('Would you like to save "%s"?' % self.txtDocument.GetFilename(), "DrPython"):
                    #end limodou
                        self.OnSave(event)
                self.OnClose(event)
            x = x - 1

    def OnClosePrompt(self, event):
        oldpos = self.promptPosition
        oldfinder = self.txtPromptArray[oldpos].Finder
        self.OnEnd(None)

        if len(self.txtPromptArray) > 1:
            self.txtPromptArray.pop(self.promptPosition)

            self.promptnotebook.DeletePage(self.promptPosition)
            if self.promptPosition > 0:
                self.promptPosition = self.promptPosition - 1
            elif len(self.txtPromptArray) > 1:
                if self.promptPosition > 0:
                    self.promptPosition = self.promptPosition + 1
            self.setPromptTo(self.promptPosition)
            #11/24:
            if oldpos > self.promptPosition:
                if self.txtPrompt.Finder:
                    self.txtPrompt.Finder.Copy(oldfinder)
        else:
            self.txtPrompt.SetText("")
            self.txtPrompt.EmptyUndoBuffer()
            self.txtPrompt.SetSavePoint()
            self.UpdateMenuAndToolbar()
            self.promptnotebook.SetPageText(self.promptPosition, "Prompt")
            #The set size stuff ensures that wx.widgets repaints the tab.
            x, y = self.GetSizeTuple()
            self.SetSize((x-1, y-1))
            self.SetSize((x, y))


        self.promptnotebook.OnPageChanged(None)

    def OnCloseW(self, event):
        if event.CanVeto():
            try:
                x = self.docPosition
                if self.docPosition > 0:
                    fromzero = self.docPosition
                l = len(self.txtDocumentArray)
                while x < l:
                    if self.txtDocumentArray[x].GetModify():
                        answer = wx.MessageBox('Would you like to save "%s"?' % self.txtDocumentArray[x].GetFilename(),
                            "DrPython", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                        if answer == wx.YES:
                            self.setDocumentTo(x)
                            self.OnSave(event)
                        elif answer == wx.CANCEL:
                            return
                    x = x + 1

                if fromzero > 0:
                    x = 0
                    l = fromzero
                    while x < l:
                        if self.txtDocumentArray[x].GetModify():
                            answer = wx.MessageBox('Would you like to save "%s"?' % self.txtDocumentArray[x].GetFilename(),
                                "DrPython", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
                            if answer == wx.YES:
                                self.setDocumentTo(x)
                                self.OnSave(event)
                            elif answer == wx.CANCEL:
                                return
                        x = x + 1
            except:
                if self.prefs.alwayspromptonexit:
                    if not self.Ask("Are you sure you want to exit?   ", "DrPython"):
                        return

        #self.ignoreevents = True
        self.disableeventhandling = True
        wx.GetApp().Unbind(wx.EVT_ACTIVATE_APP) # needed for wxpython 2.9, else deadobject error, because of delivering event
        wx.GetApp().Unbind(wx.EVT_IDLE) # needed, else wx._core.PyDeadObjectError at the end
        if self.prefs.rememberwindowsizeandposition:
            wasMaximized = 0
            if self.IsMaximized(): #only to get the right values
                self.Maximize(False)
                wasMaximized = 1

            #if not self.IsMaximized(): #else some problems appears (?)
            try:
                f = open(self.datdirectory + "/drpython.sizeandposition.dat", 'w')
                x, y = self.GetSizeTuple()
                px, py = self.GetPositionTuple()
                f.write(str(x) + '\n' + str(y) + '\n' + str(px) + '\n' + str(py) + '\n' + str(wasMaximized))
                f.close()
            except:
                self.ShowMessage("Error Saving Window Size", 'Error')

        self.mainpanel.MemorizePanelSizes()

        event.Skip()

    def OnCommentRegion(self, event):
        selstart, selend = self.txtDocument.GetSelection()
        #From the start of the first line selected
        oldcursorpos = self.txtDocument.GetCurrentPos()
        startline = self.txtDocument.LineFromPosition(selstart)
        self.txtDocument.GotoLine(startline)
        start = self.txtDocument.GetCurrentPos()
        #To the end of the last line selected
        #Bugfix Chris Wilson
        #Edited by Dan (selend fix)
        if selend == selstart:
            tend = selend
        else:
            tend = selend - 1
        docstring = self.prefs.doccommentstring[self.txtDocument.filetype]
        if os.path.splitext(self.txtDocument.filename)[1] == ".lua":
            docstring = "--"

        end = self.txtDocument.GetLineEndPosition(self.txtDocument.LineFromPosition(tend))
        #End Bugfix Chris Wilson
        eol = self.txtDocument.GetEndOfLineCharacter()
        corr = 0
        l = len(self.txtDocument.GetText())
        if self.prefs.doccommentmode == 0:
            self.txtDocument.SetSelection(start, end)
            text = docstring + self.txtDocument.GetSelectedText()
            text = text.replace(eol, eol + docstring)
            self.txtDocument.ReplaceSelection(text)
        else:
            mask = self.txtDocument.GetModEventMask()
            self.txtDocument.SetModEventMask(0)
            wpos = start
            while wpos < end:
                ws = self.txtDocument.GetLineIndentPosition(startline)
                le = self.txtDocument.GetLineEndPosition(startline)
                if ws != le:
                    self.txtDocument.InsertText(ws, docstring)
                startline += 1
                wpos = self.txtDocument.PositionFromLine(startline)
            self.txtDocument.SetModEventMask(mask)
        corr = len(self.txtDocument.GetText()) - l
        self.txtDocument.GotoPos(oldcursorpos + corr)

    def OnUnCommentRegion(self, event):
        #franz: pos is not used
        selstart, selend = self.txtDocument.GetSelection()
        #From the start of the first line selected
        startline = self.txtDocument.LineFromPosition(selstart)
        oldcursorpos = self.txtDocument.GetCurrentPos()
        self.txtDocument.GotoLine(startline)
        start = self.txtDocument.GetCurrentPos()
        #To the end of the last line selected
        #Bugfix Chris Wilson
        #Edited by Dan (selend fix)
        if selend == selstart:
            tend = selend
        else:
            tend = selend - 1
        end = self.txtDocument.GetLineEndPosition(self.txtDocument.LineFromPosition(tend))
        #End Bugfix Chris Wilson

        mask = self.txtDocument.GetModEventMask()
        self.txtDocument.SetModEventMask(0)
        lpos = start
        newtext = ""
        l = len(self.txtDocument.GetText())

        docstring = self.prefs.doccommentstring[self.txtDocument.filetype]
        if os.path.splitext(self.txtDocument.filename)[1] == ".lua":
            docstring = "--"

        ldocstring = len(docstring)
        while lpos < end:
            lpos = self.txtDocument.PositionFromLine(startline)
            line = self.txtDocument.GetLine(startline)
            lc = line.find(docstring)
            if lc > -1:
                prestyle = self.txtDocument.GetStyleAt(lpos + lc - 1)
                style = self.txtDocument.GetStyleAt(lpos + lc)
                if self.txtDocument.filetype == 1 or os.path.splitext(self.txtDocument.filename)[1] == ".lua":
                    #if not ((not (prestyle == wx.stc.STC_C_COMMENTLINE) and not (prestyle == wx.stc.STC_C_COMMENT) and not\
                    #(prestyle == wx.stc.STC_C_COMMENTDOC)) and \
                    #((style == wx.stc.STC_C_COMMENTLINE) or (style == wx.stc.STC_C_COMMENT) or (style == wx.stc.STC_C_COMMENTDOC))):
                    if 0:
                        newtext += line
                    else:
                        newtext += line[0:lc] + line[lc+ldocstring:]
                else:
                    #if not ((not (prestyle == wx.stc.STC_P_COMMENTLINE) and not (prestyle == wx.stc.STC_P_COMMENTBLOCK))\
                    #and ((style == wx.stc.STC_P_COMMENTLINE) or (style == wx.stc.STC_P_COMMENTBLOCK))):
                    #    newtext += line
                    #else:
                    newtext += line[0:lc] + line[lc+ldocstring:]
            else:
                newtext += line
            startline += 1
            lpos = self.txtDocument.PositionFromLine(startline)
        self.txtDocument.SetModEventMask(mask)
        self.txtDocument.SetSelection(start, end)
        self.txtDocument.ReplaceSelection(newtext.rstrip(self.txtDocument.GetEndOfLineCharacter()))
        corr = len(self.txtDocument.GetText()) - l
        self.txtDocument.GotoPos(oldcursorpos + corr)

    def OnCustomizePopUpMenu(self, event):
        from drPopUpMenuDialog import drPopUpMenuDialog
        d = drPopUpMenuDialog(self)
        d.ShowModal()
        d.Destroy()

    def OnCustomizeToolBar(self, event):
        from drToolBarDialog import drToolBarDialog
        d = drToolBarDialog(self)
        d.ShowModal()
        d.Destroy()

    def OnCustomizeShortcuts(self, event):
        from drShortcutsDialog import drShortcutsDialog
        d = drShortcutsDialog(self)
        d.ShowModal()
        d.Destroy()

    def OnDedentRegion(self, event):
        #Submitted Patch:  Franz Steinhausler
        #Submitted Patch (ModEvent Mask), Franz Steinhausler
        beg, end = self.txtDocument.GetSelection()
        begline = self.txtDocument.LineFromPosition(beg)
        endline = self.txtDocument.LineFromPosition(end)

        mask = self.txtDocument.GetModEventMask()
        self.txtDocument.SetModEventMask(0)

        if begline == endline:
            #This section modified by Dan
            pos = self.txtDocument.PositionFromLine(begline)
            self.txtDocument.SetSelection(pos, pos)
            self.txtDocument.GotoPos(pos)
            self.txtDocument.BackTab()
            self.txtDocument.SetSelection(pos, self.txtDocument.GetLineEndPosition(begline))
            self.txtDocument.SetModEventMask(mask)
            return

        #Submitted Patch:  Christian Daven
        self.txtDocument.BackTab()
        self.txtDocument.SetModEventMask(mask)

    def OnEditBookmarks(self, event):
        from drBookmarksDialog import drBookmarksDialog
        d = drBookmarksDialog(self, self.datdirectory + "/bookmarks.dat")
        d.ShowModal()
        d.Destroy()
        self.bookmarksmenu.reloadBookmarks()

    def OnEditScriptMenu(self, event):
        from drScriptDialog import drScriptDialog
        d = drScriptDialog(self)
        d.ShowModal()
        d.Destroy()
        self.drscriptmenu.reloadscripts()

    def OnEditPlugin(self, event):
        plist = os.listdir(self.pluginsdirectory)

        PluginList = []

        for p in plist:
            i = p.find(".py")
            l = len(p)
            if i > -1 and (i + 3 == l):
                PluginList.append(p[:i])

        PluginList.sort()

        try:
            d = drSingleChoiceDialog(self, "Select the Plugin to Edit:", PluginList, wx.CHOICEDLG_STYLE, header="Edit Plugin")
            d.SetSize((250, 250))
            answer = d.ShowModal()
            d.Destroy()
            if answer == wx.ID_OK:
                self.EditPlugin(d.GetStringSelection())
        except:
            self.ShowMessage("Error Editing Plugin", "Edit Plugin Error")


    #for calling from plugins ord scripts
    def OnRunScript(self, lookscript):
        #print lookscript, self.drscriptmenu.scripts
        if not os.path.isabs(lookscript):
            lookscript = os.path.join(self.drscriptsdirectory, lookscript)
        if not lookscript in self.drscriptmenu.scripts:
            wx.MessageBox("'" + lookscript + "' not found", "Run DrScript", wx.ICON_EXCLAMATION)
        else:
            self.drscriptmenu.RunScript(lookscript)

    #for calling from plugins ord scripts
    def OnRunPlugin(self, lookplugin):
        if lookplugin in self.PluginShortcutFunctionNames:
            index = self.PluginShortcutFunctionNames.index(lookplugin)
            self.PluginShortcutFunctions[index](None)
        else:
            wx.MessageDialog(self, "'" + lookplugin + "' not found", "Run PluginFunction", wx.ICON_EXCLAMATION).ShowModal()

    def OnEnd(self, event):
        if self.txtPrompt.pid != -1:
            self.promptnotebook.SetPageImage(self.promptPosition, 2)
            self.UpdateMenuAndToolbar()
            wx.Process_Kill(self.txtPrompt.pid, wx.SIGKILL)
            self.txtPrompt.SetReadOnly(1)

    def OnExit(self, event):
        self.Close(False)

    def OnExpandAll(self, event):
        if self.prefs.docfolding[self.txtDocument.filetype]:
            wx.BeginBusyCursor()
            self.txtDocument.FoldAll(True)
            wx.EndBusyCursor()

    def OnFindAndComplete(self, event):
        #Submitted Patch by Martinho
        #now stops at '.' (repre)
        #re-ordered the text so the list shows the nearer completion words first.

        #Get The Current Word
        text = self.txtDocument.GetText()
        pos = self.txtDocument.GetCurrentPos()
        repre = re.compile("\(|\)|\[|\]|\{|\}|\<|\>|\.", re.IGNORECASE | re.MULTILINE)
        regex = re.compile("\w*\Z", re.IGNORECASE | re.MULTILINE)
        #franz: regexend is not used
        eol = self.txtDocument.GetEndOfLineCharacter()

        #Get the left bit
        i = text[0:pos].rfind(eol)
        if i == -1:
            i = 0
        else:
            i = i + len(eol)

        #Check for characters to stop at.
        t = re.finditer(repre, text[i:pos])
        if t is not None:
            try:
                preresult = t.next()
            except:
                preresult = None
            try:
                while t.next() is not None:
                    preresult = t.next()
            except:
                if preresult is not None:
                    t = i + preresult.start() + 1
                    #If t == pos, then you do not want to stop
                    #at the character.
                    if t <= pos:
                        i = t

        #Find Non Whitespace Characters.
        result = regex.search(text[i:pos])

        if result is None:
            start = i
        else:
            start = i + result.start()

        if (pos - start) <= 0:
            return

        #Handle special characters
        oword = text[start:pos]
        word = oword.replace('\\', "\\\\").replace('^', "\\^").replace('*', "\\*").replace('$', "\\$")
        word = word.replace('+', "\\+").replace('?', "\\?").replace('{', "\\{").replace('}', "\\}")
        word = word.replace('[', "\\[").replace(']', "\\]").replace('(', "\\(").replace(')', "\\)")
        word = word.replace('.', "\\.").replace('|', "\\|").replace('<', "\\<").replace('>', "\\>")

        #Find all matches in the document.
        findandcompleteregex = re.compile(r"\b" + word + r"\w*\b", re.MULTILINE)

        text_lines = text.split(eol)
        cl = self.txtDocument.GetCurrentLine()
        s_i = cl
        e_i = cl
        sorted_text = ""
        while (s_i>=0) or (e_i < len(text_lines)):
            if s_i>=0 :
                sorted_text += text_lines[s_i] + eol
                s_i = s_i - 1
            if e_i < len(text_lines) :
                sorted_text += text_lines[e_i] + eol
                e_i = e_i + 1

        r = findandcompleteregex.findall(sorted_text)
        r.sort()

        results = ""
        tr = []
        for item in r:
            try:
                tr.index(item)
            except:
                if not item == oword:
                    results = results + " " + item
                    tr.append(item)

        results = results.strip()

        if tr:
            try:
                self.txtDocument.AutoCompShow(len(oword), results)
            except:
                #What is this mess?
                pass

    def OnFoldAll(self, event):
        if self.prefs.docfolding[self.txtDocument.filetype]:
            wx.BeginBusyCursor()
            self.txtDocument.FoldAll(False)
            wx.EndBusyCursor()

    def OnFormatMacMode(self, event):
        wx.BeginBusyCursor()
        wx.Yield()
        self.txtDocument.SetEOLMode(wx.stc.STC_EOL_CR)
        text = self.txtDocument.GetText()
        text = self.FormatMacReTarget.sub('\r', text)
        self.txtDocument.SetText(text)
        self.txtDocument.OnModified(None)
        wx.EndBusyCursor()

    def OnFormatUnixMode(self, event):
        wx.BeginBusyCursor()
        wx.Yield()
        self.txtDocument.SetEOLMode(wx.stc.STC_EOL_LF)
        text = self.txtDocument.GetText()
        text = self.FormatUnixReTarget.sub('\n', text)
        self.txtDocument.SetText(text)
        self.txtDocument.OnModified(None)
        wx.EndBusyCursor()

    def OnFormatWinMode(self, event):
        wx.BeginBusyCursor()
        wx.Yield()
        self.txtDocument.SetEOLMode(wx.stc.STC_EOL_CRLF)
        text = self.txtDocument.GetText()
        text = self.FormatWinReTarget.sub('\r\n', text)
        self.txtDocument.SetText(text)
        self.txtDocument.OnModified(None)
        wx.EndBusyCursor()


    def CenterCurrentLine(self, linenr):
        self.txtDocument.EnsureVisible(linenr)
        #patch: [ 1366679 ] Goto Line Should Not Display At Top Of Window
        #self.txtDocument.ScrollToLine(v)
        top = linenr - self.txtDocument.LinesOnScreen()/2
        if top < 0:
            top = 0
        self.txtDocument.ScrollToLine(top)
        #self.txtDocument.GotoLine(linenr)


    def OnGoTo(self, event):
        d = wx.TextEntryDialog(self, "Go To Line Number:", "DrPython - Go To", "")
        answer = d.ShowModal()
        v = d.GetValue()
        d.Destroy()
        if answer == wx.ID_OK:
            try:
                v = int(v) - 1
                if (v >= 0) and (v < self.txtDocument.GetLineCount()):
                    self.CenterCurrentLine(v)
                    self.txtDocument.GotoLine(v)
                else:
                    self.ShowMessage("That line does not exist", "DrPython Error")
            except StandardError:
                self.ShowMessage("You must enter an integer (1, 2, 3, etc)", "DrPython Error")

    def OnGoToBlockEnd(self, event):
        drGetBlockInfo.GoToBlockEnd(self.txtDocument)

    def OnGoToBlockStart(self, event):
        drGetBlockInfo.GoToBlockStart(self.txtDocument)

    def OnGoToClassEnd(self, event):
        drGetBlockInfo.GoToBlockEnd(self.txtDocument, 'class')

    def OnGoToClassStart(self, event):
        drGetBlockInfo.GoToBlockStart(self.txtDocument, 'class')

    def OnGoToDefEnd(self, event):
        drGetBlockInfo.GoToBlockEnd(self.txtDocument, 'def')

    def OnGoToDefStart(self, event):
        drGetBlockInfo.GoToBlockStart(self.txtDocument, 'def')

    def OnIndentRegion(self, event):
        #Submitted Patch:  Franz Steinhausler
        #Submitted Patch (ModEvent Mask), Franz Steinhausler
        beg, end = self.txtDocument.GetSelection()
        begline = self.txtDocument.LineFromPosition(beg)
        endline = self.txtDocument.LineFromPosition(end)

        mask = self.txtDocument.GetModEventMask()
        self.txtDocument.SetModEventMask(0)

        if begline == endline:
            #This section modified by Dan
            pos = self.txtDocument.PositionFromLine(begline)
            self.txtDocument.SetSelection(pos, pos)
            self.txtDocument.GotoPos(pos)
            self.txtDocument.Tab()
            self.txtDocument.SetSelection(pos, self.txtDocument.GetLineEndPosition(begline))
            self.txtDocument.SetModEventMask(mask)
            return

        #Submitted Patch:  Christian Daven
        self.txtDocument.Tab()
        self.txtDocument.SetModEventMask(mask)

    def OnInsertRegEx(self, event):
        from drRegularExpressionDialog import drRegularExpressionDialog
        d = drRegularExpressionDialog(self, -1, "Insert Regular Expression", self.txtPrompt.GetSTCFocus())
        d.Show()

    def OnInsertSeparator(self, event):
        d = drSeparatorDialog(self, 'Insert Separator')
        answer = d.ShowModal()
        label = d.GetLabel()
        d.Destroy()
        if answer == wx.ID_OK:
            pos = self.txtDocument.GetCurrentPos()
            self.txtDocument.InsertText(pos, label)
            self.txtDocument.GotoPos(pos + len(label))

    def OnKeyDown(self, event):
        self.RunShortcuts(event)

        event.Skip()

    def OnLowercase(self, event):
        if self.txtPrompt.GetSTCFocus():
            self.txtPrompt.CmdKeyExecute(wx.stc.STC_CMD_LOWERCASE)
        else:
            self.txtDocument.CmdKeyExecute(wx.stc.STC_CMD_LOWERCASE)

    def OnMenuFind(self, event):
        stc = self.GetActiveSTC()
        d = drFindReplaceDialog(self, -1, "Find", stc)
        d.SetOptions(self.FindOptions)
        if stc.GetSelectionStart() < stc.GetSelectionEnd():
            d.SetFindString(stc.GetSelectedText())
        elif self.prefs.findreplaceundercursor:
            pos = stc.GetCurrentPos()
            findstring = stc.GetTextRange(stc.WordStartPosition(pos, 1), stc.WordEndPosition(pos, 1)) #word under cursor
            if not findstring:
                if self.FindHistory:
                    findstring = self.FindHistory[-1]
            d.SetFindString(findstring)
        else:
            d.SetFindString(stc.Finder.GetFindText())
        d.Show(True)

    def OnMenuFindNext(self, event):
        self.GetActiveSTC().Finder.DoFindNext()

    def OnMenuFindPrevious(self, event):
        self.GetActiveSTC().Finder.DoFindPrevious()

    def OnMenuReplace(self, event):
        stc = self.GetActiveSTC()
        d = drFindReplaceDialog(self, -1, "Replace", stc, 1)
        d.SetOptions(self.ReplaceOptions)

        if stc.GetSelectionStart() < stc.GetSelectionEnd():
            d.SetFindString(stc.GetSelectedText())

        elif self.prefs.findreplaceundercursor:
            pos = stc.GetCurrentPos()
            findstring = stc.GetTextRange(stc.WordStartPosition(pos, 1), stc.WordEndPosition(pos, 1)) #word under cursor
            if not findstring:
                if self.FindHistory:
                    findstring = DrFrame.FindHistory[-1]
            d.SetFindString(findstring)
        else:
            d.SetFindString(stc.Finder.GetFindText())
        if len(self.ReplaceHistory) > 0:
            d.txtReplaceWith.SetValue(self.ReplaceHistory[-1])

        d.Show(True)

    def OnNew(self, event):
        l = len(self.txtDocumentArray)
        unumbers = map(lambda x: x.untitlednumber, self.txtDocumentArray)
        unumbers.sort()
        x = 0
        last = 0
        while x < l:
            if unumbers[x] > 0:
                if unumbers[x] != (last + 1):
                    x = l
                else:
                    last = unumbers[x]
                    x = x + 1
            else:
                x = x + 1
        last = last + 1

        nextpage = drPanel(self.documentnotebook, self.ID_APP)
        self.txtDocumentArray.append(DrText(nextpage, self.ID_APP, self))
        nextpage.SetSTC(self.txtDocumentArray[l])
        self.documentnotebook.AddPage(nextpage, "Untitled " + str(last))
        self.txtDocumentArray[l].untitlednumber = last

        self.txtDocumentArray[l].Finder.Copy(self.txtDocument.Finder)

        self.lastprogargsArray.append("")
        self.txtDocumentArray[l].SetTargetPosition(l)
        self.txtDocument.IsActive = False
        self.txtDocument.OnModified(None)
        self.setDocumentTo(l)

        self.txtDocument.SetupPrefsDocument(1)

        self.reloaddocumentsmenu()

        self.txtDocument.SetSTCFocus(True)

        self.PPost(self.EVT_DRPY_NEW)

    def OnNewPrompt(self, event):
        l = len(self.txtPromptArray)

        nextpage = drPanel(self.promptnotebook, self.ID_APP)
        self.txtPromptArray.append(DrPrompt(nextpage, self.ID_APP, self))
        nextpage.SetSTC(self.txtPromptArray[l])
        self.promptnotebook.AddPage(nextpage, "Prompt")

        self.txtPromptArray[l].Finder.Copy(self.txtPrompt.Finder)

        self.setPromptTo(l)

        self.txtPrompt.SetupPrefsPrompt(1)

        self.txtPrompt.SetSTCFocus(True)

        self.PPost(self.EVT_DRPY_NEW_PROMPT)

    def OnOpen(self, event):
        dlg = drFileDialog.FileDialog(self, "Open", self.prefs.wildcard, MultipleSelection=True, ShowRecentFiles=True)
        if self.ddirectory:
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                #self.ShowMessage("Error Setting Default Directory To: " + self.ddirectory, "DrPython Error")
                #don't care, when next files are opened, ddirectory will be set properly.
                pass
        if dlg.ShowModal() == wx.ID_OK:
            filenames = dlg.GetPaths()
            filenames = map(lambda x: x.replace("\\", '/'), filenames)

            for fname in filenames:
                if not os.path.exists(fname):
                    if wx.MessageBox('"' + fname + '" does not exist.\Do you want to create it?',
                        "Warning", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.YES:
                        f = open(fname, "w")
                        f.close()
                    else:
                        continue
                self.OpenOrSwitchToFile(fname, encoding=dlg.GetEncoding())

        dlg.Destroy()

    def OnOpenImportedModule(self, event):
        from drOpenImportedModuleDialog import drOpenImportedModuleDialog, GetModulePath, ParseImportStatement
        text = self.txtDocument.GetText()
        importmatches = self.reimport.findall(text)
        fromimportmatches = self.refromimport.findall(text)

        modulelist = []

        rmodulelist = []
        imatchesarray = ParseImportStatement(importmatches)
        for imatch in imatchesarray:
            rmodulelist.extend(imatch)
        fmatchesarray = ParseImportStatement(fromimportmatches)
        for fmatch in fmatchesarray:
            rmodulelist.extend(fmatch)

        for mod in rmodulelist:
            modulelist.append(mod.strip(','))

        docpath = os.path.split(self.txtDocument.filename)[0]

        pathlist = []

        x = 0
        l = len(modulelist)
        while x < l:
            if modulelist.count(modulelist[x]) > 1:
                modulelist.pop(x)
                x -= 1
                l -= 1
            else:
                n, mpath = GetModulePath(docpath, modulelist[x], self.PLATFORM_IS_WIN)
                if mpath is None:
                    modulelist.pop(x)
                    x -= 1
                    l -= 1
                else:
                    pathlist.append([n, mpath])
            x = x + 1

        modulelist.sort()

        pathdictionary = dict(pathlist)

        d = drOpenImportedModuleDialog(self, modulelist)
        answer = d.ShowModal()
        d.Destroy()

        if answer == wx.ID_OK:
            selectedmodule = d.GetSelectedModule()

            modulefile = pathdictionary[selectedmodule]
            self.OpenOrSwitchToFile(modulefile)

    def OnOpenRecentFile(self, event):
        index = event.GetId() - self.recentfiles.IdBase
        self.OpenOrSwitchToFile(self.recentfiles[index])

    def OnPrefs(self, event):
        from drPrefsDialog import drPrefsDialog
        d = drPrefsDialog(self, -1, "DrPython - Preferences")
        d.ShowModal()
        d.Destroy()

    def OnPrint(self, event):
        self.Printer.Print(self.txtDocument.GetText(), self.txtDocument.filename, self.prefs.printdoclinenumbers)

    def OnPrintSetup(self, event):
        self.Printer.PrinterSetup(self)

    def OnPrintPrompt(self, event):
        self.Printer.Print(self.txtPrompt.GetText(), self.txtDocument.filename, self.prefs.printpromptlinenumbers)

    def OnProcessEnded(self, event):
        #Set the process info to the correct position in the array.
        i = 0
        epid = event.GetPid()
        try:
            i = map(lambda tprompt: tprompt.pid == epid, self.txtPromptArray).index(True)
        except:
            return

        #First, check for any leftover output.
        self.txtPromptArray[i].OnIdle(event)

        #If this is the process for the current window:
        if self.promptPosition == i:
            self.txtPrompt.process.Destroy()
            self.txtPrompt.process = None
            self.txtPrompt.pid = -1
            self.txtPrompt.SetReadOnly(1)
            self.txtPrompt.pythonintepreter = 0
            self.UpdateMenuAndToolbar()
            self.SetStatusText("", 2)
            self.promptnotebook.SetPageImage(i, 2)
        else:
            self.txtPromptArray[i].process.Destroy()
            self.txtPromptArray[i].process = None
            self.txtPromptArray[i].pid = -1
            self.txtPromptArray[i].SetReadOnly(1)
            self.txtPromptArray[i].pythonintepreter = 0
            self.promptnotebook.SetPageImage(i, 0)
        self.txtDocument.SetFocus()

    def OnPython(self, event):
        if self.prefs.defaultencoding == "cp1252":
            self.ShowMessage("Python Interpreter with encoding cp1252 not possible, otherwise the program crashes.\nPlease change the encoding in preferences for the python interpreter", "DrPython Error")
            return

        self.ExecutePython()

    def OnRedo(self, event):
        if self.txtPrompt.GetSTCFocus():
            self.txtPrompt.Redo()
        else:
            self.txtDocument.Redo()

    def OnReload(self, event, ask = True):
        if self.Ask("This will reload the current file.\nAny changes will be lost.\nAre you sure you want to do this?", "DrPython"):
            if self.txtDocument.filename:
                pos = self.txtDocument.GetCurrentPos()
                self.OpenFile(self.txtDocument.filename, False)
                self.txtDocument.SetSelection(pos,pos) #with setcurrentpos, begin of document until cursor pos are selected otherwise
        event.Skip()

    def OnRestoreFromBackup(self, event):
        if os.path.exists(self.txtDocument.filename + ".bak"):
            if self.Ask("This will restore the current file from the last backup.\nAny changes will be lost.\nAre you sure you want to do this?", "DrPython"):
                if self.txtDocument.filename:
                    old = self.txtDocument.filename
                    filename = self.txtDocument.filename + ".bak"
                    self.OpenFile(filename, False, False)
                    self.txtDocument.filename = old
                    self.txtDocument.OnModified(None)
        else:
            self.ShowMessage("No Backup File For: \"" + self.txtDocument.filename + "\"", "DrPython Error")

    def OnRun(self, event):
        #patch [ 1367222 ] Improved Run Command + HTML Browser
        if not self.txtDocument.filename:
            return
        if self.txtDocument.GetModify():
            if self.prefs.saveonrun or self.Ask("The file has been modified and must " + "be saved before it can be run.\nWould you like to save it?", "DrPython"):
                if not self.OnSave(event):
                    return
            else:
                return
        root, ext = os.path.splitext(self.txtDocument.filename)
        if self.checkiffileisHTML(self.txtDocument.filename):
            drHtmlBrowser.ShowHtmlFile(self, self.txtDocument.filename)
            return

        cdir, filen = os.path.split(self.txtDocument.filename)
        cwd = os.getcwd()
        try:
            os.chdir(cdir)
        except:
            self.ShowMessage("Error Setting current directory for Python.", "DrPython RunError")
        if self.checkiffileisPython (self.txtDocument.filename):
            largs = ""
            if (len(self.lastprogargs) > 0):
                largs = ' ' + self.lastprogargs
            if self.PLATFORM_IS_WIN:
                self.runcommand((self.pythexecw + " -u " +  self.prefs.pythonargs + ' "' +
                                 self.txtDocument.filename.replace("\\", "/") + '"' + largs),
                                 "Running " + filen, filen)
            else:
                self.runcommand((self.pythexec + " -u " +  self.prefs.pythonargs + ' "' + self.txtDocument.filename + '"'  + largs), "Running " + filen, filen)                #patch: [ 1366679 ] Goto Line Should Not Display At Top Of Window
        elif ext == ".lua":
            self.runcommand("lua " + self.txtDocument.filename, "Running " + filen, filen)
        else:
            #another extra handling for that
            pass
        os.chdir(cwd)


    def OnSave(self, event):
        if not self.txtDocument.filename:
            return self.OnSaveAs(event)
        else:
            self.SaveFile(self.docPosition)
            if self.prefs.sourcebrowserautorefreshonsave and (self.SourceBrowser is not None):
                self.SourceBrowser.Browse()
        return True

    def OnSaveAll(self, event):
        oldpos = self.docPosition

        x = 0
        if self.prefs.promptonsaveall:
            tosaveArray = []
            tosaveLabels = []
            for document in self.txtDocumentArray:
                if self.txtDocumentArray[x].GetModify():
                    tosaveArray.append(x)
                    tosaveLabels.append(self.txtDocumentArray[x].GetFilenameTitle())
                x += 1
            if not tosaveLabels:
                self.ShowMessage('No Modified Documents.', 'Save All')
                return
            d = wx.lib.dialogs.MultipleChoiceDialog(self, "Save All Modified Documents?", "Save All", tosaveLabels, size=(300, 300))
            l = len(tosaveArray)
            y = 0
            while y < l:
                d.lbox.SetSelection(y)
                y += 1
            answer = d.ShowModal()
            selections = d.GetValue()
            d.Destroy()
            if answer == wx.ID_OK:
                for selection in selections:
                    if not self.txtDocumentArray[tosaveArray[selection]].filename:
                        self.setDocumentTo(tosaveArray[selection])
                        self.OnSaveAs(None)
                    else:
                        self.SaveFile(tosaveArray[selection])
            else:
                return False
        else:
            for document in self.txtDocumentArray:
                if self.txtDocumentArray[x].GetModify():
                    if not self.txtDocumentArray[x].filename:
                        self.setDocumentTo(x)
                        self.OnSaveAs(None)
                    else:
                        self.SaveFile(x)
                x += 1

        self.setDocumentTo(oldpos)

        return True

    def OnSaveAs(self, event):
        dlg = drFileDialog.FileDialog(self, "Save File As", self.prefs.wildcard, IsASaveDialog=True)
        if self.ddirectory:
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                #franz: ddirectory
                self.ShowMessage("Error Setting Default Directory To: " + self.ddirectory, "DrPython Error")
        dlg.SetFilename(os.path.split(self.txtDocument.filename)[1])
        if dlg.ShowModal() == wx.ID_OK:
            old = self.txtDocument.filename
            if self.txtDocument.untitlednumber > 0:
                self.txtDocument.untitlednumber = -1
            self.txtDocument.filename = dlg.GetPath().replace("\\", "/")
            self.ddirectory = os.path.dirname(self.txtDocument.filename)
            if not self.SaveFile(self.docPosition, not (old == self.txtDocument.filename)):
                self.txtDocument.filename = old
                return
            self.UpdateMenuAndToolbar()

            #Highlighting
            if not self.prefs.doconlyusedefaultsyntaxhighlighting:
                if self.checkiffileisPython(self.txtDocument.filename):
                    #Python
                    self.txtDocument.filetype = 0
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_PYTHON, True)
                elif self.checkiffileisCPP(self.txtDocument.filename):
                    #C/C++
                    self.txtDocument.filetype = 1
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_CPP, True)
                elif self.checkiffileisHTML(self.txtDocument.filename):
                    #HTML
                    self.txtDocument.filetype = 2
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_HTML, True)
                elif self.checkiffileisPlainText(self.txtDocument.filename):
                    #Plain Text
                    self.txtDocument.filetype = 3
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_PLAIN_TEXT, True)
                else:
                    #Default
                    pass
                self.txtDocument.SetupPrefsDocument()

            self.recentfiles.AddFileToHistory(self.txtDocument.filename)
            self.WriteRecentFiles()

            dlg.Destroy()
            self.reloaddocumentsmenu()
            #Refreshes the tab.
            x, y = self.documentnotebook.GetSizeTuple()
            self.documentnotebook.SetSize((x+1, y+1))
            self.documentnotebook.SetSize((x, y))
        else:
            return False
        return True

    def OnSaveCopy(self, event):
        #add feature to save a copy, midtoad 2005-10-03
        dlg = drFileDialog.FileDialog(self, "Save Copy To", self.prefs.wildcard, IsASaveDialog=True)
        if self.ddirectory:
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                self.ShowMessage("Error Setting Default Directory To: " + self.ddirectory, "DrPython Error")
        dlg.SetFilename(os.path.split(self.txtDocument.filename)[1])
        if dlg.ShowModal() == wx.ID_OK:
            cfilename = dlg.GetPath().replace("\\", "/")
            self.ddirectory = os.path.dirname(cfilename)
            try:
                shutil.copyfile(self.txtDocument.filename, cfilename)
                if self.prefs.enablefeedback:
                    self.ShowMessage("Saved %s to %s" % (self.txtDocument.filename, cfilename), "Save as Copy")
            except IOError:
                self.ShowMessage("Error copying file to: " + cfilename, "DrPython Error")
        dlg.Destroy()

    def OnSavePrompt(self, event):
        dlg = drFileDialog.FileDialog(self, 'Save Prompt Text To', 'Text File (*.txt)|*.txt|All files (*)|*', IsASaveDialog=True)
        if self.ddirectory:
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                #franz: ddirectory
                self.ShowMessage("Error Setting Default Directory To: " + self.ddirectory, "DrPython Error")
        if dlg.ShowModal() == wx.ID_OK:
            pfilename = dlg.GetPath().replace("\\", "/")
            self.ddirectory = os.path.dirname(pfilename)
            try:
                ctext = drEncoding.DecodeText(self, self.txtPrompt.GetText())

                cfile = open(pfilename, 'wb')
                cfile.write(ctext)
                cfile.close()
            except:
                self.ShowMessage("Error Writing: " + pfilename, "DrPython Error")
            dlg.Destroy()

    def OnSelectAll(self, event):
        if self.txtPrompt.GetSTCFocus():
            self.txtPrompt.SelectAll()
        else:
            self.txtDocument.SelectAll()

    def OnSelectDocument(self, event):
        eid = event.GetId()
        i = eid - self.ID_DOCUMENTS_BASE
        self.documentnotebook.SetSelection(i)
        #self.documentnotebook.SetTab()

    def OnSelectDocumentFirst(self, event):
        self.documentnotebook.SetSelection(0)
        #self.documentnotebook.SetTab()

    def OnSelectDocumentLast(self, event):
        self.documentnotebook.SetSelection(self.documentnotebook.GetPageCount()-1)
        #self.documentnotebook.SetTab()

    def OnSelectDocumentNext(self, event):
        self.documentnotebook.AdvanceSelection(True)
        #self.documentnotebook.SetTab()

    def OnSelectDocumentPrevious(self, event):
        self.documentnotebook.AdvanceSelection(False)
        #self.documentnotebook.SetTab()

    def OnSetArgs(self, event):
        d = wx.TextEntryDialog(self, "Arguments:", "DrPython - Set Arguments", self.lastprogargs)
        if d.ShowModal() == wx.ID_OK:
            self.lastprogargs = d.GetValue()
            self.lastprogargsArray[self.docPosition] = self.lastprogargs
        d.Destroy()

    def OnSourceBrowserGoTo(self, event):
        drSourceBrowserGoTo.SourceBrowserGoTo(self, self.txtDocument)

    def OnSyntaxHighlightingPython(self, event):
        self.txtDocument.filetype = 0
        self.txtDocument.SetupPrefsDocument()

    def OnSyntaxHighlightingCPP(self, event):
        self.txtDocument.filetype = 1
        self.txtDocument.SetupPrefsDocument()

    def OnSyntaxHighlightingHTML(self, event):
        self.txtDocument.filetype = 2
        self.txtDocument.SetupPrefsDocument()

    def OnSyntaxHighlightingText(self, event):
        self.txtDocument.filetype = 3
        self.txtDocument.SetupPrefsDocument()

    def OnToggleFold(self, event):
        try:
            self.txtDocument.ToggleFold(self.txtDocument.GetCurrentLine())
        except:
            self.ShowMessage('Error Folding Line', 'Fold Error')

    def OnTogglePrompt(self, event):
        if self.mainpanel.PromptIsVisible:
            self.mainpanel.PromptIsVisible = False
            if self.hasToolBar:
                self.toolbar.ToggleTool(self.ID_TOGGLE_PROMPT,  False)
            self.mainpanel.OnSize(None)
            self.txtDocument.SetFocus()
        else:
            self.mainpanel.PromptIsVisible = True
            if self.hasToolBar:
                self.toolbar.ToggleTool(self.ID_TOGGLE_PROMPT,  True)
            self.mainpanel.OnSize(None)
            self.txtPrompt.SetFocus()

    def OnToggleSourceBrowser(self, event):
        if self.SourceBrowser is None:
            target, i = self.mainpanel.GetTargetNotebookPage(self.prefs.sourcebrowserpanel, 'Source Browser')
            self.SourceBrowser = drSourceBrowserPanel(target, -1, self.prefs.sourcebrowserpanel, i)
            self.mainpanel.SetPanelSize(self.prefs.sourcebrowserpanel, self.prefs.sourcebrowsersize)
            target.SetPanel(self.SourceBrowser)
            self.mainpanel.ShowPanel(self.prefs.sourcebrowserpanel, i)
        else:
            if not self.mainpanel.IsVisible(self.SourceBrowser.position, self.SourceBrowser.Index):
                self.SourceBrowser.Browse()
            self.mainpanel.TogglePanel(self.SourceBrowser.position, self.SourceBrowser.Index)

    def OnToggleViewWhiteSpace(self, event):
        if self.txtPrompt.GetSTCFocus():
            c = self.txtPrompt.GetViewWhiteSpace()
            self.txtPrompt.SetViewWhiteSpace(not c)
            if self.prefs.vieweol:
                self.txtPrompt.SetViewEOL(not c)
        else:
            c = self.txtDocument.GetViewWhiteSpace()
            self.txtDocument.SetViewWhiteSpace(not c)
            if self.prefs.vieweol:
                self.txtDocument.SetViewEOL(not c)

    def OnOpenWidgetInspector(self, evt):
        if self.prefs.debugmodus:
            # Activate the widget inspection tool
            try:
                from wx.lib.inspection import InspectionTool
            except:
                self.ShowMessage("Inspect Tool not found\nPlease check your wxPython version!", "DrPython Error")
                return

            if not InspectionTool().initialized:
                InspectionTool().Init()

            # Find a widget to be selected in the tree.  Use either the
            # one under the cursor, if any, or this frame.
            wnd = wx.FindWindowAtPointer()
            if not wnd:
                wnd = self
            InspectionTool().Show(wnd, True)
        else:
            self.ShowMessage("Please switch on debug modus in preferences menu", "DrPython Error")


    def OnToolBar(self, event):
        try:
            i = event.GetId() - self.ID_OTHER
            txt = self.ToolBarList[i]
            if txt in self.stcshortcutlist:
                pos = self.stcshortcutlist.index(txt)
                if self.txtPrompt.GetSTCFocus():
                    self.txtPrompt.CmdKeyExecute(self.txtPrompt.STCCOMMANDLIST[pos])
                else:
                    self.txtDocument.CmdKeyExecute(self.txtDocument.STCCOMMANDLIST[pos])
            else:
                if txt in self.PluginToolBarLabels:
                    pos = self.PluginToolBarLabels.index(txt)
                    self.PluginToolBarFunctions[pos](event)
        except:
            self.ShowMessage("ToolBar Action Error", "DrPython Error")

    def OnUndo(self, event):
        if self.txtPrompt.GetSTCFocus():
            self.txtPrompt.Undo()
        else:
            self.txtDocument.Undo()

    def OnUppercase(self, event):
        if self.txtPrompt.GetSTCFocus():
            self.txtPrompt.CmdKeyExecute(wx.stc.STC_CMD_UPPERCASE)
        else:
            self.txtDocument.CmdKeyExecute(wx.stc.STC_CMD_UPPERCASE)

    def OnViewAbout(self, event):
        import drAboutDialog
        drAboutDialog.Show(self, DRPY_VER)

    def OnViewHelp(self, event):
        self.ViewURLInBrowser(self.programdirectory + "/documentation/help.html")


    def OnViewInLeftPanel(self, event):
        self.viewinpaneltarget = 0

        self.ViewInPanelMenu(event)

    def OnViewInRightPanel(self, event):
        self.viewinpaneltarget = 1

        self.ViewInPanelMenu(event)

    def OnViewInTopPanel(self, event):
        self.viewinpaneltarget = 2

        self.ViewInPanelMenu(event)

    def OnViewPythonDocs(self, event):
        self.ViewURLInBrowser(self.prefs.documentationpythonlocation)

    def OnViewREHowtoDocs(self, event):
        self.ViewURLInBrowser(self.prefs.documentationrehowtolocation)

    def OnViewWxWidgetsDocs(self, event):
        self.ViewURLInBrowser(self.prefs.documentationwxwidgetslocation)

    def OnZoomIn(self, event):
        if self.txtPrompt.GetSTCFocus():
            zoom = self.txtPrompt.GetZoom()
            if zoom < 20:
                self.txtPrompt.SetZoom(zoom + 1)
        else:
            zoom = self.txtDocument.GetZoom()
            if zoom < 20:
                self.txtDocument.SetZoom(zoom + 1)

    def OnZoomOut(self, event):
        if self.txtPrompt.GetSTCFocus():
            zoom = self.txtPrompt.GetZoom()
            if zoom > -9:
                self.txtPrompt.SetZoom(zoom - 1)
        else:
            zoom = self.txtDocument.GetZoom()
            if zoom > -9:
                self.txtDocument.SetZoom(zoom - 1)

    def OpenFile(self, filename, OpenInNewTab, editrecentfiles = True, encoding='<Default Encoding>'):
        wx.BeginBusyCursor()
        self.PPost(self.EVT_DRPY_FILE_OPENING)
        filename = os.path.abspath(filename).replace("\\", '/')
        if not os.path.exists(filename):
            self.ShowMessage("Error Opening: " + filename + " (File not exist)", "DrPython Error")
            wx.EndBusyCursor()
            return
        try:
            cfile = open(filename, 'rb')
        except:
            self.ShowMessage("Error Opening: " + filename, "DrPython Error")
            wx.EndBusyCursor()
            return
        if (self.txtDocument.untitlednumber > 0) and not OpenInNewTab:
            self.txtDocument.untitlednumber = -1
        if editrecentfiles:
            self.recentfiles.AddFileToHistory(filename)
            self.WriteRecentFiles()

        if (((not (self.txtDocument.filename == filename))) and (self.txtDocument.GetModify())) or OpenInNewTab:
            self.OnNew(None)

        self.txtDocumentArray[self.docPosition].filename = filename
        self.txtDocumentArray[self.docPosition].untitlednumber = -1

        try:
            oof = cfile.read()
            if not self.prefs.doconlyusedefaultsyntaxhighlighting:
                if self.checkiffileisPython(filename):
                    #Python
                    self.txtDocument.filetype = 0
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_PYTHON, True)
                elif self.checkiffileisCPP(filename):
                    #C/C++
                    self.txtDocument.filetype = 1
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_CPP, True)
                elif self.checkiffileisHTML(filename):
                    #HTML
                    self.txtDocument.filetype = 2
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_HTML, True)
                elif self.checkiffileisPlainText(filename):
                    #Plain Text
                    self.txtDocument.filetype = 3
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_PLAIN_TEXT, True)
                else:
                    #Default
                    self.txtDocument.filetype = 3
                    self.highlightmenu.Check(self.ID_HIGHLIGHT_PLAIN_TEXT, True)
                self.txtDocument.SetupPrefsDocument()

            #Encoding

            try:
                oof, e = drEncoding.EncodeText(self, oof, encoding, True)
                self.txtDocument.SetText(oof)
                self.txtDocument.SetEncoding(e)
            except:
                self.ShowMessage('There was an error opening the document %s.' % filename, 'Open Error')
                wx.EndBusyCursor()
                self.OnClose(None)
                return

            self.txtDocument.EmptyUndoBuffer()
            self.txtDocument.SetSavePoint()
            cfile.close()

            self.txtDocument.SetupLineNumbersMargin()

            #Indentation Type:
            self.txtDocument.indentationtype = self.txtDocument.CheckIndentation()

            #Save Stat Info:
            self.txtDocument.mtime = int(os.stat(filename).st_mtime)

            self.txtDocument.SetScrollWidth(1)

            self.UpdateMenuAndToolbar()

            #Indentation
            if self.prefs.docusefileindentation:
                indentation = self.txtDocument.CheckIndentation(oof)
                if self.prefs.checkindentation:
                    if self.prefs.docusetabs[self.txtDocument.filetype]:
                        i = 1
                    else:
                        i = -1
                    if (indentation != i) and (indentation != 2):
                        answer = self.Ask((filename + ' is currently '\
                            + self.TABMESSAGE[indentation+1] +
                            ".\nWould you like to change it to the default?\nThe Default is: " +
                            self.TABMESSAGE[i+1]), "Indentation Not Default")
                        if answer:
                            indentation = i
                            if i == 1:
                                self.txtDocument.SetToTabs(self.prefs.doctabwidth[self.txtDocument.filetype])
                            else:
                                self.txtDocument.SetToSpaces(self.prefs.doctabwidth[self.txtDocument.filetype])
                if indentation == -1:
                    usetabs = False
                elif indentation == 1:
                    usetabs = True
                else:
                    usetabs = self.prefs.docusetabs[self.txtDocument.filetype]
                self.txtDocument.SetUseTabs(usetabs)
                self.txtDocument.SetupTabs(usetabs)

            #Line Endings

            self.txtDocument.lineendingsaremixed = 0

            winresult = self.relewin.search(oof)
            unixresult = self.releunix.search(oof)
            macresult = self.relemac.search(oof)

            win = winresult is not None
            unix = unixresult is not None
            mac = macresult is not None

            if (win + unix + mac) > 1:
                #Which came first, unix, mac, or win?
                first = -1
                useemode = 0
                if winresult is not None:
                    first = winresult.start()
                    useemode = 1
                if unixresult is not None:
                    if first == -1:
                        first = unixresult.start()
                    else:
                        i = unixresult.start()
                        if i < first:
                            first = i
                            useemode = 0
                if macresult is not None:
                    if first == -1:
                        first = macresult.start()
                    else:
                        i = macresult.start()
                        if i < first:
                            first = i
                            useemode = 2
                self.txtDocument.lineendingsaremixed = 1
                emodenum = useemode
            else:
                if win:
                    emodenum = 1
                elif unix:
                    emodenum = 0
                elif mac:
                    emodenum = 2
                else:
                    emodenum = self.prefs.doceolmode[self.txtDocument.filetype]
                self.txtDocument.lineendingsaremixed = 0

            dmodenum = self.prefs.doceolmode[self.txtDocument.filetype]

            if self.prefs.checkeol:
                if not emodenum == self.prefs.doceolmode[self.txtDocument.filetype]:
                    if self.txtDocument.lineendingsaremixed:
                        answer = self.Ask((filename + " is currently "+ self.FFMESSAGE[emodenum] +
                            "(Mixed).\nWould you like to change it to the default?\n(Since the file is mixed, this is highly recommended.\nThe Default is: " +
                            self.FFMESSAGE[dmodenum]), "Mixed Line Ending")
                    else:
                        answer = self.Ask((filename + " is currently " + self.FFMESSAGE[emodenum] +
                            ".\nWould you like to change it to the default?  The Default is: " +
                            self.FFMESSAGE[dmodenum]), "Line Ending")
                    if answer:
                        #Bugfix, Thanks Stephen Anderson.
                        if self.prefs.doceolmode[self.txtDocument.filetype] == 1:
                            self.OnFormatWinMode(None)
                        elif self.prefs.doceolmode[self.txtDocument.filetype] == 2:
                            self.OnFormatMacMode(None)
                        else:
                            self.OnFormatUnixMode(None)
                        self.txtDocument.lineendingsaremixed = 0
                        emodenum = dmodenum

            if emodenum == 1:
                emode = wx.stc.STC_EOL_CRLF
            elif emodenum == 2:
                emode = wx.stc.STC_EOL_CR
            else:
                emode = wx.stc.STC_EOL_LF
            self.txtDocument.SetEOLMode(emode)

            #/Line Endings

            #Scrolling
            lines = oof.split(self.txtDocument.GetEndOfLineCharacter())

            spaces = "\t".expandtabs(self.prefs.doctabwidth[self.txtDocument.filetype])

            line = ''
            length = 0
            x = 0
            for l in lines:
                if len(l) > length:
                    line = l
                    length = len(l)
                x += 1

            line = line.replace('\t', spaces) + '000'

            scrollwidth = self.txtDocument.TextWidth(wx.stc.STC_STYLE_DEFAULT, line)

            self.txtDocument.SetScrollWidth(scrollwidth)

            self.txtDocument.SetXOffset(0)
            #/End Scrolling

            self.txtDocument.OnModified(None)

            #Load SourceBrowser:
            if self.prefs.sourcebrowserisvisible:
                self.ShowSourceBrowser()

            #Refresh SourceBrowser:
            if self.SourceBrowser is not None:
                self.SourceBrowser.Browse()

            if editrecentfiles:
                self.ddirectory = os.path.dirname(filename)
        except:
            self.ShowMessage("Error Opening: " + filename + "Processing failed" , "DrPython Error")

        #The following chunk of code is an ugly way to work around a bug in wx.STC.
        #As things stand, word wrap may not update on file load.
        #This fixes the problem, by forcing drpython to reset the wx.STC instances.
        if self.prefs.docwordwrap:
            x, y = self.GetSizeTuple()
            self.SetSize((x+1, y+1))
            self.SetSize((x, y))
        #End of the chunk.

        self.reloaddocumentsmenu()

        self.PPost(self.EVT_DRPY_FILE_OPENED)

        wx.EndBusyCursor()

    def OpenOrSwitchToFile(self, filename, editRecentFiles=True, encoding='<Default Encoding>', force=False):
        filename = filename.replace("\\", "/")
        alreadyopen = self.GetAlreadyOpen()
        filename = os.path.abspath(filename)
        if filename.lower() in alreadyopen:
            self.setDocumentTo(alreadyopen.index(filename.lower()))
        else:
            if not os.path.exists(filename):
                if not force:
                    self.ShowMessage('"' + filename + '" Does Not Exist.', "File not found")
                else:
                    f = open(filename, 'w')
                    f.write("")
                    f.close()
                    self.OpenFile(filename, True, editRecentFiles, encoding)
            else:
                if len(self.txtDocument.filename) > 0 or self.txtDocument.GetModify():
                    self.OpenFile(filename, True, editRecentFiles, encoding)
                else:
                    self.OpenFile(filename, False, editRecentFiles, encoding)


    def PBind(self, eventtype, function, *args):
        self.drpyevents.append((eventtype, function, args))

    def PPost(self, eventtype):
        for evt in self.drpyevents:
            if evt[0] == eventtype:
                if evt[2]:
                    apply(evt[1], evt[2])
                else:
                    evt[1]()

    def PrintTraceback(self):
        slist = traceback.format_tb(sys.exc_info()[2])
        l = len(slist)
        if l > 0:
            x = 0
            rstring = ""
            while x < l:
                rstring = rstring + slist[x]
                x = x + 1
            tracebackstring = "Traceback (most recent call last):\n" + rstring \
            + str(sys.exc_info()[0]).lstrip("exceptions.") + ": " + str(sys.exc_info()[1])
            message = "\n\n\n" + tracebackstring
            print message

    def PUnbind(self, eventtype, function):
        x = 0
        for evt in self.drpyevents:
            if (evt[0] == eventtype) and (evt[1] == function):
                self.drpyevents.pop(x)
            else:
                x += 1

    def reloaddocumentsmenu(self):
        mnuitems = self.documentsmenu.GetMenuItems()
        for mnuitem in mnuitems:
            self.documentsmenu.Remove(mnuitem.GetId())
            #mnuitems[x].Destroy()
        self.setupdocumentsmenu()

    def RemovePluginIcon(self, name):
        toolbarfile = self.datdirectory + "/toolbar.custom.icons.dat"
        f = open(toolbarfile, 'r')
        lines = f.read().split('\n')
        f.close()
        name = "<Plugin>:" + name
        f = open(toolbarfile, 'w')
        for line in lines:
            if line:
                currentname = drPrefsFile.ExtractPreferenceFromText(line, "Name")
                if currentname != name:
                    f.write(line + '\n')
        f.close()

    def RemoveTrailingWhitespace(self, docPos):
        #only for python files?
        #if self.prefs.docremovetrailingwhitespace and self.txtDocument.filetype != 1:
        if self.prefs.docremovetrailingwhitespace[self.txtDocument.filetype]:

            # text = self.txtDocumentArray[docPos].GetText()

            #newtext, n = self.retrailingwhitespace.subn('', text)

            #patch, 23.03.2006:
            # newtext = re.sub(r"\s+[\n\r]+", lambda x: x.expand("\g<0>").lstrip(" \t\f\v"), text)

            # if newtext != text:
                # #save current line
                # curline = self.txtDocumentArray[docPos].GetCurrentLine()
                # self.txtDocumentArray[docPos].SetText(newtext)
                # #jump to saved current line
                # self.txtDocumentArray[docPos].GotoLine(curline)
                # self.SetStatusText("Removed trailing whitespaces", 2)
            # else:
                # self.SetStatusText("", 2)


            eol = self.txtDocument.GetEndOfLineCharacter()
            lines = self.txtDocument.GetText().split(eol)
            new_lines = []
            nr_lines = 0
            nr_clines = 0
            regex = re.compile('\s+' + eol, re.MULTILINE)

            for line in lines:
                nr_lines += 1
                result = regex.search(line + eol)
                if result is not None:
                    end = result.start()
                    nr_clines += 1
                    new_lines.append (line [:end])
                else:
                    new_lines.append(line)

            changed = False
            if nr_clines > 0:
            #file has trailing whitespaces
                #if answer == wx.OK:
                #if self.Ask("File %s has trailing Whitespaces\nCorrect?" % self.txtDocument.filename, "Remove trailing Whitespace")
                if 1:
                    changed = True
                    newtext = string.join(new_lines, eol)
                    #save current line
                    curline = self.txtDocument.GetCurrentLine()
                    col = self.txtDocument.GetColumn(self.txtDocument.GetCurrentPos())
                    self.txtDocument.SetText(newtext)
                    #jump to saved current line
                    self.txtDocument.GotoLine(curline)
                    newpos = self.txtDocument.GetCurrentPos() + col
                    self.txtDocument.SetSelection (newpos, newpos)
                    self.SetStatusText("Removed trailing whitespaces", 2)
            if not changed:
                self.SetStatusText("", 2)




    def runcommand(self, command, statustext = "Running Command", pagetext="Prompt", redin="", redout = "", rederr=""):
        if self.txtPrompt.pid > -1:
            self.OnNewPrompt(None)
        self.promptnotebook.SetPageText(self.promptPosition, pagetext)

        self.txtPrompt.SetReadOnly(0)
        self.txtPrompt.SetText(command + '\n')
        if not self.mainpanel.PromptIsVisible:
            self.mainpanel.PromptIsVisible = True
            self.mainpanel.OnSize(None)
        self.promptnotebook.SetPageImage(self.promptPosition, 3)
        self.txtPrompt.SetScrollWidth(1)
        self.txtPrompt.editpoint = self.txtPrompt.GetLength()
        self.txtPrompt.GotoPos(self.txtPrompt.editpoint)
        self.SetStatusText(statustext, 2)
        self.txtPrompt.process = wx.Process(self)
        self.txtPrompt.process.Redirect()
        if self.PLATFORM_IS_WIN:
            self.txtPrompt.pid = wx.Execute(command, wx.EXEC_ASYNC | wx.EXEC_NOHIDE, self.txtPrompt.process)
        else:
            self.txtPrompt.pid = wx.Execute(command, wx.EXEC_ASYNC, self.txtPrompt.process)
        self.txtPrompt.inputstream = self.txtPrompt.process.GetInputStream()
        self.txtPrompt.errorstream = self.txtPrompt.process.GetErrorStream()
        self.txtPrompt.outputstream = self.txtPrompt.process.GetOutputStream()

        self.txtPrompt.process.redirectOut = redout
        self.txtPrompt.process.redirectErr = rederr

        self.UpdateMenuAndToolbar()
        self.txtPrompt.SetFocus()

    def RunShortcuts(self, event, stc = None, SplitView = 0):
        return drShortcuts.RunShortcuts(self, event, stc, SplitView)

    def LoadDialogSizeAndPosition(self, dialog, dialogfile, defaultdir=''):
        if self.prefs.rememberdialogsizesandpositions:
            if not defaultdir:
                defaultdir = self.datdirectory
            sizeposfile = defaultdir + '/' + dialogfile
            try:
                if os.path.exists(sizeposfile):
                    f = open(sizeposfile, 'rb')
                    text = f.read()
                    f.close()
                    x, y, px, py = map(int, text.split('\n'))
                    dialog.SetSize((x, y))
                    dialog.Move(wx.Point(px, py))
            except:
                drScrolledMessageDialog.ShowMessage(dialog, 'Error Loading Dialog Size.  The file: "%s" may be corrupt.'\
                                                    % sizeposfile, 'Error')
        dialog.Bind(wx.EVT_CLOSE, dialog.OnCloseW)


    def SaveDialogSizeAndPosition(self, dialog, dialogfile, defaultdir=''):
        if self.prefs.rememberdialogsizesandpositions:
            try:
                if not defaultdir:
                    defaultdir = self.datdirectory
                f = open(defaultdir + '/' + dialogfile, 'wb')
                x, y = dialog.GetSizeTuple()
                px, py = dialog.GetPositionTuple()
                f.write(str(x) + '\n' + str(y) + '\n' + str(px) + '\n' + str(py))
                f.close()
            except:
                drScrolledMessageDialog.ShowMessage(dialog, "Error Saving Dialog Size", 'Error')

    def SaveFile(self, docPos, IsSaveAs = False, encoding='FromText'):
        self.PPost(self.EVT_DRPY_FILE_SAVING)
        #Submitted Write Access Patch.
        #Edited slightly by Dan (one if statement, string format).
        if (not os.access(self.txtDocumentArray[docPos].filename, os.W_OK)) and \
            (os.path.exists(self.txtDocumentArray[docPos].filename)):
              if not self.PLATFORM_IS_GTK: #because try for gtk below
                  self.ShowMessage('Error: Write Access: "%s"' % (self.txtDocumentArray[docPos].filename), 'Save Error')
                  return False
        try:
            if self.prefs.backupfileonsave and not IsSaveAs:
                try:
                    shutil.copyfile(self.txtDocumentArray[docPos].filename, self.txtDocumentArray[docPos].filename+".bak")
                except:
                    self.ShowMessage("Error Backing up to: " + self.txtDocumentArray[docPos].filename + ".bak", "DrPython Error")

            if encoding == 'FromText':
                encoding = self.txtDocumentArray[docPos].GetEncoding()

            self.RemoveTrailingWhitespace(docPos)

            ctext = drEncoding.DecodeText(self, self.txtDocumentArray[docPos].GetText(), encoding)

            #gtk and root file stuff
            alreadysaved = False
            if self.PLATFORM_IS_GTK:
              if (not os.access(self.txtDocumentArray[docPos].filename, os.W_OK)) and \
                  (os.path.exists(self.txtDocumentArray[docPos].filename)):
                  answer = self.DrMessageBox("Maybe this file: '" + self.txtDocumentArray[docPos].filename + \
                           "' is a file with root rights\nDo you want to try to save it as root file?",
                          "Cannot save file", wx.YES_NO | wx.ICON_QUESTION)
                  #self.ShowMessage("Error Writing: " + self.txtDocumentArray[docPos].filename, "DrPython Error")
                  if answer == wx.YES:
                      savetmpfile = os.path.join(os.path.expanduser('~'), "savetmpfile.tmp")
                      tmpfile = open(savetmpfile, 'wb')
                      tmpfile.write(ctext)
                      tmpfile.close()

                      drSaveRootFile = os.path.join(self.programdirectory, "drSaveRootFile.py")
                      backupfile = self.prefs.backupfileonsave and not IsSaveAs
                      retvalue = os.system("gksudo python %s %s %s %d" % (drSaveRootFile, self.txtDocumentArray[docPos].filename, savetmpfile, backupfile))
                      #print retvalue 0... success, otherwise the passwd was wrong (retvalue 768) or (cancel retvalue 256)
                      #a) return value didn't work b) environment variable also not => so 3) simply ask, if file is still there, so the success can be discovered
                      if not os.path.exists(savetmpfile): #success opened the possibilty to save that file
                          alreadysaved = True
                      else:
                        #wx.MessageBox("tmpfile still existed, there must be some problems, deleting herewith", "Info")
                        if retvalue != 0:
                            #wx.MessageBox("The file was not saved (if the reason was not a wrong passwd, there must be some problems), deleting herewith", "Info")
                            wx.MessageBox("The file was not saved, there must be some problems, deleting herewith", "Info")
                        os.remove(savetmpfile)

                  if not alreadysaved:
                      #answer = wx.MessageBox("Root file was not saved (return)", "Info")
                      return

            if not alreadysaved:
                cfile = open(self.txtDocumentArray[docPos].filename, 'wb')
                cfile.write(ctext)
                cfile.close()

            #Save Stat Info:
            self.txtDocumentArray[docPos].mtime = int(os.stat(self.txtDocumentArray[docPos].filename).st_mtime)
        except:
            self.ShowMessage("Error Writing: " + self.txtDocumentArray[docPos].filename, "DrPython Error")
            return False

        self.txtDocumentArray[docPos].SetSavePoint()
        self.txtDocumentArray[docPos].OnModified(None)

        if self.prefs.checksyntaxonsave:
            if self.prefs.checksyntaxextensions:
                exts = self.prefs.checksyntaxextensions.split()
                cext = os.path.splitext(self.txtDocumentArray[docPos].filename)[1][1:]
                if cext in exts:
                    self.CheckSyntax(docPos)
            else:
                self.CheckSyntax(docPos)

        self.PPost(self.EVT_DRPY_FILE_SAVED)

        return True

    def setDocumentTo(self, number, ignoreold = 0):
        if not ignoreold:
            self.lastprogargsArray[self.docPosition] = self.lastprogargs
        #copy old finder limodou 2004/04/19
        oldfinder = self.txtDocumentArray[self.docPosition].Finder
        #end limodou

        #save show eol and whitespace state
        try:
            prev_vieweol = self.txtDocument.GetViewEOL()
            prev_viewwhitespace = self.txtDocument.GetViewWhiteSpace()
        except:
            prev_vieweol = False
            prev_viewwhitespace = False


        self.docPosition = number
        self.txtDocument = self.txtDocumentArray[self.docPosition]

        #set from prev eol and whitespace state
        #flicker
        if self.txtDocument.GetViewEOL() != prev_vieweol:
            self.txtDocument.SetViewEOL(prev_vieweol)
        self.txtDocument.SetViewWhiteSpace(prev_viewwhitespace)

        #copy old finder limodou 2004/04/19
        self.txtDocument.Finder.Copy(oldfinder)
        #end limodou

        self.lastprogargs = self.lastprogargsArray[self.docPosition]

        self.currentpage = self.documentnotebook.GetPage(number)

        if self.txtDocument.filename:
            self.ddirectory = os.path.split(self.txtDocument.filename)[0]

        #franz: (Bad Argument).
        self.updatePrefsMDI()

        #Syntax Highlighting
        if self.txtDocument.filetype == 0:
            self.highlightmenu.Check(self.ID_HIGHLIGHT_PYTHON, True)
        if self.txtDocument.filetype == 1:
            self.highlightmenu.Check(self.ID_HIGHLIGHT_CPP, True)
        if self.txtDocument.filetype == 2:
            self.highlightmenu.Check(self.ID_HIGHLIGHT_HTML, True)
        if self.txtDocument.filetype == 3:
            #comment limodou 2004/04/13
            self.highlightmenu.Check(self.ID_HIGHLIGHT_PLAIN_TEXT, True)
            #end limodou

        if not self.txtDocument.filename:
            title = "DrPython - Untitled " + str(self.txtDocument.untitlednumber)
        else:
            title = "DrPython - " + self.txtDocument.filename
        if self.txtDocument.GetModify():
            title += '[Modified]'
        if self.disableeventhandling:
            self.SetTitle(title)

        self.txtDocument.IsActive = True
        self.txtDocument.targetPosition = number
        self.txtDocument.OnModified(None)

        self.documentnotebook.SetSelection(self.docPosition)

        self.txtDocument.SetFocus()

        self.PPost(self.EVT_DRPY_DOCUMENT_CHANGED)

    def setPromptTo(self, number):
        oldfinder = self.txtPromptArray[self.promptPosition].Finder

        self.promptPosition = number
        self.txtPrompt = self.txtPromptArray[self.promptPosition]

        self.txtPrompt.Finder.Copy(oldfinder)

        self.currentprompt = self.promptnotebook.GetPage(number)

        #franz: (Bad Argument).
        self.updatePrefsPromptMDI()

        if self.txtPromptArray[self.promptPosition].pid != -1:
            if self.txtPrompt.pythonintepreter:
                self.SetStatusText("Running Python Interpreter", 2)
            else:
                self.SetStatusText(("Running " + os.path.split(self.txtDocument.filename)[1]), 2)
        else:
            self.SetStatusText("", 2)

        self.promptnotebook.SetSelection(self.promptPosition)

    def setupdocumentsmenu(self):
        self.tabnavmenu = drMenu(self)
        self.tabnavmenu.Append(self.ID_NEXT_DOCUMENT, "Next Document")
        self.tabnavmenu.Append(self.ID_PREVIOUS_DOCUMENT, "Previous Document")
        self.tabnavmenu.Append(self.ID_FIRST_DOCUMENT, "First Document")
        self.tabnavmenu.Append(self.ID_LAST_DOCUMENT, "Last Document")
        self.documentsmenu.AppendMenu(self.ID_DOCUMENT_NAVIGATION_MENU, "Navigation", self.tabnavmenu)
        self.documentsmenu.AppendSeparator()
        self.documentsmenu.Append(self.ID_SAVE_ALL, "Save All Documents")
        self.documentsmenu.AppendSeparator()
        self.documentsmenu.Append(self.ID_CLOSE_ALL, "Close &All Documents")
        self.documentsmenu.Append(self.ID_CLOSE_ALL_OTHER_DOCUMENTS, "Close All &Other Documents")
        self.documentsmenu.AppendSeparator()

        #Sort it first
        def _get_title(x):
            return x.GetFilenameTitle()
        def _x(x):
            return x

        indextitles = map(_get_title, self.txtDocumentArray)
        sortedtitles = map(_x, indextitles)

        sortedtitles.sort()

        #End Sort

        x = 0
        l = len(self.txtDocumentArray)
        if l > 10:
            y = 0
            yl = 10
            if yl > l:
                yl = l
            a = 0
            self.documentsubmenus = []
            while y < yl:
                self.documentsubmenus.append(wx.Menu())
                self.documentsmenu.AppendMenu(self.ID_DOCUMENTS_MENU_BASE+a, sortedtitles[y] + " - " + sortedtitles[yl-1], self.documentsubmenus[a])
                while x < yl:
                    i = indextitles.index(sortedtitles[x])
                    self.documentsubmenus[a].Append(self.ID_DOCUMENTS_BASE+i, sortedtitles[x])
                    self.Bind(wx.EVT_MENU, self.OnSelectDocument, id=self.ID_DOCUMENTS_BASE+i)
                    x = x + 1
                if y == l:
                    break
                y = y + 10
                yl = yl + 10
                a = a + 1
                if yl > l:
                    yl = l
        else:
            while x < l:
                i = indextitles.index(sortedtitles[x])
                self.documentsmenu.Append(self.ID_DOCUMENTS_BASE+i, sortedtitles[x])
                self.Bind(wx.EVT_MENU, self.OnSelectDocument, id=self.ID_DOCUMENTS_BASE+i)
                x = x + 1

    def setupfiletypeextensions(self):

        self.refiletypeiscpp = re.compile(self.getfileextensionstring(1), re.IGNORECASE)
        self.refiletypeishtml = re.compile(self.getfileextensionstring(2), re.IGNORECASE)
        self.refiletypeistxt = re.compile(self.getfileextensionstring(3), re.IGNORECASE)
        self.refiletypeispy = re.compile(self.getfileextensionstring(0), re.IGNORECASE)

    def SetupToolBar(self):
        return drToolBarFile.SetupToolBar(self)

    def ShowMessage(self, msg, title='DrPython'):
        drScrolledMessageDialog.ShowMessage(self, msg, title)

    def ShowSourceBrowser(self):
        if self.SourceBrowser is None:
            target, i = self.mainpanel.GetTargetNotebookPage(self.prefs.sourcebrowserpanel, 'Source Browser')
            self.SourceBrowser = drSourceBrowserPanel(target, -1, self.prefs.sourcebrowserpanel, i)
            self.mainpanel.SetPanelSize(self.prefs.sourcebrowserpanel, self.prefs.sourcebrowsersize)
            target.SetPanel(self.SourceBrowser)
            self.mainpanel.ShowPanel(self.prefs.sourcebrowserpanel, i)
        else:
            self.SourceBrowser.Browse()
            self.mainpanel.ShowPanel(self.SourceBrowser.position, self.SourceBrowser.Index, True)
        self.txtDocument.SetFocus()


    def ShowPrompt(self, Visible = True):
        if Visible:
            if self.mainpanel.PromptIsVisible:
                return
            self.mainpanel.PromptIsVisible = True
            if self.hasToolBar:
                self.toolbar.ToggleTool(self.ID_TOGGLE_PROMPT,  True)
            self.mainpanel.OnSize(None)
            self.txtPrompt.SetFocus()
        else:
            if not self.mainpanel.PromptIsVisible:
                return
            self.mainpanel.PromptIsVisible = False
            if self.hasToolBar:
                self.toolbar.ToggleTool(self.ID_TOGGLE_PROMPT,  False)
            self.mainpanel.OnSize(None)
            self.txtDocument.SetFocus()

    def UpdateMenuAndToolbar(self):
        isrunning = self.txtPrompt.pid != -1
        thereisafile = len(self.txtDocument.filename) > 0

        #Toolbar
        if self.hasToolBar:
            self.toolbar.EnableTool(self.ID_RELOAD, thereisafile)

            self.toolbar.EnableTool(self.ID_END, isrunning)

        #Menus
        self.filemenu.Enable(self.ID_RELOAD, thereisafile)
        self.filemenu.Enable(self.ID_RESTORE_FROM_BACKUP, thereisafile)

        if not isrunning:
            self.programmenu.Enable(self.ID_PYTHON, True)
            self.programmenu.Enable(self.ID_END, False)
            self.programmenu.Enable(self.ID_RUN, thereisafile)
        else:
            self.programmenu.Enable(self.ID_PYTHON, False)
            self.programmenu.Enable(self.ID_END, True)
            if thereisafile:
                self.programmenu.Enable(self.ID_RUN, False)

    #franz: oldprefs not used.
    def updatePrefsMDI(self):
        #Determine What is showing
        self.mainpanel.OnSize(None)

        self.Layout()

        self.UpdateMenuAndToolbar()

        #Shortcuts
        self.STCKeycodeArray = drShortcuts.SetSTCShortcuts(self.txtDocument, self.STCShortcuts, self.STCUseDefault)

    def updatePrefsPromptMDI(self):
        #Determine What is showing
        self.currentprompt.OnSize(None)

        self.Layout()

        self.UpdateMenuAndToolbar()

        #Shortcuts
        drShortcuts.SetSTCShortcuts(self.txtPrompt, self.STCShortcuts, self.STCUseDefault)

    def updatePrefs(self, oldprefs):
        #self.bSizer.Remove(self.mainpanel)

        #Styling:
        for prompt in self.txtPromptArray:
            prompt.StyleResetDefault()
            prompt.StyleClearAll()
            prompt.SetupPrefsPrompt(0)

        for document in self.txtDocumentArray:
            document.StyleResetDefault()
            document.StyleClearAll()
            document.SetupPrefsDocument(0)

        self.mainpanel.OnSize(None)

        self.setupfiletypeextensions()

        #Find/Replace:
        if  (self.prefs.findreplaceregularexpression != oldprefs.findreplaceregularexpression) or \
        (self.prefs.findreplacematchcase != oldprefs.findreplacematchcase) or \
        (self.prefs.findreplacefindbackwards != oldprefs.findreplacefindbackwards) or \
        (self.prefs.findreplacewholeword != oldprefs.findreplacewholeword) or \
        (self.prefs.findreplaceinselection != oldprefs.findreplaceinselection) or \
        (self.prefs.findreplacefromcursor != oldprefs.findreplacefromcursor) or \
        (self.prefs.findreplacepromptonreplace != oldprefs.findreplacepromptonreplace):
            self.FindOptions = []
            self.ReplaceOptions = []

#       #SourceBrowser:
#       if not (self.prefs.sourcebrowserpanel == oldprefs.sourcebrowserpanel):
#           for document in self.txtDocumentArray:
#               if document.SourceBrowser:
#                   document.SourceBrowser = None

        #DrScript:
        if self.prefs.drscriptloadexamples != oldprefs.drscriptloadexamples:
            self.drscriptmenu.reloadscripts()

        #Toolbar
        if self.prefs.iconsize > 0:
            if self.hasToolBar:
                self.DestroyToolBar()
                self.SetToolBar(None)
            self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
            self.ToolBarIdList = self.SetupToolBar()
            self.SetToolBar(self.toolbar)
            self.hasToolBar = 1
        else:
            if self.hasToolBar:
                self.DestroyToolBar()
                self.SetToolBar(None)
                self.hasToolBar = 0

        #Styling:
        self.txtDocument.StyleResetDefault()
        self.txtDocument.StyleClearAll()

        self.txtPrompt.StyleResetDefault()
        self.txtPrompt.StyleClearAll()

        self.txtDocument.SetupPrefsDocument(0)
        if self.txtDocument.GetViewWhiteSpace():
            self.txtDocument.SetViewEOL(self.prefs.vieweol)
        self.txtPrompt.SetupPrefsPrompt(0)
        if self.txtPrompt.GetViewWhiteSpace():
            self.txtPrompt.SetViewEOL(self.prefs.vieweol)

        if oldprefs.docfolding[self.txtDocument.filetype]:
            if not self.prefs.docfolding[self.txtDocument.filetype]:
                self.txtDocument.FoldAll(True)

        #Add The Stuff to the Sizer

        #self.bSizer.Add(self.mainpanel, 1, wx.EXPAND)

        self.txtDocument.OnModified(None)
        self.txtDocument.OnPositionChanged(None)

        #Parenthesis Matching:
        if oldprefs.docparenthesismatching != self.prefs.docparenthesismatching:
            if not self.prefs.docparenthesismatching:
                #Clear Parenthesis Highlighting
                self.txtDocument.BraceBadLight(wx.stc.STC_INVALID_POSITION)
                self.txtDocument.BraceHighlight(wx.stc.STC_INVALID_POSITION, wx.stc.STC_INVALID_POSITION)

        self.Layout()

    def ViewInPanel(self, event):
        docnumber = event.GetId() - self.ID_VIEW_IN_PANEL_BASE

        target, i = self.mainpanel.GetTargetNotebookPage(self.viewinpaneltarget, "View In Panel")
        if docnumber < 0:
            drsplit = drSplitTextPanel(target, self, self.txtDocumentArray[self.docPosition], self.viewinpaneltarget, i)
        else:
            drsplit = drSplitTextPanel(target, self, self.txtDocumentArray[docnumber], self.viewinpaneltarget, i)
        target.SetPanel(drsplit)
        self.mainpanel.ShowPanel(self.viewinpaneltarget, i)

    def ViewInPanelMenu(self, event):
        docMenu = wx.Menu()
        x = 0
        l = len(self.txtDocumentArray)
        docMenu.Append(self.ID_VIEW_IN_PANEL_BASE-1, "Current Document")
        self.Bind(wx.EVT_MENU, self.ViewInPanel, id=self.ID_VIEW_IN_PANEL_BASE-1)
        docMenu.AppendSeparator()
        if l > 10:
            y = 0
            yl = 10
            if yl > l:
                yl = l
            a = 0
            docSubMenus = []
            while y < yl:
                docSubMenus.append(wx.Menu())
                docMenu.AppendMenu(self.ID_VIEW_IN_PANEL_BASE+a, str(y+1) + " - " + str(yl), docSubMenus[a])
                while x < yl:
                    if self.txtDocumentArray[x].filename:
                        docSubMenus[a].Append(self.ID_VIEW_IN_PANEL_BASE+x, os.path.basename(self.txtDocumentArray[x].filename))
                    else:
                        docSubMenus[a].Append(self.ID_VIEW_IN_PANEL_BASE+x, "Untitled " + str(self.txtDocumentArray[x].untitlednumber))
                    self.Bind(wx.EVT_MENU, self.ViewInPanel, id=self.ID_VIEW_IN_PANEL_BASE+x)
                    x = x + 1
                if y == l:
                    break
                y = y + 10
                yl = yl + 10
                a = a + 1
                if yl > l:
                    yl = l
        else:
            while x < l:
                if self.txtDocumentArray[x].filename:
                    docMenu.Append(self.ID_VIEW_IN_PANEL_BASE+x, os.path.basename(self.txtDocumentArray[x].filename))
                else:
                    docMenu.Append(self.ID_VIEW_IN_PANEL_BASE+x, "Untitled " + str(self.txtDocumentArray[x].untitlednumber))
                self.Bind(wx.EVT_MENU, self.ViewInPanel, id=self.ID_VIEW_IN_PANEL_BASE+x)
                x = x + 1

        self.PopupMenu(docMenu, self.ScreenToClient(wx.GetMousePosition()))
        docMenu.Destroy()

    def ViewURLInBrowser(self, url):
        if url.find('http:') == -1:
            url = os.path.normpath(url)
        if self.prefs.documentationbrowser == '<os.startfile>' and self.PLATFORM_IS_WIN:
            os.startfile(url)
            return
        wx.Execute((self.prefs.documentationbrowser + ' "' + url + '"'), wx.EXEC_ASYNC)

    def WriteRecentFiles(self):
        filename = self.datdirectory + "/recent_files.log"
        try:
            self.recentfiles.SaveToFile(filename)
        except IOError:
            self.ShowMessage("Error Writing: " + filename, "Recent Files Error")

    #Initialize menus for Advanced mode (more items)
    def CreateMenus(self):
        self.filemenu = drMenu(self)
        self.filemenu.Append(self.ID_NEW, 'New', False, 0)
        self.filemenu.Append(self.ID_OPEN, 'Open', True, 0)
        self.filemenu.Append(self.ID_OPEN_IMPORTED_MODULE, 'Open Imported Module', True)
        self.recentmenu = self.CreateRecentFileMenu()
        self.filemenu.AppendMenu(self.ID_OPEN_RECENT, "Op&en Recent", self.recentmenu)
        self.filemenu.Append(self.ID_RELOAD, 'Reload File', False, 0)
        self.filemenu.Append(self.ID_RESTORE_FROM_BACKUP, 'Restore From Backup')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.ID_CLOSE, 'Close', False, 0)
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.ID_CLEAR_RECENT, 'Clear Recent File List')
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.ID_SAVE, 'Save', False, 0)
        self.filemenu.Append(self.ID_SAVE_AS, 'Save As', True, 5)
        self.filemenu.Append(self.ID_SAVE_COPY, 'Save A Copy', True, 2)
        self.filemenu.Append(self.ID_SAVE_PROMPT, 'Save Prompt Output To File', True)
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.ID_PRINT_SETUP, 'Print Setup', True)
        self.filemenu.Append(self.ID_PRINT, 'Print File', True, 0)
        self.filemenu.Append(self.ID_PRINTPROMPT, 'Print Prompt', True)
        self.filemenu.AppendSeparator()
        self.filemenu.Append(self.ID_EXIT, 'Exit', False, 1)

        self.commentmenu = drMenu(self)
        self.commentmenu.Append(self.ID_COMMENT_REGION, 'Comment')
        self.commentmenu.Append(self.ID_UNCOMMENT_REGION, 'UnComment')

        self.whitespacemenu = drMenu(self)
        self.whitespacemenu.Append(self.ID_INDENT_REGION, 'Indent', False, 0)
        self.whitespacemenu.Append(self.ID_DEDENT_REGION, 'Dedent', False, 0)
        self.whitespacemenu.AppendSeparator()
        self.whitespacemenu.Append(self.ID_CHECK_INDENTATION, "Check Indentation Type...")
        self.whitespacemenu.Append(self.ID_CLEAN_UP_TABS, "Set Indentation To Tabs...")
        self.whitespacemenu.Append(self.ID_CLEAN_UP_SPACES, "Set Indentation To Spaces...")
        self.whitespacemenu.AppendSeparator()
        self.whitespacemenu.Append(self.ID_UNIXMODE, "Set Line Endings To Unix Mode (\"\\n\')")
        self.whitespacemenu.Append(self.ID_WINMODE, "Set Line Endings To DOS/Windows Mode (\"\\r\\n\')")
        self.whitespacemenu.Append(self.ID_MACMODE, "Set Line Endings To Mac Mode (\"\\r\')")

        self.casemenu = drMenu(self)
        self.casemenu.Append(self.ID_UPPERCASE, 'Uppercase', False, 0)
        self.casemenu.Append(self.ID_LOWERCASE, 'Lowercase', False, 0)

        self.editmenu = drMenu(self)

        self.editmenu.Append(self.ID_UNDO, 'Undo', False, 0)
        self.editmenu.Append(self.ID_REDO, 'Redo', False, 1)
        self.editmenu.AppendSeparator()

        #Order changed by drpython
        ##for keyboard macro (Keyboardmacro) recording; #ugly hack franz # removed again

        self.editmenu.Append(self.ID_CUT, 'Cut')
        self.editmenu.Append(self.ID_COPY, 'Copy')
        self.editmenu.Append(self.ID_PASTE, 'Paste')
        ##end patch keyboard macro recording #end ugly hack franz # removed again

        self.editmenu.Append(self.ID_DELETE, 'Delete')

        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.ID_SELECT_ALL, 'Select All')
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.ID_INSERT_SEPARATOR, 'Insert Separator', True)
        self.editmenu.Append(self.ID_INSERT_REGEX, 'Insert Regular Expression', True)
        self.editmenu.AppendSeparator()
        self.editmenu.Append(self.ID_FIND_AND_COMPLETE, 'Find And Complete')
        self.editmenu.AppendSeparator()
        self.editmenu.AppendMenu(self.ID_COMMENT, "&Comments", self.commentmenu)
        self.editmenu.AppendMenu(self.ID_WHITESPACE, "&Whitespace", self.whitespacemenu)
        self.editmenu.AppendMenu(self.ID_CASE, "Case", self.casemenu)

        self.searchmenu = drMenu(self)
        self.searchmenu.Append(self.ID_FIND, 'Find', True, 0)
        self.searchmenu.Append(self.ID_FIND_NEXT, 'Find Next', False, 5)
        self.searchmenu.Append(self.ID_FIND_PREVIOUS, 'Find Previous')
        self.searchmenu.Append(self.ID_REPLACE, 'Replace', True, 0)

        self.foldmenu = drMenu(self)
        self.foldmenu.Append(self.ID_TOGGLE_FOLD, 'Toggle Fold', False, 0)
        self.foldmenu.Append(self.ID_FOLD_ALL, 'Fold All', False, 0)
        self.foldmenu.Append(self.ID_EXPAND_ALL, 'Expand All', False, 0)

        self.highlightmenu = drMenu(self)
        self.highlightmenu.AppendRadioItem(self.ID_HIGHLIGHT_PYTHON, "Python")
        self.highlightmenu.AppendRadioItem(self.ID_HIGHLIGHT_CPP, "C/C++")
        self.highlightmenu.AppendRadioItem(self.ID_HIGHLIGHT_HTML, "HTML")
        self.highlightmenu.AppendRadioItem(self.ID_HIGHLIGHT_PLAIN_TEXT, "Plain Text")
        self.highlightmenu.Check(self.ID_HIGHLIGHT_PYTHON, True)

        self.viewinpanelmenu = drMenu(self)
        self.viewinpanelmenu.Append(self.ID_VIEW_IN_LEFT_PANEL, 'View In Left Panel')
        self.viewinpanelmenu.Append(self.ID_VIEW_IN_RIGHT_PANEL, 'View In Right Panel')
        self.viewinpanelmenu.Append(self.ID_VIEW_IN_TOP_PANEL, 'View In Top Panel')

        self.gotomenu = drMenu(self)
        self.gotomenu.Append(self.ID_GOTO_BLOCK_START, 'Go To Block Start', False, -1, 'Block Start')
        self.gotomenu.Append(self.ID_GOTO_BLOCK_END, 'Go To Block End', False, -1, 'Block End')
        self.gotomenu.Append(self.ID_GOTO_CLASS_START, 'Go To Class Start', False, -1, 'Class Start')
        self.gotomenu.Append(self.ID_GOTO_CLASS_END, 'Go To Class End', False, -1, 'Class End')
        self.gotomenu.Append(self.ID_GOTO_DEF_START, 'Go To Def Start', False, -1, 'Def Start')
        self.gotomenu.Append(self.ID_GOTO_DEF_END, 'Go To Def End', False, -1, 'Def End')

        self.viewmenu = drMenu(self)
        self.viewmenu.Append(self.ID_GOTO, 'Go To', True, 0)
        self.viewmenu.AppendMenu(self.ID_GOTO_MENU, "Go To", self.gotomenu)
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(self.ID_ZOOM_IN, 'Zoom In', False, 5)
        self.viewmenu.Append(self.ID_ZOOM_OUT, 'Zoom Out', False, 5)
        self.viewmenu.AppendSeparator()
        self.viewmenu.AppendMenu(self.ID_FOLDING, "&Folding", self.foldmenu)
        self.viewmenu.AppendSeparator()
        self.viewmenu.AppendMenu(self.ID_VIEW_IN_PANEL, "&View In Panel", self.viewinpanelmenu)
        self.viewmenu.AppendSeparator()
        self.viewmenu.AppendMenu(self.ID_HIGHLIGHT, "&Syntax Highlighting", self.highlightmenu)
        self.viewmenu.AppendSeparator()
        self.viewmenu.Append(self.ID_TOGGLE_SOURCEBROWSER, 'Toggle Source Browser')
        self.viewmenu.Append(self.ID_SOURCEBROWSER_GOTO, 'Source Browser Go To', True)
        self.viewmenu.AppendSeparator()
        #fix bug someone refered in forum limodou 2004/04/20
        self.viewmenu.Append(self.ID_TOGGLE_VIEWWHITESPACE, 'Toggle View Whitespace', False, 12)
        #end limodou
        self.viewmenu.Append(self.ID_TOGGLE_PROMPT, 'Toggle Prompt')

        self.programmenu = drMenu(self)
        self.programmenu.Append(self.ID_CHECK_SYNTAX, 'Check Syntax')
        self.programmenu.AppendSeparator()
        self.programmenu.Append(self.ID_RUN, 'Run')
        self.programmenu.Append(self.ID_SET_ARGS, 'Set Arguments', True)
        self.programmenu.Append(self.ID_PYTHON, 'Python', False, -1, 'Open a Python Interpreter')
        self.programmenu.Append(self.ID_END, 'End')
        self.programmenu.Append(self.ID_CLOSE_PROMPT, 'Close Prompt')
        # Feb 17 - adding PyDoc menu items
        self.programmenu.AppendSeparator()
        self.programmenu.Append(self.ID_PYDOC_CURR, self.getmenulabel('Pydoc Current File'))
        self.programmenu.Append(self.ID_PYDOC_ALL, self.getmenulabel('Pydoc All Open Files'))
        self.programmenu.Append(self.ID_VIEW_PYDOC, self.getmenulabel('Browse PyDoc...'))
        # End Pydoc changes

        self.bookmarksmenu = drBookmarksMenu(self)
        self.drscriptmenu = drScriptMenu(self)

        self.txtDocument.OnModified(None)

        #DrScript Shortcuts
        self.DrScriptShortcutsAction = self.drscriptmenu.OnScript

        self.pluginsconfiguremenu = drPluginConfigureMenu(self)
        self.pluginsindexmenu = drPluginIndexMenu(self)
        self.pluginsprefsmenu = drPluginPreferencesMenu(self)

        self.documentsmenu = drMenu(self)
        self.setupdocumentsmenu()

        self.optionsmenu = drMenu(self)
        self.optionsmenu.Append(self.ID_PREFS, 'Preferences', True, 0)
        self.optionsmenu.Append(self.ID_SHORTCUTS, 'Customize Shortcuts', True, 0)
        self.optionsmenu.Append(self.ID_POPUP, 'Customize Pop Up Menu', True)
        self.optionsmenu.Append(self.ID_CUSTOMIZE_TOOLBAR, 'Customize ToolBar', True)
        self.optionsmenu.AppendSeparator()
        self.optionsmenu.Append(self.ID_EDIT_BOOKMARKS, 'Edit Bookmarks', True, 0)
        self.optionsmenu.Append(self.ID_EDIT_SCRIPT_MENU, 'Edit &Script Menu', True)
        self.optionsmenu.AppendSeparator()
        self.optionsmenu.AppendMenu(self.ID_CONFIGURE_PLUGINS, "C&onfigure Plugins", self.pluginsconfiguremenu)
        self.optionsmenu.AppendMenu(self.ID_PLUGIN_PREFS, "Pl&ugin Preferences", self.pluginsprefsmenu)
        self.optionsmenu.AppendMenu(self.ID_LOAD_PLUGIN, "&Load Plugin From Index", self.pluginsindexmenu)
        self.optionsmenu.Append(self.ID_EDIT_PLUGIN, "E&dit Plugin Source...")
        self.pluginshelpmenu = drPluginHelpMenu(self)
        self.pluginsaboutmenu = drPluginAboutMenu(self)

        self.helpmenu = drMenu(self)
        self.helpmenu.Append(self.ID_ABOUT, "&About DrPython...")
        self.helpmenu.AppendMenu(self.ID_PLUGIN_ABOUT, "About Plugin", self.pluginsaboutmenu)
        self.helpmenu.AppendSeparator()
        self.helpmenu.Append(self.ID_HELP, 'Help', True, 0, 'DrPython &Help...')
        self.helpmenu.AppendMenu(self.ID_PLUGIN_HELP, "Plugin Help", self.pluginshelpmenu)
        self.helpmenu.AppendSeparator()
        self.helpmenu.Append(self.ID_PYTHON_DOCS, 'View Python Docs', True)
        self.helpmenu.Append(self.ID_WXWIDGETS_DOCS, 'View WxWidgets Docs', True)
        self.helpmenu.Append(self.ID_REHOWTO_DOCS, 'View Regular Expression Howto', True)

        if self.prefs.debugmodus:
            self.helpmenu.AppendSeparator()
            self.helpmenu.Append(self.ID_INSPECT_TOOL, self.getmenulabel('&Inspect Tool'))

        self.menuBar = wx.MenuBar()
        #ugly hack workaround
        #in linux, if there is a menu accelerator, the hotkeys are not working anymore.
        #menuBarNamesWin32 = ["&File", "&Edit", "&Search", "&View", "&Program", "&Bookmarks",
        #                  "D&rScript", "&Documents", "&Options", "&Help"]

        #menuBarNamesGtk = ["&File", "&Edit", "&Search", "&View", "&Program", "&Bookmarks",
        #                  "D&rScript", "&Documents", "&Options", "&Help"]
        #menuBarNamesGtk = ["File", "Edit", "Search", "View", "Program", "Bookmarks",
        #                  "DrScript", "Documents", "Options", "Help"]
        #if self.PLATFORM_IS_WIN:
        #    menuBarNames = menuBarNamesWin32
        #else:
        #    menuBarNames = menuBarNamesGtk

        menuBarNames = ["&File", "&Edit", "&Search", "&View", "&Program", "&Bookmarks",
                         "D&rScript", "&Documents", "&Options", "&Help"]

        self.menuBar.Append(self.filemenu, menuBarNames[0])
        self.menuBar.Append(self.editmenu, menuBarNames[1])
        self.menuBar.Append(self.searchmenu, menuBarNames[2])
        self.menuBar.Append(self.viewmenu, menuBarNames[3])
        self.menuBar.Append(self.programmenu, menuBarNames[4])
        self.menuBar.Append(self.bookmarksmenu, menuBarNames[5])
        self.menuBar.Append(self.drscriptmenu, menuBarNames[6])
        self.menuBar.Append(self.documentsmenu, menuBarNames[7])
        self.menuBar.Append(self.optionsmenu, menuBarNames[8])
        self.menuBar.Append(self.helpmenu, menuBarNames[9])

        self.SetMenuBar(self.menuBar)
        self.SetToolbar()

    def SetToolbar(self):
        if self.hasToolBar:
            self.DestroyToolBar()
            self.SetToolBar(None)
        try:
            #AB
            self.ToolBarList = drToolBarFile.getToolBarList(self.datdirectory)
        except:
            self.ShowMessage("Error Loading ToolBar List", "DrPython Error")

        if self.prefs.iconsize > 0:
            self.hasToolBar = True
            self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)

            self.ToolBarIdList = self.SetupToolBar()

            self.SetToolBar(self.toolbar)

    # lm - adding helper functions

    def promptSaveAll(self):
        """ check if there are any open unsaved files, and prompt the user to save each """
        x = 0
        while x < len(self.txtDocumentArray):
            if self.txtDocumentArray[x].GetModify():
                if self.Ask('Would you like to save "%s"?' % self.txtDocumentArray[x].GetFilename(), "DrPython"):
                    self.setDocumentTo(x)
                    self.OnSave(None)
            x += 1

    def promptSaveCurrent(self):
        """ ask the user if they would like to save the current file """
        if self.txtDocument.GetModify():
            if self.Ask('Would you like to save "%s"?' % self.txtDocument.GetFilename(), "DrPython"):
                self.OnSave(None)

    def promptDir(self, msg):
        """ open a directory browser and return the directory chosen """
        d = wx.DirDialog(self, msg, style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON|wx.MAXIMIZE_BOX|wx.THICK_FRAME)
        dir = ''
        if d.ShowModal() == wx.ID_OK:
            dir = d.GetPath()
        d.Destroy()
        return dir

class SysOutListener:
    def __init__(self):
        self.first = True
    def write(self, string):
        f=open(out_file, 'a')
        if self.first:
            self.first = False
            f.write('\n\n' + time.ctime() + ':\n')
        f.write(string)
        f.flush()
        f.close()
        #sys.__stdout__.write(string)
        #evt = wxStdOut(text=string)
        #wx.PostEvent(wx.GetApp().frame.output_window, evt)

class SysErrListener:
    def __init__(self):
        self.first = True
    def write(self, string):
        if len(string) > 1:
            #print "write", string, len(string)
            did_not_exist = False
            if not os.path.exists(err_file):
                did_not_exist = True
            f=open(err_file, 'a')
            if self.first:
                self.first = False
                if did_not_exist:
                    first = open(firsterr_file, 'w')
                    first.close()
                f.write('\n\n' + time.ctime() + ':\n')
            f.write(string)
            f.flush()
            f.close()
        #sys.__stderr__.write(string)
        #evt = wxStdOut(text=string)
        #wx.PostEvent(wx.GetApp().frame.output_window, evt)

def ShowErrAndRemoveErrFile(end=True):
    import wx
    if os.path.exists(err_file):
        #app = wx.App(0)
        if end:
            answer = wx.MessageBox("Do you want to see the errors?\n(You can turn off that debug modus in preferences.)", "There were errors: Output is in" + err_file, wx.YES_NO)
        else:
            answer = wx.YES
        if answer == wx.YES:
            import  wx.lib.dialogs
            f = open (err_file)
            if not end:
                wx.MessageBox("There were errors in previous startup!", "Show Errors", wx.ICON_EXCLAMATION)
            dlg = wx.lib.dialogs.ScrolledMessageDialog(None, f.read(), err_file + " File")
            dlg.ShowModal()
            dlg.Destroy()
            f.close()
        if end:
            answer = wx.MessageBox("Delete the error File", "Do you want to delete the error file?", wx.YES_NO)
            if answer == wx.YES:
                os.remove (err_file)
                if os.path.exists(out_file):
                    os.remove (out_file)
        #app.MainLoop()


#*******************************************************************************************************

class DrApp(wx.App):

    def OnIdle(self, event):
        #print "idle"
        #about every 80ms, one idle event (in 4 sec about 50 times)

        #if this is checked about every 160 ms, it should be enough
        self.idlecnt += 1
        if self.idlecnt == 2:
            self.idlecnt = 0
            #print self.frame.datdirectory
            #look, if someone wanted to start drpyhton
            openfiletmp = os.path.join(os.path.expanduser('~'), "openfile.tmp")
            if os.path.isfile(openfiletmp):
                f = open(openfiletmp, 'r')
                filename = f.read()
                f.close()
                #print filename
                os.remove(openfiletmp)
                self.frame.OpenOrSwitchToFile(filename, force=True)


    def OnInit(self):
        #print "oninit"
        #self.initready = False
        #lc = wx.Locale(wx.LANGUAGE_DEFAULT)
        #_ = wx.GetTranslation
        #lc.AddCatalogLookupPathPrefix('locale')
        #lc.AddCatalog('drpython')
        self.idlecnt = 0
        self.name = "SingleApp-%s" % (wx.GetUserId())
        self.instance = wx.SingleInstanceChecker(self.name)

        if get_option('--s') and self.instance.IsAnotherRunning():
            #at this time, there is no frame
            openfiletmp = os.path.join(os.path.expanduser('~'), "openfile.tmp")
            f = open(openfiletmp, 'w')
            filename = f.write(sys.argv[-1])
            f.close()
            del self.instance
            sys.exit(1)

        frame = self.frame = DrFrame(None, 101, "DrPython - Untitled 1")

        self.frame.Show(True)

        # import wx.py as py
        # pyCrust = py.crust.Crust(self.frame)
        # pyCrust.SetSize((400, 300))
        # pyCrust.Show()

        self.SetTopWindow(self.frame)

        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        self.Bind (wx.EVT_IDLE, self.OnIdle)

        #print "oninit - end"
        #self.initready = True
        return True

    def OnActivate(self, event):
        if event.GetActive():
            self.frame.OnActivate(event)
        else:
            self.frame.OnDeActivate(event)
        event.Skip()


#{ Command line handling

def print_help():
    print "DrPython - " + DRPY_VER
    print "usage: drpython [arguments] [files... ]"
    print ""
    print "arguments:"
    print "--s: open as single instance"
    print "--r: redirect to stdout"
    print "--preferencespath: choose an alternative preferencesdirectory"


def get_option(name):
    """Checks for option in command line arguments and removes it.

    :returns: `True` if the given option existed, otherwise `False`.
    :rtype: bool
    """
    try:
        del sys.argv[sys.argv.index(name)]
        return True
    except ValueError:
        return False


def get_option_value(name):
    """Get and remove an option from the command line arguments.

    :returns: the value of given option.
    :rtype: str

    :raises KeyError: if there was no option `name` given on the command
        line.

    :todo: Also handle options without ``=`` between option and value.
    """
    name += '='
    for index, argument in enumerate(sys.argv):
        if argument.startswith(name):
            del sys.argv[index]
            return argument[len(name):]
    raise KeyError('option %r not found' % name)
#}


def main():
    useredirecttofile = True

    if get_option('--help'):
        print_help()
        sys.exit(1)

    if get_option('--r'):
        useredirecttofile = False

    if useredirecttofile:
        sys.stdout = SysOutListener()
        sys.stderr = SysErrListener()
    app = DrApp(0)
    if os.path.exists(firsterr_file):
        os.remove (firsterr_file)
        ShowErrAndRemoveErrFile(False)
    if useredirecttofile: #assign again, else after DrApp it
        sys.stdout = SysOutListener()
        sys.stderr = SysErrListener()

    app.MainLoop()
    del app.instance
    debugmodus = app.debugmodus
    if debugmodus:
        ShowErrAndRemoveErrFile()


if __name__ == '__main__':
    main()



