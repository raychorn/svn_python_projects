#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
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

#The Notebook, and Panels.

import os.path
import wx
import wx.stc
from drText import DrText
import drEncoding

#*************************************************
#Used in the main panel.

class drSashWindow(wx.SashWindow):
    def __init__(self, parent, id, pos, size, style=0):
        wx.SashWindow.__init__(self, parent, id, pos, size, style)

        self.parent = parent.parent

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, event):
        self.parent.RunShortcuts(event)

    def SetNotebook(self, notebook):
        '''Can Only be called once'''

        self.notebook = notebook
        self.theSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.theSizer.Add(self.notebook, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

#*************************************************
#This is the main panel,
#Where all the sizing stuff happens.

class drMainPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.panelsizesfile = parent.datdirectory + "/drpython.panel.sizes.dat"

        self.parent = parent

        width, height = self.GetSizeTuple()

        #Variables to Keep Track of what is being used.

        self.ID_DOCUMENT = 6001
        self.ID_PROMPT = 6002
        self.ID_LEFT = 6003
        self.ID_RIGHT = 6004
        self.ID_TOP = 6005

        self.PromptIsVisible = self.parent.prefs.promptisvisible
        self.LeftIsVisible = False
        self.RightIsVisible = False
        self.TopIsVisible = False

        self.documenttuple = (width, height)
        self.prompttuple = (0, 0)
        self.lefttuple = (0, 0)
        self.righttuple = (0, 0)
        self.toptuple = (0, 0)

        self.promptsize = self.parent.prefs.promptsize

        self.prompt = drSashWindow(self, self.ID_PROMPT, wx.DefaultPosition, wx.DefaultSize, wx.SW_3D)


        self.document = drSashWindow(self, self.ID_DOCUMENT, wx.DefaultPosition, wx.DefaultSize, wx.SW_3D)

        self.leftsize = self.parent.prefs.sidepanelleftsize

        self.left = drSashWindow(self, self.ID_LEFT, wx.DefaultPosition, wx.DefaultSize, wx.SW_3D)

        self.rightsize = self.parent.prefs.sidepanelrightsize

        self.right = drSashWindow(self, self.ID_RIGHT, wx.DefaultPosition, wx.DefaultSize, wx.SW_3D)

        self.topsize = self.parent.prefs.sidepaneltopsize

        self.top = drSashWindow(self, self.ID_TOP, wx.DefaultPosition, wx.DefaultSize, wx.SW_3D)


        self.oldwidth, self.oldheight = 0, 0

        self.leftNotebook = drSidePanelNotebook(self.left, -1, 0)
        self.rightNotebook = drSidePanelNotebook(self.right, -1, 1)
        self.topNotebook = drSidePanelNotebook(self.top, -1, 1)

        self.left.SetNotebook(self.leftNotebook)
        self.right.SetNotebook(self.rightNotebook)
        self.top.SetNotebook(self.topNotebook)

        self.lidx = []
        self.ridx = []
        self.tidx = []

        self.OnSize(None)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SASH_DRAGGED, self.OnSashDrag, id=self.ID_DOCUMENT)
        self.Bind(wx.EVT_SASH_DRAGGED, self.OnSashDrag, id=self.ID_PROMPT)
        if not parent.PLATFORM_IS_GTK:
        #if 0:
            self.document.SetSashVisible(wx.SASH_BOTTOM, True)
            #self.document.SetSashBorder(wx.SASH_BOTTOM, True)
            self.prompt.SetSashVisible(wx.SASH_TOP, True)
            #self.prompt.SetSashBorder(wx.SASH_TOP, True)
            self.document.SetSashVisible(wx.SASH_LEFT, True)
            #self.document.SetSashBorder(wx.SASH_LEFT, True)
            self.document.SetSashVisible(wx.SASH_RIGHT, True)
            #self.document.SetSashBorder(wx.SASH_RIGHT, True)
            self.document.SetSashVisible(wx.SASH_TOP, True)
            #self.document.SetSashBorder(wx.SASH_TOP, True)

            self.prompt.SetSashVisible(wx.SASH_LEFT, True)
            #self.prompt.SetSashBorder(wx.SASH_LEFT, True)
            self.prompt.SetSashVisible(wx.SASH_RIGHT, True)
            #self.prompt.SetSashBorder(wx.SASH_RIGHT, True)

    def _getindex(self, Position, Index):
        #Left
        if Position == 0:
            if Index in self.lidx:
                Index = self.lidx.index(Index)
        #Right
        elif Position == 1:
            if Index in self.ridx:
                Index = self.ridx.index(Index)
        #Top
        else:
            if Index in self.tidx:
                Index = self.tidx.index(Index)

        return Index

    def ClosePanel(self, Position, Index):
        Index = self._getindex(Position, Index)

        #Left
        if Position == 0:
            self.leftNotebook.DeletePage(Index)
            self.lidx.pop(Index)
            if self.leftNotebook.GetPageCount() < 1:
                self.LeftIsVisible = False
        #Right
        elif Position == 1:
            self.rightNotebook.DeletePage(Index)
            self.ridx.pop(Index)
            if self.rightNotebook.GetPageCount() < 1:
                self.RightIsVisible = False
        #Top
        else:
            self.topNotebook.DeletePage(Index)
            self.tidx.pop(Index)
            if self.topNotebook.GetPageCount() < 1:
                self.TopIsVisible = False

        wx.Yield()

        self.OnSize(None)

    def GetTargetNotebookPage(self, Position=1, Title='  '):
        #Left
        if Position == 0:
            l = self.leftNotebook.GetPageCount()
            self.lidx.append(l)
            newpage = drSidePanel(self.leftNotebook, -1)
            self.leftNotebook.AddPage(newpage, Title, True)
            self.LeftIsVisible = True
        #Right
        elif Position == 1:
            l = self.rightNotebook.GetPageCount()
            self.ridx.append(l)
            newpage = drSidePanel(self.rightNotebook, -1)
            self.rightNotebook.AddPage(newpage, Title, True)
            self.RightIsVisible = True
        #Top
        else:
            l = self.topNotebook.GetPageCount()
            self.tidx.append(l)
            newpage = drSidePanel(self.topNotebook, -1)
            self.topNotebook.AddPage(newpage, Title, True)
            self.TopIsVisible = True

        return newpage, l

    def IsVisible(self, Position=1, Index=0):
        Index = self._getindex(Position, Index)

        #Left
        if Position == 0:
            return (self.leftNotebook.GetSelection() == Index) and self.LeftIsVisible
        #Right
        elif Position == 1:
            return (self.rightNotebook.GetSelection() == Index) and self.RightIsVisible
        #Top
        else:
            return (self.topNotebook.GetSelection() == Index) and self.TopIsVisible

    def MemorizePanelSizes(self):
        if self.parent.prefs.rememberpanelsizes:
            try:
                f = open(self.panelsizesfile, 'wb')
                f.write(str(self.promptsize) + '\n' + str(self.leftsize) + '\n' + str(self.rightsize) + '\n' + str(self.topsize))
                f.close()
            except:
                self.parent.ShowMessage('Error Memorizing Panel Sizes.')

    def OnSashDrag(self, event):
        evtheight = event.GetDragRect().height
        evtwidth = event.GetDragRect().width
        width, height = self.GetSizeTuple()
        if evtwidth < 0:
            evtwidth = 0
        elif evtwidth > width:
            evtwidth = width
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            if (not self.PromptIsVisible) or (evtheight < height):
                evtheight = 0
            else:
                evtheight = height
        elif evtheight > height:
            evtheight = height

        oldsize = self.promptsize
        loldsize = self.leftsize
        roldsize = self.rightsize
        toldsize = self.topsize

        #Edge Drag
        e = event.GetId()
        edge = event.GetEdge()
        if edge == wx.SASH_LEFT:
            self.leftsize = ((width*100) - (evtwidth*100)) / width
        elif edge == wx.SASH_RIGHT:
            self.rightsize = ((width*100) - (evtwidth*100)) / width
        elif e == self.ID_DOCUMENT:
            if edge == wx.SASH_BOTTOM:
                self.promptsize = ((height*100) - (evtheight*100)) / height
                self.documenttuple = (self.documenttuple[0], evtheight)
                self.prompttuple = (self.prompttuple[0], height-evtheight)
            elif edge == wx.SASH_TOP:
                self.topsize = ((height*100) - (evtheight*100)) / height
        elif e == self.ID_PROMPT:
            self.promptsize = ((evtheight*100) / height)

        #Prompt Is Visible
        if self.promptsize == 0:
            self.promptsize = oldsize
            self.PromptIsVisible = False
        elif not self.PromptIsVisible and self.prompttuple[1] > 0:
            self.PromptIsVisible = True

        #Left Is Visible
        if self.leftsize == 0:
            self.leftsize = loldsize
            self.LeftIsVisible = False
        elif not self.LeftIsVisible and self.lefttuple[0] > 0:
            self.LeftIsVisible = True

        #Right Is Visible
        if self.rightsize == 0:
            self.rightsize = roldsize
            self.RightIsVisible = False
        elif not self.RightIsVisible and self.righttuple[0] > 0:
            self.RightIsVisible = True

        #Top Is Visible
        if self.topsize == 0:
            self.topsize = toldsize
            self.TopIsVisible = False
        elif not self.TopIsVisible and self.toptuple[1] > 0:
            self.TopIsVisible = True

        self.OnSize(None)

    def OnSize(self, event):
        width, height = self.GetSizeTuple()

        if (event is not None) and (width == self.oldwidth) and (height == self.oldheight):
            return
        self.oldwidth, self.oldheight = width, height

        #Height

        heightPrompt = 0
        heightTop = 0

        if self.TopIsVisible:
            heightTop = (height * self.topsize) / 100
        if self.PromptIsVisible:
            heightPrompt = (height * self.promptsize) / 100

        heightDocument = height - heightTop - heightPrompt

        if heightPrompt != 100:
            if heightDocument < 50:
                if heightTop > 0:
                    heightTop = heightTop / 2
                if heightPrompt > 0:
                    heightPrompt = heightPrompt / 2
                heightDocument += heightTop + heightPrompt


        #Width
        widthLeft = 0
        widthRight = 0

        if self.LeftIsVisible:
            widthLeft = (width * self.leftsize) / 100
        if self.RightIsVisible:
            widthRight = (width * self.rightsize) / 100

        widthMain = width - widthLeft - widthRight

        if widthMain < 50:
            if widthLeft > 0:
                widthLeft = widthLeft / 2
            if widthRight > 0:
                widthRight = widthRight / 2
            widthMain += widthLeft + widthRight

        #Tuples
        self.documenttuple = (widthMain, heightDocument)
        self.prompttuple = (widthMain, heightPrompt)
        self.lefttuple = (widthLeft, height)
        self.righttuple = (widthRight, height)
        self.toptuple = (widthMain, heightTop)

        #Set Move, Then Set Size
        self.document.Move((widthLeft, heightTop))
        self.prompt.Move((widthLeft, heightDocument+heightTop))
        self.left.Move((0, 0))
        self.right.Move((widthLeft+widthMain, 0))
        self.top.Move((widthLeft, 0))

        self.document.SetSize(self.documenttuple)
        self.prompt.SetSize(self.prompttuple)
        self.left.SetSize(self.lefttuple)
        self.right.SetSize(self.righttuple)
        self.top.SetSize(self.toptuple)

    def RememberPanelSizes(self):
        if self.parent.prefs.rememberpanelsizes:
            if not os.path.exists(self.panelsizesfile):
                return
            try:
                f = open(self.panelsizesfile, 'rb')
                text = f.read()
                f.close()
                p, l, r, t = map(int, text.split('\n'))
                self.promptsize = p
                self.leftsize = l
                self.rightsize = r
                self.topsize = t
            except:
                self.parent.ShowMessage('Error Remembering Panel Sizes.\nThe File: "%s" may be corrupt.\nTry removing it, and restarting DrPython.' % self.panelsizesfile)

    def SetPanelSize(self, Position, size):
        if Position == 0:
            self.leftsize = size
        elif Position == 1:
            self.rightsize = size
        else:
            self.topsize = size

    def ShowPanel(self, Position, Index, Show=True):
        Index = self._getindex(Position, Index)

        #Left
        if Position == 0:
            self.LeftIsVisible = Show
            if self.LeftIsVisible:
                self.leftNotebook.SetSelection(Index)
                self.leftNotebook.GetPage(Index).OnSize(None)
        #Right
        elif Position == 1:
            self.RightIsVisible = Show
            if self.RightIsVisible:
                self.rightNotebook.SetSelection(Index)
                self.rightNotebook.GetPage(Index).OnSize(None)
        #Top
        else:
            self.TopIsVisible = Show
            if self.TopIsVisible:
                self.topNotebook.SetSelection(Index)
                self.topNotebook.GetPage(Index).OnSize(None)
        self.OnSize(None)

    def TogglePanel(self, Position=1, Index=0):
        Index = self._getindex(Position, Index)

        #Left
        if Position == 0:
            if not self.LeftIsVisible:
                self.LeftIsVisible = True
                self.leftNotebook.SetSelection(Index)
            else:
                self.LeftIsVisible = False
        #Right
        elif Position == 1:
            if not self.RightIsVisible:
                self.RightIsVisible = True
                self.rightNotebook.SetSelection(Index)
            else:
                self.RightIsVisible = False
        #Top
        else:
            if not self.TopIsVisible:
                self.TopIsVisible = True
                self.topNotebook.SetSelection(Index)
            else:
                self.TopIsVisible = False
        self.OnSize(None)

#*************************************************

def _refresh(x):
    x.Refresh()

#*******************************************************************************************************
#Notebook base class

class drNotebook(wx.Notebook):
    def __init__(self, parent, id, images, closefunction):
        wx.Notebook.__init__(self, parent, id, wx.DefaultPosition, (-1, -1), wx.CLIP_CHILDREN)

        self.parent = parent

        self.grandparent = parent.parent

        self.closefunction = closefunction

        if images:
            imagesize = (16, 16)

            self.imagelist = wx.ImageList(imagesize[0], imagesize[1])
            self.images = images

            map(self.imagelist.Add, self.images)

            self.AssignImageList(self.imagelist)

        #wxPython bug workaround, OldSelection doesn't work.
        self.oldselection = 0

    def OnLeftDoubleClick(self, event):
        if isinstance (self, drDocNotebook): #otherwise exception
            if self.grandparent.prefs.doubleclicktoclosetab:
                self.closefunction(None)

#*************************************************
#Document Notebook

class drDocNotebook(drNotebook):
    def __init__(self, parent, id):
        grandparent = parent.parent
        images = [wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/unmodified.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/modified.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/active unmodified.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/active modified.png", wx.BITMAP_TYPE_PNG))]

        drNotebook.__init__(self, parent, id, images, grandparent.OnClose)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NAVIGATION_KEY, self.OnNavigationKey)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUp)
        self.Bind(wx.EVT_LEFT_UP, self.OnSelectTab)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)

    def OnNavigationKey(self, event): #only in windows? on gtk, that is apparantly never called.
        ignorekey = False
        if self.grandparent.prefs.docignorectrlpageupdown:
            if wx.GetKeyState(wx.WXK_CONTROL):
                if wx.GetKeyState(wx.WXK_PAGEUP) or wx.GetKeyState(wx.WXK_PAGEDOWN):
                    ignorekey = True
                #if wx.GetKeyState(wx.WXK_TAB):
                #    ignorekey = True
        if ignorekey:
            keycode = 0
            if wx.GetKeyState(wx.WXK_TAB):
                keycode = wx.WXK_TAB
            if wx.GetKeyState(wx.WXK_PAGEUP):
                keycode = wx.WXK_PAGEUP
            if wx.GetKeyState(wx.WXK_PAGEDOWN):
                keycode = wx.WXK_PAGEDOWN
            evt = wx.KeyEvent()
            evt.m_controlDown = wx.GetKeyState(wx.WXK_CONTROL)
            evt.m_keyCode = keycode
            evt.m_shiftDown = wx.GetKeyState(wx.WXK_SHIFT)
            evt.SetEventType(wx.wxEVT_KEY_DOWN)

            self.grandparent.txtDocument.GetEventHandler().ProcessEvent(evt)
        else:
            event.Skip()

    def OnPageChanged(self, event):
        #if self.grandparent.ignoreevents:
        if self.grandparent.disableeventhandling:
            return

        if not self.grandparent.txtDocumentArray:
            if event is not None:
                event.Skip()
            return
        if event is not None:
            i = event.GetSelection()
        else:
            i = self.GetSelection()
        l = self.GetPageCount()
        if (i < 0) or (i >= l):
            if event is not None:
                event.Skip()
            return
        if self.oldselection < l:
            if len (self.grandparent.txtDocumentArray) > self.oldselection:
                self.grandparent.txtDocumentArray[self.oldselection].IsActive = False
                self.grandparent.txtDocumentArray[self.oldselection].OnModified(None)

        self.oldselection = i

        self.grandparent.txtDocumentArray[i].IsActive = True
        self.grandparent.txtDocumentArray[i].OnModified(None)

        wx.CallAfter (self.SetTab) #bug reported and patch supplied by Tiziano Mueller, which itself was supplied by a user, 25. Feb. 2008, thanks.
        if event is not None:
            event.Skip()

    def OnPopUp(self, event):

        tabmenu = wx.Menu()
        tabmenu.Append(self.grandparent.ID_CLOSE, "&Close")
        tabmenu.Append(self.grandparent.ID_CLOSE_ALL, "Close &All Tabs")
        tabmenu.Append(self.grandparent.ID_CLOSE_ALL_OTHER_DOCUMENTS, "Close All &Other Tabs")
        tabmenu.AppendSeparator()
        tabmenu.Append(self.grandparent.ID_NEXT_DOCUMENT, "Next Tab")
        tabmenu.Append(self.grandparent.ID_PREVIOUS_DOCUMENT, "Previous Tab")
        tabmenu.Append(self.grandparent.ID_FIRST_DOCUMENT, "First Tab")
        tabmenu.Append(self.grandparent.ID_LAST_DOCUMENT, "Last Tab")
        tabmenu.AppendSeparator()
        tabmenu.Append(self.grandparent.ID_RELOAD, "&Reload File")
        tabmenu.Append(self.grandparent.ID_RESTORE_FROM_BACKUP, "&Restore From Backup")
        tabmenu.AppendSeparator()
        tabmenu.Append(self.grandparent.ID_SAVE, "&Save")
        tabmenu.Append(self.grandparent.ID_SAVE_AS, "Save &As...")

        ht = self.HitTest(event.GetPosition())[0]
        if ht > -1:
            self.SetSelection(ht)
            self.SetTab()

        tabmenu.Enable(self.grandparent.ID_RELOAD, len(self.grandparent.txtDocument.filename) > 0)
        tabmenu.Enable(self.grandparent.ID_RESTORE_FROM_BACKUP, len(self.grandparent.txtDocument.filename) > 0)
        self.PopupMenu(tabmenu, event.GetPosition())
        tabmenu.Destroy()

    def OnSelectTab(self, event):
        selection = self.GetSelection()
        if selection != self.grandparent.docPosition:
            self.SetTab()
        event.Skip()

    def SetTab(self):
        #if not self.IsBeingDeleted(): # is not None: #pydeadobject error
        selection = self.GetSelection()
        if selection != -1:
            self.grandparent.setDocumentTo(selection)

#*************************************************
#Prompt Notebook

class drPromptNotebook(drNotebook):
    def __init__(self, parent, id):
        grandparent = parent.parent
        images = [wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/not running.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/running.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/active not running.png", wx.BITMAP_TYPE_PNG)),
        wx.BitmapFromImage(wx.Image(grandparent.bitmapdirectory + "/16/active running.png", wx.BITMAP_TYPE_PNG))]

        drNotebook.__init__(self, parent, id, images, grandparent.OnClosePrompt)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LEFT_UP, self.OnSelectTab)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUp)

    def OnPageChanged(self, event):
        if not self.grandparent.txtPromptArray:
            if event is not None:
                event.Skip()
            return
        if event is not None:
            i = event.GetSelection()
        else:
            i = self.GetSelection()
        l = self.GetPageCount()
        if (i < 0) or (i >= l):
            if event is not None:
                event.Skip()
            return
        if self.oldselection < l:
            if len(self.grandparent.txtPromptArray) > self.oldselection:
                if self.grandparent.txtPromptArray[self.oldselection].pid > -1:
                    self.SetPageImage(self.oldselection, 1)
                else:
                    self.SetPageImage(self.oldselection, 0)

        self.oldselection = i

        if self.grandparent.txtPromptArray[i].pid > -1:
            self.SetPageImage(i, 3)
        else:
            self.SetPageImage(i, 2)

        if event is not None:
            event.Skip()

    def OnSelectTab(self, event):
        selection = self.GetSelection()
        if selection != self.grandparent.promptPosition:
            self.SetTab()
        event.Skip()

    def SetTab(self):
        selection = self.GetSelection()
        if selection != -1:
            self.grandparent.setPromptTo(selection)

    def OnPopUp(self, event):

        tabmenu = wx.Menu()
        tabmenu.Append(self.grandparent.ID_CLOSE_PROMPT, "&Close Prompt")
        tabmenu.AppendSeparator()
        tabmenu.Append(self.grandparent.ID_PYTHON, "&Python")
        tabmenu.Append(self.grandparent.ID_RUN, "&Run Current Document")
        tabmenu.Append(self.grandparent.ID_END, "&End")

        ht = self.HitTest(event.GetPosition())[0]
        if ht > -1:
            self.SetSelection(ht)
            self.SetTab()

        tabmenu.Enable(self.grandparent.ID_RUN, (len(self.grandparent.txtDocument.filename) > 0))
        tabmenu.Enable(self.grandparent.ID_END, (self.grandparent.txtPrompt.pid > -1))
        self.PopupMenu(tabmenu, event.GetPosition())
        tabmenu.Destroy()

#*************************************************
#Notebook to be used in the side panels.

class drSidePanelNotebook(drNotebook):
    def __init__(self, parent, id, Position):
        self.parent = parent.parent

        self.PanelPosition = Position

        self.ID_CLOSE = 50

        drNotebook.__init__(self, parent, id, [], self.OnClose)

        self.grandparent = self.GetParent().GetParent()

        self.Bind(wx.EVT_MENU, self.OnClose, id=self.ID_CLOSE)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnClose(self, event):
        if self.GetPageCount() > 0:
            self.grandparent.ClosePanel(self.PanelPosition, self.GetSelection())
            self.grandparent.OnSize(None)

    def OnPageChanged(self, event):
        sel = self.GetSelection()

        if sel > -1:
            self.GetPage(sel).OnSize(None)

        event.Skip()


    def OnSize(self, event):
        if event is not None:
            if self.GetPageCount() > 0:
                self.GetPage(self.GetSelection()).SetSize(self.GetSize())
            event.Skip()

    def OnPopUp(self, event):

        tabmenu = wx.Menu()
        tabmenu.Append(self.ID_CLOSE, "&Close Panel")

        ht = self.HitTest(event.GetPosition())[0]
        if ht > -1:
            self.SetSelection(ht)

        self.PopupMenu(tabmenu, event.GetPosition())
        tabmenu.Destroy()

#*************************************************
#Panel class for panels with a single stc.

class drPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.grandparent = parent.GetGrandParent()

        self.stc = None

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, event):
        self.grandparent.GetParent().RunShortcuts(event)

    def OnSize(self, event):
        if self.stc is not None:
            self.stc.SetSize(self.GetSize())
        if event is not None:
            event.Skip()

    def SetSTC(self, stc):
        self.stc = stc

#*************************************************
#Panel class for side panels.

class drSidePanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.panel = None

        self.parent = parent

        self.grandparent = parent.GetGrandParent()

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        if self.panel is not None:
            self.panel.SetSize(self.GetSize())
        if event is not None:
            event.Skip()

    def OnKeyDown(self, event):
        self.grandparent.GetParent().RunShortcuts(event)

    def SetPanel(self, panel):
        self.panel = panel

#*************************************************
#View In Panel

class drSplitTextPanel(wx.Panel):
    def __init__(self, parent, grandparent, targetstc, position, index):
        docid = grandparent.txtDocument.GetId()
        wx.Panel.__init__(self, parent, docid)

        ID_CLOSE = grandparent.GetNewId()

        self.position = position
        self.index = index

        self.parent = parent

        self.grandparent = grandparent

        if docid == targetstc.GetId():
            sv = -1
        else:
            sv = 1

        self.txtDoc = DrText(self, docid, grandparent, SplitView=sv)
        self.txtDoc.SetupPrefsDocument()
        self.txtDoc.SetDocPointer(targetstc.GetDocPointer())
        self.txtDoc.GotoPos(targetstc.GetCurrentPos())
        self.txtDoc.ScrollToLine(targetstc.GetCurrentLine())

        self.label = wx.TextCtrl(self, -1, " Viewing: " + targetstc.GetFilenameTitle(), size=(150, -1), style=wx.TE_READONLY)

        self.btnClose = wx.Button(self, ID_CLOSE, "Close")

        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.topSizer.Add(self.label, 1, wx.EXPAND)
        self.topSizer.Add(self.btnClose, 0, wx.SHAPED | wx.ALIGN_RIGHT)

        self.theSizer.Add(self.topSizer, 0, wx.EXPAND)
        self.theSizer.Add(self.txtDoc, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        text = self.txtDoc.GetText()

        #Scrolling
        bufferstring = drEncoding.EncodeText(self.grandparent, '000', self.txtDoc.GetEncoding())
        lines = text.split(self.txtDoc.GetEndOfLineCharacter())
        spaces = "\t".expandtabs(self.grandparent.prefs.doctabwidth[self.txtDoc.filetype])
        line = ""
        length = 0
        for l in lines:
            if len(l) > length:
                length = len(l)
                line = l
        line = line.replace('\t', spaces)
        self.txtDoc.SetScrollWidth(self.txtDoc.TextWidth(wx.stc.STC_STYLE_DEFAULT, line + bufferstring))

        self.txtDoc.SetXOffset(0)
        #/End Scrolling

        self.Bind(wx.EVT_BUTTON, self.OnbtnClose, id=ID_CLOSE)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnbtnClose(self, event):
        self.grandparent.mainpanel.ClosePanel(self.position, self.index)

    def OnKeyDown(self, event):
        self.grandparent.RunShortcuts(event)
