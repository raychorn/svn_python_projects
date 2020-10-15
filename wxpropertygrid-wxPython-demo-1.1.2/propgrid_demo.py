#!/usr/bin/python


import sys
import wx
import wx.propgrid
import main_frame

# The objective with all this separate file stuff is to avoid having to edit this file - ever.

class PGApp(wx.App):
    """Main PG application class"""
    def __init__(self, bln_output_to_window=True, str_output_file_name=None):
        wx.App.__init__(self, redirect=bln_output_to_window, filename=str_output_file_name)
        
    def OnInit(self):
        """Sets everything up"""
        self._v_python_version = get_python_version()
        self._v_wxpython_version = get_wxpython_version()
        self._v_wxpropertygrid_version = get_wxpropertygrid_version()
        
        self._v_app_name = "wxPropertyGrid Demo"
        self._v_major_version = 1
        self._v_revision = 1
        self._v_patch = 2
        self._v_version = ("%i.%i.%i") %(self._v_major_version, self._v_revision, self._v_patch)
        print "Running " + self._v_app_name + " " + self._v_version
        
        self._v_cursor_busy = wx.StockCursor(wx.CURSOR_WAIT)
        self._v_cursor_ready = wx.StockCursor(wx.CURSOR_ARROW)
        
        wx.InitAllImageHandlers()
        
        self.main_frame = main_frame.Main_Frame(self)
        self.main_frame.Show()
        self.SetTopWindow(self.main_frame)
        self.main_frame.Maximize(False)
        return True	# return true to tell wx we started successfully
        
    def OnExit(self):
        return True
        
def get_python_version():
    try:
        python_version = ("%i.%i.%i") % (sys.version_info[0],sys.version_info[1],sys.version_info[2])
        return python_version
        
    except AttributeError, err:
        print "AttributeError"
        print err
        return "0.0.0"
    
    except StandardError, err:
        print "StandardError"
        print err
        return "0.0.0"
    
def get_wxpython_version():
    try:
        wxpython_version = ("%s") % (wx.__version__)
        return wxpython_version
        
    except AttributeError, err:
        print "AttributeError"
        print err
        return "0.0.0"
    
    except StandardError, err:
        print "StandardError"
        print err
        return "0.0.0"
    
def get_wxpropertygrid_version():
    try:
        wxpropertygrid_version = ("%i.%i.%i") % (wx.propgrid.PROPGRID_MAJOR, wx.propgrid.PROPGRID_MINOR, wx.propgrid.PROPGRID_RELEASE)
        return wxpropertygrid_version
        
    except AttributeError, err:
        print "AttributeError"
        print err
        return "0.0.0"
    
    except StandardError, err:
        print "StandardError"
        print err
        return "0.0.0"
    
def main():
    print ("Using Python %s") % (get_python_version())
    print ("Using wxPython %s") % (get_wxpython_version())
    print ("Using wxPropertyGrid %s") % (get_wxpropertygrid_version())
    app = PGApp(bln_output_to_window=False)
    app.MainLoop()
    
main()