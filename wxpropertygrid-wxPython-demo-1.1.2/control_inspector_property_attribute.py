# What's an attribute?

import wx

class Property_Attribute(object):
    def __init__(self):
        pass
        # print "Property_Attribute"
        self.mf = wx.GetApp().GetTopWindow()	# I like it!
        self._v_log = self.mf
        self._v_debug = self.mf._v_debug
        self._v_debug_level = self.mf._v_debug_level
        
        self._v_name = "" # Name and Label for the property attribute.
        self._v_number = 0  # The flag-mask constant for this property attribute.
        self._v_is_set = False  # Is this property attribute on or off?
        self._v_value_label = "" # Label for the property attribute value.
        self._v_value_datatype = "" # Datatype for the property attribute value.
        self._v_value_dict = {} # Dictionary of choices and values for ENUMproperty datatype.
        self._v_value = None
        self._v_value_desc = "" # Help string for the property attribute value.
        self._v_flags_label = "" # Label for the property attribute flag.
        self._v_flags_number = 0  # The flag-mask constant for this property attribute flag.
        self._v_flags_is_set = False  # Is this property attribute flag on or off?
        self._v_flags_desc = "" # Help string for the property attribute flag.
        self._v_enabled = False
        self._v_desc = "" # Help string for the property attribute.
        
        
    def get_name(self):
        return self._v_name
        
    def set_name(self, new_value):
        self._v_name = new_value
    
    
    def get_number(self):
        return self._v_number
        
    def set_number(self, new_value):
        self._v_number = new_value
    
    
    def get_is_set(self):
        return self._v_is_set
        
    def set_is_set(self, new_value):
        self._v_is_set = new_value
    
    
    def get_value_label(self):
        return self._v_value_label
        
    def set_value_label(self, new_value):
        self._v_value_label = new_value
    
    
    def get_value_datatype(self):
        return self._v_value_datatype
        
    def set_value_datatype(self, new_value):
        self._v_value_datatype = new_value
    
    
    def get_value_dict(self):
        return self._v_value_dict
        
    def set_value_dict(self, new_value):
        self._v_value_dict = new_value
    
    
    def get_value(self):
        return self._v_value
        
    def set_value(self, new_value):
        self._v_value = new_value
    
    
    def get_value_desc(self):
        return self._v_value_desc
        
    def set_value_desc(self, new_value):
        self._v_value_desc = new_value
        
    
    def get_flags_label(self):
        return self._v_flags_label
        
    def set_flags_label(self, new_value):
        self._v_flags_label = new_value
    
    
    def get_flags_number(self):
        return self._v_flags_number
        
    def set_flags_number(self, new_value):
        self._v_flags_number = new_value
    
    
    def get_flags_is_set(self):
        return self._v_flags_is_set
        
    def set_flags_is_set(self, new_value):
        self._v_flags_is_set = new_value
    
    
    def get_flags_desc(self):
        return self._v_flags_desc
        
    def set_flags_desc(self, new_value):
        self._v_flags_desc = new_value
        
    
    def get_enabled(self):
        return self._v_enabled
        
    def set_enabled(self, new_value):
        self._v_enabled = new_value
    
    
    def get_desc(self):
        return self._v_desc
        
    def set_desc(self, new_value):
        self._v_desc = new_value
    
    
    
    name = property(fget=get_name, fset=set_name, doc="The name property.")
    number = property(fget=get_number, fset=set_number, doc="The number property.")
    is_set = property(fget=get_is_set, fset=set_is_set, doc="The is_set property.")
    value_label = property(fget=get_value_label, fset=set_value_label, doc="The value_label property.")
    value_datatype = property(fget=get_value_datatype, fset=set_value_datatype, doc="The value_datatype property.")
    value_dict = property(fget=get_value_dict, fset=set_value_dict, doc="The value_dict property.")
    value = property(fget=get_value, fset=set_value, doc="The value property.")
    value_desc = property(fget=get_value_desc, fset=set_value_desc, doc="The value_description property.")
    flags_label = property(fget=get_flags_label, fset=set_flags_label, doc="The flags_label property.")
    flags_number = property(fget=get_flags_number, fset=set_flags_number, doc="The flags_number property.")
    flags_is_set = property(fget=get_flags_is_set, fset=set_flags_is_set, doc="The flags_is_set property.")
    flags_desc = property(fget=get_flags_desc, fset=set_flags_desc, doc="The flags_description property.")
    enabled = property(fget=get_enabled, fset=set_enabled, doc="The enabled property.")
    desc = property(fget=get_desc, fset=set_desc, doc="The description property.")
    
    