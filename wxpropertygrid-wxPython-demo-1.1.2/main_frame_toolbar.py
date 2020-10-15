
import wx
import os
import sys


class Toolbar():
        
    def __init__(self, parent = None):
        self.parent = parent
        self.create_toolbar()		# This is the method of creating a toolbar taken from wxPython in Action, Chapter 6.
        
    def create_toolbar(self):
        toolbar = self.parent.CreateToolBar()
        for item in self.toolbar_data():
            self.create_simple_tool(toolbar, *item)
        toolbar.AddSeparator()
        toolbar.Realize()
        
    def create_simple_tool(self, toolbar, label, filename, help, handler):
        if not label:
            toolbar.AddSeparator()
        else:
            main_dir = sys.path[0]
            graphics_dir = os.path.join(main_dir, "", "graphics")
            path_name = os.path.join(graphics_dir, filename)
            img = wx.Image(path_name)
            bitmap = wx.BitmapFromImage(img)
            tool = toolbar.AddSimpleTool(-1, bitmap, label, help)
            self.parent.Bind( wx.EVT_MENU, handler, tool )
        
    def toolbar_data(self):
        tuple_toolbar = (
                ("New Property'", "folder_orange.png", "Create a new property", self.parent._v_menu.menu_property_add), 
                ("","","",""), 
                ("Delete Property", "tab_remove.png", "Delete the current property", self.parent._v_menu.menu_property_delete)
                )
        return tuple_toolbar
        
        