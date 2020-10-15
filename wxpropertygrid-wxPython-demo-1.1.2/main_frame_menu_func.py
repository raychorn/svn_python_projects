
import wx



class Menu():
    
    def __init__(self, parent = None):
        self.parent = parent
        self._v_log = self
        self._v_msg = self
        
    def menu_file_new(self, event=None):
        """docstring"""
        pass
        
    def menu_file_open(self, event=None):
        """docstring"""
        pass
        
    def menu_file_save(self, event=None):
        """docstring"""
        pass
        
    def menu_file_close(self, event=None):
        """docstring"""
        pass
        
    def menu_print_print(self, event=None):
        """docstring"""
        pass
        
    def menu_exit(self, event=None):
        """docstring"""
        pass
        self.parent.Close()
        
    def menu_page_add(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_add(event)
        
    def menu_page_insert(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_insert(event)
        
    def menu_page_edit(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_edit(event)
        
    def menu_page_delete(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_delete(event)
        
    def menu_page_clear(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_clear(event)
        
    def menu_page_iterate_cat_forward(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_iterate_categories(event)
        
    def menu_page_iterate_cat_reverse(self, event=None):
        """docstring"""
        pass
        
    def menu_page_iterate_prop_forward(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_iterate_properties(event)
        
    def menu_page_iterate_prop_reverse(self, event=None):
        """docstring"""
        pass
        
    def menu_page_iterate_visible_forward(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_iterate_visible_properties(event)
        
    def menu_page_show_all(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_show_all(event)
        
    def menu_page_collapse_all(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_collapse_all(event)
        
    def menu_page_expand_all(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_expand_all(event)
        
    def menu_page_freeze(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_freeze(event)
        
    def menu_page_hide_margin(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_hide_margin(event)
        
    def menu_page_static_splitter(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_static_splitter(event)
        
    def menu_page_static_layout(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_static_layout(event)
        
    def menu_page_clear_modified_status(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_page_clear_modified_status(event)
        
    def menu_category_add(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_add_category(event)
        
    def menu_category_edit(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_edit_category(event)
        
    def menu_category_delete(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_delete_category(event)
        
    def menu_category_collapse(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_category_collapse(event)
        
    def menu_category_expand(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_category_expand(event)
        
    def menu_property_add(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_add(event)
        
    def menu_property_edit(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_edit(event)
        
    def menu_property_delete(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.property.on_delete(event)
        
    def menu_property_set_default(self, event=None):
        """docstring"""
        pass
        
    def menu_property_select_default(self, event=None):
        """docstring"""
        print "menu_property_select_default"
        
    def menu_edit_cut(self, event=None):
        """docstring"""
        pass
        
    def menu_edit_copy(self, event=None):
        """docstring"""
        pass
        
    def menu_edit_paste(self, event=None):
        """docstring"""
        pass
        
    def menu_edit_options(self, event=None):
        """docstring"""
        pass
        
    def menu_format_font(self, event=None):
        """docstring"""
        pass
        
    def menu_format_colour(self, event=None):
        """docstring"""
        pass
        self.parent.panel_left.inspector.on_scheme(event)
        
        
    def menu_help_about(self, event=None):
        """docstring"""
        pass
        self.parent.help_about()
        
    def menu_help_contents(self, event=None):
        """docstring"""
        pass
        
    def menu_adv_display_values_as_list(self, event=None):
        """docstring"""
        pass
        
    def menu_adv_change_children_of_flags_property(self, event=None):
        """docstring"""
        pass
        
    def menu_adv_insert_property_choice(self, event=None):
        """docstring"""
        pass
        
    def menu_adv_delete_property_choice(self, event=None):
        """docstring"""
        pass
        
    def menu_adv_collapse_selected(self, event=None):
        """docstring"""
        pass
        
        
        
        
        
    def menu_window_close(self, event=None):
        """Closes the current window"""
        event.Skip()
        
        
        
        
    def write_msg_string(self, message):
        self.parent.write(message)
        
    def write_log_string(self, message):
        self.parent.write(message)
            
    def get_log(self):
        # self._v_log.write_log_string(("%s retrieving: log") % (self.__class__))
        return self._v_log
        
    def set_log(self, new_value):
        #print ("%s updating: log with <%s>") % (self.__class__, new_value)
        self._v_log = new_value
        
    def get_msg(self):
        # self._v_log.write_msg_string(("%s retrieving: msg") % (self.__class__))
        return self._v_msg
        
    def set_msg(self, new_value):
        #print ("%s updating: msg with <%s>") % (self.__class__, new_value)
        self._v_msg = new_value
        
    log = property(fget=get_log, fset=set_log, doc="The log property.")
    msg = property(fget=get_msg, fset=set_msg, doc="The msg property.")
    
