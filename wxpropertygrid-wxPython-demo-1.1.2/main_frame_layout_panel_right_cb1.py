
# These are the prerequisites that THIS FILE needs to have in order to run.
import wx
import log
import cStringIO


class My_Choicebook(wx.Choicebook):
    # Called from main_frame_layout_panel_right
    
    def __init__(self, parent = None):
        wx.Choicebook.__init__(self, parent=parent, id=wx.ID_ANY)
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        self.cb_create()
        
        
    def cb_create(self):
        
        self.cb_log_window_create()	# Set up a log window
        
        self.parent.panel_right_label2 = wx.StaticBox(self.parent, -1, "Comments")
        self.parent.panel_right_sizer2 = wx.StaticBoxSizer(self.parent.panel_right_label2, self.mf.orientation_v)
        
        self.parent.panel_right_sizer2.Add(self, 1, wx.EXPAND | wx.ALL, self.mf.controls_border_width)
        
        self.parent.panel_right_sizer1.Add(self.parent.panel_right_sizer2, 5, wx.EXPAND | wx.ALL, self.mf.controls_border_width)
        
        self.parent.SetSizer(self.parent.panel_right_sizer1)
        
        
    def cb_log_window_create(self):
        panel_label = "Log Window"
        panel_icon = 2
        self.parent.log = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.AddPage(page=self.parent.log, text=panel_label, select=False, imageId=panel_icon)
        wx.Log_SetActiveTarget(log.My_Log(self.parent.log))
        
        