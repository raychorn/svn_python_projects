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
# Programmer: Eur Ing Christopher Thoday.
# Copyright: assigned to the DrPython project

# drHtmlBrowser.py

import wx, os
import wx.html
"""This module provides a browser for displaying HTML files composed in
   the DrPython text editor.  Links are displayed within separate pages
   within the browser. The tab name for the page is the HTML title if given,
   else it is the file name."""

note = None
history = {}

def _AddPage(href):
    if href[0:5] != "http:":
        if not os.path.exists(href):
            href = os.path.normpath(os.path.join(dir, href))
            if not os.path.exists(href):
                wx.MessageBox("File does not exist: " + href, "DrPython HTML Browser")
                return
    if href in history:
        note.SetSelection(history[href])
        return
    np = note.GetPageCount()
    history[href] = np
    page = HtmlPage(note, -1)
    note.AddPage(page, "", True)
    page.LoadPage(href)
    title = page.GetOpenedPageTitle()
    (fname, ext) = os.path.splitext(title)
    if ext[0:4] == ".htm" or ext[0:5] == ".html":
        title = fname.title()
    note.SetPageText(np, title)

class HtmlPage(wx.html.HtmlWindow):
    def __init__(self, parent, id):
        wx.html.HtmlWindow.__init__(self, parent, id,
            style=wx.NO_FULL_REPAINT_ON_RESIZE)
        if "gtk2" in wx.PlatformInfo: self.SetStandardFonts()

    def OnLinkClicked(self, link):
        href = link.GetHref()
        #print href
        _AddPage(href)

class HtmlBrowser(wx.Dialog):
    def __init__(self,  parent, file, title):
        global note, dir
        dir = os.path.dirname(file)
        wx.Dialog.__init__(self, parent, -1, title, size=(500, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME)
        note = wx.Notebook(self, -1)
        history.clear()
        _AddPage(file)
        note.SetSelection(0)
        #else nothing is displayed
        event = wx.SizeEvent()
        self.GetEventHandler().ProcessEvent(event)


def ShowHtmlFile(parent, file, title=""):
    if title == "":
        title = file
    d = HtmlBrowser(parent, file, title)
    d.ShowModal()
    d.Destroy()



