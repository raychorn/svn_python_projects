import wx
import control_property_properties
import ptl


class Dialog_Property_Create(wx.Dialog):
    """\
    Dialog creating properties.
    """
    def __init__(self, page = 0, type = ptl.PROPERTY_TYPE_NORMAL, category = None, datatype = None, property_id = None, parent=None, id=-1, title="New Property", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.OK|wx.CANCEL|wx.CENTER, pos=(500, 200)):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, style=style, pos=pos)
        
        self.parent = parent
        self.pg = self.parent
        self._v_page = page
        if self._v_page > -1:
            self.pg.SelectPage(self._v_page)
        self._v_category = category
        self._v_parent = ""
        self._v_property_datatype = datatype
        self._v_property_id = property_id
        self._v_property_name = ""
        self._v_property_label = ""
        self._v_property_choices = []
        self._v_property_values = []
        self._v_property_value = ""
        self._v_property_help = ""
        self._v_property_is_enabled = True
        self._v_property_is_default = False
        self._v_property_is_low_priority = True
        self._v_property_colour_bg = ""
        self._v_property_colour_txt = ""
        self._v_property_image_file_name = ""
        self._v_property_attributes = {}
        
        orientation_v = wx.VERTICAL
        orientation_h = wx.HORIZONTAL
        no_border = 0
        border_width = 5
        controls_border_width = 3
        frame_border_width = 5
        value_border_width = 25
        toolbar_border_width = 15
        controls_width = 200
        
        self.sizer = wx.BoxSizer(orientation_v)
        self.pg2 = control_property_properties.PP( parent = self, page = self._v_page, type = type, category = self._v_category, datatype = self._v_property_datatype, property_id = self._v_property_id )
        self.sizer.Add(self.pg2, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.btnsizer = wx.StdDialogButtonSizer()
        
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        self.sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP, 5)
        
        self.btn = wx.Button(self, wx.ID_OK)
        self.btn.SetDefault()
        self.btnsizer.SetAffirmativeButton(self.btn)
        
        self.btn = wx.Button(self, wx.ID_CANCEL)
        self.btnsizer.SetCancelButton(self.btn)
        
        self.btnsizer.Realize()
        
        self.sizer.Add(self.btnsizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.sizer.Fit(self)
        #self.SetFocus()
        
        self.SetPosition( wx.Point(400, 60) )
        # self.SetSize( wx.Size(620, 800) )
        self.SetSize( wx.Size(620, 600) )
        
        
    def get_page(self):
        self._v_page = self.pg2.property_page
        return self._v_page
        
    def get_type(self):
        self._v_property_type = self.pg2.property_type
        return self._v_property_type
        
    def get_category(self):
        self._v_category = self.pg2.property_category
        return self._v_category
        
    def get_parent(self):
        self._v_parent = self.pg2.property_parent
        return self._v_parent
        
    def get_datatype(self):
        self._v_property_datatype = self.pg2.property_datatype
        return self._v_property_datatype
        
    def get_name(self):
        self._v_property_name = self.pg2.property_name
        return self._v_property_name
        
    def get_label(self):
        self._v_property_label = self.pg2.property_label
        return self._v_property_label
        
    def get_choices(self):
        self._v_property_choices = self.pg2.property_choices
        return self._v_property_choices
        
    def get_values(self):
        self._v_property_values = self.pg2.property_values
        return self._v_property_values
        
    def get_value(self):
        self._v_property_value = self.pg2.property_value
        return self._v_property_value
        
    def get_help(self):
        self._v_property_help = self.pg2.property_help
        return self._v_property_help
        
    def get_is_enabled(self):
        self._v_property_is_enabled = self.pg2.property_is_enabled
        return self._v_property_is_enabled
        
    def get_is_default(self):
        self._v_property_is_default = self.pg2.property_is_default
        return self._v_property_is_default
        
    def get_is_low_priority(self):
        self._v_property_is_low_priority = self.pg2.property_is_low_priority
        return self._v_property_is_low_priority
        
    def get_colour_bg(self):
        self._v_property_colour_bg = self.pg2.property_colour_bg
        return self._v_property_colour_bg
        
    def get_colour_txt(self):
        self._v_property_colour_txt = self.pg2.property_colour_txt
        return self._v_property_colour_txt
        
    def get_image_file_name(self):
        self._v_property_image_file_name = self.pg2.property_image_file_name
        return self._v_property_image_file_name
        
    def get_attributes(self):
        self._v_property_attributes = self.pg2.property_attributes
        return self._v_property_attributes
        
    property_page = property(fget=get_page, doc="The page property.")
    property_type = property(fget=get_type, doc="The type property.")
    property_category = property(fget=get_category, doc="The category property.")
    property_parent = property(fget=get_parent, doc="The parent property.")
    property_datatype = property(fget=get_datatype, doc="The datatype property.")
    property_name = property(fget=get_name, doc="The name property.")
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
        
        
    