# -*- coding: iso-8859-15 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: PDFexporter.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid

# Window functions

ID_TEXT = 10000
ID_BUTTON = 10001

def AboutBoxFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.BoxSizer( wx.VERTICAL )
    parent._sizer = item0
    
    item1 = wx.StaticText( parent, ID_TEXT, 
        "(c). Copyright 1990-2020, Vyper Logix Corp., \n"
        "\n"
        "                   All Rights Reserved.\n"
        "\n"
        "Published under Creative Commons License \n"
        "(http://creativecommons.org/licenses/by-nc/3.0/) \n"
        "restricted to non-commercial educational use only., \n"
        "\n"
        "http://www.VyperLogix.com for details\n"
        "\n"
        "THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO\n"
        "THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\n"
        "FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,\n"
        "INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING\n"
        "FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\n"
        "NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\n"
        "WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !\n"
        "\n"
        "USE AT YOUR OWN RISK.\n"
        "",
        wx.DefaultPosition, wx.DefaultSize, 0 )
    item0.Add( item1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    item2 = wx.Button( parent, ID_BUTTON, "OK", wx.DefaultPosition, wx.DefaultSize, 0 )
    item0.Add( item2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

ID_MENU = 10002

def MyMenuBarFunc():
    item0 = wx.MenuBar()
    
    item1 = wx.Menu()
    item1.Append( wx.ID_ABOUT, "About", "" )
    item1.Append( wx.ID_EXIT, "Quit", "" )
    item0.Append( item1, "File" )
    
    return item0

# Toolbar functions


def MyToolBarFunc( parent ):
    parent.SetMargins( [2,2] )
    
    
    parent.Realize()

# Bitmap functions


# End of generated file
