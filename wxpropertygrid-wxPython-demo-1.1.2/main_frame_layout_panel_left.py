
# These are the prerequisites that THIS FILE needs to have in order to run.
import wx
import log
import control_inspector


if False:
    pass
    #            +--- panel_left(panel)
    #                     +--- panel_left_sizer1(boxsizer_V)
    #                              +--- panel_left_sizer2(staticboxsizer_V)
    #                                       +--- panel_left_nb1(notebook)
    #                                                +--- panel_left_tree1(tree)
    #                              +--- panel_left_sizer3(staticboxsizer_H) - NodeTemplates
    #                                       +--- panel_left_cbo1(choice) - NodeTemplateSelect
    #                                       +--- panel_left_b1(button) - NodeTemplateMaintenance

class Panel_Left(wx.Panel):
    
    def __init__(self, parent = None):
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        wx.Panel.__init__(self, self.parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour(wx.Color(10, 110, 150))	# dark blue
        self.SetBackgroundColour("light gray")
        self.SetBackgroundColour(wx.Color(217, 224, 240))	# light sky blue (RGB)
        self.SetBackgroundColour("light blue")
        self.panel_left_sizer1 = wx.BoxSizer(self.mf.orientation_v)	# Make a border for the static boxes
        self.property_grid_create()	# Add property grid
        self.SetSizer(self.panel_left_sizer1)
        
        
    def property_grid_create(self):
        self.inspector = control_inspector.Inspector( parent = self )
        self.panel_left_sizer1.Add(self.panel_left_sizer2, 5, wx.EXPAND | wx.ALL, self.mf.controls_border_width)
        
        
        
        
