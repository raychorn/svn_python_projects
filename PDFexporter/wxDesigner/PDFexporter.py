#!/bin/env python
# -*- coding: iso-8859-15 -*-
#----------------------------------------------------------------------------
# Name:         PDFexporter.py
# Author:       Vyper Logix Corp
# Created:      08/02/2008
# Copyright:    
#----------------------------------------------------------------------------

import wx

from PDFexporter_wdr import *

__copyright__ = """\
(c). Copyright 1990-2020, Vyper Logix Corp., 

                   All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

# WDR: classes

class TopFrame(wx.Frame):
    def __init__(self, parent, id, title,
        pos = wx.DefaultPosition, size = wx.DefaultSize,
        style = wx.DEFAULT_FRAME_STYLE ):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        
        self.CreateMyMenuBar()
        
        self.CreateMyToolBar()
        
        self.CreateStatusBar(1)
        self.SetStatusText("Welcome!")
        
        # insert main window here
        
        # WDR: handler declarations for TopFrame
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnQuit)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        wx.EVT_SIZE(self, self.OnSize)
        
    # WDR: methods for TopFrame
    
    def CreateMyMenuBar(self):
        self.SetMenuBar( MyMenuBarFunc() )
    
    def CreateMyToolBar(self):
        tb = self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER)
        MyToolBarFunc( tb )
    
    # WDR: handler implementations for TopFrame
    
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "Welcome to PDFexporter v1.0\n%s" % (__copyright__),
            "About PDFexporter v1.0", wx.OK|wx.ICON_INFORMATION )
        dialog.CentreOnParent()
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnQuit(self, event):
        self.Close(True)
    
    def OnCloseWindow(self, event):
        self.Destroy()
    
    def OnSize(self, event):
        event.Skip(True)
    

#----------------------------------------------------------------------------

class PDFexporter(wx.App):
    
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = TopFrame( None, -1, "PDFexporter v1.0", [20,20], [800,600] )
        frame.Show(True)
        
        return True

#----------------------------------------------------------------------------

app = PDFexporter(True)
app.MainLoop()

