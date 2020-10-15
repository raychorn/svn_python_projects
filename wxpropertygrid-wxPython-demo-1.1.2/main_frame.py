
import wx, wx.html
from wx.lib.wordwrap import wordwrap
import log
import main_frame_layout
import main_frame_toolbar
import main_frame_menu_def
import main_frame_event_def
import main_frame_menu_func
import main_frame_event_func



class Main_Frame(wx.Frame):
    """The Main Frame of the program"""
    if False:
        pass
        # Building an octopus with arms, tenticles, and a brain...
        #
        # main_frame
        #	+--	_v_layout	gui=graphical screen elements/definitions/functions
        #	+--	_v_menu		menu definitions/functions gathered into a separate file
        # 	+--	_v_event		event handler definitions/functions gathered into a separate file
        #
        # Whaaat??
        # The objective with all this separate file stuff is to avoid having to edit this file - ever.
    
    def __init__(self, parent=None):
        """Constructor"""
        # wx.Frame.__init__(parent, id=-1, title="", pos=wx.DEFAULTPOSITION, size=wx.DEFAULTSIZE, style=wx.DefAULT_FRAME_STYLE, name="frame")
        frame_parent = parent
        self._v_python_version = frame_parent._v_python_version
        self._v_wxpython_version = frame_parent._v_wxpython_version
        self._v_wxpropertygrid_version = frame_parent._v_wxpropertygrid_version
        self._v_pg_version = frame_parent._v_version
        self._v_app_name = frame_parent._v_app_name
        id_main_frame_id = wx.ID_ANY
        str_main_frame_title = ("%s version: %s") % (self._v_app_name, self._v_pg_version)
        point_main_frame_position = wx.Point(0, 0)
        size_main_frame_size = wx.Size(1149, 620)
        style_main_frame_style = wx.DEFAULT_FRAME_STYLE
        str_main_frame_name = "Main_Frame"
        wx.Frame.__init__(self, parent=None, id=id_main_frame_id, title=str_main_frame_title, pos=point_main_frame_position, size=size_main_frame_size, style=style_main_frame_style, name=str_main_frame_name)
        
        self._v_debug = True
        self._v_debug_level = 7000
        
        self.__set_properties()
        
        self.menu = None
        
        self._v_layout = main_frame_layout.Layout(parent = self)
        
        self._v_menu = main_frame_menu_func.Menu(parent = self)
        self._v_event = main_frame_event_func.Event(parent = self)
        
        self._v_menu_def = main_frame_menu_def.Menus(parent = self)
        self._v_event_def = main_frame_event_def.Events(parent = self)
        
        self._v_toolbar = main_frame_toolbar.Toolbar(parent = self)
        
        # printer object to use for the app
        self.printer = wx.html.HtmlEasyPrinting()
        self.Layout()	# wxPython built-in function, just to confuse you!
        
        self.write("Using Python " + self._v_python_version)
        self.write("Using wxPython " + self._v_wxpython_version)
        self.write("Using wxPropertyGrid " + self._v_wxpropertygrid_version)
        self.write("Running " + self._v_app_name + " version " + self._v_pg_version)
        
        
        
    def __set_properties(self):
        self.SetBackgroundColour('Lime Green')
        self.orientation_v = wx.VERTICAL
        self.orientation_h = wx.HORIZONTAL
        self.no_border = 0
        self.border_width = 5
        self.controls_border_width = 3
        self.frame_border_width = 5
        self.value_border_width = 25
        self.toolbar_border_width = 15
        
        self.node_id = -1
        self.node_template_id = -1
        self.property_template_id = -1
        
        self.font_size_numeric = 22
        self.font_size_text = 14
        
        
    def write_text(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        wx.LogMessage(text)
            
    def write(self, message):
        pass
        # print message
        self.write_text(message)
        
    def set_status(self, msg, col=0):
        """Sets the status bar text for a given column.
        Column 0 is the left-most column, 
        Column -1 is the right-most column.
        """
        if col < 0:
            col = self.statusbar.GetFieldsCount() + col
        self.statusbar.SetStatusText(msg, col)
        
    def  help_about(self):
        pass
        info = wx.AboutDialogInfo()
        info.Name = self._v_app_name + " " + self._v_pg_version
        info.Version = self._v_pg_version
        info.Copyright = "wxPropertyGrid Sample Program"
        info.Description = wordwrap( "wxPropertyGrid is a property-sheet control for wxWidgets.  "
            "It is a two-column grid for editing properties such as text, numbers, flag-sets, text-lists, fonts, and colours.  "
            "In addition to a basic, two-column grid, wxPropertyGrid supports arranging properties in nested, collapsible categories and even sub-properties within properties.  "
            "For all the features of wxPropertyGrid plus the additional features of multiple pages, optional toolbar and description text-box, use wxPropertyGridManager.", 
            550, wx.ClientDC(self))
        info.WebSite = ("http://wxpropgrid.sourceforge.net/cgi-bin/index?page=about", "wxPropertyGrid home page")
        info.Developers = [ "wxPropertyGrid for wxPython demo by Loren Jones\nwxPropertyGrid control by Jaakko Salli  [jmsalli@users.sourceforge.net],\n and volunteers around the world." ]
        info.License = wordwrap("wxPropertyGrid is distributed under the wxWindows License, which is the same license used by wxWidgets itself.", 500, wx.ClientDC(self))
        wx.AboutBox(info)
