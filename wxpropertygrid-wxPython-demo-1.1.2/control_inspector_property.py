# What's a property?

import wx
import wx.propgrid
import datetime
import control_inspector_mytime_property
import dialog_property
import ptl

class PropertyGrid_Property(object):
    def __init__(self, parent=None):
        pass
        # print "PropertyGrid_Property"
        self.parent = parent
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        self._v_log = self.mf
        self._v_debug = self.mf._v_debug
        self._v_debug_level = self.mf._v_debug_level
        
        
    def add(self, page = 0, property_type = ptl.PROPERTY_TYPE_NORMAL, category = None, property_datatype_name="", property_name="", property_label="", property_value=None, help_string=None, low_priority=None, enabled=True, default=False, colour_txt=None, colour_bg=None, icon_name=None, attributes=None, property_choices=None, property_values=None):
        func_name = "add"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        result = -1
        p_id1 = None
        
        self._v_page = page
        self.parent.SelectPage(self._v_page)
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "property_datatype_name: %s: %s: page: %d ") % ( property_datatype_name, property_name, self._v_page)
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "property_type: %s ") % ( property_type, )
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        if property_type == "Category Member":
            if category and category != "None":
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ( "category: %s ") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                category_id = self.parent.GetPropertyByName( category )
                if category_id:
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes,property_choices=property_choices, property_values=property_values)
                    result = p_id1
                else:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "No category id for: %s ") % ( category, )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        
                    category_id = self.parent.Append( wx.propgrid.PropertyCategory( category ) )
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                    result = p_id1
                    
            else:
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ( "Must specify category for 'Category Member' type %s") % ( property_name, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
        elif property_type == "Category":
            if category and category != "None":
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ( "category: %s ") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                # category_id = self.parent.GetPropertyCategory( category ) # Broken.  Only works if category is a pg_id.
                category_id = self.parent.GetPropertyByName( category )
                if category_id:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "category_id: %s ") % ( str(category_id), )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=ptl.PROPERTY_DATATYPE_CATEGORY, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                    result = p_id1
                else:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "No category id for: %s ") % ( category, )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        
                    category_id = self.parent.Append( wx.propgrid.PropertyCategory( category ) )
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=ptl.PROPERTY_DATATYPE_CATEGORY, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                    result = p_id1
            else:
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ( "category: %s ") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                # Null category is the same as 'Normal' property type.
                # Root level category
                p_id1 = self.append( property_datatype_name=ptl.PROPERTY_DATATYPE_CATEGORY, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                result = p_id1
            
        elif property_type == "Normal":
                p_id1 = self.append( property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                result = p_id1
            
        elif property_type == "Parent":
            if category and category != "None":
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ( "category: %s ") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                category_id = self.parent.GetPropertyByName( category )
                if category_id:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = "category found."
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=ptl.PROPERTY_DATATYPE_PARENT, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                    result = p_id1
                else:
                    if self._v_debug and self._v_debug_level > 5999:
                        msg = ( "No category id for: %s ") % ( category, )
                        self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                        
                    category_id = self.parent.Append( wx.propgrid.PropertyCategory( category ) )
                    p_id1 = self.insert( category_id=category_id, property_datatype_name=ptl.PROPERTY_DATATYPE_PARENT, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                    result = p_id1
            else:
                # Null category is the same as 'Normal' property type.
                # Root level category
                p_id1 = self.append( property_datatype_name=ptl.PROPERTY_DATATYPE_PARENT, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                result = p_id1
            
        elif property_type == "Child":
            parent_id = self.parent.GetPropertyByName( category )
            if parent_id:
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ("parent found. %s") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                p_id1 = self.insert( category_id=parent_id, property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
                result = p_id1
            else:
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ("parent not found. %s") % ( category, )
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        else:
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "invalid property type: %s ") % ( property_type, )
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                print msg
                
            
        if result == -1:
            pass
            if self._v_debug and self._v_debug_level > 2999:
                msg = ( "add failed.  property datatype name: %s, name: %s ") % ( property_datatype_name, property_name)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                print msg
                
        else:
            self.set_attributes(property_id = p_id1, help_string=help_string, low_priority=low_priority, enabled=enabled, default=default, dict_attributes=attributes, colour_txt=colour_txt, colour_bg=colour_bg, icon_name=icon_name )
        
        self.parent.Refresh()
        return result
            
            
    def set_attributes(self, property_id = None, help_string=None, low_priority=None, enabled=True, default=False, dict_attributes={}, colour_txt=None, colour_bg=None, icon_name=None):
        func_name = "set_attributes"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "enabled: %s default: %s txt: %s bg: %s") % ( enabled, default, str(colour_txt), str(colour_bg))
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        if property_id:
            if help_string:
                self.parent.SetPropertyHelpString(property_id, help_string)
            if low_priority:
                self.parent.SetPropertyPriority(property_id, wx.propgrid.PG_LOW)
            if not enabled:
                self.parent.DisableProperty(property_id)
            if default:
                r = 0
                g =0
                b = 255
                a = 255
                new_colour = wx.Colour( r, g, b, a)
                self.parent.SetPropertyTextColour( property_id, new_colour )
                self._v_default_property[self._v_page] = property_id
                self._v_default_exists = True
            if dict_attributes:
                pass
                keys = dict_attributes.keys()
                for key in keys:
                    attribute = dict_attributes[key]
                    if attribute.is_set:
                        if self._v_debug and self._v_debug_level > 5999:
                            msg = ( "attribute: %s on: %s value: %s flag: %s flag #: %s") % ( attribute.name, str(attribute.is_set), str(attribute.value), str(attribute.flags_is_set), str(attribute.flags_number))
                            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                            # print msg
                            
                        if attribute.flags_is_set:
                            self.parent.SetPropertyAttribute(property_id, attribute.number, attribute.is_set, long(attribute.flags_number))
                        else:
                            self.parent.SetPropertyAttribute(property_id, attribute.number, attribute.is_set, attribute.value)
                    
                
            
            if colour_txt:
                property_datatype = self.parent.GetPVTN(property_id)
                # If property_datatype is Null, it is a category
                if property_datatype == "null":
                    property_datatype = "Category"
                if property_datatype == "Category":
                    # wx.MessageBox( str(dir(self.parent)) )
                    # self.parent.SetCaptionForegroundColour( property_id, colour_txt )
                    self.parent.SetPropertyTextColour( property_id, colour_txt )
                else:
                    self.parent.SetPropertyTextColour( property_id, colour_txt )
            if colour_bg:
                self.parent.SetPropertyBackgroundColour( property_id, colour_bg )
            if icon_name:
                # icon = wx.LoadImage(icon_name)
                icon = self.parent.import_file( file_name = icon_name )
                self.parent.SetPropertyImage( property_id, icon )
            
    def insert(self, category_id=None, property_datatype_name="", property_name="", property_label="", property_value=None, attributes=None, property_choices=None, property_values=None):
        func_name = "insert"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id1 = None
        
        if category_id:
            if self._v_debug and self._v_debug_level > 5999:
                msg = ( "property_datatype_name: %s: %s ") % ( property_datatype_name, property_name)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self.parent.SelectPage(self._v_page)
            
            prop = self.create(property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
            p_id1 = self.parent.AppendIn( category_id, prop )
            self.parent.Refresh()
            
        
        return p_id1
        
        
    def create(self, property_datatype_name="", property_name="", property_label="", property_value=None, attributes=None, property_choices=None, property_values=None):
        func_name = "create"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "property_datatype_name: %s: %s ") % ( property_datatype_name, property_name)
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        new_prop = None
        
        if property_datatype_name == ptl.PROPERTY_DATATYPE_TEXT or property_datatype_name == ptl.PROPERTY_DATATYPE_STRING:
            new_prop = wx.propgrid.StringProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_FONT:
            new_prop = wx.propgrid.FontProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_FONTDATA:
            new_prop = wx.propgrid.FontDataProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_COLOUR:
            new_prop = wx.propgrid.ColourProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_SYSTEMCOLOUR:
            new_prop = wx.propgrid.SystemColourProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_CURSOR:
            new_prop = wx.propgrid.CursorProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_SIZE:
            new_prop = wx.propgrid.SizeProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_POINT:
            new_prop = wx.propgrid.PointProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_DIR:
            new_prop = wx.propgrid.DirProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_DIRS:
            new_prop = wx.propgrid.DirsProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_LONGSTRING:
            new_prop = wx.propgrid.LongStringProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_ADVIMAGEFILE:
            new_prop = wx.propgrid.AdvImageFileProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_CUSTOM:
            new_prop = wx.propgrid.CustomProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_IMAGEFILE:
            new_prop = wx.propgrid.ImageFileProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_FILE:
            new_prop = wx.propgrid.FileProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_ENUM:
            if property_choices:
                new_prop = wx.propgrid.EnumProperty(name=property_name, label=property_label, choices=property_choices, values=property_values)
            else:
                new_prop = wx.propgrid.EnumProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_EDITENUM:
            if property_choices:
                new_prop = wx.propgrid.EditEnumProperty(name=property_name, label=property_label, choices=property_choices, values=property_values)
            else:
                new_prop = wx.propgrid.EditEnumProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_MULTICHOICE:
            if property_choices:
                new_prop = wx.propgrid.EditEnumProperty(name=property_name, label=property_label, choices=property_choices, values=property_values)
            else:
                new_prop = wx.propgrid.EditEnumProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_FLAGS:
            new_prop = wx.propgrid.FlagsProperty(name=property_name, label=property_label, flag_labels=property_choices, values=property_values, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_ARRAYSTRING:
            if property_choices:
                new_prop = wx.propgrid.ArrayStringProperty(name=property_name, label=property_label, choices=property_choices, values=property_values)
            else:
                new_prop = wx.propgrid.ArrayStringProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_ARRAYDOUBLE:
            if property_choices:
                new_prop = wx.propgrid.ArrayDoubleProperty(name=property_name, label=property_label, choices=property_choices, values=property_values)
            else:
                new_prop = wx.propgrid.ArrayDoubleProperty(name=property_name, label=property_label)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_NUMERIC:
            new_prop = wx.propgrid.FloatProperty(name=property_name, label=property_label, value=float(property_value))
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_FLOAT:
            new_prop = wx.propgrid.FloatProperty(name=property_name, label=property_label, value=float(property_value))
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_INTEGER:
            new_prop = wx.propgrid.IntProperty(name=property_name, label=property_label, value=float(property_value))
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_UINTEGER:
            new_prop = wx.propgrid.UIntProperty(name=property_name, label=property_label, value=float(property_value))
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_LOGICAL or property_datatype_name == ptl.PROPERTY_DATATYPE_BOOLEAN:
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
            new_prop = wx.propgrid.BoolProperty(name=property_name, label=property_label, value=property_value)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_DATE:
            d_day = property_value.Day  # datetime module uses Caps! weird.
            d_month = property_value.Month
            d_year = property_value.Year
            wxdate = wx.DateTime_Now()	# Initialize the variable
            wx.DateTime.Set(wxdate, d_day, d_month, d_year)	# Set the value
            
            new_prop = wx.propgrid.DateProperty(name=property_name, label=property_label, value=wxdate)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_TIME:
            new_prop = control_inspector_mytime_property.MyTimeProperty(name=property_name, label=property_label, value=property_value)
            # self.parent.SetPropertyEditor(new_prop, "clock")
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_DATETIME:
            d_second = property_value.Second
            d_minute = property_value.Minute
            d_hour = property_value.Hour
            d_day = property_value.Day
            d_month = property_value.Month
            d_year = property_value.Year
            
            wxdate = wx.DateTime.Now()	# Initialize the variable
            wxdate.Set(day=d_day, month=d_month, year=d_year, hour=d_hour, minute=d_minute, second=d_second)	# Set the value
            
            if wxdate.IsValid():
                pass
            else:
                print "DateTime error"
                wxdate = wx.DateTime.Now()
            
            new_prop = wx.propgrid.DateProperty(name=property_name, label=property_label, value=wxdate)
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_CATEGORY:
            new_prop = wx.propgrid.PropertyCategory(name=property_name, label=property_label )
            
        elif property_datatype_name == ptl.PROPERTY_DATATYPE_PARENT:
            new_prop = wx.propgrid.ParentProperty(name=property_name, label=property_label )
            
        else:
            if self._v_debug and self._v_debug_level > 1999:
                msg = ( "Invalid property type name: %s") % ( property_datatype_name)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                print msg
        
        return new_prop
        
        
    def create_parent(self, property_name="", property_label="", attributes=None):
        func_name = "create_parent"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        new_prop = None
        
        new_prop = wx.propgrid.ParentProperty(name=property_name, label=property_label)
        
        return new_prop
        
        
    def append(self, property_datatype_name="", property_name="", property_label="", property_value=None, attributes=None, property_choices=None, property_values=None):
        func_name = "append"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        if self._v_debug and self._v_debug_level > 5999:
            msg = ( "property_datatype_name: %s: %s ") % ( property_datatype_name, property_name)
            self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
            
        p_id1 = None
        
        self.parent.SelectPage(self._v_page)
        prop = self.create(property_datatype_name=property_datatype_name, property_name=property_name, property_label=property_label, property_value=property_value, attributes=attributes, property_choices=property_choices, property_values=property_values)
        self.unset_current_category()
        p_id1 = self.parent.Append( prop )
        if property_datatype_name == ptl.PROPERTY_DATATYPE_TIME:
            # self.parent.EnsureVisible(p_id1)
            self.parent.SetPropertyEditor(p_id1, "clock")
        self.parent.Refresh()
        
        return p_id1
        
        
    def unset_current_category(self):
        func_name = "unset_current_category"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
            
        # Call this before adding 'Normal' properties that you don't want to appear inside any category.
        category_id = self.parent.Append( wx.propgrid.PropertyCategory( "zzxyz" ) )
        self.parent.Delete( category_id )
        
        
    def on_add_category(self, event):
        func_name = "on_add_category"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dlg = dialog_property.Dialog_Property_Create(page = self.parent._v_page, type = ptl.PROPERTY_TYPE_CATEGORY, category=None, datatype=ptl.PROPERTY_DATATYPE_TEXT, title="Add Category", parent=self.parent)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            pass
            prop_page = dlg.property_page
            prop_type = dlg.property_type
            prop_category = dlg.property_category
            prop_parent = dlg.property_parent
            prop_datatype = dlg.property_datatype
            prop_name = dlg.property_name
            prop_label = dlg.property_label
            prop_value = dlg.property_value
            prop_help = dlg.property_help
            prop_is_enabled = dlg.property_is_enabled
            prop_is_default = dlg.property_is_default
            prop_is_low_priority = dlg.property_is_low_priority
            prop_colour_txt = dlg.property_colour_txt
            prop_colour_bg = dlg.property_colour_bg
            prop_image_file_name = dlg.property_image_file_name
            prop_attributes = dlg.property_attributes
            if prop_type == ptl.PROPERTY_TYPE_CHILD:
                prop_category = prop_parent
                
            if self._v_debug and self._v_debug_level > 5999:
                msg = ("Page: %d, Type: %s, Category: %s, DataType: %s") % (prop_page, prop_type, prop_category, prop_datatype)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("Name: %s, Label: %s, Value: %s") % (prop_name, prop_label, str(prop_value))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("txt: %s, bg: %s, image: %s") % (str(prop_colour_txt), str(prop_colour_bg), str(prop_image_file_name))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self.p_id1 = self.add( page = prop_page, property_type = prop_type, category = prop_category, property_datatype_name=prop_datatype, property_name=prop_name, property_label=prop_label, property_value=prop_value, help_string=prop_help, low_priority=prop_is_low_priority, enabled=prop_is_enabled, default=prop_is_default, colour_txt=prop_colour_txt, colour_bg=prop_colour_bg, icon_name=prop_image_file_name)
            self._v_current_property = prop_name
            
        else:
            pass
        dlg.Destroy()
        
    def on_edit_category(self, event):
        func_name = "on_edit_category"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.parent.GetSelectedProperty()
        if p_id:
            prop_name = self.parent.GetPropertyName( p_id )
            print prop_name
            self._v_current_property = prop_name
            class_name = self.parent.GetPropertyClassName(p_id)
            print class_name
            current_type = None
            current_category = None
            if class_name == "wxPropertyCategory":
                current_type = ptl.PROPERTY_TYPE_CATEGORY
            elif class_name == "wxParentProperty":
                current_type = ptl.PROPERTY_DATATYPE_PARENT
            else:
                parent_id = self.parent.GetPropertyParent(p_id)
                parent_datatype = self.parent.GetPropertyClassName(parent_id)
                print parent_datatype
                if parent_datatype == "wxParentProperty":
                    current_type = ptl.PROPERTY_TYPE_CHILD
                    current_category = self.parent.GetPropertyName( parent_id )
                elif parent_datatype == "wxPGRootProperty":
                    current_type = ptl.PROPERTY_TYPE_NORMAL
                    current_category = None
                elif parent_datatype == "wxPropertyCategory":
                    current_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
                    current_category = self.parent.GetPropertyName( parent_id )
                else:
                    print "I don't know that it is."
            print current_type
            print current_category
            dlg = dialog_property.Dialog_Property_Create(page = self.parent._v_page, type=current_type, category=current_category, datatype=ptl.PROPERTY_DATATYPE_TEXT, property_id = p_id, title="Edit Property", parent=self.parent)
            retval = dlg.ShowModal()
            if retval == wx.ID_OK:
                pass
                prop_page = dlg.property_page
                prop_type = dlg.property_type
                prop_category = dlg.property_category
                prop_parent = dlg.property_parent
                prop_datatype = dlg.property_datatype
                prop_name = dlg.property_name
                prop_label = dlg.property_label
                prop_value = dlg.property_value
                prop_help = dlg.property_help
                prop_is_enabled = dlg.property_is_enabled
                prop_is_default = dlg.property_is_default
                prop_is_low_priority = dlg.property_is_low_priority
                prop_colour_txt = dlg.property_colour_txt
                prop_colour_bg = dlg.property_colour_bg
                prop_image_file_name = dlg.property_image_file_name
                prop_attributes = dlg.property_attributes
                if prop_type == ptl.PROPERTY_TYPE_CHILD:
                    prop_category = prop_parent
                    
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ("Page: %d, Type: %s, Category: %s, DataType: %s") % (prop_page, prop_type, prop_category, prop_datatype)
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    msg = ("Name: %s, Label: %s, Value: %s") % (prop_name, prop_label, str(prop_value))
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    msg = ("txt: %s, bg: %s, image: %s") % (str(prop_colour_txt), str(prop_colour_bg), str(prop_image_file_name))
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                # self.parent.SetPropertyLabel( p_id, prop_label )    # This produces GPF crash for category properties. (referenced memory at 30)
                p_id.SetLabel( prop_label ) # This works for properties and categories.
                wx.MessageBox( message=str(dir(p_id)), caption="Edit Category", style=wx.OK | wx.ICON_ERROR )
                wx.MessageBox( message=str(dir(self.parent)), caption="Edit Category", style=wx.OK | wx.ICON_ERROR )
                self.set_attributes( property_id = p_id, help_string=prop_help, low_priority=prop_is_low_priority, enabled=prop_is_enabled, default=prop_is_default, colour_txt=prop_colour_txt, colour_bg=prop_colour_bg, icon_name=prop_image_file_name )
                self.parent.Refresh()
                
            else:
                pass
            dlg.Destroy()
            
        else:
            wx.MessageBox( message="No category selected.", caption="Edit Category", style=wx.OK | wx.ICON_ERROR )
        
        
    def on_delete_category(self, event):
        func_name = "on_delete_category"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.parent.GetSelectedProperty()
        if p_id:
            if self.parent.IsPropertyCategory(p_id):
                self._v_property_category = self.parent.GetPropertyName(p_id)
                property_name = self.parent.GetPropertyName( p_id )
                self._v_current_property = property_name
                self.parent.Delete( self._v_current_property )
            else:
                wx.MessageBox( message="No category selected.", caption="Delete Category", style=wx.OK | wx.ICON_ERROR )
        else:
            wx.MessageBox( message="No category selected.", caption="Delete Category", style=wx.OK | wx.ICON_ERROR )
        
        
    def on_add(self, event):
        func_name = "on_add"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        dlg = dialog_property.Dialog_Property_Create(page = self.parent._v_page, category=None, datatype=ptl.PROPERTY_DATATYPE_TEXT, parent=self.parent)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            pass
            prop_page = dlg.property_page
            prop_type = dlg.property_type
            prop_category = dlg.property_category
            prop_parent = dlg.property_parent
            prop_datatype = dlg.property_datatype
            prop_name = dlg.property_name
            prop_label = dlg.property_label
            prop_choices = dlg.property_choices
            prop_values = dlg.property_values
            prop_value = dlg.property_value
            prop_help = dlg.property_help
            prop_is_enabled = dlg.property_is_enabled
            prop_is_default = dlg.property_is_default
            prop_is_low_priority = dlg.property_is_low_priority
            prop_colour_txt = dlg.property_colour_txt
            prop_colour_bg = dlg.property_colour_bg
            prop_image_file_name = dlg.property_image_file_name
            prop_attributes = dlg.property_attributes
            if prop_type == ptl.PROPERTY_TYPE_CHILD:
                prop_category = prop_parent
                
            if self._v_debug and self._v_debug_level > 5999:
                msg = ("Page: %d, Type: %s, Category: %s, DataType: %s") % (prop_page, prop_type, prop_category, prop_datatype)
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("Name: %s, Label: %s, Value: %s") % (prop_name, prop_label, str(prop_value))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                msg = ("txt: %s, bg: %s, image: %s") % (str(prop_colour_txt), str(prop_colour_bg), str(prop_image_file_name))
                self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                
            self.p_id1 = self.add( page = prop_page, property_type = prop_type, category = prop_category, property_datatype_name=prop_datatype, property_name=prop_name, property_label=prop_label, property_choices=prop_choices, property_values=prop_values, property_value=prop_value, help_string=prop_help, low_priority=prop_is_low_priority, enabled=prop_is_enabled, default=prop_is_default, attributes=prop_attributes, colour_txt=prop_colour_txt, colour_bg=prop_colour_bg, icon_name=prop_image_file_name)
            self._v_current_property = prop_name
            
        else:
            pass
        dlg.Destroy()
        
    def on_edit(self, event):
        func_name = "on_edit"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.parent.GetSelectedProperty()
        if p_id:
            prop_name = self.parent.GetPropertyName( p_id )
            self._v_current_property = prop_name
            class_name = self.parent.GetPropertyClassName(p_id)
            # print class_name
            current_type = None
            current_category = None
            if class_name == "wxPropertyCategory":
                current_type = ptl.PROPERTY_TYPE_CATEGORY
            elif class_name == "wxParentProperty":
                current_type = ptl.PROPERTY_DATATYPE_PARENT
            else:
                parent_id = self.parent.GetPropertyParent(p_id)
                parent_datatype = self.parent.GetPropertyClassName(parent_id)
                print parent_datatype
                if parent_datatype == "wxParentProperty":
                    current_type = ptl.PROPERTY_TYPE_CHILD
                    current_category = self.parent.GetPropertyName( parent_id )
                elif parent_datatype == "wxPGRootProperty":
                    current_type = ptl.PROPERTY_TYPE_NORMAL
                    current_category = None
                elif parent_datatype == "wxPropertyCategory":
                    current_type = ptl.PROPERTY_TYPE_CATEGORY_MEMBER
                    current_category = self.parent.GetPropertyName( parent_id )
                else:
                    print "I don't know what it is."
            # print current_type
            # print current_category
            dlg = dialog_property.Dialog_Property_Create(page = self.parent._v_page, type=current_type, category=current_category, datatype=ptl.PROPERTY_DATATYPE_TEXT, property_id = p_id, title="Edit Property", parent=self.parent)
            retval = dlg.ShowModal()
            if retval == wx.ID_OK:
                pass
                prop_page = dlg.property_page
                prop_type = dlg.property_type
                prop_category = dlg.property_category
                prop_parent = dlg.property_parent
                prop_datatype = dlg.property_datatype
                prop_name = dlg.property_name
                prop_label = dlg.property_label
                prop_value = dlg.property_value
                prop_help = dlg.property_help
                prop_is_enabled = dlg.property_is_enabled
                prop_is_default = dlg.property_is_default
                prop_is_low_priority = dlg.property_is_low_priority
                prop_colour_txt = dlg.property_colour_txt
                prop_colour_bg = dlg.property_colour_bg
                prop_image_file_name = dlg.property_image_file_name
                prop_attributes = dlg.property_attributes
                if prop_type == ptl.PROPERTY_TYPE_CHILD:
                    prop_category = prop_parent
                    
                if self._v_debug and self._v_debug_level > 5999:
                    msg = ("Page: %d, Type: %s, Category: %s, DataType: %s") % (prop_page, prop_type, prop_category, prop_datatype)
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    msg = ("Name: %s, Label: %s, Value: %s") % (prop_name, prop_label, str(prop_value))
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    msg = ("txt: %s, bg: %s, image: %s") % (str(prop_colour_txt), str(prop_colour_bg), str(prop_image_file_name))
                    self._v_log.write(("%s:%s:%s") % (self.__class__, func_name, msg))
                    
                # wx.MessageBox( message=str(dir(p_id)), caption="Edit Property", style=wx.OK | wx.ICON_ERROR )
                # self.parent.SetPropertyLabel( p_id, prop_label )    # This produces GPF crash for category properties. (referenced memory at 30)
                p_id.SetLabel( prop_label ) # This works for properties and categories.
                
                self.set_attributes( property_id = p_id, help_string=prop_help, low_priority=prop_is_low_priority, enabled=prop_is_enabled, default=prop_is_default, colour_txt=prop_colour_txt, colour_bg=prop_colour_bg, icon_name=prop_image_file_name )
                self.parent.Refresh()
                
            else:
                pass
            dlg.Destroy()
            
        else:
            wx.MessageBox( message="No property selected.", caption="Edit Property", style=wx.OK | wx.ICON_ERROR )
        
        
    def on_delete(self, event):
        func_name = "on_delete"
        if self._v_debug and self._v_debug_level > 5999:
            self._v_log.write(("%s:%s") % (self.__class__, func_name))
        
        p_id = self.parent.GetSelectedProperty()
        if p_id:
            self.parent.Delete( p_id )
            # parent_id = self.parent.GetPropertyParent(p_id)
            # parent_class = self.parent.GetPropertyClassName(parent_id)
            # print str(parent_class)
            # property_name = self.parent.GetPropertyName( p_id )
            # property_class = self.parent.GetPropertyClassName(p_id)
            # print str(property_class)
            # self._v_current_property = property_name
            # if parent_class == ptl.PROPERTY_DATATYPE_PARENT:
                # self.parent.Delete( parent_id.p_id )
            # else:
                # self.parent.Delete( p_id )
                # self.parent.Delete( self._v_current_property )
        else:
            wx.MessageBox( message="No property selected.", caption="Delete Property", style=wx.OK | wx.ICON_ERROR )
        
        
    
    
    
