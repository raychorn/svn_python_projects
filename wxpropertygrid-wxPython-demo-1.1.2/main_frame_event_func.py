

import wx

g_debug = True
g_debug_level = 9000


class Event():
    
    def __init__(self, parent = None):
        self.parent = parent
        self._v_log = self
        self._v_msg = self
        
    def on_begin_right_drag(self, event):
        func_name = "on_begin_right_drag"
        if g_debug and g_debug_level > 7999:
            self._v_log.write_log_string(("%s:%s") % (self.__class__, func_name))
        
    def on_paste_click(self, event):
        func_name = "on_paste_click"
        if g_debug and g_debug_level > 7999:
            self._v_log.write_log_string(("%s:%s") % (self.__class__, func_name))
        
    def on_copy_click(self, event):
        func_name = "on_copy_click"
        if g_debug and g_debug_level > 7999:
            self._v_log.write_log_string(("%s:%s") % (self.__class__, func_name))
        
    def on_size(self, event=None):
        func_name = "on_size"
        if g_debug and g_debug_level > 9999:
            self._v_log.write_log_string(("%s:%s") % (self.__class__, func_name))
        
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
    
