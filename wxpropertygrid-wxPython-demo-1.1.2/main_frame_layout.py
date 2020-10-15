
# These are the prerequisites that THIS FILE needs to have in order to run.
import wx
import os
import sys
import log
import wx.lib.splitter
import wx.calendar
import main_frame_layout_panel_right
import main_frame_layout_panel_left

class Layout():

    if False:
        pass
        # Layout
        #
        # fs1(boxsizer_V)
        #   +--- toolbar_sizer(boxsizer_H)  [why not use wx.Frame.ToolBar]???
        #   +--- sp1(MultiSplitterWindow_V)
        #            +--- panel_left(panel)
        #                     +--- panel_left_sizer1(boxsizer_V)
        #                              +--- panel_left_sizer2(staticboxsizer_V)
        #                                       +--- panel_left_nb1(notebook)
        #                                                +--- panel_left_tree1(tree)
        #                              +--- panel_left_sizer3(staticboxsizer_H) - NodeTemplates
        #                                       +--- panel_left_cbo1(choice) - NodeTemplateSelect
        #                                       +--- panel_left_b1(button) - NodeTemplateMaintenance
        #            +--- panel_right(panel)
        #                     +--- panel_right_sizer1(boxsizer_V)
        #                              +--- panel_right_sizer2(staticboxsizer_V)
        #                                       +--- panel_right_nb1(notebook)
        #                                                +--- mutput(output)
        #                                                +--- self.commandlog(commandlog)
        #                                                +--- self.picture(My_Canvas) [wx.PyScrolledWindow]
        #                              +--- panel_right_sizer3(staticboxsizer_H) - PropertyValueTemplates
        #                                       +--- panel_right_cbo1(choice) - PropertyValueTemplateSelect
        #                                       +--- panel_right_b1(button) - PropertyValueTemplateMaintenance
        #   +--- StatusBar(wx.Frame.StatusBar)
        #
    def __init__(self, parent = None):
        self.parent = parent
        # self.icons_create()	# Create icons
        self.icons_create()
        
        # ==================== The Main Sizer ==================
        self.parent.fs1 = wx.BoxSizer(self.parent.orientation_v)
        self.parent.SetSizer(self.parent.fs1)
        
        # ===============Workspace=================
        self.workspace_create()	# Create split window with 2 panels
        
        # status bar
        self.parent.statusbar = self.parent.CreateStatusBar()	# wxPython built-in function, just to confuse you!
        self.parent.statusbar.SetFieldsCount(3)
        # self.parent.statusbar.SetStatusStyles([wx.SB_NORMAL, wx.SB_FLAT, wx.SB_RAISED] )
        # self.parent.statusbar.SetStatusStyles([wx.SB_RAISED, wx.SB_NORMAL, wx.SB_FLAT] )
        self.parent.statusbar.SetStatusStyles([wx.SB_NORMAL, wx.SB_RAISED, wx.SB_NORMAL] )
        self.parent.statusbar.SetStatusWidths([-1, 100, 100])
        status_text = "Status"
        status_field = 1
        self.parent.statusbar.SetStatusText(status_text, status_field)
        status_text = "Ready"
        status_field = 2
        self.parent.statusbar.SetStatusText(status_text, status_field)
        
        
    def icons_create(self):
        main_dir = sys.path[0]
        graphics_dir = os.path.join(main_dir, "", "graphics")
        
        
        self.parent.image_list1 = wx.ImageList(16, 16)
        for name in [ 'flashkard.png', 'mycomputer.png']:
            path_name = os.path.join(graphics_dir, name)
            img = wx.Image(path_name)
            bitmap = wx.BitmapFromImage(img)
            self.parent.image_list1.Add( bitmap )

        
        self.parent.image_list2 = wx.ImageList(16, 16)
        for name in [ 'datasources.png', 'view_text.png', 'database.png', 'query.png', 'package_editors.png', 'databasetable.png', 'querytable.png', 'server.png', 'tables.png']:
            path_name = os.path.join(graphics_dir, name)
            img = wx.Image(path_name)
            bitmap = wx.BitmapFromImage(img)
            self.parent.image_list2.Add( bitmap )
        
        self.parent.image_list3 = wx.ImageList(16, 16)
        for name in [ 'view_text.png', 'package_editors.png', 'kcmpartitions.png' ]:
            path_name = os.path.join(graphics_dir, name)
            img = wx.Image(path_name)
            bitmap = wx.BitmapFromImage(img)
            self.parent.image_list3.Add( bitmap )
        
        self.parent.image_list4 = wx.ImageList(16, 16)
        for name in [ 'kdf.png', 'randr.png', 'kdat.png' ]:
            path_name = os.path.join(graphics_dir, name)
            img = wx.Image(path_name)
            bitmap = wx.BitmapFromImage(img)
            self.parent.image_list4.Add( bitmap )
        
        
    def workspace_create(self):
        # Create two window panes
        self.parent.sp1 = wx.lib.splitter.MultiSplitterWindow(self.parent, style=wx.SP_LIVE_UPDATE)
        
        self.panel_right_create()
        self.panel_left_create()
        
        # Add the panels to the window panes
        self.parent.sp1.AppendWindow(self.parent.panel_left, 10)
        self.parent.sp1.AppendWindow(self.parent.panel_right, 10)
        
        self.parent.fs1.Add(self.parent.sp1, 1, wx.EXPAND)
        
        self.parent.sp1.SetSashPosition(0, 500)
        # self.parent.sp1.SetSashPosition(1, 286)
        
        
    def panel_right_create(self):
        self.parent.panel_right = main_frame_layout_panel_right.Panel_Right(parent = self.parent.sp1)
        
        
    def panel_left_create(self):
        self.parent.panel_left = main_frame_layout_panel_left.Panel_Left(parent = self.parent.sp1)
        
        
        
