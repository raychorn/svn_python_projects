# control_property_properties.py
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


import wx
import datetime
import wx.lib.masked
import wx.propgrid
import StringIO
import cStringIO
import  base64
# import control_inspector
import control_inspector_property
import control_inspector_property_attribute
import control_inspector_mytime_property
import ptl


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


MODE_ADD = "add"
MODE_EDIT = "edit"
PREFIX_CAT = "cat"

DS_SIMPLE = 10
DS_SIMPLE_ALL = 20
DS_PARENT = 30
DS_CATEGORY = 40

# Controls how property attributes are displayed and handled.  (see add_item_property_attributes and on_change)
DS_STYLE = DS_SIMPLE
DS_STYLE = DS_SIMPLE_ALL
DS_STYLE = DS_PARENT
# DS_STYLE = DS_CATEGORY
        


class PP(wx.propgrid.PropertyGridManager):
    def __init__(self, parent=None, page = 0, type = ptl.PROPERTY_TYPE_NORMAL, category = None, datatype = None, property_id = None):
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        wx.propgrid.PropertyGridManager.__init__(self, parent, wx.ID_ANY, style=wx.propgrid.PG_DESCRIPTION | wx.propgrid.PG_BOLD_MODIFIED | wx.propgrid.PG_SPLITTER_AUTO_CENTER )
        
        self._v_log = self.mf
        self._v_debug = self.mf._v_debug
        self._v_debug_level = self.mf._v_debug_level
        
        self.property = control_inspector_property.PropertyGrid_Property(parent=self)
        
        if page <  0:
            self.limit_to_page = True   # We are adding/editing a page
        else:
            self.limit_to_page = False  # We are adding/editing a category or regular property
        
        self.init_labels()
        
        self.lst_property_attributes = []
        self.lst_property_attribute_values = []
        self.dict_attributes_by_datatype = self.build_dict_attributes_by_datatype()
        
        self.attributes = self.build_attributes_dict()
        # self.lst_all_attributes = self.attributes.keys()
        # self.lst_all_attribute_values = self.attributes.values()
        self.lst_all_attributes = self.build_attributes_list()
        self.lst_all_attribute_values = self.build_attribute_values_list()
        
        self._v_page = 0	# the current page of THIS property grid
        
        self._v_source_grid = self.parent.parent
        
        self._v_current_property = ""
        self._v_property_id = property_id
        if property_id:
            self._v_mode = MODE_EDIT
        else:
            self._v_mode = MODE_ADD
        
        
        r = 0
        g = 0
        b = 0
        a = 255
        self._v_default_colour_txt = wx.Colour( r, g, b, a)
        
        r = 255
        g =255
        b = 255
        a = 255
        self._v_default_colour_bg = wx.Colour( r, g, b, a)
        
        if self.limit_to_page:
            category_id = None
        else:
            tmp_property_id = self._v_source_grid.GetSelectedProperty()
            if tmp_property_id:
                category_id = self._v_source_grid.GetPropertyCategory( tmp_property_id )
            else:
                category_id = self._v_source_grid.GetFirstCategory()
        
        if category_id:
            pass
            self._v_default_colour_txt = self._v_source_grid.GetPropertyTextColour( category_id )
            self._v_default_colour_bg = self._v_source_grid.GetPropertyColour( category_id )
        
        self.max_page_index = 0
        
        self.max_type_index = 0
        self.list_type_choices = []
        
        self.max_category_index = 0
        self.list_category_choices = []
        
        self.RegisterAdditionalEditors()
        self.RegisterEditor(control_inspector_mytime_property.MyTimeEditor, "clock")
        
        
        if self.limit_to_page:
            self._v_property_page = self._v_source_grid.GetPageCount()
        else:
            self._v_property_page = page	# the destination page of the property we are creating
        self._v_property_type_index = 0
        self._v_property_type = type
        self._v_property_category_index = 0
        self._v_property_category = category
        self._v_property_parent_index = 0
        self._v_property_parent = ""
        self._v_property_datatype_index = 0
        self._v_property_datatype = datatype
        self._v_property_name = ""
        self._v_property_label = ""
        self._v_property_choicesvalues = ""
        self._v_property_choices = []
        self._v_property_values = []
        self._v_property_value = ""
        self._v_property_help = ""
        self._v_property_is_enabled = True
        self._v_property_is_default = False
        self._v_property_is_low_priority = True
        self._v_property_colour_txt = self._v_default_colour_txt
        self._v_property_colour_bg = self._v_default_colour_bg
        self._v_property_colour_preview = "Just some sample text to show the colours."
        self._v_colour_preview_id = None
        self._v_property_image_file_name = ""
        self._v_property_attributes = self.build_dict_attributes()
        
        self.build_dict_translate()
        self.initialize_values()
        self.build_dict_help()
        self.add_initial_properties()
        
        
        # Event handling
        self.Bind(wx.propgrid.EVT_PG_PAGE_CHANGED, self.on_page_change)
        self.Bind(wx.propgrid.EVT_PG_SELECTED, self.on_select)
        self.Bind(wx.propgrid.EVT_PG_CHANGED, self.on_change)
        
        # self.SetSplitterPosition( 100 )
        
    def init_labels(self):
        SPACE = " "
        self.lbl_page = "Page"
        self.lbl_category = "Category"
        self.lbl_parent = "Parent"
        self.lbl_property = "Property"
        self.lbl_page_number = self.lbl_page + SPACE + "Number"
        self.lbl_property_type = self.lbl_property + SPACE + "Type"
        self.lbl_category_name = self.lbl_category + SPACE + "Name"
        self.lbl_parent_name = self.lbl_parent + SPACE + "Name"
        self.lbl_property_datatype = self.lbl_property + SPACE + "DataType"
        self.lbl_property_name = self.lbl_property + SPACE + "Name"
        if self.limit_to_page:
            self.lbl_property_label = self.lbl_page + SPACE + "Title"
        else:
            self.lbl_property_label = self.lbl_property + SPACE + "Label"
        self.lbl_property_choicesvalues = self.lbl_property + SPACE + "Choice/Value Pairs"
        self.lbl_property_value = self.lbl_property + SPACE + "Value"
        self.lbl_property_help = self.lbl_property + SPACE + "Help String"
        self.lbl_property_options = self.lbl_property + SPACE + "Options"
        self.lbl_property_is_enabled = self.lbl_property + SPACE + "Enabled"
        self.lbl_property_is_default = self.lbl_property + SPACE + "Default"
        self.lbl_property_is_low_priority = self.lbl_property + SPACE + "Low Priority"
        self.lbl_property_colour_fg = self.lbl_property + SPACE + "Foreground Colour"
        self.lbl_property_colour_bg = self.lbl_property + SPACE + "Background Colour"
        self.lbl_property_colour_txt = self.lbl_property + SPACE + "Text Colour"
        self.lbl_property_colour_preview = self.lbl_property + SPACE + "Colour Preview"
        if self.limit_to_page:
            self.lbl_property_image = self.lbl_page + SPACE + "Icon"
        else:
            self.lbl_property_image = self.lbl_property + SPACE + "Icon"
        self.lbl_property_attributes = self.lbl_property + SPACE + "Attributes"
        self.lbl_desc = self.lbl_property_datatype + SPACE + "Description"
        
        
    def initialize_values(self):
        func_name = "initialize_values"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_mode == MODE_ADD:
            if self._v_debug and self._v_debug_level > 7999:
                msg = ( "Mode: %s ") % ( self._v_mode, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self._v_property_type_index = 0
            self._v_property_category_index = 0
            self._v_property_parent_index = 0
            self._v_property_datatype_index = 0
            self._v_property_name = ""
            self._v_property_label = ""
            self._v_property_choicesvalues = ""
            self._v_property_choices = []
            self._v_property_values = []
            self._v_property_value = ""
            self._v_property_help = ""
            self._v_property_is_enabled = True
            self._v_property_is_default = False
            self._v_property_is_low_priority = True
            self._v_property_colour_txt = self._v_default_colour_txt
            self._v_property_colour_bg = self._v_default_colour_bg
            self._v_property_colour_preview = "Just some sample text to show the colours."
            self._v_property_image_file_name = ""
            # self._v_property_attributes = {}
            
        elif self._v_mode == MODE_EDIT:
            if self._v_debug and self._v_debug_level > 7999:
                msg = ( "Mode: %s ") % ( self._v_mode, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self._v_property_type_index = 0
            self._v_property_category_index = 0
            # if self._v_property_category:
                # self._v_property_category = self._v_source_grid.GetPropertyName(self._v_property_category)
            self._v_property_parent_index = 0
            self._v_property_datatype_index = 0
            # self._v_property_datatype = self._v_source_grid.GetPropertyValueType(self._v_property_id)
            self._v_property_datatype = self.dict_gridtype_to_ptl.get(self._v_source_grid.GetPropertyClassName(self._v_property_id), ptl.PROPERTY_DATATYPE_TEXT)    # This is a bug, what if the key is not found?
            self._v_property_name = self._v_source_grid.GetPropertyName(self._v_property_id)
            self._v_property_label = self._v_source_grid.GetPropertyLabel(self._v_property_id)
            if self._v_property_type != ptl.PROPERTY_DATATYPE_PARENT and self._v_property_type != ptl.PROPERTY_DATATYPE_CATEGORY:
                self._v_property_value = self._v_source_grid.GetPropertyValue(self._v_property_id)
            self._v_property_help = self._v_source_grid.GetPropertyHelpString(self._v_property_id)
            self._v_property_is_enabled = self._v_source_grid.IsPropertyEnabled(self._v_property_id)
            self._v_property_is_default = False
            self._v_property_is_low_priority = self._v_source_grid.GetPropertyPriority(self._v_property_id)
            self._v_property_colour_txt = self._v_source_grid.GetPropertyTextColour( self._v_property_id )
            self._v_property_colour_bg = self._v_source_grid.GetPropertyColour( self._v_property_id )
            self._v_property_colour_preview = "Just some sample text to show the colours."
            # self._v_property_image_file_name = self._v_source_grid.GetPropertyImage(self._v_property_id)
            self._v_property_image_file_name = ""
            # self._v_property_attributes = {}
            
        else:
            pass
            if self._v_debug and self._v_debug_level > 7999:
                msg = ( "Invalid mode: %s ") % ( self._v_mode, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        
        
    def build_dict_translate(self):
        self.dict_gridtype_to_ptl = {}
        self.dict_gridtype_to_ptl["wxParentProperty"] = ptl.PROPERTY_DATATYPE_STRING
        self.dict_gridtype_to_ptl["wxIntProperty"] = ptl.PROPERTY_DATATYPE_INTEGER
        self.dict_gridtype_to_ptl["wxUIntProperty"] = ptl.PROPERTY_DATATYPE_UINTEGER
        self.dict_gridtype_to_ptl["wxFloatProperty"] = ptl.PROPERTY_DATATYPE_FLOAT
        self.dict_gridtype_to_ptl["wxStringProperty"] = ptl.PROPERTY_DATATYPE_STRING
        self.dict_gridtype_to_ptl["wxBoolProperty"] = ptl.PROPERTY_DATATYPE_BOOLEAN
        self.dict_gridtype_to_ptl["wxDateProperty"] = ptl.PROPERTY_DATATYPE_DATE
        self.dict_gridtype_to_ptl["wxDate1Property"] = ptl.PROPERTY_DATATYPE_DATETIME
        self.dict_gridtype_to_ptl["wxDate2Property"] = ptl.PROPERTY_DATATYPE_TIME
        self.dict_gridtype_to_ptl["wxFontProperty"] = ptl.PROPERTY_DATATYPE_FONT
        self.dict_gridtype_to_ptl["wxFontDataProperty"] = ptl.PROPERTY_DATATYPE_FONTDATA
        self.dict_gridtype_to_ptl["wxColourProperty"] = ptl.PROPERTY_DATATYPE_COLOUR
        self.dict_gridtype_to_ptl["wxSystemColourProperty"] = ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR
        self.dict_gridtype_to_ptl["wxFlagsProperty"] = ptl.PROPERTY_DATATYPE_FLAGS
        self.dict_gridtype_to_ptl["wxCursorProperty"] = ptl.PROPERTY_DATATYPE_CURSOR
        self.dict_gridtype_to_ptl["wxPositionProperty"] = ptl.PROPERTY_DATATYPE_POINT
        self.dict_gridtype_to_ptl["wxDirProperty"] = ptl.PROPERTY_DATATYPE_DIR
        self.dict_gridtype_to_ptl["wxDirsProperty"] = ptl.PROPERTY_DATATYPE_DIRS
        self.dict_gridtype_to_ptl["wxLongStringProperty"] = ptl.PROPERTY_DATATYPE_LONGSTRING
        self.dict_gridtype_to_ptl["wxAdvImageFileProperty"] = ptl.PROPERTY_DATATYPE_ADVIMAGEFILE
        self.dict_gridtype_to_ptl["wxCustomProperty"] = ptl.PROPERTY_DATATYPE_CUSTOM
        self.dict_gridtype_to_ptl["wxImageProperty"] = ptl.PROPERTY_DATATYPE_IMAGEFILE
        self.dict_gridtype_to_ptl["wxEnumProperty"] = ptl.PROPERTY_DATATYPE_ENUM
        self.dict_gridtype_to_ptl["wxFileProperty"] = ptl.PROPERTY_DATATYPE_FILE

    
    def build_dict_help(self):
        pass
        help_property_type = "The property type determines what options and attributes are available.  This is implemented as an ENUM property."
        
        self.dict_help = {}	# Start with an empty dictionary
        
        key = ptl.PROPERTY_DATATYPE_NUMERIC
        help = "Non-standard property.  "
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_TEXT
        help = "Non-standard property.  "
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_STRING
        help = "Simple string property. wxPG_STRING_PASSWORD attribute may be used to echo value as asterisks and use wxTE_PASSWORD for wxTextCtrl."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_LOGICAL
        help = "Same as boolean"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_BOOLEAN
        help = "Represents a boolean (true/false) value.  By default, wxChoice is used as the editor control.  The property attribute, wxPG_BOOL_USE_CHECKBOX, causes the property to use a check box as the editor control instead or wxChoice."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_DATE
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_TIME
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_DATETIME
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_INTEGER
        help = "Like wxStringProperty, but converts text to a signed long integer."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_UINTEGER
        help = "Like wxIntProperty, but displays value as unsigned int. To set the prefix used globally, manipulate wxPG_UINT_PREFIX string attribute. To set the globally used base, manipulate wxPG_UINT_BASE int attribute. Regardless of current prefix, understands (hex) values starting with both '0x' and '$'."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_FLOAT
        help = "Like wxStringProperty, but converts text to a double-precision floating point. Default float-to-text precision is 6 decimals, but this can be changed by modifying wxPG_FLOAT_PRECISION attribute."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_FONT
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_FONTDATA
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_COLOUR
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_FLAGS
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_CURSOR
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_POINT
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_DIR
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_DIRS
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_LONGSTRING
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_ADVIMAGEFILE
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_CUSTOM
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_IMAGEFILE
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_ENUM
        help = "helpstring"
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_DATATYPE_FILE
        help = "helpstring"
        self.dict_help[key] = help
        
        key = self.lbl_page_number
        help = "The page of the target property-grid control that this new property will be created in.  When this value is changed, the target property-grid control is updated immediatly to display the page.  The property category value is re-populated with a list of the categories that exist in the target property-grid control.  This is implemented as an ENUM property."
        self.dict_help[key] = help
        
        key = self.lbl_property_type
        help = help_property_type
        self.dict_help[key] = help
        
        key = self.lbl_category_name
        help = "The category of the target property-grid control that this new property will be created in.  This is implemented as an ENUM property."
        self.dict_help[key] = help
        
        key = self.lbl_property_name
        help = "The name that will be used to track this new property in the target property-grid control."
        self.dict_help[key] = help
        
        key = self.lbl_property_label
        help = "The label that will appear in the left column of this new property in the target property-grid control."
        self.dict_help[key] = help
        
        key = self.lbl_property_value
        help = "The value entry that will appear in the right column of this new property in the target property-grid control."
        self.dict_help[key] = help
        
        key = self.lbl_property_help
        help = "The descriptive text that is displayed when the property is selected."
        self.dict_help[key] = help
        
        key = self.lbl_property_options
        help = "This item does not correspond to any direct property-grid items.  It is just for my reference to group non-essential attributes."
        self.dict_help[key] = help
        
        key = self.lbl_property_is_enabled
        help = "If TRUE, the new property is active and can be edited.  If FALSE, the new property is disabled and appears gray.  In the disabled state, the value cannot be changed."
        self.dict_help[key] = help
        
        key = self.lbl_property_is_default
        help = "Non-standard property.  The idea is to have only zero or one property marked as a default property.  It is colour-coded to stand-out and is selected when the control is first created."
        self.dict_help[key] = help
        
        key = self.lbl_property_is_low_priority
        help = "Low priority properties are not shown if the property-grid is in a 'compact' state."
        self.dict_help[key] = help
        
        key = self.lbl_property_colour_txt
        help = "This sets the colour for the text of the property."
        self.dict_help[key] = help
        
        key = self.lbl_property_colour_bg
        help = "This sets the colour for the background of the property."
        self.dict_help[key] = help
        
        key = self.lbl_property_colour_preview
        help = "Non-standard property.  For my reference."
        self.dict_help[key] = help
        
        key = self.lbl_property_colour_fg
        help = "Non-standard property.  For my reference.  Same as colour_txt"
        self.dict_help[key] = help
        
        key = self.lbl_property_image
        help = "File name of a graphic icon that will be displayed in the right column, next to the property value."
        self.dict_help[key] = help
        
        key = self.lbl_property_attributes
        help = "Property flags control extra settings for advanced properties."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_TYPE_NORMAL
        help = help_property_type + "\n" + "A 'Normal' property appears at the top or root level instead of in a category."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_TYPE_CATEGORY
        help = help_property_type + "\n" + "A 'Category' property appears in the grid as a category heading."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
        help = help_property_type + "\n" + "A 'Category Member' property appears in a category section."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_TYPE_PARENT
        help = help_property_type + "\n" + "A 'Parent' property summarizes the child properties that it contains."
        self.dict_help[key] = help
        
        key = ptl.PROPERTY_TYPE_CHILD
        help = help_property_type + "\n" + "A 'Child' property appears below a parent property."
        self.dict_help[key] = help
        
        key = "key"
        help = "helpstring"
        self.dict_help[key] = help
        
        
    def add_item_page(self):
        func_name = "add_item_page"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Page
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        if self._v_mode == MODE_ADD:    # Page property enabled to allow change.
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_page_number, property_label=self.lbl_page_number, property_value=self._v_property_page, help_string=None, low_priority=None, enabled=True, default=False)
        elif self._v_mode == MODE_EDIT:    # Page property disabled.
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_page_number, property_label=self.lbl_page_number, property_value=self._v_property_page, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_page_number
        self.set_help( property = p_id1, key = self._v_current_property )
        self.init_page()
        return p_id1
        
        
    def add_item_property_type(self):
        func_name = "add_item_property_type"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Type
        #-----------------------------------------------------------------------------------------------
        # Property Type can be: PROPERTY_TYPE_NORMAL, PROPERTY_TYPE_CATEGORY, PROPERTY_TYPE_CATEGORY_MEMBER, PROPERTY_TYPE_PARENT, PROPERTY_TYPE_CHILD
        # To create a child, a parent property must already exist.
        # To create a category member, a category must already exist.
        # A parent property can have a category.
        # The list of property types available is created dynamically based on the above criteria.
        p_id1 = None
        if self._v_mode == MODE_ADD:
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_property_type, property_label=self.lbl_property_type, property_value=self._v_property_type_index, help_string=None, low_priority=None, enabled=True, default=False)
        elif self._v_mode == MODE_EDIT:
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_property_type, property_label=self.lbl_property_type, property_value=self._v_property_type_index, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_property_type
        self.init_property_type()
        return p_id1
        
        
    def add_item_category(self):
        func_name = "add_item_category"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Category
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        if self._v_mode == MODE_ADD:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_category_name, property_label=self.lbl_category_name, property_value=self._v_property_category_index, help_string=None, low_priority=None, enabled=True, default=False)
        elif self._v_mode == MODE_EDIT:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_category_name, property_label=self.lbl_category_name, property_value=self._v_property_category_index, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_category_name
        self.set_help( property = p_id1, key = self._v_current_property )
        self.init_category()
        return p_id1
        
        
    def add_item_parent(self):
        func_name = "add_item_parent"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id1 = None
        if self._v_mode == MODE_ADD:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_parent_name, property_label=self.lbl_parent_name, property_value=self._v_property_parent_index, help_string=None, low_priority=None, enabled=True, default=False)
        elif self._v_mode == MODE_EDIT:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_parent_name, property_label=self.lbl_parent_name, property_value=self._v_property_parent_index, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_parent_name
        self.set_help( property = p_id1, key = self._v_current_property )
        self.init_parent()
        return p_id1
        
    def add_item_property_datatype(self):
        func_name = "add_item_property_datatype"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property DataType
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        if self._v_mode == MODE_ADD:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_property_datatype, property_label=self.lbl_property_datatype, property_value=self._v_property_datatype_index, help_string=None, low_priority=None, enabled=True, default=False)
        elif self._v_mode == MODE_EDIT:
            p_id1 = self.property.add( page = self._v_page, property_datatype_name=ptl.PROPERTY_DATATYPE_ENUM, property_name=self.lbl_property_datatype, property_label=self.lbl_property_datatype, property_value=self._v_property_datatype_index, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_property_datatype
        self.init_property_datatype()
        return p_id1
        
        
    def add_item_property_name(self):
        func_name = "add_item_property_name"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Name
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        if self._v_mode == MODE_ADD:
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_name, property_label=self.lbl_property_name, property_value=self._v_property_name, help_string=None, low_priority=None, enabled=True, default=False)
            default_p_id = p_id1
        elif self._v_mode == MODE_EDIT:
            p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_name, property_label=self.lbl_property_name, property_value=self._v_property_name, help_string=None, low_priority=None, enabled=False, default=False)
        self._v_current_property = self.lbl_property_name
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_label(self):
        func_name = "add_item_property_label"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Label
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_label, property_label=self.lbl_property_label, property_value=self._v_property_label, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_label
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_choicesvalues(self):
        func_name = "add_item_property_choicesvalues"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property ChoicesValues
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_ARRAYSTRING, property_name=self.lbl_property_choicesvalues, property_label=self.lbl_property_choicesvalues, property_value="", help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_choicesvalues
        self.set_help( property = p_id1, key = self._v_current_property )
        # p_id1 = self.init_value()
        if self._v_mode == MODE_EDIT:
            self.EnableProperty( p_id1, False )
        return p_id1
        
        
    def add_item_property_value(self):
        func_name = "add_item_property_value"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Value
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_value, property_label=self.lbl_property_value, property_value=str(self._v_property_value), help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_value
        self.set_help( property = p_id1, key = self._v_current_property )
        p_id1 = self.init_value()
        if self._v_mode == MODE_EDIT:
            self.EnableProperty( p_id1, False )
        return p_id1
        
        
    def add_item_property_help(self):
        func_name = "add_item_property_help"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Help
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_LONGSTRING, property_name=self.lbl_property_help, property_label=self.lbl_property_help, property_value=self._v_property_help, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_help
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_enabled(self):
        func_name = "add_item_property_enabled"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Enabled
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=self.lbl_property_is_enabled, property_label=self.lbl_property_is_enabled, property_value=self._v_property_is_enabled, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_is_enabled
        self.set_help( property = p_id1, key = self._v_current_property )
        self.SetPropertyAttribute(self._v_current_property, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
        return p_id1
        
        
    def add_item_property_default(self):
        func_name = "add_item_property_default"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Default
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=self.lbl_property_is_default, property_label=self.lbl_property_is_default, property_value=self._v_property_is_default, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_is_default
        self.set_help( property = p_id1, key = self._v_current_property )
        self.SetPropertyAttribute(self._v_current_property, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
        # print self.GetPropertyAttributes(p_id1)
        return p_id1
        
        
    def add_item_property_priority(self):
        func_name = "add_item_property_priority"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Priority
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=self.lbl_property_is_low_priority, property_label=self.lbl_property_is_low_priority, property_value=self._v_property_is_low_priority, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_is_low_priority
        self.set_help( property = p_id1, key = self._v_current_property )
        self.SetPropertyAttribute(self._v_current_property, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
        return p_id1
        
        
    def add_item_property_colour_txt(self):
        func_name = "add_item_property_colour_txt"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Colour TXT
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, property_name=self.lbl_property_colour_txt, property_label=self.lbl_property_colour_txt, property_value=self._v_property_colour_txt, help_string="", low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_colour_txt
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_colour_bg(self):
        func_name = "add_item_property_colour_bg"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Colour BG
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_COLOUR, property_name=self.lbl_property_colour_bg, property_label=self.lbl_property_colour_bg, property_value=self._v_property_colour_bg, help_string="", low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_colour_bg
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_colour_preview(self):
        func_name = "add_item_property_colour_preview"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Colour Preview
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_colour_preview, property_label=self.lbl_property_colour_preview, property_value=self._v_property_colour_preview, help_string="", low_priority=None, enabled=True, default=False, colour_txt=self._v_property_colour_txt, colour_bg=self._v_property_colour_bg)
        self._v_current_property = self.lbl_property_colour_preview
        self.set_help( property = p_id1, key = self._v_current_property )
        self._v_colour_preview_id = p_id1
        return p_id1
        
        
    def add_item_property_image(self):
        func_name = "add_item_property_image"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Image
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_IMAGEFILE, property_name=self.lbl_property_image, property_label=self.lbl_property_image, property_value=self._v_property_image_file_name, help_string=None, low_priority=None, enabled=True, default=False)
        self._v_current_property = self.lbl_property_image
        self.set_help( property = p_id1, key = self._v_current_property )
        return p_id1
        
        
    def add_item_property_attributes(self):
        func_name = "add_item_property_attributes"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Attributes
        #-----------------------------------------------------------------------------------------------
        choices = None
        values = None
        cat = self.GetPropertyByName("Attributes")
        if cat:
            self.Delete(cat)
            cat = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY, property_name="Attributes", property_label="Attributes", help_string="", low_priority=None, enabled=True, default=False )
        p_id1 = None
        keys = self._v_property_attributes.keys()
        for key in keys:
            # attribute = name, number, value, enabled, desc
            attribute = self._v_property_attributes[key]
            if DS_STYLE == DS_SIMPLE:
                if attribute.enabled:
                    p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, category = "Attributes", property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=attribute.name, property_label=attribute.name, property_value=attribute.value, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                    self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
                    self._v_current_property = attribute.name
            elif DS_STYLE == DS_SIMPLE_ALL:
                p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, category = "Attributes", property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=attribute.name, property_label=attribute.name, property_value=attribute.value, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
                self._v_current_property = attribute.name
            elif DS_STYLE == DS_PARENT:
                if attribute.enabled:
                    p_id3 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_PARENT, category = "Attributes", property_name=PREFIX_CAT+attribute.name, property_label=attribute.name, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                    p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CHILD, category = PREFIX_CAT+attribute.name, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=str(attribute.number)+"Set", property_label="Set this attribute", property_value=attribute.value, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                    self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
                    # Value
                    if attribute.value_label:
                        if attribute.value_dict:
                            choices = attribute.value_dict.keys()
                            values = attribute.value_dict.values()
                        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CHILD, category = PREFIX_CAT+attribute.name, property_datatype_name=attribute.value_datatype, property_name=str(attribute.number)+"Value", property_label=attribute.value_label, property_value=attribute.value, help_string=attribute.value_desc, low_priority=None, enabled=attribute.enabled, default=False, property_choices=choices, property_values=values )
                    # Flags
                    if attribute.flags_label and attribute.flags_label != "":
                        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CHILD, category = PREFIX_CAT+attribute.name, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=str(attribute.number)+"Flags", property_label=attribute.flags_label, property_value=attribute.flags_is_set, help_string=attribute.flags_desc, low_priority=None, enabled=attribute.enabled, default=False )
                        self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
            elif DS_STYLE == DS_CATEGORY:
                if attribute.enabled:
                    p_id3 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY, category = "Attributes", property_name=PREFIX_CAT+attribute.name, property_label=attribute.name, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                    # Is_Set
                    p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, category = PREFIX_CAT+attribute.name, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=str(attribute.number)+"Set", property_label="Set this attribute", property_value=attribute.is_set, help_string=attribute.desc, low_priority=None, enabled=attribute.enabled, default=False )
                    self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
                    # Value
                    if attribute.value_label:
                        if attribute.value_dict:
                            choices = attribute.value_dict.keys()
                            values = attribute.value_dict.values()
                        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, category = PREFIX_CAT+attribute.name, property_datatype_name=attribute.value_datatype, property_name=str(attribute.number)+"Value", property_label=attribute.value_label, property_value=attribute.value, help_string=attribute.value_desc, low_priority=None, enabled=attribute.enabled, default=False, property_choices=choices, property_values=values )
                    # Flags
                    if attribute.flags_label and attribute.flags_label != "":
                        p_id1 = self.property.add( page = self._v_page, property_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER, category = PREFIX_CAT+attribute.name, property_datatype_name=ptl.PROPERTY_DATATYPE_LOGICAL, property_name=str(attribute.number)+"Flags", property_label=attribute.flags_label, property_value=attribute.flags_is_set, help_string=attribute.flags_desc, low_priority=None, enabled=attribute.enabled, default=False )
                        self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
            else:
                pass
            
        # It is a long list of attributes, collapse it down under it's category
        # cat = self.GetPropertyByName("Attributes")
        if cat:
            pass
            # self.Collapse(cat)
        
        return p_id1
        
        
    def update_colour_preview(self):
        func_name = "update_colour_preview"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Colour Preview
        #-----------------------------------------------------------------------------------------------
        #def set_attributes(self, property_id = None, help_string=None, low_priority=None, enabled=True, default=False, colour_txt=None, colour_bg=None, icon_name=None):
        self.property.set_attributes(self._v_colour_preview_id, colour_txt=self._v_property_colour_txt, colour_bg=self._v_property_colour_bg)
        
        
    def add_initial_properties(self):
        func_name = "add_initial_properties"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "add page: %s ") % ( "Page 1 - Property Settings", )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self.add_page( title = "Page 1 - Property Settings" )
        self.change_property_type()
        
        
    def zap(self):
        func_name = "zap"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.ClearPage(0)
        self.max_page_index = 0
        self.max_category_index = 0
        self.max_parent_index = 0
        self.max_type_index = 0
        
        
    def add_page(self, title = "New Page" ):
        func_name = "add_page"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = self.GetPageCount()
        
        if title == "New Page":
            title = "Page %d" % self._v_page
            
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "title: %s") % ( title, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self.AddPage( title )
        self._v_page = self.GetPageCount() - 1
        
        
    def add_category(self):
        func_name = "add_category"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = 0
        self.SelectPage(self._v_page)
        
        for property_datatype in ptl.LIST_PROPERTY_DATATYPE:
            category_id = self.Append( wx.propgrid.PropertyCategory( property_datatype ) )
            if self._v_debug and self._v_debug_level > 7999:
                msg = ( "%s ") % ( property_datatype, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        
    def import_file(self, file_name="tmp.bmp", img_type=wx.BITMAP_TYPE_BMP):
        func_name = "import_file"
        if self._v_debug and self._v_debug_level > 7999:
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
                    if self._v_debug and self._v_debug_level > 7999:
                        self._v_log.write(("%s:%s: %s") % (self.__class__, func_name, msg))
                    self._v_bmp = wx.EmptyBitmap(100, 100, -1)	# wx Bitmap object
                    self._v_bmp = wx.NullBitmap	# wx Bitmap object
            else:
                    msg = "File does not exist."
                    if self._v_debug and self._v_debug_level > 7999:
                        self._v_log.write(("%s:%s: %s") % (self.__class__, func_name, msg))
                    self._v_bmp = wx.NullBitmap	# wx Bitmap object
                
        return self._v_bmp
        
        
    def select_default_page(self):
        func_name = "select_default_page"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self._v_page = self._v_default_page
        self.SelectPage(self._v_page)
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "page: %d ") % ( self._v_page, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        
        
    def select_default_property(self):
        func_name = "select_default_property"
        if self._v_debug and self._v_debug_level > 7999:
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
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_default_property[self._v_page]:
            self.select_property( property_id = self._v_default_property[self._v_page] )
        
        
    def select_property(self, property_id):
        func_name = "select_property"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "property_id: %s") % ( property_id, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self.SelectProperty( property_id, True )	# Two SelectProperty, why won't one due the job?
        self.SelectProperty( property_id, True )	# I think because i added the same property to page 0 and page 1
        self.EnsureVisible( property_id )
        p_id = self.GetSelectedProperty()
        if p_id:
            property_name = self.GetPropertyName( p_id )
            self._v_current_property = property_name
        
        

    def build_dict_attributes_by_datatype(self):
        func_name = "build_dict_attributes_by_datatype"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dict_attributes_by_datatype = {}
        
        # key = datatype from ptl.  For example: ptl.PROPERTY_DATATYPE_LOGICAL
        # value = list of property grid property attribute identifiers.  For example: wx.propgrid.PG_BOOL_USE_CHECKBOX, wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        
        datatype = ptl.PROPERTY_DATATYPE_NOPROP
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_CATEGORY
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_PARENT
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_NUMERIC
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_FLOAT_PRECISION, wx.propgrid.PG_UINT_BASE, wx.propgrid.PG_UINT_PREFIX]
        
        datatype = ptl.PROPERTY_DATATYPE_FLOAT
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_FLOAT_PRECISION, wx.propgrid.PG_UINT_BASE, wx.propgrid.PG_UINT_PREFIX]
        
        datatype = ptl.PROPERTY_DATATYPE_INTEGER
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_UINTEGER
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_UINT_BASE, wx.propgrid.PG_UINT_PREFIX]
        
        datatype = ptl.PROPERTY_DATATYPE_TEXT
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_STRING_PASSWORD]
        
        datatype = ptl.PROPERTY_DATATYPE_STRING
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_STRING_PASSWORD]
        
        datatype = ptl.PROPERTY_DATATYPE_LOGICAL
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_BOOL_USE_CHECKBOX, wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING]
        
        datatype = ptl.PROPERTY_DATATYPE_BOOLEAN
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_BOOL_USE_CHECKBOX, wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING]
        
        datatype = ptl.PROPERTY_DATATYPE_DATE
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_DATE_PICKER_STYLE, wx.propgrid.PG_DATE_FORMAT]
        
        datatype = ptl.PROPERTY_DATATYPE_TIME
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_DATETIME
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_DATE_PICKER_STYLE, wx.propgrid.PG_DATE_FORMAT]
        
        datatype = ptl.PROPERTY_DATATYPE_FONT
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_FONTDATA
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_COLOUR
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_COLOUR_ALLOW_CUSTOM]
        
        datatype = ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_COLOUR_ALLOW_CUSTOM]
        
        datatype = ptl.PROPERTY_DATATYPE_FLAGS
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_BOOL_USE_CHECKBOX]
        
        datatype = ptl.PROPERTY_DATATYPE_CURSOR
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_POINT
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_DIR
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_DIR_DIALOG_MESSAGE]
        
        datatype = ptl.PROPERTY_DATATYPE_DIRS
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_DIR_DIALOG_MESSAGE]
        
        datatype = ptl.PROPERTY_DATATYPE_LONGSTRING
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_ADVIMAGEFILE
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_FILE_DIALOG_TITLE, wx.propgrid.PG_FILE_INITIAL_PATH, wx.propgrid.PG_FILE_SHOW_FULL_PATH, wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH, wx.propgrid.PG_FILE_WILDCARD]
        
        datatype = ptl.PROPERTY_DATATYPE_CUSTOM
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_IMAGEFILE
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_FILE_DIALOG_TITLE, wx.propgrid.PG_FILE_INITIAL_PATH, wx.propgrid.PG_FILE_SHOW_FULL_PATH, wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH, wx.propgrid.PG_FILE_WILDCARD]
        
        datatype = ptl.PROPERTY_DATATYPE_ENUM
        dict_attributes_by_datatype[datatype] = []
        
        datatype = ptl.PROPERTY_DATATYPE_FILE
        dict_attributes_by_datatype[datatype] = [wx.propgrid.PG_FILE_DIALOG_TITLE, wx.propgrid.PG_FILE_INITIAL_PATH, wx.propgrid.PG_FILE_SHOW_FULL_PATH, wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH, wx.propgrid.PG_FILE_WILDCARD]
        
        # attribute.number = wx.propgrid.PG_BOOL_USE_CHECKBOX
        # attribute.number = wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        # attribute.number = wx.propgrid.PG_COLOUR_ALLOW_CUSTOM
        # attribute.number = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        # attribute.number = wx.propgrid.PG_CUSTOM_PRIVATE_CHILDREN
        # attribute.number = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        # attribute.number = wx.propgrid.PG_DATE_PICKER_STYLE
        # attribute.number = wx.propgrid.PG_DIR_DIALOG_MESSAGE
        # attribute.number = wx.propgrid.PG_FILE_DIALOG_TITLE
        # attribute.number = wx.propgrid.PG_FILE_INITIAL_PATH
        # attribute.number = wx.propgrid.PG_FILE_SHOW_FULL_PATH
        # attribute.number = wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH
        # attribute.number = wx.propgrid.PG_FILE_WILDCARD
        # attribute.number = wx.propgrid.PG_FLOAT_PRECISION
        # attribute.number = wx.propgrid.PG_STRING_PASSWORD
        # attribute.number = wx.propgrid.PG_UINT_BASE
        # attribute.number = wx.propgrid.PG_UINT_PREFIX
        # attribute.number = wx.propgrid.PG_USER_ATTRIBUTE
        
        return dict_attributes_by_datatype
        
        
    def build_dict_attributes(self):
        func_name = "build_dict_attributes"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dict_attributes = {}
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Boolean uses checkbox"
        attribute.number = wx.propgrid.PG_BOOL_USE_CHECKBOX
        attribute.desc = "This attribute applies to the boolean (logical) property datatype.  Setting this attribute will cause the property value to be displayed using a checkbox control.  True will appear as checked, false will appear as unchecked.  Normally, boolean properties use a drop-down choice control that is similar to a combo control."
        attribute.flags_label = "Apply recursively to all children"
        attribute.flags_number = wx.propgrid.PG_RECURSE 
        attribute.flags_desc = "Setting this flag will apply this attribute recursively to all the children of the property."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Boolean uses Double-click to change value"
        attribute.number = wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        attribute.desc = "This attribute applies to the boolean (logical) property datatype.  Setting this attribute will cause the property value to toggle when it is double-clicked."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Color picker displays custom colours"
        attribute.number = wx.propgrid.PG_COLOUR_ALLOW_CUSTOM
        attribute.desc = "This attribute applies to the colour and system-colour property datatype.  Setting this attribute causes custom colours to be displayed in the list of choices."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Repaint function for custom property"
        attribute.number = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        attribute.desc = "Sets callback function (of type wxPGPaintCallback) that is called whenever image in front of property needs to be repainted. This attribute takes precedence over bitmap set with wxPG_CUSTOM_IMAGE, and it is only proper way to draw images to wxCustomProperty's drop down choices list.  Remarks:  Callback must handle measure calls (i.e. when rect.x < 0, set paintdata.m_drawn Height to height of item in question). "
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Children of a custom property are set to private"
        attribute.number = wx.propgrid.PG_CUSTOM_PRIVATE_CHILDREN
        attribute.desc = "Setting this attribute makes children private, similar to other properties with children.  Remarks: * Children must be added when this attribute has value 0. Otherwise there will be an assertion failure.* Changed event occurs on the parent only. "
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Sets displayed date format"
        attribute.number = wx.propgrid.PG_DATE_FORMAT
        attribute.desc = "Sets displayed date format for wxDateProperty."
        attribute.value_label = "Formatting string"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "DD:MM:YYYY"
        attribute.value_desc = "The formatting string is used as a template to display the date."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Set century style for date picker"
        attribute.number = wx.propgrid.PG_DATE_PICKER_STYLE
        attribute.desc = "Sets wxDatePickerCtrl window style used with wxDateProperty.  Default is wxDP_DEFAULT | wxDP_SHOWCENTURY. "
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Sets a specific message for the dir dialog"
        attribute.number = wx.propgrid.PG_DIR_DIALOG_MESSAGE
        attribute.desc = "Sets a specific message for the dir dialog."
        attribute.value_label = "Message text"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "Dir Message"
        attribute.value_desc = "Sets a specific message for the dir dialog."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Sets a specific title for the file dialog"
        attribute.number = wx.propgrid.PG_FILE_DIALOG_TITLE
        attribute.desc = "Sets a specific title for the dir dialog."
        attribute.value_label = "Title text"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "Dir Title"
        attribute.value_desc = "Sets a specific title for the dir dialog."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Sets the initial path of where to look for files"
        attribute.number = wx.propgrid.PG_FILE_INITIAL_PATH
        attribute.desc = "Sets the initial path of where to look for files."
        attribute.value_label = "Initial path"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "/"
        attribute.value_desc = "The initial path of where to look for files."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Display the drive, directory, and file name"
        attribute.number = wx.propgrid.PG_FILE_SHOW_FULL_PATH
        attribute.desc = "When 0, only the file name is shown (i.e. drive and directory are hidden)."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Displays path name relative to a given path"
        attribute.number = wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH
        attribute.desc = "If set, then the filename is shown relative to the given path string."
        attribute.desc = "Sets the initial path of where to look for files."
        attribute.value_label = "Base path"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "/"
        attribute.value_desc = "The base path to which the property value is added to compose a complete path."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Sets the wildcard used in the file picker"
        attribute.number = wx.propgrid.PG_FILE_WILDCARD
        attribute.desc = "Sets the wildcard used in the triggered wxFileDialog. Format is the same."
        attribute.value_label = "File wildcard"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_TEXT
        attribute.value = "*.*"
        attribute.value_desc = "The wildcard used in the triggered wxFileDialog."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Floating point precision"
        attribute.number = wx.propgrid.PG_FLOAT_PRECISION
        attribute.desc = "Sets the (max) precision used when floating point value is rendered as text. The default -1 means infinite precision."
        attribute.value_label = "Precision"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        attribute.value = "-1"
        attribute.value_desc = "The maximum precision used when floating point value is rendered as text."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Text echoed as asterisks"
        attribute.number = wx.propgrid.PG_STRING_PASSWORD
        attribute.desc = "The text will be echoed as asterisks (wxTE_PASSWORD will be passed to textctrl etc)."
        dict_attributes[attribute.number] = attribute
        
        # // Valid constants for wxPG_UINT_BASE attribute
        # // (long because of wxVariant constructor)
        #define wxPG_BASE_OCT                       (long)8
        #define wxPG_BASE_DEC                       (long)10
        #define wxPG_BASE_HEX                       (long)16
        #define wxPG_BASE_HEXL                      (long)32
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Base used by a wxUIntProperty"
        attribute.number = wx.propgrid.PG_UINT_BASE
        attribute.desc = "Valid constants are wxPG_BASE_OCT, wxPG_BASE_DEC, wxPG_BASE_HEX and wxPG_BASE_HEXL (lowercase characters)."
        attribute.value_label = "Base"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_ENUM
        attribute.value_dict = {"Octal":8L, "Decimal":10L, "Hexidecimal":16L, "Hexidecimal (lowercase)":32L}
        # attribute.value = wx.propgrid.wxPG_BASE_DEC       # Explodes!!
        attribute.value = 10L   # L means it is a long integer
        attribute.value_desc = "The base used by an unsigned integer property."
        dict_attributes[attribute.number] = attribute
        
        # // Valid constants for wxPG_UINT_PREFIX attribute
        #define wxPG_PREFIX_NONE                    (long)0
        #define wxPG_PREFIX_0x                      (long)1
        #define wxPG_PREFIX_DOLLAR_SIGN             (long)2
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "Prefix rendered to wxUIntProperty"
        attribute.number = wx.propgrid.PG_UINT_PREFIX
        attribute.desc = "Accepted constants wxPG_PREFIX_NONE, wxPG_PREFIX_0x, and wxPG_PREFIX_DOLLAR_SIGN. Note: Only wxPG_PREFIX_NONE works with Decimal and Octal numbers."
        attribute.value_label = "Prefix"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_ENUM
        attribute.value_dict = {"None":0L, "Zero":1L, "Dollar sign":2L}
        attribute.value = 0L
        attribute.value_desc = "The prefix added to an unsigned integer property."
        dict_attributes[attribute.number] = attribute
        
        attribute = control_inspector_property_attribute.Property_Attribute()
        attribute.name = "First attribute id that is guaranteed not to be used built-in properties"
        attribute.number = wx.propgrid.PG_USER_ATTRIBUTE
        attribute.desc = "First attribute id that is guaranteed not to be used by built-in properties."
        attribute.value_label = "Id"
        attribute.value_datatype = ptl.PROPERTY_DATATYPE_INTEGER
        attribute.value = "0"
        attribute.value_desc = "The first attribute id that is guaranteed not to be used by built-in properties."
        dict_attributes[attribute.number] = attribute
        
        return dict_attributes
        
        
    def build_attributes_dict(self):
        func_name = "build_attributes_dict"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dict_attributes = {}
        
        # attribute_index = 0
        # for each attribute_index in range(len(attributes)):
            # attribute_name = attributes[ attribute_index ]
            # attribute_value = values[ attribute_index ]
            # dict_attributes[attribute_name] = attribute_value
            # attribute_index = attribute_index + 1
            
        attribute_name = "Boolean uses checkbox"
        attribute_value = wx.propgrid.PG_BOOL_USE_CHECKBOX
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Boolean uses Double-click to change value"
        attribute_value = wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Color picker displays custom colours"
        attribute_value = wx.propgrid.PG_COLOUR_ALLOW_CUSTOM
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Repaint function for custom property"
        attribute_value = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Children of a custom property are set to private"
        attribute_value = wx.propgrid.PG_CUSTOM_PRIVATE_CHILDREN
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Sets displayed date format"
        attribute_value = wx.propgrid.PG_DATE_FORMAT
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Set century style for date picker"
        attribute_value = wx.propgrid.PG_DATE_PICKER_STYLE
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Sets a specific message for the dir dialog"
        attribute_value = wx.propgrid.PG_DIR_DIALOG_MESSAGE
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Sets a specific title for the file dialog"
        attribute_value = wx.propgrid.PG_FILE_DIALOG_TITLE
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Sets the initial path of where to look for files"
        attribute_value = wx.propgrid.PG_FILE_INITIAL_PATH
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Display the drive, directory, and file name"
        attribute_value = wx.propgrid.PG_FILE_SHOW_FULL_PATH
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Displays path name relative to a given path"
        attribute_value = wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Sets the wildcard used in the file picker"
        attribute_value = wx.propgrid.PG_FILE_WILDCARD
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Floating point precision"
        attribute_value = wx.propgrid.PG_FLOAT_PRECISION
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Text echoed as asterisks"
        attribute_value = wx.propgrid.PG_STRING_PASSWORD
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Base used by a wxUIntProperty"
        attribute_value = wx.propgrid.PG_UINT_BASE
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "Prefix rendered to wxUIntProperty"
        attribute_value = wx.propgrid.PG_UINT_PREFIX
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        attribute_name = "First attribute id that is guaranteed not to be used built-in properties"
        attribute_value = wx.propgrid.PG_USER_ATTRIBUTE
        # attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        dict_attributes[attribute_name] = attribute_value
        
        return dict_attributes
        
        
    def build_attributes_list(self):
        func_name = "build_attributes_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        list_attributes = []
        self.dict_attributes = {}
        
        # attribute_index = 0
        # for each attribute_index in range(len(attributes)):
            # attribute_name = attributes[ attribute_index ]
            # attribute_value = values[ attribute_index ]
            # dict_attributes[attribute_name] = attribute_value
            # attribute_index = attribute_index + 1
            
        attribute_name = "Boolean uses checkbox"
        attribute_value = wx.propgrid.PG_BOOL_USE_CHECKBOX
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Boolean uses Double-click to change value"
        attribute_value = wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        self.dict_attributes[ptl.PROPERTY_DATATYPE_LOGICAL] = list_attributes
        # print self.dict_attributes[ptl.PROPERTY_DATATYPE_LOGICAL]
        self.lst_property_attributes = list_attributes
        
        attribute_name = "Color picker displays custom colours"
        attribute_value = wx.propgrid.PG_COLOUR_ALLOW_CUSTOM
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Repaint function for custom property"
        attribute_value = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Children of a custom property are set to private"
        attribute_value = wx.propgrid.PG_CUSTOM_PRIVATE_CHILDREN
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Sets displayed date format"
        attribute_value = wx.propgrid.PG_DATE_FORMAT
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Set century style for date picker"
        attribute_value = wx.propgrid.PG_DATE_PICKER_STYLE
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Sets a specific message for the dir dialog"
        attribute_value = wx.propgrid.PG_DIR_DIALOG_MESSAGE
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Sets a specific title for the file dialog"
        attribute_value = wx.propgrid.PG_FILE_DIALOG_TITLE
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Sets the initial path of where to look for files"
        attribute_value = wx.propgrid.PG_FILE_INITIAL_PATH
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Display the drive, directory, and file name"
        attribute_value = wx.propgrid.PG_FILE_SHOW_FULL_PATH
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Displays path name relative to a given path"
        attribute_value = wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Sets the wildcard used in the file picker"
        attribute_value = wx.propgrid.PG_FILE_WILDCARD
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Floating point precision"
        attribute_value = wx.propgrid.PG_FLOAT_PRECISION
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Text echoed as asterisks"
        attribute_value = wx.propgrid.PG_STRING_PASSWORD
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Base used by a wxUIntProperty"
        attribute_value = wx.propgrid.PG_UINT_BASE
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "Prefix rendered to wxUIntProperty"
        attribute_value = wx.propgrid.PG_UINT_PREFIX
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        attribute_name = "First attribute id that is guaranteed not to be used built-in properties"
        attribute_value = wx.propgrid.PG_USER_ATTRIBUTE
        attribute_name = attribute_name + " (" + str(attribute_value) + ")"
        list_attributes.append(attribute_name)
        
        return list_attributes
        
        
    def build_attribute_values_list(self):
        func_name = "build_attribute_values_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        list_attribute_values = []
        
        attribute_value = wx.propgrid.PG_BOOL_USE_CHECKBOX
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_BOOL_USE_DOUBLE_CLICK_CYCLING
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_COLOUR_ALLOW_CUSTOM
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_CUSTOM_PAINT_CALLBACK
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_CUSTOM_PRIVATE_CHILDREN
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_DATE_FORMAT
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_DATE_PICKER_STYLE
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_DIR_DIALOG_MESSAGE
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FILE_DIALOG_TITLE
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FILE_INITIAL_PATH
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FILE_SHOW_FULL_PATH
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FILE_SHOW_RELATIVE_PATH
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FILE_WILDCARD
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_FLOAT_PRECISION
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_STRING_PASSWORD
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_UINT_BASE
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_UINT_PREFIX
        list_attribute_values.append(attribute_value)
        
        attribute_value = wx.propgrid.PG_USER_ATTRIBUTE
        list_attribute_values.append(attribute_value)
        
        return list_attribute_values
        
        
    def build_page_list(self):
        func_name = "build_page_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        page_list = []	# Start with an empty list.
        self.max_page_index = self.parent.pg.GetPageCount()
        for i in range(self.max_page_index):
            page_list.append( str(i) )
        return page_list
        
        
    def init_page(self):
        func_name = "init_page"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        null_page = "0"
        page_index = self._v_property_page
        
        # Clear list of choices
        i = 0
        while i < self.max_page_index:
            self.DeletePropertyChoice( self.lbl_page_number, 0 )
            i = i + 1
        self.max_page_index = 0
        
        # Populate list of choices and select one
        self.list_page = self.build_page_list()
        if len(self.list_page) > 0:
            # Valid choices are available
            index = 0
            for page in self.list_page:
                self.AddPropertyChoice( self.lbl_page_number, page, index )
                index = index + 1
            self.max_page_index = index
        else:
            # Empty category list
            self.AddPropertyChoice( self.lbl_page_number, null_page, page_index )
            self.max_page_index = 1
        self.SetPropertyValue( self.lbl_page_number, page_index )
        
    def build_type_list(self):
        func_name = "build_type_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        type_list = []	# Start with an empty list.
        self.list_type_choices = []
        i = 0
        
        type_list.append(ptl.PROPERTY_TYPE_NORMAL)
        self.list_type_choices.append( ptl.PROPERTY_TYPE_NORMAL )
        self.list_type_choices.append( i )
        i = i + 1
        
        type_list.append(ptl.PROPERTY_TYPE_CATEGORY)
        self.list_type_choices.append( ptl.PROPERTY_TYPE_CATEGORY )
        self.list_type_choices.append( i )
        i = i + 1
        
        if self.is_category_member_allowed():
            type_list.append(ptl.PROPERTY_TYPE_CATEGORY_MEMBER)
            self.list_type_choices.append( ptl.PROPERTY_TYPE_CATEGORY_MEMBER )
            self.list_type_choices.append( i )
            i = i + 1
        
        type_list.append(ptl.PROPERTY_TYPE_PARENT)
        self.list_type_choices.append( ptl.PROPERTY_TYPE_PARENT )
        self.list_type_choices.append( i )
        i = i + 1
        
        if self.is_child_allowed():
            type_list.append(ptl.PROPERTY_TYPE_CHILD)
            self.list_type_choices.append( ptl.PROPERTY_TYPE_CHILD )
            self.list_type_choices.append( i )
            i = i + 1
        
        return type_list
        
        
    def is_category_member_allowed(self):
        func_name = "is_category_member_allowed"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # If the grid has at least one category, then category members are allowed.
        retval = False
        category = self._v_source_grid.GetFirstCategory()
        if category:
            retval = True
        
        return retval
        
        
    def is_child_allowed(self):
        func_name = "is_child_allowed"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # If the grid has at least one parent, then children are allowed.
        retval = False
        p_id = self._v_source_grid.GetFirstProperty()
        if p_id:
            if self._v_source_grid.GetPropertyClassName(p_id) == "wxParentProperty":
                retval = True
                
            while p_id:
                p_id = self._v_source_grid.GetNextProperty(p_id)
                if p_id:
                    if self._v_source_grid.GetPropertyClassName(p_id) == "wxParentProperty":
                        retval = True
                        
            
        
        return retval
        
        
    def init_property_type(self):
        func_name = "init_property_type"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        null_type = "None"
        self._v_property_type_index = 0
        p = self.GetPropertyByName( self.lbl_property_type )
        
        # Clear list of choices
        i = 0
        while i < self.max_type_index:
            self.DeletePropertyChoice( p, 0 )
            i = i + 1
        self.max_type_index = 0
        
        # Populate list of choices and select one
        self.list_property_type = self.build_type_list()
        if len(self.list_property_type) > 0:
            # Valid choices are available
            index = 0
            for t in self.list_property_type:
                self.AddPropertyChoice( p, t, index )
                if t == self._v_property_type:
                    self._v_property_type_index = index
                index = index + 1
            self.max_type_index = index
            # just pick the first one on the list.
            self._v_property_type = self.list_property_type[ self._v_property_type_index ]
        else:
            pass
            # Empty type list
            self._v_property_type = null_type
            self.AddPropertyChoice( p, null_type, self._v_property_type_index )
            self.max_type_index = 1
        self.SetPropertyValue( p, self._v_property_type_index )
        self.update_property_type_help( property = p, list_index = self._v_property_type_index )
        
    def build_category_list(self):
        func_name = "build_category_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        category_list = []	# Start with an empty list.
        if self._v_property_type == ptl.PROPERTY_TYPE_CATEGORY_MEMBER:
            pass
            # 'Category Member' must have a category so 'None' should not be an option.
        else:
            category_list.append("None")
        self.list_category_choices = []
        # Enumerate categories in the property grid.
        self.parent.pg.SelectPage(self._v_property_page)
        i = 0
        category = self.parent.pg.GetFirstCategory()
        while category:
            category_list.append(self.parent.pg.GetPropertyName (category))
            self.list_category_choices.append( self.parent.pg.GetPropertyName (category) )
            self.list_category_choices.append( i )
            category = self.parent.pg.GetNextCategory (category)
            i = i + 1
        return category_list
        
        
    def init_category(self):
        func_name = "init_category"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        null_category = "None"
        self._v_property_category_index = 0
        p = self.GetPropertyByName( self.lbl_category_name )
        
        # Clear list of choices
        i = 0
        while i < self.max_category_index:
            self.DeletePropertyChoice( p, 0 )
            i = i + 1
        self.max_category_index = 0
        
        # Populate list of choices and select one
        self.list_category = self.build_category_list()
        if len(self.list_category) > 0:
            # Valid choices are available
            index = 0
            for category in self.list_category:
                self.AddPropertyChoice( p, category, index )
                if category == self._v_property_category:
                    self._v_property_category_index = index
                index = index + 1
            self.max_category_index = index
            # just pick the first one on the list.
            self._v_property_category = self.list_category[ self._v_property_category_index ]
        else:
            pass
            # Empty category list
            self._v_property_category = null_category
            self.AddPropertyChoice( p, null_category, self._v_property_category_index )
            self.max_category_index = 1
        self.SetPropertyValue( p, self._v_property_category_index )
        self.set_default_colour()
        if self._v_mode == MODE_ADD:
            self._v_property_colour_txt = self._v_default_colour_txt
            self._v_property_colour_bg = self._v_default_colour_bg
        
    def build_parent_list(self):
        func_name = "build_parent_list"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        parent_list = []	# Start with an empty list.
        self.list_parent_choices = []
        # Enumerate categories in the property grid.
        self._v_source_grid.SelectPage(self._v_property_page)
        i = 0
        parent = self._v_source_grid.GetFirstProperty()
        while parent:
            if self._v_source_grid.GetPropertyClassName(parent) == "wxParentProperty":
                parent_list.append(self._v_source_grid.GetPropertyName (parent))
                self.list_parent_choices.append( self._v_source_grid.GetPropertyName (parent) )
                self.list_parent_choices.append( i )
                i = i + 1
            parent = self._v_source_grid.GetNextProperty(parent)
        return parent_list
        
        
    def init_parent(self):
        func_name = "init_parent"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        null_parent = "None"
        self._v_property_parent_index = 0
        p = self.GetPropertyByName( self.lbl_parent_name )
        
        # Clear list of choices
        i = 0
        while i < self.max_parent_index:
            self.DeletePropertyChoice( p, 0 )
            i = i + 1
        self.max_parent_index = 0
        
        # Populate list of choices and select one
        self.list_parent = self.build_parent_list()
        if len(self.list_parent) > 0:
            # Valid choices are available
            index = 0
            for parent in self.list_parent:
                self.AddPropertyChoice( p, parent, index )
                if parent == self._v_property_parent:
                    self._v_property_parent_index = index
                index = index + 1
            self.max_parent_index = index
            # just pick the first one on the list.
            self._v_property_parent = self.list_parent[ self._v_property_parent_index ]
        else:
            pass
            # Empty parent list (should never happen)
            self._v_property_parent = null_parent
            self.AddPropertyChoice( p, null_parent, self._v_property_parent_index )
            self.max_parent_index = 1
        self.SetPropertyValue( p, self._v_property_parent_index )
        # self.set_default_colour()
        if self._v_mode == MODE_ADD:
            self._v_property_colour_txt = self._v_default_colour_txt
            self._v_property_colour_bg = self._v_default_colour_bg
        
        
    def init_property_datatype(self):
        func_name = "init_property_datatype"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        self.list_property_datatype = ptl.LIST_PROPERTY_DATATYPE
        p = self.GetPropertyByName( self.lbl_property_datatype )
        self._v_property_datatype_index = 0
        index = 0
        for property_datatype in self.list_property_datatype:
            self.AddPropertyChoice( p, property_datatype, index )
            if property_datatype == self._v_property_datatype:
                self._v_property_datatype_index = index
            index = index + 1
        self.SetPropertyValue( p, self._v_property_datatype_index )
        
        self._v_property_datatype = self.list_property_datatype[ self._v_property_datatype_index ]
        
        self.update_property_datatype_help( property = p, list_index = self._v_property_datatype_index )
        
        
    def init_value(self):
        func_name = "init_value"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p = self.GetPropertyByName( self.lbl_property_value )
        
        #-----------------------------------------------------------------------------------------------
        # Property Value
        #-----------------------------------------------------------------------------------------------
        # self.p_id1 = self.add_property( page = self._v_page, category = None, property_datatype_name=ptl.PROPERTY_DATATYPE_TEXT, property_name=self.lbl_property_value, property_label=self.lbl_property_value, property_value=self._v_property_value, help_string=None, low_priority=None, enabled=True, default=False)
        # self._v_current_property = self.lbl_property_value
        # self.set_help( property = self.p_id1, key = self._v_current_property )
        
        property_name = self.lbl_property_value
        property_label = self.lbl_property_value
        if self._v_mode == MODE_ADD:
            self._v_property_value = "" # Non-text properties are initialized in the elif clause.
        property_value = self._v_property_value
        
        p_id2 = None
        
        if self._v_property_datatype == ptl.PROPERTY_DATATYPE_TEXT or self._v_property_datatype == ptl.PROPERTY_DATATYPE_STRING:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.StringProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_FONT:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FontProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_FONTDATA:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FontDataProperty(name=property_name, label=property_label) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_COLOUR:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.ColourProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.SystemColourProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_CURSOR:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.CursorProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_SIZE:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.SizeProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_POINT:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.PointProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_DIR:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.DirProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_DIRS:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.DirsProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_LONGSTRING:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.LongStringProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_ADVIMAGEFILE:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.AdvImageFileProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_CUSTOM:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.CustomProperty(name=property_name, label=property_label) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_IMAGEFILE:
            p_id2 = self.ReplaceProperty( p, wx.propgrid.ImageFileProperty(name=property_name, label=property_label, value=property_value) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_ENUM:
            # self.setup_choicesvalues()
            # p_id2 = self.ReplaceProperty( p, wx.propgrid.EnumProperty(name=property_name, label=property_label) )
            p_id2 = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_EDITENUM:
            p_id2 = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_MULTICHOICE:
            p_id2 = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_FLAGS:
            # p_id2 = self.ReplaceProperty( p, wx.propgrid.FlagsProperty(name=property_name, label=property_label, flag_labels=flags, values=values, value=property_value) )
            # p_id2 = self.ReplaceProperty( p, wx.propgrid.ArrayStringProperty(name=property_name, label=property_label, value="") )
            p_id2 = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_NUMERIC:
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=float(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_FLOAT:
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=float(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_INTEGER:
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_UINTEGER:
            if self._v_mode == MODE_ADD:
                property_value = 0
                self._v_property_value = property_value
            p_id2 = self.ReplaceProperty( p, wx.propgrid.FloatProperty(name=property_name, label=property_label, value=int(property_value)) )
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_LOGICAL or self._v_property_datatype == ptl.PROPERTY_DATATYPE_BOOLEAN:
            if property_value:
                if str(property_value) == "0":
                    property_value = False
                elif str(property_value).upper() == "FALSE":
                    property_value = False
                elif str(property_value).upper() == "F":
                    property_value = False
                elif str(property_value).upper() == "NO":
                    property_value = False
                elif str(property_value).upper() == "N":
                    property_value = False
                elif str(property_value).upper() == "UNCHECKED":
                    property_value = False
                else:
                    property_value = True
            else:
                property_value = False
            self._v_property_value = property_value
            p_id2 = self.ReplaceProperty(p, wx.propgrid.BoolProperty(name=property_name, label=property_label, value=property_value))
            self.SetPropertyAttribute(p_id2, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
            
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_DATE:
            wxdate = wx.DateTime_Now()	# Initialize the variable
            if property_value:
                d_day = property_value.Day
                d_month = property_value.Month
                d_year = property_value.Year
                wx.DateTime.Set(wxdate, d_day, d_month, d_year)	# Set the value
            
            if wxdate.IsValid():
                pass
            else:
                print "Date error"
                wxdate = wx.DateTime.Now()
            
            self._v_property_value = wxdate
            p_id2 = self.ReplaceProperty(p, wx.propgrid.DateProperty(name=property_name, label=property_label, value=wxdate))
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_TIME:
            if False:   # old junk
                if type(property_value) != datetime.datetime:
                    property_value = datetime.datetime.now()
                self._v_property_value = property_value
                # self._v_property_value = property_value.strftime("%H:%M:%S")
            if self._v_mode == MODE_ADD:
                mydatetime = datetime.datetime.now()
                property_value = mydatetime.strftime("%H:%M:%S")    # convert to string
                self._v_property_value = property_value
            myprop = control_inspector_mytime_property.MyTimeProperty(name=property_name, label=property_label, value=property_value)
            p_id2 = self.ReplaceProperty(p, myprop)
            # self.SetPropertyEditor(p_id2, "clock")
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_DATETIME:
            wxdate = wx.DateTime.Now()	# Initialize the variable
            if property_value:
                d_second = property_value.Second
                d_minute = property_value.Minute
                d_hour = property_value.Hour
                d_day = property_value.Day
                d_month = property_value.Month
                d_year = property_value.Year
                wxdate.Set(day=d_day, month=d_month, year=d_year, hour=d_hour, minute=d_minute, second=d_second)	# Set the value
            
            if wxdate.IsValid():
                pass
            else:
                print "DateTime error"
                wxdate = wx.DateTime.Now()
            
            self._v_property_value = wxdate
            p_id2 = self.ReplaceProperty(p, wx.propgrid.DateProperty(name=property_name, label=property_label, value=wxdate))
            
        elif self._v_property_datatype == ptl.PROPERTY_DATATYPE_PARENT:
            pass
            
        else:
            if self._v_debug and self._v_debug_level > 1999:
                msg = ( "Invalid property type name: %s") % ( self._v_property_datatype)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        
        if p_id2:
            self.SetPropertyValue( p_id2, self._v_property_value )
            self.enable_specific_attributes()
            self.add_item_property_attributes()
            # self.update_attributes()
            
        
        return p_id2
        
        
    def update_attributes(self):
        func_name = "update_attributes"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        #-----------------------------------------------------------------------------------------------
        # Property Attributes
        #-----------------------------------------------------------------------------------------------
        p_id1 = None
        keys = self._v_property_attributes.keys()
        for key in keys:    # Iterate thru all the attributes.
            attribute = self._v_property_attributes[key]    # attribute = name, number, value, enabled, desc
            p = self.GetPropertyByName(attribute.name)  # Get the property for the attribute
            if p:
                # Update the property with new value, new enabled, and new help string.
                p_id1 = self.ReplaceProperty(p, wx.propgrid.BoolProperty(name=attribute.name, label=attribute.name, value=attribute.value))
                self.SetPropertyAttribute(p_id1, wx.propgrid.PG_BOOL_USE_CHECKBOX, 1, wx.propgrid.PG_RECURSE);
                if attribute.enabled:
                    self.EnableProperty(p_id1)
                else:
                    self.DisableProperty(p_id1)
                self.SetPropertyHelpString( p_id1, attribute.desc )
        
        
        
    def enable_specific_attributes(self):
        func_name = "enable_specific_attributes"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        
        self.disable_all_attributes()
        # Get the keys just for this, specific, datatype
        datatype_specific_keys = self.dict_attributes_by_datatype[self._v_property_datatype]
        for key in datatype_specific_keys:  # Iterate the attributes that pertain to this datatype
            attribute = self._v_property_attributes[key]
            attribute.enabled = True    # Enable the attribute
            
        
        
        
    def disable_all_attributes(self):
        func_name = "disable_all_attributes"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        
        keys = self._v_property_attributes.keys()
        for key in keys:    # Iterate thru all the attributes.
            attribute = self._v_property_attributes[key]    # attribute = name, number, value, enabled, desc
            attribute.enabled = False    # Disable the attribute
            # attribute.value = ""    # Initialize the value
        
        
    def get_property_choices(self, choicesvalues):
        func_name = "get_property_choices"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        pass
        retval = []
        for item in choicesvalues:
            a, b = item.split(":")
            retval.append(a)
            
        
        return retval
        
        
    def get_property_values(self, choicesvalues):
        func_name = "get_property_values"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        pass
        retval = []
        for item in choicesvalues:
            a, b = item.split(":")
            retval.append(b)
            
        
        return retval
        
        
    def setup_choicesvalues(self):
        func_name = "setup_choicesvalues"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "property type: %s") % ( self._v_property_type )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        default_p_id = None
        self.Freeze()
        self.zap()
        self.disable_all_attributes()
        if self._v_property_type == ptl.PROPERTY_TYPE_CATEGORY_MEMBER:
            pass
            p_id = self.add_item_page()
            p_id = self.add_item_property_type()
            p_id = self.add_item_category()
            p_id = self.add_item_property_datatype()
            p_id = self.add_item_property_name()
            p_id = self.add_item_property_label()
            p_id = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_EDIT:
                default_p_id = p_id
            p_id = self.add_item_property_value()
            p_id = self.add_item_property_help()
            p_id = self.add_item_property_enabled()
            p_id = self.add_item_property_default()
            p_id = self.add_item_property_priority()
            p_id = self.add_item_property_colour_txt()
            p_id = self.add_item_property_colour_bg()
            p_id = self.add_item_property_colour_preview()
            p_id = self.add_item_property_image()
            p_id = self.add_item_property_attributes()
            
        elif self._v_property_type == ptl.PROPERTY_TYPE_CATEGORY:
            pass
            p_id = self.add_item_page()
            p_id = self.add_item_property_type()
            p_id = self.add_item_category()
            p_id = self.add_item_property_name()
            p_id = self.add_item_property_label()
            if self._v_mode == MODE_EDIT:
                default_p_id = p_id
            p_id = self.add_item_property_help()
            p_id = self.add_item_property_enabled()
            p_id = self.add_item_property_default()
            p_id = self.add_item_property_priority()
            p_id = self.add_item_property_colour_txt()
            p_id = self.add_item_property_colour_bg()
            p_id = self.add_item_property_colour_preview()
            p_id = self.add_item_property_image()
            p_id = self.add_item_property_attributes()
            
        elif self._v_property_type == ptl.PROPERTY_TYPE_PARENT:
            pass
            p_id = self.add_item_page()
            p_id = self.add_item_property_type()
            p_id = self.add_item_category()
            p_id = self.add_item_property_name()
            p_id = self.add_item_property_label()
            if self._v_mode == MODE_EDIT:
                default_p_id = p_id
            p_id = self.add_item_property_help()
            p_id = self.add_item_property_enabled()
            p_id = self.add_item_property_default()
            p_id = self.add_item_property_priority()
            p_id = self.add_item_property_colour_txt()
            p_id = self.add_item_property_colour_bg()
            p_id = self.add_item_property_colour_preview()
            p_id = self.add_item_property_image()
            p_id = self.add_item_property_attributes()
            
        elif self._v_property_type == ptl.PROPERTY_TYPE_CHILD:
            pass
            p_id = self.add_item_page()
            p_id = self.add_item_property_type()
            p_id = self.add_item_parent()
            p_id = self.add_item_property_datatype()
            p_id = self.add_item_property_name()
            p_id = self.add_item_property_label()
            p_id = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_EDIT:
                default_p_id = p_id
            p_id = self.add_item_property_value()
            p_id = self.add_item_property_help()
            p_id = self.add_item_property_enabled()
            p_id = self.add_item_property_default()
            p_id = self.add_item_property_priority()
            p_id = self.add_item_property_colour_txt()
            p_id = self.add_item_property_colour_bg()
            p_id = self.add_item_property_colour_preview()
            p_id = self.add_item_property_image()
            p_id = self.add_item_property_attributes()
            
        elif self._v_property_type == ptl.PROPERTY_TYPE_NORMAL:
            pass
            p_id = self.add_item_page()
            p_id = self.add_item_property_type()
            p_id = self.add_item_property_datatype()
            p_id = self.add_item_property_name()
            p_id = self.add_item_property_label()
            p_id = self.add_item_property_choicesvalues()
            if self._v_mode == MODE_EDIT:
                default_p_id = p_id
            p_id = self.add_item_property_value()
            p_id = self.add_item_property_help()
            p_id = self.add_item_property_enabled()
            p_id = self.add_item_property_default()
            p_id = self.add_item_property_priority()
            p_id = self.add_item_property_colour_txt()
            p_id = self.add_item_property_colour_bg()
            p_id = self.add_item_property_colour_preview()
            p_id = self.add_item_property_image()
            p_id = self.add_item_property_attributes()
            
        else:
            if self._v_debug and self._v_debug_level > 1999:
                msg = ( "Invalid property type: %s") % ( self._v_property_type )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                print msg
                
        if default_p_id:
            self.SelectProperty(default_p_id)
            self.EnsureVisible(default_p_id)
            self.SetFocus()
        
        # self.SetSplitterPosition( 100, refresh=True )
        self.Thaw()
        
    def change_property_type(self):
        func_name = "change_property_type"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "property type: %s") % ( self._v_property_type )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        default_p_id = None
        self.Freeze()
        self.zap()
        if self.limit_to_page:
                p_id = self.add_item_property_label()
                default_p_id = p_id
                p_id = self.add_item_property_image()
        else:
            self.disable_all_attributes()
            if self._v_property_type == ptl.PROPERTY_TYPE_CATEGORY_MEMBER:
                pass
                p_id = self.add_item_page()
                p_id = self.add_item_property_type()
                p_id = self.add_item_category()
                p_id = self.add_item_property_datatype()
                p_id = self.add_item_property_name()
                p_id = self.add_item_property_label()
                if self._v_mode == MODE_EDIT:
                    default_p_id = p_id
                p_id = self.add_item_property_value()
                p_id = self.add_item_property_help()
                p_id = self.add_item_property_enabled()
                p_id = self.add_item_property_default()
                p_id = self.add_item_property_priority()
                p_id = self.add_item_property_colour_txt()
                p_id = self.add_item_property_colour_bg()
                p_id = self.add_item_property_colour_preview()
                p_id = self.add_item_property_image()
                p_id = self.add_item_property_attributes()
                
            elif self._v_property_type == ptl.PROPERTY_TYPE_CATEGORY:
                pass
                p_id = self.add_item_page()
                p_id = self.add_item_property_type()
                p_id = self.add_item_category()
                p_id = self.add_item_property_name()
                p_id = self.add_item_property_label()
                if self._v_mode == MODE_EDIT:
                    default_p_id = p_id
                p_id = self.add_item_property_help()
                p_id = self.add_item_property_enabled()
                p_id = self.add_item_property_default()
                p_id = self.add_item_property_priority()
                p_id = self.add_item_property_colour_txt()
                p_id = self.add_item_property_colour_bg()
                p_id = self.add_item_property_colour_preview()
                p_id = self.add_item_property_image()
                p_id = self.add_item_property_attributes()
                
            elif self._v_property_type == ptl.PROPERTY_TYPE_PARENT:
                pass
                p_id = self.add_item_page()
                p_id = self.add_item_property_type()
                p_id = self.add_item_category()
                p_id = self.add_item_property_name()
                p_id = self.add_item_property_label()
                if self._v_mode == MODE_EDIT:
                    default_p_id = p_id
                p_id = self.add_item_property_help()
                p_id = self.add_item_property_enabled()
                p_id = self.add_item_property_default()
                p_id = self.add_item_property_priority()
                p_id = self.add_item_property_colour_txt()
                p_id = self.add_item_property_colour_bg()
                p_id = self.add_item_property_colour_preview()
                p_id = self.add_item_property_image()
                p_id = self.add_item_property_attributes()
                
            elif self._v_property_type == ptl.PROPERTY_TYPE_CHILD:
                pass
                p_id = self.add_item_page()
                p_id = self.add_item_property_type()
                p_id = self.add_item_parent()
                p_id = self.add_item_property_datatype()
                p_id = self.add_item_property_name()
                p_id = self.add_item_property_label()
                if self._v_mode == MODE_EDIT:
                    default_p_id = p_id
                p_id = self.add_item_property_value()
                p_id = self.add_item_property_help()
                p_id = self.add_item_property_enabled()
                p_id = self.add_item_property_default()
                p_id = self.add_item_property_priority()
                p_id = self.add_item_property_colour_txt()
                p_id = self.add_item_property_colour_bg()
                p_id = self.add_item_property_colour_preview()
                p_id = self.add_item_property_image()
                p_id = self.add_item_property_attributes()
                
            elif self._v_property_type == ptl.PROPERTY_TYPE_NORMAL:
                pass
                p_id = self.add_item_page()
                p_id = self.add_item_property_type()
                p_id = self.add_item_property_datatype()
                p_id = self.add_item_property_name()
                p_id = self.add_item_property_label()
                if self._v_property_datatype == ptl.PROPERTY_DATATYPE_FLAGS or self._v_property_datatype == ptl.PROPERTY_DATATYPE_ENUM:
                    p_id = self.add_item_property_choicesvalues()
                if self._v_mode == MODE_EDIT:
                    default_p_id = p_id
                p_id = self.add_item_property_value()
                p_id = self.add_item_property_help()
                p_id = self.add_item_property_enabled()
                p_id = self.add_item_property_default()
                p_id = self.add_item_property_priority()
                p_id = self.add_item_property_colour_txt()
                p_id = self.add_item_property_colour_bg()
                p_id = self.add_item_property_colour_preview()
                p_id = self.add_item_property_image()
                p_id = self.add_item_property_attributes()
                
            else:
                if self._v_debug and self._v_debug_level > 1999:
                    msg = ( "Invalid property type: %s") % ( self._v_property_type )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    print msg
                    
        if default_p_id:
            self.SelectProperty(default_p_id)
            self.EnsureVisible(default_p_id)
            self.SetFocus()
        
        # self.SetSplitterPosition( 100, refresh=True )
        self.Thaw()
        
    def update_property_type_help(self, property = None, list_index = None):
        func_name = "update_property_type_help"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # Update the help string for the selected property type
        # to display a usage hint in the description box.
        self.set_help( property = property, key = self.list_property_type[ list_index ] )
        self.ClearSelection()
        self.SelectProperty( property )
        
        
    def update_property_datatype_help(self, property = None, list_index = None):
        func_name = "update_property_datatype_help"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        # Update the help string for the selected property datatype
        # to display a usage hint in the description box.
        self.set_help( property = property, key = ptl.LIST_PROPERTY_DATATYPE[ list_index ] )
        self.ClearSelection()
        self.SelectProperty( property )
        
        
    def set_help(self, property = None, key = None):
        func_name = "set_help"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        nomatch_return_value = ""
        txt_help = self.dict_help.get( key, nomatch_return_value )
        self.SetPropertyHelpString( property, txt_help )
        
        
    def set_default_colour(self):
        func_name = "set_default_colour"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        category_id = self.parent.pg.GetPropertyByName( self._v_property_category )
        if category_id:
            pass
            self._v_default_colour_txt = self.parent.pg.GetPropertyTextColour( category_id )
            self._v_default_colour_bg = self.parent.pg.GetPropertyColour( category_id )
        
        
    def on_select(self, event):
        func_name = "on_select"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p = event.GetProperty()
        if self._v_debug_level > 500:
            if p:
                if self._v_debug and self._v_debug_level > 7999:
                    msg = ( "%s %s selected") % ( event.GetPropertyLabel(), event.GetPropertyName())
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
            else:
                if self._v_debug and self._v_debug_level > 7999:
                    msg = "Nothing selected"
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
        if p:
                property_name = event.GetPropertyName()
                # print ('on_select: property name: %s' % (property_name))
                self._v_current_property = property_name
                
                # Method 1 for getting property type
                property_datatype = self.GetPVTN(p)
                
                # Method 2 for getting property type
                base_type = self.GetPropertyValueType(p)
                property_datatype = base_type.GetTypeName()
                
                # print ('on_select: property type name: %s' % (property_datatype))
                # If property_datatype is Null, it is a category
                
                
                if self._v_debug and self._v_debug_level > 2999:
                    msg = "Property Name: " + property_name + " Type: " + property_datatype
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        else:
            # print 'Nothing selected'
            if self._v_debug and self._v_debug_level > 2999:
                msg = "Nothing selected"
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
            
    def on_page_change(self, event):
        func_name = "on_page_change"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        new_page = self.GetSelectedPage()
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( ("switching from page: %d to page: %d" ) % (self._v_page, new_page) )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        self._v_page = new_page
        propertygrid_page = self.GetPage( self._v_page )
        p_id = propertygrid_page.GetPropertyByName(self._v_current_property)
        if p_id:
            self.SelectProperty(p_id)
            self.EnsureVisible(p_id)
        
        
    def on_add_property(self, event):
        func_name = "on_add_property"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dlg = dialog_property.Dialog_Property_Create(page = self._v_page, category=None, type=ptl.PROPERTY_DATATYPE_TEXT, parent=self)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            pass
            prop_page = dlg.get_page()
            prop_category = dlg.get_category()
            prop_type = dlg.get_type()
            prop_name = dlg.get_name()
            prop_label = dlg.get_label()
            prop_value = dlg.get_value()
            prop_help = dlg.get_help()
            prop_is_enabled = dlg.get_is_enabled()
            prop_is_default = dlg.get_is_default()
            prop_is_low_priority = dlg.get_is_low_priority()
            if self._v_debug and self._v_debug_level > 7999:
                msg = ("Page: %d, Category: %s, Type: %s") % (prop_page, prop_category, prop_type)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("Name: %s, Label: %s, Value: %s") % (prop_name, prop_label, str(prop_value))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("txt: %s, bg: %s, image: %s") % (str(prop_colour_txt), str(prop_colour_bg), str(prop_image_file_name))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self.p_id1 = self.add_property( page = prop_page, category = prop_category, property_datatype_name=prop_type, property_name=prop_name, property_label=prop_label, property_value=prop_value, help_string=prop_help, low_priority=prop_is_low_priority, enabled=prop_is_enabled, default=prop_is_default)
            self._v_current_property = prop_name
            
        else:
            pass
            # wx.MessageBox( "dialog exited without selecting a database to open.", "Info")
        dlg.Destroy()
    def on_change(self, event):
        func_name = "on_change"
        if self._v_debug and self._v_debug_level > 7999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p = event.GetProperty()
        property_name = event.GetPropertyName()
        property_value = event.GetPropertyValue()
        # print property_name
        # print property_value
        
        if self._v_debug and self._v_debug_level > 7999:
            msg = ( "Property name: %s value: %s") % ( property_name, str(property_value) )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
        
        if property_name == self.lbl_page_number:
            self._v_property_page = int(property_value)
            self.init_category()
            
        elif property_name == self.lbl_property_type:
            self._v_property_type_index = property_value
            # self.update_property_type_help( property = p, list_index = self._v_property_type_index )
            self._v_property_type = self.list_property_type[ self._v_property_type_index ]
            self.change_property_type()
            
        elif property_name == self.lbl_category_name:
            self._v_property_category_index = property_value
            self._v_property_category = self.list_category[ self._v_property_category_index ]
            
            self.set_default_colour()
            self._v_property_colour_txt = self._v_default_colour_txt
            self._v_property_colour_bg = self._v_default_colour_bg
            
            p = self.GetPropertyByName( self.lbl_property_colour_txt )
            self.SetPropertyValue( p, self._v_property_colour_txt )
            p = self.GetPropertyByName( self.lbl_property_colour_bg )
            self.SetPropertyValue( p, self._v_property_colour_bg )
            
            self.Refresh()
            
        elif property_name == self.lbl_parent_name:
            self._v_property_parent_index = property_value
            self._v_property_parent = self.list_parent[ self._v_property_parent_index ]
            
            self.set_default_colour()
            self._v_property_colour_txt = self._v_default_colour_txt
            self._v_property_colour_bg = self._v_default_colour_bg
            
            p = self.GetPropertyByName( self.lbl_property_colour_txt )
            self.SetPropertyValue( p, self._v_property_colour_txt )
            p = self.GetPropertyByName( self.lbl_property_colour_bg )
            self.SetPropertyValue( p, self._v_property_colour_bg )
            
            self.Refresh()
            
        elif property_name == self.lbl_property_datatype:
            self._v_property_datatype_index = property_value
            self.update_property_datatype_help( property = p, list_index = self._v_property_datatype_index )
            self._v_property_datatype = self.list_property_datatype[ self._v_property_datatype_index ]
            self.init_value()
            
        elif property_name == self.lbl_property_name:
            self._v_property_name = str(property_value)
            
        elif property_name == self.lbl_property_label:
            self._v_property_label = str(property_value)
            
        elif property_name == self.lbl_property_choicesvalues:
            self._v_property_choicesvalues = property_value
            self._v_property_choices = self.get_property_choices(self._v_property_choicesvalues)
            self._v_property_values = self.get_property_values(self._v_property_choicesvalues)
            
        elif property_name == self.lbl_property_value:
            self._v_property_value = property_value
            
        elif property_name == self.lbl_property_help:
            self._v_property_help = str(property_value)
            
        elif property_name == self.lbl_property_is_enabled:
            self._v_property_is_enabled = property_value
            
        elif property_name == self.lbl_property_is_default:
            self._v_property_is_default = property_value
            
        elif property_name == self.lbl_property_is_low_priority:
            self._v_property_is_low_priority = property_value
            
        elif property_name == self.lbl_property_colour_txt:
            self._v_property_colour_txt = property_value
            self.update_colour_preview()
            
        elif property_name == self.lbl_property_colour_bg:
            self._v_property_colour_bg = property_value
            self.update_colour_preview()
            
        elif property_name == self.lbl_property_colour_preview:
            pass
            
        elif property_name == self.lbl_property_image:
            self._v_property_image_file_name = property_value
            
        elif property_name == self.lbl_property_attributes:
            self._v_property_attributes = property_value
            c = self.GetPropertyChoices(p)
            print c.GetValues()
            print c.GetLabels()
            print c.GetLabel(0)
            print c.GetValue(0)
            print property_value
            if  property_value & wx.propgrid.PG_BOOL_USE_CHECKBOX:
                print "TREue"
            
        else:
            pnt = self.GetPropertyParent(p)
            if pnt:
                if self.GetPropertyName(self.GetPropertyParent(pnt)) == "Attributes":
                    id = int(property_name[0:2])
                    d = property_name[2:3]
                    # Now get the property attribute object and update it.
                    attribute = self._v_property_attributes[id]
                    if d == "S":    # Set
                        attribute.is_set = property_value
                    elif d == "V":    # Value
                        attribute.value = property_value
                    elif d == "F":    # Flag
                        attribute.flags_is_set = property_value
                    else:    # Error
                        print "Error"
                else:
                    if self._v_debug and self._v_debug_level > 1999:
                        msg = ( "Invalid!  Property name: %s value: %s") % ( property_name, str(property_value) )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        print msg
                        print "parent:", self.GetPropertyName(pnt), " grandparent:", self.GetPropertyName(self.GetPropertyParent(pnt))
                        
            else:
                if self._v_debug and self._v_debug_level > 1999:
                    msg = ( "Invalid!  Property name: %s value: %s") % ( property_name, str(property_value) )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    print msg
                    
        
        
        
    def get_page(self):
        return self._v_property_page
        
    def get_type(self):
        return self._v_property_type
        
    def get_category(self):
        return self._v_property_category
        
    def get_parent(self):
        return self._v_property_parent
        
    def get_datatype(self):
        return self._v_property_datatype
        
    def get_name(self):
        return self._v_property_name
        
    def set_name(self, new_value):
        self._v_property_name = new_value
        
    def get_label(self):
        return self._v_property_label
        
    def get_choices(self):
        return self._v_property_choices
        
    def get_values(self):
        return self._v_property_values
        
    def get_value(self):
        return self._v_property_value
        
    def get_help(self):
        return self._v_property_help
        
    def get_is_enabled(self):
        return self._v_property_is_enabled
        
    def get_is_default(self):
        return self._v_property_is_default
        
    def get_is_low_priority(self):
        return self._v_property_is_low_priority
        
    def get_colour_txt(self):
        return self._v_property_colour_txt
        
    def get_colour_bg(self):
        return self._v_property_colour_bg
        
    def get_image_file_name(self):
        return self._v_property_image_file_name
        
    def get_attributes(self):
        return self._v_property_attributes
        
    property_page = property(fget=get_page, doc="The page property.")
    property_type = property(fget=get_type, doc="The type property.")
    property_category = property(fget=get_category, doc="The category property.")
    property_parent = property(fget=get_parent, doc="The parent property.")
    property_datatype = property(fget=get_datatype, doc="The datatype property.")
    property_name = property(fget=get_name, fset=set_name, doc="The name property.")
    property_label = property(fget=get_label, doc="The label property.")
    property_choices = property(fget=get_choices, doc="The choices property.")
    property_values = property(fget=get_values, doc="The values property.")
    property_value = property(fget=get_value, doc="The value property.")
    property_help = property(fget=get_help, doc="The help property.")
    property_is_enabled = property(fget=get_is_enabled, doc="The is_enabled property.")
    property_is_default = property(fget=get_is_default, doc="The is_default property.")
    property_is_low_priority = property(fget=get_is_low_priority, doc="The is_low_priority property.")
    property_colour_txt = property(fget=get_colour_txt, doc="The colour_txt property.")
    property_colour_bg = property(fget=get_colour_bg, doc="The colour_bg property.")
    property_image_file_name = property(fget=get_image_file_name, doc="The image_file_name property.")
    property_attributes = property(fget=get_attributes, doc="The attributes property.")
    
    
