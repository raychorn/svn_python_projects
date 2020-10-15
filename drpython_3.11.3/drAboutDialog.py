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

#About Dialog

# Patch by Knut Gerwens, January 2007: added import of wx.lib.stattext,
#  replaced all occurences of 'wx.StaticText' with 'wx.lib.stattext.GenStaticText'
#  because wx.StaticText displayed some lines truncated when wxPython is run with wxGTK

import wx, wx.html, wx.lib.stattext
import sys, string

class drStaticLink(wx.Panel):

    def __init__(self, parent, id, text, target, drframe):
        wx.Panel.__init__(self, parent, id)

        self.drframe = drframe

        self.link = target

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.stText = wx.lib.stattext.GenStaticText(self, id, text)
        self.stText.SetBackgroundColour(wx.WHITE)
        self.stText.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.stText.SetForegroundColour(wx.Colour(0, 90, 255))

        self.theSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.theSizer.Add(self.stText, 0, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.SetSize(self.stText.GetSize())

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.stText.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.stText.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def OnMouseEnter(self, event):
        self.SetBackgroundColour(wx.Colour(255, 198, 107))
        event.Skip()

    def OnMouseLeave(self, event):
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        event.Skip()

    def OnLeftDown(self, event):
        self.SetBackgroundColour(wx.Colour(255, 156, 0))
        event.Skip()

    def OnLeftUp(self, event):
        self.SetBackgroundColour(wx.Colour(255, 198, 107))
        event.Skip()
        self.drframe.ViewURLInBrowser(self.link)

class drAboutContentPanel(wx.Panel):
    def __init__(self, parent, id, drframe):
        wx.Panel.__init__(self, parent, id)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        standardfont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        app = wx.lib.stattext.GenStaticText(self, -1, 'DrPython - Python IDE')
        app.SetBackgroundColour(wx.WHITE)

        app.SetFont(standardfont)

        author = wx.lib.stattext.GenStaticText(self, -1, '(c) 2003-2007, Daniel Pozmanter')
        author.SetBackgroundColour(wx.WHITE)

        author.SetFont(standardfont)

        credits = drStaticLink(self, 1, ' Credits ', drframe.programdirectory + "/documentation/credits.html", drframe)

        website = drStaticLink(self, 2, ' http://drpython.sourceforge.net/ ', 'http://drpython.sourceforge.net/', drframe)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)
        tempstat = wx.lib.stattext.GenStaticText(self, -1, '   ')
        tempstat.SetBackgroundColour(wx.WHITE)
        self.theSizer.Add(tempstat, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        self.theSizer.Add(app, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        tempstat = wx.lib.stattext.GenStaticText(self, -1, '   ')
        tempstat.SetBackgroundColour(wx.WHITE)
        self.theSizer.Add(tempstat, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        self.theSizer.Add(author, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        tempstat = wx.lib.stattext.GenStaticText(self, -1, '   ')
        tempstat.SetBackgroundColour(wx.WHITE)
        self.theSizer.Add(tempstat, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        self.theSizer.Add(credits, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        tempstat = wx.lib.stattext.GenStaticText(self, -1, '   ')
        tempstat.SetBackgroundColour(wx.WHITE)
        self.theSizer.Add(tempstat, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)
        self.theSizer.Add(website, 0, wx.SHAPED | wx.ALIGN_CENTER_HORIZONTAL)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

class drAboutPanel(wx.Panel):
    def __init__(self, parent, id, drframe):
        wx.Panel.__init__(self, parent, id)

        aboutpanel = drAboutContentPanel(self, id, drframe)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(aboutpanel, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

class drLicensePanel(wx.Panel):
    def __init__(self, parent, id, drframe):
        wx.Panel.__init__(self, parent, id)

        try:
            f = open(drframe.programdirectory + "/documentation/gpl.html", 'rb')
            text = f.read()
            f.close()
        except:
            drframe.ShowMessage('Error Reading the GPL!', 'About Dialog Error')
            return

        self.htmlBox = wx.html.HtmlWindow(self, -1)

        self.htmlBox.SetPage(text)

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(self.htmlBox, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

class drSystemPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        version = string.join(map(lambda x: str(x), sys.version_info[:4]), '.')

        wxplatform = string.join(wx.PlatformInfo[1:], ', ')

        systeminfo = '''wxPython Version: %s

wxPython Platform: %s

Python Version: %s

Python Platform: %s''' % (wx.VERSION_STRING, wxplatform, version, sys.platform)

        self.txt = wx.TextCtrl(self, -1, systeminfo, style = wx.TE_READONLY | wx.TE_MULTILINE)

        self.txt.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.theSizer.Add(self.txt, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

class drAboutDialog(wx.Dialog):

    def __init__(self, parent, app_version):
        wx.Dialog.__init__(self, parent, -1, ("About DrPython"), wx.DefaultPosition, (500, 400), wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.THICK_FRAME | wx.RESIZE_BORDER)

        self.parent = parent

        self.notebook = wx.Notebook(self, -1, style=wx.CLIP_CHILDREN)

        self.notebook.AddPage(drAboutPanel(self.notebook, -1, parent), 'About')
        self.notebook.AddPage(drLicensePanel(self.notebook, -1, parent), 'License Agreement')
        self.notebook.AddPage(drSystemPanel(self.notebook, -1), 'System Info')

        self.btnClose = wx.Button(self, 101, "&Close")

        stext = wx.lib.stattext.GenStaticText(self, -1, 'DrPython - ' + app_version)
        stext.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.topSizer.Add(wx.lib.stattext.GenStaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)

        self.topSizer.Add(wx.StaticBitmap(self, -1, wx.BitmapFromImage(wx.Image(parent.programdirectory + "/documentation/drpython.png", wx.BITMAP_TYPE_PNG))), 0, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)

        self.topSizer.Add(wx.lib.stattext.GenStaticText(self, -1, '  '), 0, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)

        self.topSizer.Add(stext, 0, wx.SHAPED | wx.ALIGN_CENTER_VERTICAL)

        self.theSizer.Add(wx.lib.stattext.GenStaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.topSizer, 0, wx.SHAPED)
        self.theSizer.Add(wx.lib.stattext.GenStaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.notebook, 1, wx.EXPAND)
        self.theSizer.Add(wx.lib.stattext.GenStaticText(self, -1, '  '), 0, wx.SHAPED)
        self.theSizer.Add(self.btnClose, 0, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_BUTTON, self.OnbtnClose, id=101)

    def OnbtnClose(self, event):
        self.EndModal(0)

def Show(parent, app_version):
    d = drAboutDialog(parent, app_version)
    d.ShowModal()
    d.Destroy()
