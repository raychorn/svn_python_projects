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

#PopUp

import wx.stc

def OnPopUp(stc, event):
        stc.actiondict = SetUpPopUpActions(stc.grandparent)

        if not stc.grandparent.popupmenulist:
            stc.grandparent.popupmenulist = ["Undo", "Redo", "<Separator>", "Cut", "Copy", "Paste", "Delete", "<Separator>", "Select All"]

        stc.PopUpMenu = wx.Menu()

        #Franz: added getlabel functions.

        x = 0
        l = len(stc.grandparent.popupmenulist)
        while x < l:
            try:
                if stc.grandparent.popupmenulist[x] == "<Separator>":
                    stc.PopUpMenu.AppendSeparator()
                elif stc.grandparent.popupmenulist[x].find("<DrScript>") > -1:
                    label = stc.grandparent.popupmenulist[x][stc.grandparent.popupmenulist[x].find(":")+1:]
                    try:
                        i = stc.grandparent.drscriptmenu.titles.index(label)
                        stc.PopUpMenu.Append(stc.grandparent.ID_SCRIPT_BASE+i, stc.grandparent.drscriptmenu.getdrscriptmenulabel(label))
                        stc.Bind(wx.EVT_MENU, stc.OnPopUpMenu, id=stc.grandparent.ID_SCRIPT_BASE+i)
                    except:
                        pass
                elif stc.grandparent.popupmenulist[x].find("<Plugin>") > -1:
                    label = stc.grandparent.popupmenulist[x][stc.grandparent.popupmenulist[x].find(":")+1:]
                    try:
                        i = stc.grandparent.PluginPopUpMenuLabels.index (label)
                        stc.grandparent.PluginPopUpMenuLabels.index(label)
                        stc.PopUpMenu.Append(stc.ID_POPUP_BASE+x, stc.grandparent.GetPluginMenuLabel(stc.grandparent.PluginPopUpMenuNames [i], label, label))
                        stc.Bind(wx.EVT_MENU, stc.OnPopUpMenu, id=stc.ID_POPUP_BASE+x)
                    except:
                        pass
                else:
                    stc.grandparent.Append_Menu(stc.PopUpMenu, stc.ID_POPUP_BASE+x, stc.grandparent.popupmenulist[x])
                    stc.Bind(wx.EVT_MENU, stc.OnPopUpMenu, id=stc.ID_POPUP_BASE+x)
            except:
                #Error with PopUpMenu Item
                pass
            x = x + 1
        stc.PopupMenu(stc.PopUpMenu, event.GetPosition())

        stc.PopUpMenu.Destroy()

def OnPopUpMenu(stc, event):
        eid = event.GetId()
        label = stc.PopUpMenu.GetLabel(eid)

        #Franz: Remove Shortcut
        f = label.find ("\t")
        if f != -1:
            label = label [:f]
        #/Remove Shortcut

        if label in stc.actiondict:
            stc.actiondict[label](event)
        elif label in stc.stclabelarray:
            if label == 'Paste':
                stc.Paste()
            else:
                i = stc.stclabelarray.index(label)
                stc.CmdKeyExecute(stc.stcactionarray[i])
        else:
            #DrScript
            try:
                i = stc.grandparent.drscriptmenu.titles.index(label)
                stc.grandparent.drscriptmenu.OnScript(event)
            except:
                pass
            #Plugins
            try:
                i = stc.grandparent.PluginPopUpMenuLabels.index(label)
                stc.grandparent.PluginPopUpMenuFunctions[i](event)
            except:
                pass

def SetUpPopUpActions(frame):

    actiondictionary = {"New":frame.OnNew, "Open":frame.OnOpen, "Open Imported Module":frame.OnOpenImportedModule,
    "Save":frame.OnSave, "Save As":frame.OnSaveAs,
    "Save All Documents":frame.OnSaveAll,
    "Save Prompt Output To File":frame.OnSavePrompt, "Reload File":frame.OnReload,
    "Restore From Backup":frame.OnRestoreFromBackup, "Close":frame.OnClose,
    "Close All Documents":frame.OnCloseAllDocuments, "Close All Other Documents":frame.OnCloseAllOtherDocuments,
    "Print Setup":frame.OnPrintSetup, "Print File":frame.OnPrint, "Print Prompt":frame.OnPrintPrompt,
    "Next Document":frame.OnSelectDocumentNext, "Previous Document":frame.OnSelectDocumentPrevious,
    "First Document":frame.OnSelectDocumentFirst, "Last Document":frame.OnSelectDocumentLast,
    "Exit":frame.OnExit,
    "Find":frame.OnMenuFind, "Find Next":frame.OnMenuFindNext, "Find Previous":frame.OnMenuFindPrevious,
    "Replace":frame.OnMenuReplace,
    "View In Left Panel":frame.OnViewInLeftPanel, "View In Right Panel":frame.OnViewInRightPanel,
    "View In Top Panel":frame.OnViewInTopPanel, "Insert Separator":frame.OnInsertSeparator,
    "Insert Regular Expression":frame.OnInsertRegEx, "Go To":frame.OnGoTo,
    "Go To Block Start":frame.OnGoToBlockStart, "Go To Block End":frame.OnGoToBlockEnd,
    "Go To Class Start":frame.OnGoToClassStart, "Go To Class End":frame.OnGoToClassEnd,
    "Go To Def Start":frame.OnGoToDefStart, "Go To Def End":frame.OnGoToDefEnd,
    "Source Browser Go To":frame.OnSourceBrowserGoTo,
    "Comment":frame.OnCommentRegion, "UnComment":frame.OnUnCommentRegion,
    "Find And Complete":frame.OnFindAndComplete,
    "Indent":frame.OnIndentRegion, "Dedent":frame.OnDedentRegion,
    "Toggle Fold":frame.OnToggleFold, "Fold All":frame.OnFoldAll, "Expand All":frame.OnExpandAll,
    "Toggle Source Browser":frame.OnToggleSourceBrowser, "Toggle View Whitespace":frame.OnToggleViewWhiteSpace,
    "Toggle Prompt":frame.OnTogglePrompt,
    "Run":frame.OnRun, "Set Arguments":frame.OnSetArgs, "Python":frame.OnPython,
    "End":frame.OnEnd, "Check Syntax":frame.OnCheckSyntax,
    "Close Prompt":frame.OnClosePrompt, "Preferences":frame.OnPrefs,
    "Customize Shortcuts":frame.OnCustomizeShortcuts, "Customize Pop Up Menu":frame.OnCustomizePopUpMenu,
    "Customize ToolBar":frame.OnCustomizeToolBar,
    "Help":frame.OnViewHelp, "View Python Docs":frame.OnViewPythonDocs, "View WxWidgets Docs":frame.OnViewWxWidgetsDocs,
    "View Regular Expression Howto":frame.OnViewREHowtoDocs}

    return actiondictionary


