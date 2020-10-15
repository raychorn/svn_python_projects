# control_inspector.py
# My own special property control


# Left-click:
# Select the property.
# Right-click:
# Display context menu.
# double-click:
# Open a dialog-box that shows the properties for the selected property.

# Actions for a property:
# Add, Edit, Delete, Insert.
# Change text colour, change background colour.
# Change text font.
# Edit property value, set to unspecified.
# Enable/disable property.
# Hide/Reveal property.
# Toggle display-only status of property.

# Actions for a grid:
# Change margin colour.
# Change line colour.
# Enable/disable tab traversal.
# Change size/position of grid.
# Select page.
# Expand/collapse categories.
# Clear page.

import os
import wx
import datetime
import wx.lib.masked
import wx.propgrid
import StringIO
import cStringIO
import  base64
import control_inspector_property
import control_inspector_property_attribute
import control_inspector_mytime_property
import dialog_property
import ptl

# p_index = 0

# PAGE_LOG = p_index
# p_index = p_index + 1
# PAGE_NOPROP = p_index
# p_index = p_index + 1
# PAGE_NUMERIC = p_index
# p_index = p_index + 1
# PAGE_TEXT = p_index
# p_index = p_index + 1
# PAGE_LOGICAL = p_index
# p_index = p_index + 1
# PAGE_RANGE = p_index
# p_index = p_index + 1
# PAGE_DATE = p_index
# p_index = p_index + 1
# PAGE_TIME = p_index
# p_index = p_index + 1
# PAGE_DATETIME = p_index
# p_index = p_index + 1
# PAGE_RICHTEXT = p_index
# p_index = p_index + 1
# PAGE_PICTURE = p_index
# p_index = p_index + 1
# PAGE_LOOKUP_NUMERIC = p_index
# p_index = p_index + 1
# PAGE_LOOKUP_TEXT = p_index


frame_style_labels = []
frame_style_labels.append( "CAPTION")
frame_style_labels.append( "MINIMIZE")
frame_style_labels.append( "MAXIMIZE")
frame_style_labels.append( "CLOSE_BOX")
frame_style_labels.append( "STAY_ON_TOP")
frame_style_labels.append( "SYSTEM_MENU")
frame_style_labels.append( "RESIZE_BORDER")
frame_style_labels.append( "FRAME_TOOL_WINDOW")
frame_style_labels.append( "FRAME_NO_TASKBAR")
frame_style_labels.append( "FRAME_FLOAT_ON_PARENT")
frame_style_labels.append( "FRAME_SHAPED")

frame_style_values = []
frame_style_values.append( wx.CAPTION )
frame_style_values.append( wx.MINIMIZE )
frame_style_values.append( wx.MAXIMIZE )
frame_style_values.append( wx.CLOSE_BOX )
frame_style_values.append( wx.STAY_ON_TOP )
frame_style_values.append( wx.SYSTEM_MENU )
frame_style_values.append( wx.RESIZE_BORDER )
frame_style_values.append( wx.FRAME_TOOL_WINDOW )
frame_style_values.append( wx.FRAME_NO_TASKBAR )
frame_style_values.append( wx.FRAME_FLOAT_ON_PARENT )
frame_style_values.append( wx.FRAME_SHAPED )

window_style_labels = []
window_style_labels.append( "SIMPLE_BORDER" )
window_style_labels.append( "DOUBLE_BORDER")
window_style_labels.append( "SUNKEN_BORDER")
window_style_labels.append( "RAISED_BORDER")
window_style_labels.append( "NO_BORDER")
window_style_labels.append( "TRANSPARENT_WINDOW")
window_style_labels.append( "TAB_TRAVERSAL")
window_style_labels.append( "WANTS_CHARS")
window_style_labels.append( "NO_FULL_REPAINT_ON_RESIZE")
window_style_labels.append( "VSCROLL")
window_style_labels.append( "ALWAYS_SHOW_SB")
window_style_labels.append( "CLIP_CHILDREN")
window_style_labels.append( "FULL_REPAINT_ON_RESIZE")

window_style_values = []
window_style_values.append( wx.SIMPLE_BORDER )
window_style_values.append( wx.DOUBLE_BORDER)
window_style_values.append( wx.SUNKEN_BORDER)
window_style_values.append( wx.RAISED_BORDER)
window_style_values.append( wx.NO_BORDER)
window_style_values.append( wx.TRANSPARENT_WINDOW)
window_style_values.append( wx.TAB_TRAVERSAL)
window_style_values.append( wx.WANTS_CHARS)
window_style_values.append( wx.NO_FULL_REPAINT_ON_RESIZE)
window_style_values.append( wx.VSCROLL)
window_style_values.append( wx.ALWAYS_SHOW_SB)
window_style_values.append( wx.CLIP_CHILDREN)
window_style_values.append( wx.FULL_REPAINT_ON_RESIZE)

cursor_list = []
cursor_list.append(wx.CURSOR_ARROW) #  A standard arrow cursor.  
cursor_list.append(wx.CURSOR_RIGHT_ARROW)  # A standard arrow cursor pointing to the right.  
cursor_list.append(wx.CURSOR_BLANK)  # Transparent cursor.  
cursor_list.append(wx.CURSOR_BULLSEYE)  # Bullseye cursor.  
cursor_list.append(wx.CURSOR_CHAR)  # Rectangular character cursor.  
cursor_list.append(wx.CURSOR_CROSS)  # A cross cursor.  
cursor_list.append(wx.CURSOR_HAND)  # A hand cursor.  
cursor_list.append(wx.CURSOR_IBEAM)  # An I-beam cursor (vertical line).  
cursor_list.append(wx.CURSOR_LEFT_BUTTON)  # Represents a mouse with the left button depressed.  
cursor_list.append(wx.CURSOR_MAGNIFIER)  # A magnifier icon.  
cursor_list.append(wx.CURSOR_MIDDLE_BUTTON)  # Represents a mouse with the middle button depressed.  
cursor_list.append(wx.CURSOR_NO_ENTRY)  # A no-entry sign cursor.  
cursor_list.append(wx.CURSOR_PAINT_BRUSH)  # A paintbrush cursor.  
cursor_list.append(wx.CURSOR_PENCIL)  # A pencil cursor.  
cursor_list.append(wx.CURSOR_POINT_LEFT)  # A cursor that points left.  
cursor_list.append(wx.CURSOR_POINT_RIGHT)  # A cursor that points right.  
cursor_list.append(wx.CURSOR_QUESTION_ARROW)  # An arrow and question mark.  
cursor_list.append(wx.CURSOR_RIGHT_BUTTON)  # Represents a mouse with the right button depressed.  
cursor_list.append(wx.CURSOR_SIZENESW)  # A sizing cursor pointing NE-SW.  
cursor_list.append(wx.CURSOR_SIZENS)  # A sizing cursor pointing N-S.  
cursor_list.append(wx.CURSOR_SIZENWSE)  # A sizing cursor pointing NW-SE.  
cursor_list.append(wx.CURSOR_SIZEWE)  # A sizing cursor pointing W-E.  
cursor_list.append(wx.CURSOR_SIZING)  # A general sizing cursor.  
cursor_list.append(wx.CURSOR_SPRAYCAN)  # A spraycan cursor.  
cursor_list.append(wx.CURSOR_WAIT)  # A wait cursor.  
cursor_list.append(wx.CURSOR_WATCH)  # A watch cursor.  
cursor_list.append(wx.CURSOR_ARROWWAIT)  # A cursor with both an arrow and an hourglass, (windows.)  


PREFIX_CAT = "cat"
PAGE1 = 0
PAGE2 = 1
PAGE3 = 2
PAGE4 = 3


class AdvImageFileProperty():
    
    def __init__(self):
        wx.propgrid.FileProperty.__init__()
        self._v_wildcard = wx.propgrid.GetDefaultImageWildcard()
        self._v_index = -1
        self._v_image = wx.NullImage()
        self._v_flags = wx.propgrid.SHOW_FULL_FILENAME	# only show names
        
    def DoSetValue(self, new_value):
        pass
        if self._v_image:
            self._v_image = wx.NullImage()
        self._v_image_name = self.GetValueAsString(0)
        if self._v_image_name.length():
            self._v_index = g_myImageNames.Index(self_v_image_name)
            if self._v_index == wx.NotFound:
                g_myImageNames.Add( self._v_image_name )
                # g_myImageArray.Add( new wx.MyImageInfo( self._v_filename.GetFullPath() ) )
                # self._v_index = g_myImageArray.GetCount() - 1
        
        
        
    def GetChoiceInfo(self):
        pass
        
    def SetValueFromInt(self):
        pass
        
    def OnEvent(self):
        pass
        
    def GetImageSize(self):
        pass
        
    def LoadThumbnails(self):
        pass
        
    def OnCustomPaint(self):
        pass
        
    
    
    
    


class Inspector(wx.propgrid.PropertyGridManager):
    def __init__(self, parent=None):
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        
        # Normal Styles
        # PG_ALPHABETIC_MODE = (PG_HIDE_CATEGORIES and PG_AUTO_SORT)
        # PG_AUTO_SORT
        # PG_BOLD_MODIFIED
        # PG_COMPACTOR
        # PG_DEFAULT_STYLE = (
                                                                    # PG_BOLD_MODIFIED and 
                                                                    # PG_SPLITTER_AUTO_CENTER and 
                                                                    # PG_AUTO_SORT and 
                                                                    # PG_HIDE_MARGIN and 
                                                                    # PG_STATIC_SPLITTER and 
                                                                    # PG_TOOLTIPS and 
                                                                    # PG_HIDE_CATEGORIES and 
                                                                    # PG_LIMITED_EDITING and 
                                                                    # TAB_TRAVERSAL and 
                                                                    # PG_TOOLBAR and 
                                                                    # PG_DESCRIPTION
                                                                    # )
        # PG_DESCRIPTION
        # PG_HIDE_CATEGORIES
        # PG_HIDE_MARGIN
        # PG_LIMITED_EDITING
        # PG_SPLITTER_AUTO_CENTER
        # PG_STATIC_LAYOUT = (PG_HIDE_MARGIN and PG_STATIC_SPLITTER)
        # PG_STATIC_SPLITTER
        # PG_TOOLBAR
        # PG_TOOLTIPS
        # PGMAN_DEFAULT_STYLE = (
                                                                    # PG_BOLD_MODIFIED and 
                                                                    # PG_SPLITTER_AUTO_CENTER and 
                                                                    # PG_AUTO_SORT and 
                                                                    # PG_HIDE_MARGIN and 
                                                                    # PG_STATIC_SPLITTER and 
                                                                    # PG_TOOLTIPS and 
                                                                    # PG_HIDE_CATEGORIES and 
                                                                    # PG_LIMITED_EDITING and 
                                                                    # TAB_TRAVERSAL and 
                                                                    # PG_TOOLBAR and 
                                                                    # PG_DESCRIPTION
                                                                    # )
        # TAB_TRAVERSAL (0x00080000)
        
        
        # Extra Styles
        # PG_EX_MODE_BUTTONS
        # PG_EX_AUTO_UNSPECIFIED_VALUES
        # PG_EX_GREY_LABEL_WHEN_DISABLED
        # PG_EX_NATIVE_DOUBLE_BUFFERING
        # PG_EX_HELP_AS_TOOLTIPS
        
        
        inspector_style = wx.propgrid.PG_BOLD_MODIFIED | \
                                        wx.propgrid.PG_SPLITTER_AUTO_CENTER | \
                                        wx.propgrid.PG_AUTO_SORT | \
                                        wx.propgrid.PG_HIDE_MARGIN | \
                                        wx.propgrid.PG_STATIC_SPLITTER | \
                                        wx.propgrid.PG_TOOLTIPS | \
                                        wx.propgrid.PG_HIDE_CATEGORIES | \
                                        wx.propgrid.PG_LIMITED_EDITING | \
                                        0x00080000 | \
                                        wx.propgrid.PG_TOOLBAR | \
                                        wx.propgrid.PG_DESCRIPTION | \
                                        wx.propgrid.PG_EX_MODE_BUTTONS
                                        
                                        
        inspector_style = wx.propgrid.PG_BOLD_MODIFIED | \
                                        wx.propgrid.PG_SPLITTER_AUTO_CENTER | \
                                        wx.propgrid.PG_AUTO_SORT | \
                                        wx.propgrid.PG_LIMITED_EDITING | \
                                        0x00080000 | \
                                        wx.propgrid.PG_TOOLBAR | \
                                        wx.propgrid.PG_COMPACTOR | \
                                        wx.propgrid.PG_DESCRIPTION | \
                                        wx.propgrid.PG_EX_MODE_BUTTONS
                                        
                                        
        inspector_extra_style = wx.propgrid.PG_EX_MODE_BUTTONS | \
                                                    wx.propgrid.PG_EX_GREY_LABEL_WHEN_DISABLED
                                        
                                        
        wx.propgrid.PropertyGridManager.__init__(self, parent, wx.ID_ANY, style=inspector_style )
        
        self.SetExtraStyle(inspector_extra_style)
        
        self.GetGrid().SetVerticalSpacing(3)
        
        self._v_log = self.mf
        self._v_debug = self.mf._v_debug
        self._v_debug_level = self.mf._v_debug_level
        
        self.property = control_inspector_property.PropertyGrid_Property(parent=self)
        
        # self.Property_List = []
        self._v_dict_properties = {}
        self._v_node_id = -1
        self._v_default_exists = False
        self._v_default_property = []
        self._v_default_property.append(0)
        self._v_default_property.append(1)
        self._v_default_page = 0
        self._v_page = -1
        self._v_scheme = []
        self._v_current_property = ""
        
        # self.RegisterAdvancedPropertyClasses()    # Not needed for wxPython
        self.RegisterAdditionalEditors()
        self.RegisterEditor(control_inspector_mytime_property.MyTimeEditor, "clock")
        
        self.populate_with_standard_items()
        
        self.parent.panel_left_label2 = wx.StaticBox(self.parent, -1, "Properties")
        self.parent.panel_left_sizer2 = wx.StaticBoxSizer(self.parent.panel_left_label2, self.mf.orientation_v)
        self.parent.panel_left_sizer2.Add(self, 1, wx.EXPAND | wx.ALL, self.mf.controls_border_width)
        
        
        # Event handling
        
        # To process input from a propertygrid control, use these event handler macros to direct input to member functions that take a wxPropertyGridEvent argument.
        
        # EVT_PG_SELECTED (id, func)	Property is selected.
        # EVT_PG_CHANGED (id, func)	Property value is modified.
        # EVT_PG_HIGHLIGHTED (id, func)	Mouse moves over property. Event's property is NULL if hovered on area that is not a property.
        # EVT_PG_PAGE_CHANGED (id, func)	User changed page in manager.
        # EVT_PG_ITEM_COLLAPSED (id, func)	User collapses a property or category.
        # EVT_PG_ITEM_EXPANDED (id, func)	User expands a property or category.
        # EVT_BUTTON (id, func)	Button in a property editor was clicked. Only occurs if the property doesn't handle button clicks itself.
        # EVT_TEXT (id, func)	wxTextCtrl based editor was updated (but property value was not yet modified)
        # EVT_PG_COMPACT_MODE_ENTERED and EVT_PG_EXPANDED_MODE_ENTERED
        
        self.Bind(wx.propgrid.EVT_PG_SELECTED, self.on_select)
        self.Bind(wx.propgrid.EVT_PG_PAGE_CHANGED, self.on_page_change)
        self.Bind(wx.propgrid.EVT_PG_CHANGED, self.on_change)
        
        # New in version 1.2.11
        if hasattr(wx.propgrid, "EVT_PG_COMPACT_MODE_ENTERED"):
            self.Bind(wx.propgrid.EVT_PG_COMPACT_MODE_ENTERED, self.on_compacted)
        else:
            msg = "The Compact/Expand button requires wxPropertyGrid version 1.2.11 or later to work properly in %s." % self.mf._v_app_name
            print msg
        if hasattr(wx.propgrid, "EVT_PG_EXPANDED_MODE_ENTERED"):
            self.Bind(wx.propgrid.EVT_PG_EXPANDED_MODE_ENTERED, self.on_expanded)
        else:
            pass
            # msg = "The Compact/Expand button requires wxPropertyGrid version 1.2.11 or later to work properly in %s." % self.mf._v_app_name
            # print msg
        
        
        # New in version 1.2.10
        if hasattr(wx.propgrid, "EVT_PG_ITEM_EXPANDED"):
            self.Bind(wx.propgrid.EVT_PG_ITEM_EXPANDED, self.on_item_expanded)
        else:
            msg = "The item collapsed/expanded event requires wxPropertyGrid version 1.2.10 or later to work properly in %s." % self.mf._v_app_name
            print msg
        if hasattr(wx.propgrid, "EVT_PG_ITEM_COLLAPSED"):
            self.Bind(wx.propgrid.EVT_PG_ITEM_COLLAPSED, self.on_item_collapsed)
        else:
            pass
            # msg = "The item collapsed/expanded event requires wxPropertyGrid version 1.2.10 or later to work properly in %s." % self.mf._v_app_name
            # print msg
        
        self.select_default_page()
        self.my_choicebook = self.mf.panel_right.panel_right_log1
        
        
    def add_page1(self):
        func_name = "add_page1"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.add_page( title = "Page 1 - Basic" )
        self.zap()
        self.ClearPage(PAGE1)
        
        
    def add_page2(self):
        func_name = "add_page2"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.add_page( title = "Page 2 - wxWidgets Library Config" )
        self.ClearPage(PAGE2)
        
        
    def add_page3(self):
        func_name = "add_page3"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.add_page( title = "Page 3 - Examples" )
        self.ClearPage(PAGE3)
        
        
    def add_page4(self):
        func_name = "add_page4"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.add_page( title = "Page 4 - " )
        self.zap()
        
        
    def add_cat_appearance(self):
        func_name = "add_cat_appearance"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        self.cat_p_id = self.Append( wx.propgrid.PropertyCategory("Appearance") )
        
        
        
    def add_cat_position(self):
        func_name = "add_cat_position"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("Position") )
        
        
    def add_cat_environment(self):
        func_name = "add_cat_environment"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("Environment") )
        
        
    def add_cat_more_examples(self):
        func_name = "add_cat_more_examples"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("More Examples") )
        
        
    def add_cat_custom_user(self):
        func_name = "add_cat_custom_user"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("Custom User Property") )
        
        
    def add_cat_library_configuration(self):
        func_name = "add_cat_library_configuration"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 1
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("wxWidgets Library Configuration") )
        
        
    def add_cat_examples(self):
        func_name = "add_cat_examples"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 2
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("Examples") )
        
        
    def add_cat_propgrid(self):
        func_name = "add_cat_propgrid"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 2
        self.SelectPage(self._v_page)
        cat_p_id = self.Append( wx.propgrid.PropertyCategory("Property Grid") )
        
        
    def add_appearance_props(self):
        func_name = "add_appearance_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_basic = 0
        cat = "Appearance"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Label", property_label="Label", property_value=self.mf.GetTitle(), help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_DATE, category=cat, property_name="Today", property_label="Today's Date", property_value=wx.DateTime.Now(), help_string=None, low_priority=None, enabled=True, default=False)
        # self.SetPropertyAttribute(self.p_id1, wx.propgrid.PG_DATE_FORMAT, "YY:MM:DD")
        fmt1 = "YY:MM:DD"
        # self.p_id1.SetAttribute( wx.propgrid.PG_DATE_FORMAT, fmt1 )
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_FONT, category=cat, property_name="Grid Font", property_label="Font", property_value=self.GetFont(), help_string="Editing this will change font used in the property grid.", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_CURSOR, category=cat, property_name="Grid Cursor", property_label="Cursor", property_value=0, help_string="", low_priority=None, enabled=True, default=False )
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Margin Colour", property_label="Margin Colour", property_value=self.GetGrid().GetMarginColour(), help_string="", low_priority=None, enabled=True, default=False)
        # self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Cell Colour", property_label="Cell Colour", property_value=self.GetPropertyColour(self.p_id1), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Cell Colour", property_label="Cell Colour", property_value=self.GetGrid().GetCellBackgroundColour(), help_string="", low_priority=None, enabled=True, default=False)
        # self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Cell Text Colour", property_label="Cell Text Colour", property_value=self.GetPropertyTextColour(self.p_id1), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Cell Text Colour", property_label="Cell Text Colour", property_value=self.GetGrid().GetCellTextColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Disabled Cell Text Colour", property_label="Disabled Cell Text Colour", property_value=self.GetGrid().GetCellDisabledTextColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Caption Text Colour", property_label="Caption Text Colour", property_value=self.GetGrid().GetCaptionForegroundColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Caption Colour", property_label="Caption Colour", property_value=self.GetGrid().GetCaptionBackgroundColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Line Colour", property_label="Line Colour", property_value=self.GetGrid().GetLineColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Selection Text Colour", property_label="Selection Text Colour", property_value=self.GetGrid().GetSelectionForegroundColour(), help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, category=cat, property_name="Selection Colour", property_label="Selection Colour", property_value=self.GetGrid().GetSelectionBackgroundColour(), help_string="", low_priority=None, enabled=True, default=False)
        
        self.SetCurrentCategory( cat )
        
        
        if False:
            pass
            # self.cat_p_id.SetLabel("Apricot")
            # self.SetPropertyLabel( self.cat_p_id, "Apricot" )
            
            p2 = self.GetFirstCategory()
            print p2.GetLabel()
            p1 = self.GetPropertyByName(cat)
            print p1.GetLabel()
            if p1 == self.cat_p_id:
                print "Yes"
            else:
                print "No"
            if p1 == p2:
                print "Yes"
            else:
                print "No"
                
            
            cat_name = self.cat_p_id.GetName()
            print cat_name
            
            p1_cat_name = p1.GetName()
            print p1_cat_name
            
            p2_cat_name = p2.GetName()
            print p2_cat_name
            
            
            # wx.MessageBox( message=str(dir(p1)), caption="Category", style=wx.OK | wx.ICON_ERROR )
            
            cat_getid = self.cat_p_id.GetId()
            p1_getid = p1.GetId()
            p2_getid = p2.GetId()
            
            if p1_getid == cat_getid:
                print "Yes"
            else:
                print "No"
            if p1_getid == p2_getid:
                print "Yes"
            else:
                print "No"
                
            
            # These three do the same thing to the same category!
            # self.cat_p_id.SetLabel("Apricot")
            # p1.SetLabel("Apricot p1")
            # p2.SetLabel("Apricot p2")
            
            # I guess "id" can only be used as a reference to a property, not an identifier.
        
        
        if False:
            pass
            # Where-for-toos of FLAGS
            # Common to store several independent yes-or-no flags as a set of bits
            
            # Bitwise Operators
            # Like most languages, Python has four operators that work on bits
            # Name	Symbol	Purpose	                                                              Example
            # And	&	        1 if both bits are 1, 0 otherwise	                  0110 & 1010 = 0010
            # Or	        |	        1 if either bit is 1	                                            0110 & 1010 = 1110
            # Xor	        ^	        1 if the bits are different, 0 if they're the same	0110 & 1010 = 1100
            # Not	        ~	        Flip each bit	                                                    ~0110 = 1001        
            
            
            #                   hex     binary
            MERCURY = 0x01  # 0001
            PHOSPHORUS = 0x02  # 0010
            CHLORINE  = 0x04  # 0100
            
            # Sample contains mercury and chlorine
            sample = MERCURY | CHLORINE
            print 'sample: %04x' % sample
            
            # Check for various elements
            for (flag, name) in [[MERCURY, "mercury"],
                                 [PHOSPHORUS, "phosphorus"],
                                 [CHLORINE, "chlorine"]]:
                if sample & flag:
                    print 'sample contains', name
                else:
                    print 'sample does not contain', name        
        
        
        ws = self.GetWindowStyle()
        
        
        property_name = "Window Styles"
        property_label = "Window Styles"
        labels = window_style_labels + frame_style_labels
        values = window_style_values + frame_style_values
        parent_style = self.parent.GetWindowStyleFlag()
        mf_style = self.mf.GetWindowStyleFlag()
        property_value = parent_style | mf_style
        self.p_id1 = self.Append( wx.propgrid.FlagsProperty(name=property_name, label=property_label, flag_labels=labels, values=values, value=property_value) )
        
        
    def add_position_props(self):
        func_name = "add_position_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_basic = 0
        cat = "Position"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_SIZE, category=cat, property_name="Size", property_label="Size", property_value=self.GetSize(), help_string="Changes width/height of the frame.", low_priority=None, enabled=True, default=False )
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_POINT, category=cat, property_name="Location", property_label="Position", property_value=self.GetPosition(), help_string="Changes position of the top/left corner of the frame.", low_priority=None, enabled=True, default=False )
        
        
    def add_environment_props(self):
        func_name = "add_environment_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_basic = 0
        cat = "Environment"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Operating System", property_label="Operating System", property_value=wx.GetOsDescription(), help_string="This property is simply disabled. Inorder to have label disabled as well, you need to set wxPG_EX_GREY_LABEL_WHEN_DISABLED using SetExtraStyle.", low_priority=None, enabled=False, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="User Id", property_label="User Id", property_value=wx.GetUserId(), help_string="This property is simply disabled. Inorder to have label disabled as well, you need to set wxPG_EX_GREY_LABEL_WHEN_DISABLED using SetExtraStyle.", low_priority=None, enabled=False, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="User Home", property_label="User Home", property_value=wx.GetUserHome(), help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="User Name", property_label="User Name", property_value=wx.GetUserName(), help_string="This property is simply disabled. Inorder to have label disabled as well, you need to set wxPG_EX_GREY_LABEL_WHEN_DISABLED using SetExtraStyle.", low_priority=None, enabled=False, default=False)
        
        
    def add_more_examples_props(self):
        func_name = "add_more_examples_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_basic = 0
        cat = "More Examples"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_FONTDATA, category=cat, property_name="GridFontData", property_label="FontData Property", property_value=None, help_string="This demonstrates wxFontDataProperty class defined in this sample app. It is exactly like wxFontProperty from the library, but also has colour sub-property.", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_DIR, category=cat, property_name="Dir Property", property_label="Dir Property", property_value="C:\\", help_string="This demonstrates wxDirsProperty class defined in this sample app. It is built with WX_PG_IMPLEMENT_ARRAYSTRING_ptl.PROPERTY_WITH_VALIDATOR macro, with custom action (dir dialog popup) defined.", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_DIRS, category=cat, property_name="Dirs Property", property_label="Dirs Property", property_value="C:\\", help_string="This demonstrates wxDirsProperty class defined in this sample app. It is built with WX_PG_IMPLEMENT_ARRAYSTRING_ptl.PROPERTY_WITH_VALIDATOR macro, with custom action (dir dialog popup) defined.", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_LONGSTRING, category=cat, property_name="LongString", property_label="Information", property_value="Editing properties will have immediate effect on this window, and vice versa (at least in most cases, that is). Low priority after Examples means it will be hidden in Compact mode.", help_string=None, low_priority=None, enabled=True, default=False)
        
        
    def add_custom_user_props(self):
        func_name = "add_custom_user_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_basic = 0
        cat = "Custom User Property"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_PARENT, property_datatype_name=ptl.PROPERTY_DATATYPE_CUSTOM, category=cat, property_name="Custom", property_label="Custom Property", property_value=None, help_string="This is example of wxCustomProperty, easily customizable property class. Editing child properties will modify this property in real-time.", low_priority=None, enabled=True, default=False)
        cat = "Custom"  # Special, for the children
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CHILD, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="CustomLabel", property_label="Label", property_value="Custom User Property", help_string="", low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CHILD, property_datatype_name=ptl.PROPERTY_DATATYPE_IMAGEFILE, category=cat, property_name="Image", property_label="Image", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        editors = []
        editors = ["Choice", "ComboBox", "TextCtrlAndButton", "ChoiceAndButton"]
        editor_values = [0, 1, 2, 3]
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CHILD, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, category=cat, property_name="Editor", property_label="Editor", property_value=editors, help_string=None, low_priority=None, enabled=True, default=False, property_choices=editors, property_values=editor_values)
        self._v_current_property = "Editor"
        
        default_choices = []
        default_choices = ["First Choice"]
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CHILD, property_datatype_name=ptl.PROPERTY_DATATYPE_ARRAYSTRING, category=cat, property_name="Choices", property_label="Choices", property_value=0, help_string=None, low_priority=None, enabled=True, default=False )
        
        paint_mode = []
        paint_mode = ["Use Image", "Use Callback"]
        self.p_id1 = self.property.add( page = page_basic, property_type = ptl.PROPERTY_TYPE_CHILD, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, category=cat, property_name="Paint Mode", property_label="Paint Mode", property_value=0, help_string=None, low_priority=None, enabled=True, default=False, property_choices=paint_mode, property_values=[0,1])
        
        
        
    def add_library_configuration_props(self):
        func_name = "add_more_examples_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_config = 1
        cat = "wxWidgets Library Configuration"
        self.SetCurrentCategory( cat )
        
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, category=cat, property_name="wxUSE_GUI", property_label="wxUSE_GUI", property_value=False, help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Compatibility Settings", property_label="Compatibility Settings", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Debugging Settings", property_label="Debugging Settings", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Unicode Support", property_label="Unicode Support", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Global Features", property_label="Global Features", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        self.p_id1 = self.property.add( page = page_config, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, category=cat, property_name="Non-GUI Features", property_label="Non-GUI Features", property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        
        
    def add_examples_props(self):
        func_name = "add_examples_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_examples = 2
        cat = "Examples"
        self.p_id1 = self.Append( wx.propgrid.StringProperty("Label", "Name", "Initial Value") )
        self.p_id1 = self.Append( wx.propgrid.StringProperty("Label1", "Name1", "Initial Value1") )
        self.p_id1 = self.Append( wx.propgrid.StringProperty("Label2", "Name2", "Initial Value2") )
        self.p_id1 = self.Append( wx.propgrid.StringProperty("Label3", "Name3", "Initial Value3") )
        
        self.p_id1 = self.Append( wx.propgrid.BoolProperty("Label4", "Name4", 0) )
        self.SetPropertyAttribute(self.p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
        
        self.p_id1 = self.property.add( page = page_example, property_type = "Category Member", category = "Examples", property_datatype_name=ptl.PROPERTY_DATATYPE_NUMERIC, property_name="IntProperty", property_label="IntProperty", property_value=12345678, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = "IntProperty"
        
        self.Append( wx.propgrid.PropertyCategory("Lamb") )
        self.Delete("Lamb")
        
        self.p_id1 = self.Append( wx.propgrid.StringProperty("Text", "Outside example", "No category") )
        
        property_label = "Car"
        c1 = self.Append( wx.propgrid.PropertyCategory("Level1") )
        pid = self.Append( wx.propgrid.ParentProperty(label = property_label, name = property_label) )
        property_label = "Model"
        self.j = self.AppendIn( pid, wx.propgrid.StringProperty(label = property_label, name = property_label, value="Lamborghini Diablo SV") )
        c2 = self.AppendIn( c1, wx.propgrid.PropertyCategory("Level2") )
        c3 = self.AppendIn( c2, wx.propgrid.PropertyCategory("Level3") )
        
        
        
        
    def add_propgrid_props(self):
        func_name = "add_propgrid_props"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        
        page_basic = 2
        cat = "Property Grid"
        self.SetCurrentCategory( cat )
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Parent Description"
        prop_value = ""
        prop_help = "Information about the 'Parent' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Parent Description"
        prop_name = "Parent Property"
        prop_value = "Pseudo-property that can have sub-properties inserted under itself. It has a textctrl editor that allows editing values of all sub-properties in a one string. In essence, it is a category that has the look and feel of a property, and whose children can be edited via the textctrl."
        prop_help = "Pseudo-property that can have sub-properties inserted under itself. It has a textctrl editor that allows editing values of all sub-properties in a one string. In essence, it is a category that has the look and feel of a property, and whose children can be edited via the textctrl."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Parent Samples"
        prop_value = ""
        prop_help = "Examples of the 'Parent' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_PARENT
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Samples"
        prop_name = "Parent Sample1"
        prop_value = ""
        prop_help = "This is a very simple example of the Parent property.  It has three sub-properties as children."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Sample1"
        prop_name = "Child1"
        prop_value = "1"
        prop_help = "The first child."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Sample1"
        prop_name = "Child2"
        prop_value = "2"
        prop_help = "The second child."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Sample1"
        prop_name = "Child3"
        prop_value = "3"
        prop_help = "The third child."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_PARENT
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Samples"
        prop_name = "Parent Sample2"
        prop_value = ""
        prop_help = "This is a sample of using the Parent property to describe a car."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Parent Sample2"
        prop_name = "Model"
        prop_value = "Lamborghini Diablo SV"
        prop_help = "Italian supercar"
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        cat = "Parent Sample2"
        prop_name = "Engine Size (cc)"
        prop_value = 5707
        prop_help = "Engine displacement"
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_PARENT
        prop_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        cat = "Parent Sample2"
        prop_name = "Speeds"
        prop_value = ""
        prop_help = "Velocity"
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        cat = "Parent Sample2.Speeds"   # Notice use of Property Name Scope: "<property>.<subproperty>"
        prop_name = "Max. Speed (mph)"
        prop_value = 300
        prop_help = "Mach 0.45"
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_FLOAT
        cat = "Parent Sample2.Speeds"
        prop_name = "0-100 mph (sec)"
        prop_value = 3.9
        prop_help = ""
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_FLOAT
        cat = "Parent Sample2.Speeds"
        prop_name = "1/4 mile (sec)"
        prop_value = 8.6
        prop_help = ""
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CHILD
        prop_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        cat = "Parent Sample2"
        prop_name = "Price ($)"
        prop_value = 300000
        prop_help = ""
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        # // Displayed value of "Parent Sample2" property is now:
        # // "Lamborghini Diablo SV; 5707 [300; 3.9; 8.6]; 300000"		
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "String Description"
        prop_value = ""
        prop_help = "Information about the 'String' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "String Description"
        prop_name = "String Property"
        prop_value = "A text property."
        prop_help = "A text property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "String Samples"
        prop_value = ""
        prop_help = "Examples of the 'String' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "String Samples"
        prop_name = "String Sample1"
        prop_value = "Some text."
        prop_help = "This is an example of the String property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Integer Description"
        prop_value = ""
        prop_help = "Information about the 'Integer' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Integer Description"
        prop_name = "Integer Property"
        prop_value = "A signed long integer."
        prop_help = "A signed long integer."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Integer Samples"
        prop_value = ""
        prop_help = "Examples of the 'Integer' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        cat = "Integer Samples"
        prop_name = "Integer Sample1"
        prop_value = 10
        prop_help = "This is an example of the Integer property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Unsigned Integer Description"
        prop_value = ""
        prop_help = "Information about the 'Unsigned Integer' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Unsigned Integer Description"
        prop_name = "Unsigned Integer Property"
        prop_value = "A unsigned long integer."
        prop_help = "A unsigned long integer."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Unsigned Integer Samples"
        prop_value = ""
        prop_help = "Examples of the 'Unsigned Integer' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_UINTEGER
        cat = "Unsigned Integer Samples"
        prop_name = "Unsigned Integer Sample1"
        prop_value = 10
        prop_help = "This is an example of the Unsigned Integer property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Float Description"
        prop_value = ""
        prop_help = "Information about the 'Float' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Float Description"
        prop_name = "Float Property"
        prop_value = "A double-precision floating point."
        prop_help = "A double-precision floating point."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Float Samples"
        prop_value = ""
        prop_help = "Examples of the 'Float' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_FLOAT
        cat = "Float Samples"
        prop_name = "Float Sample1"
        prop_value = 10
        prop_help = "This is an example of the float property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Boolean Description"
        prop_value = ""
        prop_help = "Information about the 'Boolean' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Boolean Description"
        prop_name = "Boolean Property"
        prop_value = "Represents a boolean (logical True/False) value."
        prop_help = "Represents a boolean (logical True/False) value."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Boolean Samples"
        prop_value = ""
        prop_help = "Examples of the 'Boolean' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_BOOLEAN
        cat = "Boolean Samples"
        prop_name = "Boolean Sample1"
        prop_value = True
        prop_help = "This is an example of the Boolean property.  It uses a choice control to set the value."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_BOOLEAN
        cat = "Boolean Samples"
        prop_name = "Boolean Sample2"
        prop_value = True
        prop_help = "This is an example of the Boolean property.  It uses a checkbox control to set the value, because a property attribute is set."
        dict_attributes = {}
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Boolean uses checkbox"
        attribute.number = wx.propgrid.PG_BOOL_USE_CHECKBOX
        attribute.is_set = True
        attribute.value = 1
        attribute.desc = "This attribute applies to the boolean (logical) property datatype.  Setting this attribute will cause the property value to be displayed using a checkbox control.  True will appear as checked, false will appear as unchecked.  Normally, boolean properties use a drop-down choice control that is similar to a combo control."
        attribute.flags_label = "Apply recursively to all children"
        attribute.flags_number = wx.propgrid.PG_RECURSE 
        attribute.flag_is_set = True
        attribute.flags_desc = "Setting this flag will apply this attribute recursively to all the children of the property."
        dict_attributes[wx.propgrid.PG_BOOL_USE_CHECKBOX] = attribute
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False, attributes=dict_attributes)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Long String Description"
        prop_value = ""
        prop_help = "Information about the 'Long String' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Long String Description"
        prop_name = "Long String Property"
        prop_value = "A text value with a button that triggers a small text editor dialog."
        prop_help = "A text value with a button that triggers a small text editor dialog."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Long String Samples"
        prop_value = ""
        prop_help = "Examples of the 'Long String' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Long String Samples"
        prop_name = "Long String Sample1"
        prop_value = "Large amount of text."
        prop_help = "This is an example of the Long String property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Dir Description"
        prop_value = ""
        prop_help = "Information about the 'Dir' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Dir Description"
        prop_name = "Dir Property"
        prop_value = "A text property with a button that invokes a dialog for selecting a directory."
        prop_help = "A text property with a button that invokes a dialog for selecting a directory."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Dir Samples"
        prop_value = ""
        prop_help = "Examples of the 'Dir' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_DIR
        cat = "Dir Samples"
        prop_name = "Dir Sample1"
        prop_value = ""
        prop_help = "This is an example of the Dir property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Dirs Description"
        prop_value = ""
        prop_help = "Information about the 'Dirs' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Dirs Description"
        prop_name = "Dirs Property"
        prop_value = "A text property with a button that invokes a dialog for selecting a directory."
        prop_help = "A text property with a button that invokes a dialog for selecting a directory."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Dirs Samples"
        prop_value = ""
        prop_help = "Examples of the 'Dirs' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_DIRS
        cat = "Dirs Samples"
        prop_name = "Dirs Sample1"
        prop_value = ""
        prop_help = "This is an example of the Dirs property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "File Description"
        prop_value = ""
        prop_help = "Information about the 'File' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "File Description"
        prop_name = "File Property"
        prop_value = "A text property with a button that invokes a dialog for selecting a file."
        prop_help = "A text property with a button that invokes a dialog for selecting a file."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "File Samples"
        prop_value = ""
        prop_help = "Examples of the 'File' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_FILE
        cat = "File Samples"
        prop_name = "File Sample1"
        prop_value = ""
        prop_help = "This is an example of the File property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Enumeration Description"
        prop_value = ""
        prop_help = "Information about the 'Enumeration' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Enumeration Description"
        prop_name = "Enumeration Property"
        prop_value = "Represents a single selection from a list of choices - custom combobox control is used to edit the value."
        prop_help = "Represents a single selection from a list of choices - custom combobox control is used to edit the value."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Enumeration Samples"
        prop_value = ""
        prop_help = "Examples of the 'Enumeration' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_ENUM
        cat = "Enumeration Samples"
        prop_name = "Enumeration Sample1"
        prop_value = 0
        prop_help = "This is an example of the Enumeration property."
        prop_choices = ["Option 0", "Option 1", "Option 2"]
        prop_values = [0, 1, 2]
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False, property_choices=prop_choices, property_values=prop_values)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Flags Description"
        prop_value = ""
        prop_help = "Information about the 'Flags' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Flags Description"
        prop_name = "Flags Property"
        prop_value = "Represents a bit set that fits in a long integer. wxBoolProperty sub-properties are created for editing individual bits. Textctrl is created to manually edit the flags as a text; a continous sequence of spaces, commas and semicolons is considered as a flag id separator."
        prop_help = "Represents a bit set that fits in a long integer. wxBoolProperty sub-properties are created for editing individual bits. Textctrl is created to manually edit the flags as a text; a continous sequence of spaces, commas and semicolons is considered as a flag id separator."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Flags Samples"
        prop_value = ""
        prop_help = "Examples of the 'Flags' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_FLAGS
        cat = "Flags Samples"
        prop_name = "Flags Sample1"
        prop_value = 0
        prop_help = "This is an example of the Flags property."
        prop_choices = ["Flag 0", "Flag 1", "Flag 2"]
        prop_values = [1, 2, 4]
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False, property_choices=prop_choices, property_values=prop_values)
        
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "ArrayString Description"
        prop_value = ""
        prop_help = "Information about the 'ArrayString' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "ArrayString Description"
        prop_name = "ArrayString Property"
        prop_value = "Allows editing of a list of strings in a text control and in a separate dialog."
        prop_help = "Allows editing of a list of strings in a text control and in a separate dialog."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "ArrayString Samples"
        prop_value = ""
        prop_help = "Examples of the 'ArrayString' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_ARRAYSTRING
        cat = "ArrayString Samples"
        prop_name = "ArrayString Sample1"
        prop_value = ""
        prop_help = "This is an example of the ArrayString property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False )
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "ArrayDouble Description"
        prop_value = ""
        prop_help = "Information about the 'ArrayDouble' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "ArrayDouble Description"
        prop_name = "ArrayDouble Property"
        prop_value = "Allows editing of a list of numbers in a text control and in a separate dialog."
        prop_help = "Allows editing of a list of numbers in a text control and in a separate dialog."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "ArrayDouble Samples"
        prop_value = ""
        prop_help = "Examples of the 'ArrayDouble' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_ARRAYDOUBLE # todo
        cat = "ArrayDouble Samples"
        prop_name = "ArrayDouble Sample1"
        prop_value = ""
        prop_help = "This is an example of the ArrayDouble property."
        # self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False )
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Date Description"
        prop_value = ""
        prop_help = "Information about the 'Date' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Date Description"
        prop_name = "Date Property"
        prop_value = "wxDateTime property. Default editor is DatePickerCtrl, although TextCtrl should work as well."
        prop_help = "wxDateTime property. Default editor is DatePickerCtrl, although TextCtrl should work as well."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Date Samples"
        prop_value = ""
        prop_help = "Examples of the 'Date' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_DATE
        cat = "Date Samples"
        prop_name = "Date Sample1"
        prop_value = wx.DateTime.Now()
        prop_help = "This is an example of the Date property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Edit Enumeration Description"
        prop_value = ""
        prop_help = "Information about the 'Edit Enumeration' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Edit Enumeration Description"
        prop_name = "Edit Enumeration Property"
        prop_value = "Represents a string that can be freely edited or selected from list of choices - custom combobox control is used to edit the value."
        prop_help = "Represents a string that can be freely edited or selected from list of choices - custom combobox control is used to edit the value."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Edit Enumeration Samples"
        prop_value = ""
        prop_help = "Examples of the 'Edit Enumeration' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_EDITENUM
        cat = "Edit Enumeration Samples"
        prop_name = "Edit Enumeration Sample1"
        prop_value = 0
        prop_help = "This is an example of the Edit Enumeration property."
        prop_choices = ["Option 0", "Option 1", "Option 2"]
        prop_values = [0, 1, 2]
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False, property_choices=prop_choices, property_values=prop_values)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "MultiChoice Description"
        prop_value = ""
        prop_help = "Information about the 'MultiChoice' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "MultiChoice Description"
        prop_name = "MultiChoice Property"
        prop_value = "Allows editing a multiple selection from a list of strings. This is property is pretty much built around concept of wxMultiChoiceDialog."
        prop_help = "Allows editing a multiple selection from a list of strings. This is property is pretty much built around concept of wxMultiChoiceDialog."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "MultiChoice Samples"
        prop_value = ""
        prop_help = "Examples of the 'MultiChoice' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_MULTICHOICE
        cat = "MultiChoice Samples"
        prop_name = "MultiChoice Sample1"
        prop_value = 0
        prop_help = "This is an example of the MultiChoice property."
        prop_choices = ["Option 0", "Option 1", "Option 2"]
        prop_values = [0, 1, 2]
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False, property_choices=prop_choices, property_values=prop_values)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "ImageFile Description"
        prop_value = ""
        prop_help = "Information about the 'ImageFile' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "ImageFile Description"
        prop_name = "ImageFile Property"
        prop_value = "Like wxFileProperty, but has thumbnail of the image in front of the filename and autogenerates wildcard from available image handlers."
        prop_help = "Like wxFileProperty, but has thumbnail of the image in front of the filename and autogenerates wildcard from available image handlers."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "ImageFile Samples"
        prop_value = ""
        prop_help = "Examples of the 'ImageFile' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_IMAGEFILE
        cat = "ImageFile Samples"
        prop_name = "ImageFile Sample1"
        prop_value = ""
        prop_help = "This is an example of the ImageFile property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "AdvancedImageFile Description"
        prop_value = ""
        prop_help = "Information about the 'AdvancedImageFile' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "AdvancedImageFile Description"
        prop_name = "AdvancedImageFile Property"
        prop_value = "Like ImageFileProperty, but also has a drop-down for recent image selection"
        prop_help = "Like ImageFileProperty, but also has a drop-down for recent image selection"
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "AdvancedImageFile Samples"
        prop_value = ""
        prop_help = "Examples of the 'AdvancedImageFile' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_IMAGEFILE
        cat = "AdvancedImageFile Samples"
        prop_name = "AdvancedImageFile Sample1"
        prop_value = ""
        prop_help = "This is an example of the AdvancedImageFile property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Colour Description"
        prop_value = ""
        prop_help = "Information about the 'Colour' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Colour Description"
        prop_name = "Colour Property"
        prop_value = "Represents wxColour. wxButton is used to trigger a colour picker dialog."
        prop_help = "Represents wxColour. wxButton is used to trigger a colour picker dialog."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Colour Samples"
        prop_value = ""
        prop_help = "Examples of the 'Colour' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_COLOUR
        cat = "Colour Samples"
        prop_name = "Colour Sample1"
        prop_value = ""
        prop_help = "This is an example of the Colour property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "SystemColour Description"
        prop_value = ""
        prop_help = "Information about the 'SystemColour' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "SystemColour Description"
        prop_name = "SystemColour Property"
        prop_value = "Represents wxColour and a system colour index. wxChoice is used to edit the value. Drop-down list has color images."
        prop_help = "Represents wxColour and a system colour index. wxChoice is used to edit the value. Drop-down list has color images."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "SystemColour Samples"
        prop_value = ""
        prop_help = "Examples of the 'SystemColour' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR
        cat = "SystemColour Samples"
        prop_name = "SystemColour Sample1"
        prop_value = wx.Colour(0, 0, 0)
        prop_help = "This is an example of the SystemColour property."
        # self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Font Description"
        prop_value = ""
        prop_help = "Information about the 'Font' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Font Description"
        prop_name = "Font Property"
        prop_value = "Represents wxFont. Various sub-properties are used to edit individual subvalues."
        prop_help = "Represents wxFont. Various sub-properties are used to edit individual subvalues."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Font Samples"
        prop_value = ""
        prop_help = "Examples of the 'Font' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_FONT
        cat = "Font Samples"
        prop_name = "Font Sample1"
        prop_value = self.GetGrid().GetFont()
        prop_help = "This is an example of the Font property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "FontData Description"
        prop_value = ""
        prop_help = "Information about the 'FontData' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "FontData Description"
        prop_name = "FontData Property"
        prop_value = "Represents wxFont. Various sub-properties are used to edit individual subvalues."
        prop_help = "Represents wxFont. Various sub-properties are used to edit individual subvalues."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "FontData Samples"
        prop_value = ""
        prop_help = "Examples of the 'FontData' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_FONT
        cat = "FontData Samples"
        prop_name = "FontData Sample1"
        prop_value = self.GetGrid().GetFont()
        prop_help = "This is an example of the FontData property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Cursor Description"
        prop_value = ""
        prop_help = "Information about the 'Cursor' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Cursor Description"
        prop_name = "Cursor Property"
        prop_value = "Represents a wxCursor. wxChoice is used to edit the value. Drop-down list has cursor images under some (wxMSW) platforms."
        prop_help = "Represents a wxCursor. wxChoice is used to edit the value. Drop-down list has cursor images under some (wxMSW) platforms."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Cursor Samples"
        prop_value = ""
        prop_help = "Examples of the 'Cursor' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_CURSOR
        cat = "Cursor Samples"
        prop_name = "Cursor Sample1"
        prop_value = 0
        prop_help = "This is an example of the Cursor property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Size Description"
        prop_value = ""
        prop_help = "Information about the 'Size' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Size Description"
        prop_name = "Size Property"
        prop_value = "Represents a wxSize."
        prop_help = "Represents a wxSize."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Size Samples"
        prop_value = ""
        prop_help = "Examples of the 'Size' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_SIZE
        cat = "Size Samples"
        prop_name = "Size Sample1"
        prop_value = wx.Size(10, 20)
        prop_help = "This is an example of the Size property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Point Description"
        prop_value = ""
        prop_help = "Information about the 'Point' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Point Description"
        prop_name = "Point Property"
        prop_value = "Represents a wxPoint."
        prop_help = "Represents a wxPoint."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Point Samples"
        prop_value = ""
        prop_help = "Examples of the 'Point' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_POINT
        cat = "Point Samples"
        prop_name = "Point Sample1"
        prop_value = wx.Point(14, 15)
        prop_help = "This is an example of the Point property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        cat = "Property Grid"
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        prop_cat = cat
        prop_name = "Custom Description"
        prop_value = ""
        prop_help = "Information about the 'Custom' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        cat = "Custom Description"
        prop_name = "Custom Property"
        prop_value = "A customizable property class with string data type. Value image, Editor class, and children can be modified."
        prop_help = "A customizable property class with string data type. Value image, Editor class, and children can be modified."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY
        prop_datatype = ptl.PROPERTY_DATATYPE_TEXT
        cat = "Property Grid"
        prop_name = "Custom Samples"
        prop_value = ""
        prop_help = "Examples of the 'Custom' property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        prop_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        prop_datatype = ptl.PROPERTY_DATATYPE_CUSTOM
        cat = "Custom Samples"
        prop_name = "Custom Sample1"
        prop_value = ""
        prop_help = "This is an example of the Custom property."
        self.p_id1 = self.property.add( page = page_basic, property_type = prop_type, property_datatype_name=prop_datatype, category=cat, property_name=prop_name, property_label=prop_name, property_value=prop_value, help_string=prop_help, low_priority=None, enabled=True, default=False)
        
        
        
        
        
        
    def populate_with_standard_items(self):
        func_name = "populate_with_standard_items"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        
        self.add_page1()
        
        self.add_cat_appearance()
        self.add_appearance_props()
        
        self.add_cat_position()
        self.add_position_props()
        
        self.add_cat_environment()
        self.add_environment_props()
        
        self.add_cat_more_examples()
        self.add_more_examples_props()
        
        self.add_cat_custom_user()
        self.add_custom_user_props()
        
        
        
        
        self.add_page2()
        
        self.add_cat_library_configuration()
        self.add_library_configuration_props()
        
        
        
        
        
        self.add_page3()
        
        self.add_cat_propgrid()
        self.add_propgrid_props()
        
        
        
        
        
        
        page_basic = 0
        
        
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        self.SetSplitterLeft()
        
        
    def zap(self):
        func_name = "zap"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page = 0
        for page in range( self.GetPageCount() ):
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "clear page: %d ") % ( page, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self.ClearPage(page)
        
        
    def add_page(self, title = "New Page", icon_name = "" ):
        func_name = "add_page"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        bmp = None
        self._v_page = self.GetPageCount()
        
        if title == "New Page":
            title = "Page %d" % self._v_page
            
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "title: %s") % ( title, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        bmp = self.import_file( file_name = icon_name )
        self.AddPage( title, bmp )
        self._v_page = self.GetPageCount() - 1
        self._v_scheme.append("Standard")
        
        
    def insert_page(self, title = "New Page", icon_name = "" ):
        func_name = "insert_page"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        allow_page_insert = False
        if allow_page_insert:
            bmp = None
            # self._v_page = self.GetPageCount()
            
            if title == "New Page":
                title = "Page %d" % self._v_page
                
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "title: %s") % ( title, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            bmp = self.import_file( file_name = icon_name )
            self._v_page = self.InsertPage( self._v_page, title, bmp )
            # self._v_page = self.GetPageCount() - 1
            
        else:
            wx.MessageBox( message="Page insert is not allowed, due to a limitation of wxToolbar.", caption="Insert Page", style=wx.OK | wx.ICON_ERROR )
            
            
            
    def delete_page(self ):
        func_name = "delete_page"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if (self._v_page > -1) and (self._v_page < self.GetPageCount()):
            self.RemovePage(self._v_page)
            self._v_page = self._v_page - 1 # Move to the left
            if self._v_page < 0:
                if self.GetPageCount() > 0: # Are there more pages to the right?
                    self._v_page = 0
                else:
                    self._v_page = self.GetPageCount() - 1  # Don't let _v_page go below -1
            self.SelectPage(self._v_page)
        
        
    def add_category(self, label="", name=None, help=None, colour_txt=None, colour_bg=None ):
        func_name = "add_category"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        if not name:
            name = label
        category_id = self.AppendCategory( label = label, name = name )
        self.set_property_attributes(property_id = category_id, help_string=help, colour_txt=colour_txt, colour_bg=colour_bg )
        self.Refresh()
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "%s ") % ( label, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        
        
    def add_list_of_categories(self):
        func_name = "add_list_of_categories"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        
        for property_datatype in ptl.LIST_PROPERTY_DATATYPE:
            category_id = self.Append( wx.propgrid.PropertyCategory( property_datatype ) )
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "%s ") % ( property_datatype, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        
    def on_select(self, event):
        func_name = "on_select"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        
        p = event.GetProperty()
        
        if p:
                
                # What information is available about a property?
                
                # First, make sure u can treat it like a property.
                is_cat = self.IsPropertyCategory(p) # Categories need special treatment.
                
                # Label
                # -------------------------------------------------------------------------------------------
                property_label = str(self.GetPropertyLabel(p))
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_label: [%s]") % ( property_label, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Name
                # -------------------------------------------------------------------------------------------
                property_name = str(event.GetPropertyName())
                # print ('on_select: property name: %s' % (property_name))
                self._v_current_property = property_name
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_name: [%s]") % ( property_name, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Index
                # -------------------------------------------------------------------------------------------
                property_index = str(self.GetPropertyIndex(p))
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_index: [%s]") % ( property_index, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Data Type (U need the datatype b4 u get the value)
                # -------------------------------------------------------------------------------------------
                property_datatype = "None"
                property_datatype_short = "None"
                if is_cat:
                    property_datatype = "Category"
                else:
                    property_datatype = str(self.GetPropertyClassName(p))
                    ##property_datatype_short = self.GetPropertyShortClassName(p)     # Encoding error
                    property_datatype_short = "n/a"
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_datatype: [%s] (%s)") % ( property_datatype, property_datatype_short )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Value Type
                # -------------------------------------------------------------------------------------------
                # Method 1 for getting property value type
                property_valuetype = self.GetPVTN(p)
                
                # Method 2 for getting property value type
                base_type = self.GetPropertyValueType(p)
                property_valuetype = base_type.GetTypeName()
                
                # Method 3 for getting property value type
                property_valuetype = self.GetPropertyValueType(p).GetTypeName()
                
                property_valuetype = str(property_valuetype)
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_valuetype: [%s]") % ( property_valuetype, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Value (U need the valuetype b4 u get the value - makes sense doesn't it.)
                # -------------------------------------------------------------------------------------------------------
                # if is_cat:
                    # property_value = "n/a"
                # else:
                    # if property_datatype == "wxParentProperty": # Is seems that GetPropertyValue explodes on wxParentProperty.
                        # property_value = "n/a"
                    # else:
                        # property_value = str(self.GetPropertyValue(p))
                if property_valuetype == "null":
                    property_value = "n/a"
                else:
                    property_value = str(self.GetPropertyValue(p))
                if len(property_value) > 20:
                    property_value = property_value[0:19]
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_value: [%s]") % ( property_value, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Default Value
                # -------------------------------------------------------------------------------------------
                if property_valuetype == "null":
                    property_default_value = "n/a"  # Null valuetypes don't have default values.
                else:
                    # Tricky: handle variant
                    property_default_value = "variant"
                    if property_valuetype == "string" or property_valuetype == "long":
                        property_default_value = self.GetPropertyValueType(p).GetDefaultValue()
                        property_default_value = str(property_default_value)
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_default_value: [%s]") % ( property_default_value, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Priority
                # -------------------------------------------------------------------------------------------
                priority_number = self.GetPropertyPriority(p)
                if priority_number == 1:
                    property_priority = "Low"
                elif priority_number == 2:
                    property_priority = "High"
                else:
                    property_priority = "Invalid"
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_priority: [%s]") % ( property_priority, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Parent
                # -------------------------------------------------------------------------------------------
                root = self.GetRoot()
                parent = self.GetPropertyParent(p)
                if parent:
                    if parent == root:
                        property_parent = "Root"
                    else:
                        property_parent = str(self.GetPropertyName(parent))
                else:
                    property_parent = "None"
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_parent: [%s]") % ( property_parent, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
                
                # Attributes
                # -------------------------------------------------------------------------------------------
                property_attributes = str(self.GetPropertyAttributes(p, flagmask = 0xFFFF))
                if self._v_debug and self._v_debug_level > 6999:
                    msg = ( "property_attributes: [%s]") % ( property_attributes, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                
                status_text = ( "LABEL: %s   INDEX: %s   NAME: %s   VALUE: %s   DATATYPE: %s   PRIORITY: %s   PARENT: %s") % ( property_label, property_index, property_name, property_value, property_datatype, property_priority, property_parent )
                status_field = 0
                self.mf.statusbar.SetStatusText(status_text, status_field)
                
                
        else:
            if self._v_debug and self._v_debug_level > 500:
                msg = "Nothing selected"
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
            
    def on_page_change(self, event):
        func_name = "on_page_change"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        new_page = self.GetSelectedPage()
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( ("switching from page: %d to page: %d" ) % (self._v_page, new_page) )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self._v_page = new_page
        
        menu_bar = self.mf.GetMenuBar()
        title = "Format"
        position = menu_bar.FindMenu(title)
        menu = menu_bar.GetMenu(position)
        menu_items = menu.GetMenuItems()
        for menu_item in menu_items:
            if menu_item.GetLabel() == "Colour Scheme":
                submenu = menu_item.GetSubMenu()
                submenu_items = submenu.GetMenuItems()
                for submenu_item in submenu_items:
                    if submenu_item.GetLabel() == self._v_scheme[self._v_page]:
                        submenu_item.Check()
        
        propertygrid_page = self.GetPage( self._v_page )
        self.SetTargetPage(self._v_page)
        p_id = propertygrid_page.GetPropertyByName(self._v_current_property)
        if p_id:
            self.SelectProperty(p_id)
            self.EnsureVisible(p_id)
        
        
    def select_default_page(self):
        func_name = "select_default_page"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = self._v_default_page
        self.SelectPage(self._v_page)
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "page: %d ") % ( self._v_page, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        
        
    def on_page_add(self, event):
        func_name = "on_page_add"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dlg = dialog_property.Dialog_Property_Create(page = -1, category=None, datatype=None, parent=self)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            pass
            prop_label = dlg.property_label
            prop_image_file_name = dlg.property_image_file_name
            
            self.add_page(title=prop_label, icon_name=prop_image_file_name)
            
        else:
            pass
            # wx.MessageBox( "dialog exited without selecting a database to open.", "Info")
        dlg.Destroy()
        
    def on_page_insert(self, event):
        func_name = "on_page_insert"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        allow_page_insert = False
        if allow_page_insert:
            dlg = dialog_property.Dialog_Property_Create(page = -1, category=None, datatype=None, parent=self)
            retval = dlg.ShowModal()
            if retval == wx.ID_OK:
                pass
                prop_label = dlg.property_label
                prop_image_file_name = dlg.property_image_file_name
                
                self.insert_page(title=prop_label, icon_name=prop_image_file_name)
                
            else:
                pass
                # wx.MessageBox( "dialog exited without selecting a database to open.", "Info")
            dlg.Destroy()
                
        else:
            wx.MessageBox( message="Page insert is not allowed, due to a limitation of wxToolbar.", caption="Insert Page", style=wx.OK | wx.ICON_ERROR )
            
            
        
    def on_page_edit(self, event):
        func_name = "on_page_edit"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dlg = dialog_property.Dialog_Property_Create(page = self._v_page, category=None, datatype=None, parent=self)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            pass
            prop_label = dlg.property_label
            prop_image_file_name = dlg.property_image_file_name
            
            self.add_page(title=prop_label, icon_name=prop_image_file_name)
            
        else:
            pass
            # wx.MessageBox( "dialog exited without selecting a database to open.", "Info")
        dlg.Destroy()
        
    def on_page_delete(self, event):
        func_name = "on_page_delete"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        self.delete_page()
        
    def on_page_clear(self, event):
        func_name = "on_page_clear"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        self.ClearPage(self._v_page)
        
    def on_category_collapse(self, event):
        func_name = "on_category_collapse"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.GetSelectedProperty()
        if p_id:
            self.Collapse(p_id)
        
        
    def on_category_expand(self, event):
        func_name = "on_category_expand"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.GetSelectedProperty()
        if p_id:
            self.Expand(p_id)
        
        
    def select_default_property(self):
        func_name = "select_default_property"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # Uses page and property to select the default property.
        if self.GetPageCount() > 0:
            self.select_default_page()
            if self._v_page == 0:
                self.default_property_select()
            elif self._v_page == 1:
                self.default_property_select()
            else:
                self.default_property_select()
        
        
    def default_property_select(self):
        func_name = "default_property_select"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_default_property[self._v_page]:
            self.select_property( property_id = self._v_default_property[self._v_page] )
        
        
    def select_property(self, property_id):
        func_name = "select_property"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "property_id: %s") % ( property_id, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self.SelectProperty( property_id, True )	# Two SelectProperty, why won't one due the job?
        self.SelectProperty( property_id, True )	# I think because i added the same property to page 0 and page 1
        self.EnsureVisible( property_id )
        p_id = self.GetSelectedProperty()
        if p_id:
            property_name = self.GetPropertyName( p_id )
            self._v_current_property = property_name
        
        

    def import_file(self, file_name="tmp.bmp", img_type=wx.BITMAP_TYPE_BMP):
        func_name = "import_file"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # data = open(opj('bitmaps/image.png'), "rb").read()
        # stream = cStringIO.StringIO(data)
        # bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        
        self._v_bmp = wx.EmptyBitmap(100, 100, -1)	# wx Bitmap object
        self._v_bmp = wx.NullBitmap	# wx Bitmap object
        
        # f_name = self.opj(file_name)		# does not work
        f_name = file_name
        if len(f_name) > 0:
            if os.path.exists(f_name):
                file = open(f_name, "rb")	# Open file in read-binary mode.
                file_data = file.read()
                self._v_data = file_data
                stream = cStringIO.StringIO(file_data)
                self._v_img = wx.ImageFromStream(stream)
                self._v_bmp = wx.BitmapFromImage(self._v_img)
                mask = wx.Mask(self._v_bmp, wx.BLUE)
                self._v_bmp.SetMask(mask)
                self._v_width = self._v_img.GetWidth()
                self._v_height = self._v_img.GetHeight()
                
                if img_type>-1:
                    
                    pass
                    
                else:
                    msg = "Invalid image type"
                    if self._v_debug and self._v_debug_level > 5999:
                        self._v_log.write(("%s:%s: %s") % (self.__class__, func_name, msg))
                    self._v_bmp = wx.EmptyBitmap(100, 100, -1)	# wx Bitmap object
                    self._v_bmp = wx.NullBitmap	# wx Bitmap object
            else:
                    msg = "File does not exist."
                    if self._v_debug and self._v_debug_level > 5999:
                        self._v_log.write(("%s:%s: %s") % (self.__class__, func_name, msg))
                    self._v_bmp = wx.NullBitmap	# wx Bitmap object
                
        return self._v_bmp
        
        
    def on_show_all(self, event):
        func_name = "on_show_all"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # wx.MessageBox(str(dir(event)))
        # print "Checked", str(event.IsChecked()), str(event.Checked())
        # print "Selection", str(event.GetSelection()), event.Selection
        # print "String", str(event.GetString()), event.String
        # print "Id", str(event.GetId()), str(event.Id)
        
        self.Compact(not event.IsChecked())
        
        
        
    def on_expand(self, event):
        pass
        func_name = "on_expand"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # wx.MessageBox(str(dir(event)))
        
        
        
    def on_scheme(self, event):
        func_name = "on_scheme"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        
        menu_bar = self.mf.GetMenuBar()
        id = event.GetId()
        item = menu_bar.FindItemById(id)
        item_txt = item.GetLabel()
        
        if item_txt == "Standard":
            self._v_scheme[self._v_page] = "Standard"
            
            r = 192
            g = 192
            b = 192
            default_grey_1 = wx.Colour(r, g, b)
            grid = self.GetGrid()
            
            # Build a list of categories
            lst_category = []
            p_id = self.GetFirstCategory()
            if p_id:
                lst_category.append(p_id)
                while p_id:
                    p_id = self.GetNextCategory(p_id)
                    if p_id:
                        lst_category.append(p_id)
                    
            self.Freeze()
            grid.SetMarginColour( default_grey_1 )
            grid.SetLineColour( default_grey_1 )
            grid.SetCaptionBackgroundColour( default_grey_1 )
            for category_id in lst_category:
                self.SetPropertyColourToDefault( category_id )
                # self.SetPropertyColourToDefault( self.GetPropertyByName(self.GetPropertyName(category_id)) )
                # self.SetPropertyColourToDefault( self.GetPropertyByName("Environment") )
                # self.SetPropertyColourToDefault( self.GetPropertyByName("Position") )
                # self.SetPropertyColourToDefault( self.GetPropertyByName("More Examples") )
            self.Thaw()
            self.Refresh()
        elif item_txt == "White":
            self._v_scheme[self._v_page] = "White"
            r = 212
            g = 208
            b = 200
            my_grey_1 = wx.Colour(r, g, b)
            r = 113
            g = 111
            b = 100
            my_grey_3 = wx.Colour(r, g, b)
            self.Freeze()
            grid = self.GetGrid()
            grid.SetMarginColour( wx.WHITE )
            grid.SetCaptionBackgroundColour( wx.WHITE )
            grid.SetCellBackgroundColour( wx.WHITE )
            grid.SetCellTextColour( my_grey_3 )
            grid.SetLineColour( my_grey_1 )
            self.Thaw()
            
        elif item_txt == ".Net":
            self._v_scheme[self._v_page] = ".Net"
            r = 212
            g = 208
            b = 200
            my_grey_1 = wx.Colour(r, g, b)
            r = 236
            g = 233
            b = 216
            my_grey_2 = wx.Colour(r, g, b)
            self.Freeze()
            grid = self.GetGrid()
            grid.SetMarginColour( my_grey_1 )
            grid.SetCaptionBackgroundColour( my_grey_1 )
            # grid.SetCellBackgroundColour( wx.WHITE )
            # grid.SetCellTextColour( my_grey_3 )
            grid.SetLineColour( my_grey_1 )
            self.Thaw()
            
        elif item_txt == "Cream":
            self._v_scheme[self._v_page] = "Cream"
            
            r = 212
            g = 208
            b = 200
            my_grey_1 = wx.Colour(r, g, b)
            r = 241
            g = 239
            b = 226
            my_grey_2 = wx.Colour(r, g, b)
            r = 113
            g = 111
            b = 100
            my_grey_3 = wx.Colour(r, g, b)
            self.Freeze()
            grid = self.GetGrid()
            grid.SetMarginColour( wx.WHITE )
            grid.SetCaptionBackgroundColour( wx.WHITE )
            grid.SetCellBackgroundColour( my_grey_2 )
            grid.SetCellTextColour( my_grey_3 )
            grid.SetLineColour( my_grey_1 )
            self.Thaw()
            
        elif item_txt == "Category Specific":
            
            self._v_scheme[self._v_page] = "Category Specific"
            
            r = 192
            g = 192
            b = 192
            default_grey_1 = wx.Colour(r, g, b)
            grid = self.GetGrid()
            
            # Build a colour matrix
            rainbow = []
            
            r = 255
            g = 0
            b = 0
            caption = wx.Colour(r, g, b)
            
            r = 255
            g = 255
            b = 183
            background = wx.Colour(r, g, b)
            
            r = 255
            g = 0
            b = 183
            text = wx.Colour(r, g, b)
            
            cat_colour = [caption, background, text]
            rainbow.append(cat_colour)
            
            r = 230
            g = 118
            b = 0
            caption = wx.Colour(r, g, b)
            
            r = 255
            g = 226
            b = 190
            background = wx.Colour(r, g, b)
            
            r = 255
            g = 0
            b = 190
            text = wx.Colour(r, g, b)
            
            cat_colour = [caption, background, text]
            rainbow.append(cat_colour)
            
            r = 0
            g = 128
            b = 64
            caption = wx.Colour(r, g, b)
            r = 208
            g = 240
            b = 175
            background = wx.Colour(r, g, b)
            r = 0
            g = 98
            b = 0
            text = wx.Colour(r, g, b)
            
            cat_colour = [caption, background, text]
            rainbow.append(cat_colour)
            
            r = 0
            g = 0
            b = 128
            caption = wx.Colour(r, g, b)
            r = 172
            g = 237
            b = 255
            background = wx.Colour(r, g, b)
            r = 172
            g = 0
            b = 255
            text = wx.Colour(r, g, b)
            
            cat_colour = [caption, background, text]
            rainbow.append(cat_colour)
            
            # page = 0    # I hate this!
            # self.SelectPage(page)
            
            # Build a list of categories
            lst_category = []
            p_id = self.GetFirstCategory()
            if p_id:
                lst_category.append(p_id)
                while p_id:
                    p_id = self.GetNextCategory(p_id)
                    if p_id:
                        lst_category.append(p_id)
                    
            # Colour my world
            # Cycle thru the colour matrix, applying color to a category.
            group_count = len(rainbow)
            colour_group = 0
            self.Freeze()
            grid.SetMarginColour( default_grey_1 )
            grid.SetLineColour( default_grey_1 )
            grid.SetCaptionBackgroundColour( default_grey_1 )
            for category_id in lst_category:
                if colour_group > group_count-1:
                    colour_group = 0
                grp = rainbow[colour_group]
                colour_caption, colour_background, colour_text = grp[0], grp[1], grp[2]
                self.SetCaptionTextColour( category_id, colour_caption )
                self.SetPropertyBackgroundColour( category_id, colour_background )
                self.SetPropertyTextColour( category_id, colour_text )
                if self.GetChildrenCount(category_id):
                    c_id = self.GetFirstChild(category_id)
                    # msg = ( "Category name: %s property: %s") % ( self.GetPropertyName(category_id), self.GetPropertyName(c_id))
                    # self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    self.SetPropertyBackgroundColour( c_id, colour_background )
                    self.SetPropertyTextColour( c_id, colour_text )
                colour_group = colour_group + 1
            self.Thaw()
            self.Refresh()
            
        else:
            print "Invalid scheme."
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "Invalid scheme: %s ") % ( item_txt, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            
            
    def on_iterate_categories(self, event):
        pass
        func_name = "on_iterate_categories"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.GetFirstCategory()
        if p_id:
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "Category name: %s ") % ( self.GetPropertyName(p_id), )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
            while p_id:
                p_id = self.GetNextCategory(p_id)
                if p_id:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "Category name: %s ") % ( self.GetPropertyName(p_id), )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
            
            
            
    def on_iterate_properties(self, event):
        pass
        func_name = "on_iterate_properties"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.GetFirstProperty()
        if p_id:
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "Property name: %s ") % ( self.GetPropertyName(p_id), )
                msg = ( "Property name: %s, class name: %s, short class name:%s ") % ( self.GetPropertyName(p_id), self.GetPropertyClassName(p_id), self.GetPropertyShortClassName(p_id) )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
            while p_id:
                p_id = self.GetNextProperty(p_id)
                if p_id:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "Property name: %s, class name: %s, short class name:%s ") % ( self.GetPropertyName(p_id), self.GetPropertyClassName(p_id), self.GetPropertyShortClassName(p_id) )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
            
        
        
    def on_iterate_visible_properties(self, event):
        pass
        func_name = "on_iterate_visible_properties"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # ----------------------------------------------------------------------
        # GetFirstVisible generates an error, not sure why.
        # ----------------------------------------------------------------------
            if self._v_debug and self._v_debug_level > 5999:
                msg = "The feature is currently not available."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
        
        # p_id = self.GetFirstVisible()
        # if p_id:
            # if self._v_debug and self._v_debug_level > 5999:
                # msg = ( "Property name: %s ") % ( self.GetPropertyName(p_id), )
                # self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
            # while p_id:
                # p_id = self.GetNextVisible(p_id)
                # if p_id:
                    # if self._v_debug and self._v_debug_level > 5999:
                        # msg = ( "Property name: %s ") % ( self.GetPropertyName(p_id), )
                        # self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
            
        
        
    def on_collapse_all(self, event):
        func_name = "on_collapse_all"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.CollapseAll()
        
        
    def on_expand_all(self, event):
        func_name = "on_expand_all"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.ExpandAll()
        
        
    def on_freeze(self, event):
        func_name = "on_freeze"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self.IsFrozen():
            self.Thaw()
        else:
            self.Freeze()
        
        
    def on_hide_margin(self, event):
        func_name = "on_hide_margin"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if event.IsChecked():
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Hide the margin."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Hide the margin
            flags = self.GetWindowStyleFlag()
            flag = wx.propgrid.PG_HIDE_MARGIN
            self.SetWindowStyleFlag( flags | flag ) # "|" is bitwise "or"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            self.update_menu(menu=menu)
            
        else:
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Reveal the margin."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Reveal the margin
            flags = self.GetWindowStyleFlag()
            flag = ~wx.propgrid.PG_HIDE_MARGIN  # "~" is "invert bits"
            self.SetWindowStyleFlag( flags & flag ) # "&" is bitwise "and"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            menu_items = menu.GetMenuItems()
            for menu_item in menu_items:
                if menu_item.GetLabel() == "Static Layout":
                    menu_item.Check(check=False)
            
        
        
    def on_static_splitter(self, event):
        func_name = "on_static_splitter"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if event.IsChecked():
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Freeze the splitter."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Freeze the splitter
            flags = self.GetWindowStyleFlag()
            flag = wx.propgrid.PG_STATIC_SPLITTER
            self.SetWindowStyleFlag( flags | flag ) # "|" is bitwise "or"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            self.update_menu(menu=menu)
            
        else:
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Thaw the splitter."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Thaw the splitter
            flags = self.GetWindowStyleFlag()
            flag = ~wx.propgrid.PG_STATIC_SPLITTER  # "~" is "invert bits"
            self.SetWindowStyleFlag( flags & flag ) # "&" is bitwise "and"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            menu_items = menu.GetMenuItems()
            for menu_item in menu_items:
                if menu_item.GetLabel() == "Static Layout":
                    menu_item.Check(check=False)
            
        
        
    def on_static_layout(self, event):
        func_name = "on_static_layout"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # wxPG_STATIC_LAYOUT   (wxPG_HIDE_MARGIN|wxPG_STATIC_SPLITTER)
        if event.IsChecked():
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Hide the margin and freeze the splitter."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Hide the margin and freeze the splitter
            flags = self.GetWindowStyleFlag()
            flag = wx.propgrid.PG_STATIC_LAYOUT
            self.SetWindowStyleFlag( flags | flag ) # "|" is bitwise "or"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            menu_items = menu.GetMenuItems()
            for menu_item in menu_items:
                if menu_item.GetLabel() == "Hide Margin":
                    menu_item.Check(check=True)
                elif menu_item.GetLabel() == "Static Splitter":
                    menu_item.Check(check=True)
        
        else:
            if self._v_debug and self._v_debug_level > 5999:
                msg = "Reveal the margin and thaw the splitter."
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            # Reveal the margin and thaw the splitter
            flags = self.GetWindowStyleFlag()
            flag = ~wx.propgrid.PG_STATIC_LAYOUT  # "~" is "invert bits"
            self.SetWindowStyleFlag( flags & flag ) # "&" is bitwise "and"
            menu_bar = self.mf.GetMenuBar()
            id = event.GetId()
            item = menu_bar.FindItemById(id)
            menu = item.GetMenu()
            menu_items = menu.GetMenuItems()
            for menu_item in menu_items:
                if menu_item.GetLabel() == "Hide Margin":
                    menu_item.Check(check=False)
                elif menu_item.GetLabel() == "Static Splitter":
                    menu_item.Check(check=False)
            
        
        
        
    def update_menu(self, menu=None):
        func_name = "update_menu"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        is_hide_margin_checked = False
        is_static_splitter_checked = False
        is_static_layout_checked = False
        hide_margin_id = 0
        static_splitter_id = 0
        static_layout_id = 0
        menu_items = menu.GetMenuItems()
        for menu_item in menu_items:
            if menu_item.GetLabel() == "Hide Margin":
                hide_margin_id = menu_item.GetId()
                is_hide_margin_checked = menu_item.IsChecked()
                menu_item_hide_margin = menu_item
            elif menu_item.GetLabel() == "Static Splitter":
                static_splitter_id = menu_item.GetId()
                is_static_splitter_checked = menu_item.IsChecked()
                menu_item_static_splitter = menu_item
            elif menu_item.GetLabel() == "Static Layout":
                static_layout_id = menu_item.GetId()
                is_static_layout_checked = menu_item.IsChecked()
                menu_item_static_layout = menu_item
        
        # If "Hide_Margin" and "Static_Splitter", then also check "Static_Layout", otherwise, uncheck "Static Layout".
        if is_hide_margin_checked and is_static_splitter_checked:
            menu_item_static_layout.Check(check=True)
        else:
            menu_item_static_layout.Check(check=False)
        # If "Static_Layout", then also check "Hide_Margin" and "Static_Splitter".  (already done in the static_layout routine)
        # if is_static_layout_checked:
            # menu_item_hide_margin.Check(check=True)
            # menu_item_static_splitter.Check(check=True)
        
        
        
    def on_page_clear_modified_status(self, event):
        func_name = "on_page_clear_modified_status"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.ClearModifiedStatus()
        
        
    def on_compacted(self, event):
        func_name = "on_compacted"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.CollapseAll()
        self.show_all_uncheck()
        
        
    def on_expanded(self, event):
        func_name = "on_expanded"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.ExpandAll()
        self.show_all_check()
        
    def show_all_uncheck(self):
        func_name = "show_all_uncheck"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        menu_bar = self.mf.GetMenuBar()
        title = "Page"
        position = menu_bar.FindMenu(title)
        menu = menu_bar.GetMenu(position)
        menu_items = menu.GetMenuItems()
        for menu_item in menu_items:
            if menu_item.GetLabel() == "Show All":
                menu_item.Check(check=False)
        
        
    def show_all_check(self):
        func_name = "show_all_check"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        menu_bar = self.mf.GetMenuBar()
        title = "Page"
        position = menu_bar.FindMenu(title)
        menu = menu_bar.GetMenu(position)
        menu_items = menu.GetMenuItems()
        for menu_item in menu_items:
            if menu_item.GetLabel() == "Show All":
                menu_item.Check(check=True)
        
    def on_change(self, event):
        func_name = "on_change"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p = event.GetProperty()
        property_name = event.GetPropertyName()
        property_value = event.GetPropertyValue()
        # print property_name
        # print property_value
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "Property name: %s value: %s") % ( property_name, str(property_value) )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
        
        if property_name == "Line Colour":
            self.GetGrid().SetLineColour(property_value)
        
        if property_name == "Margin Colour":
            self.GetGrid().SetMarginColour(property_value)
        
        if property_name == "Selection Text Colour":
            self.GetGrid().SetSelectionForeground(property_value)
        
        if property_name == "Selection Colour":
            self.GetGrid().SetSelectionBackground(property_value)
        
        if property_name == "Caption Colour":
            self.GetGrid().SetCaptionBackgroundColour(property_value)
        
        if property_name == "Caption Text Colour":
            self.GetGrid().SetCaptionForegroundColour(property_value)
        
        if property_name == "Disabled Cell Text Colour":
            self.GetGrid().SetCellDisabledTextColour(property_value)
        
        if property_name == "Cell Text Colour":
            self.SetPropertyTextColour(p, property_value)
        
        if property_name == "Cell Colour":
            self.SetPropertyBackgroundColour(p, property_value)
        
        if property_name == "Grid Cursor":
            self.parent.SetCursor(wx.StockCursor(cursor_list[property_value]))
        
        if property_name == "Grid Font":
            self.SetFont(property_value)
        
        
        
    def on_item_expanded(self, event):
        func_name = "on_item_expanded"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        
    def on_item_collapsed(self, event):
        func_name = "on_item_collapsed"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        
        