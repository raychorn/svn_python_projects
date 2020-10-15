
# These are the prerequisites that THIS FILE needs to have in order to run.
import wx
import log
import cStringIO
import main_frame_layout_panel_right_cb1


class Panel_Right(wx.Panel):
    
    def __init__(self, parent = None):
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        wx.Panel.__init__(self, self.parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour("sky blue")
        self.panel_right_sizer1 = wx.BoxSizer(self.mf.orientation_v)	# Make a border for the static boxes
        self.panel_right_log1 = main_frame_layout_panel_right_cb1.My_Choicebook(parent = self)
        
        
