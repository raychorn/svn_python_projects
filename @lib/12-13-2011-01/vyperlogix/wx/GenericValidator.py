"""
Note that every validator must implement the Clone() method.
"""
import re
import types
import wx

ERR_COLOR = "yellow"
# Regular expressions for validating common data requirements.
# Pass one into Generic(regex).
NUMBER = r'\d+$'
FLOAT = r'\d+(\.\d{1,2})?$'
FLOAT_OPT = r'$|\d+(\.\d{1,2})?$'
NOT_EMPTY = r'.+'
EMAIL = r'([\w-]+\.)*[\w-]+@([\w-]+\.)+\w+\s*$'
STATE = '[a-zA-Z]{2,2}'

# Error messages associated with the above regular expressions.
errmsg = {\
     NUMBER:"This field must be a number!",
     FLOAT:"This field must be a decimal number!",
     FLOAT_OPT:"This field must be empty or a decimal number!",
     NOT_EMPTY:"This field must contain some text!",
     EMAIL:"This field must contain an email address in the form\nuser.name at your.domain.com",
     STATE:"State must consist of two letters",
}

class Generic(wx.PyValidator):
     """A generic validator that takes:
         1. optional regular expression for data validation (common re's are available)
         2. optional dictionary + key for getting and setting data
     """
     def __init__(self, regex=None, data={}, key=None):
         wx.PyValidator.__init__(self)
         self.regex = regex
         self.data = data
         self.key = key
         if self.regex:
             self.re = re.compile(regex)

     def Clone (self):
         return Generic(self.regex, self.data, self.key)

     def Validate(self, window):
         if not self.regex:
             return True
         window = self.GetWindow()
         text = window.GetValue().strip()
         if self.re.match(text):
             window.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
             window.Refresh()
             return True
         else:
             window.SetBackgroundColour(ERR_COLOR)
             window.SetFocus()
             window.Refresh()
             msg = errmsg.get(self.regex, "This field is the wrong format!")
             wx.MessageBox(msg, "Error")
             return False

     def TransferToWindow(self):
         if self.key:
             data = self.data.get(self.key, "")
             wnd = self.GetWindow()
             # make a note of the native type
             self.type = type(data)
             if type(wnd) == wx._controls.CheckBox:
                 if self.type != types.BooleanType:
                     # native type is not boolean, so convert it
                     data = bool(data)
                 wnd.SetValue(data)
             elif type(wnd) == wx._controls.ListBox:
                 for idx in range(wnd.GetCount()):
                     lbData = wnd.GetClientData(idx) or wnd.GetString(idx)
                     if lbData == data:
                         wnd.SetSelection(idx)
                         break
             else:
                 if self.type != types.StringType:
                     # native type is not string, so convert it
                     data = str(data)
                     # show floats with no fraction as integers
                     if self.type == types.FloatType and data[-2:] == '.0':
                         data = data[0:-2]
                 wnd.SetValue(data)
         return True

     def TransferFromWindow(self):
         if self.key:
             wnd = self.GetWindow()
             if type(wnd) == wx._controls.ListBox:
                 idx = wnd.GetSelection()
                 if idx < 0:
                     return False
                 data = wnd.GetClientData(idx)
                 if not data:
                     data = wnd.GetString(idx)
             else:
                 data = wnd.GetValue()
             if self.type == types.StringType:
                 pass
             # native type is not string, so convert it back
             elif self.type == types.IntType:
                 data = int(data)
             elif self.type == types.FloatType:
                 if data:
                     data = float(data)
                 else: # FLOAT_OPT can bring us here
                     data = 0.0
             elif self.type == types.BooleanType:
                 data = bool(data)
             else:
                 raise TypeError, "%s data is stored as unknown type %s"%(self.key,str(self.type))
             self.data[self.key] = data
         return True
