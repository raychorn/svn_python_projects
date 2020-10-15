
import wx
import datetime
import wx.lib.masked


class MyTimeEditor(wx.propgrid.PyEditor):
    class_name = "MyTimeEditor"
    def __init__(self, name="clock"):
        func_name = "__init__"
        print "MyTimeEditor.__init__"
        wx.propgrid.PyEditor.__init__(self)
        mf = wx.GetApp().GetTopWindow()	# I like it!
        _v_log = mf
        msg = ( "Initializing: %s: %s ") % ( "a", "b")
        _v_log.write(("%s:%s") % (func_name, msg))
        
    def CreateControls(self, propgrid, property, pos, sz):
        print "MyTimeEditor.CreateControls"
        func_name = "CreateControls"
        mf = wx.GetApp().GetTopWindow()	# I like it!
        _v_log = mf
        # msg = ( "Creating: %s: %s ") % ( property.GetName(), "b")
        # _v_log.write(("%s:%s") % (func_name, msg))
        # _v_log.write(("%s:%s:%s") % (__class__.class_name, func_name, msg))
        
        try:
            print "MyTimeEditor.CreateControls.try"
            x = propgrid.GetSplitterPosition()
            x2 = propgrid.GetClientSize().x
            bw = propgrid.GetRowHeight()
            
            # wx.MessageBox( caption="Grid", message=str(dir(propgrid)) )
            # wx.MessageBox( caption="Property", message=str(dir(property)) )
            # wx.MessageBox( caption="Position", message=str(dir(pos)) )
            # wx.MessageBox( caption="Size", message=str(dir(sz)) )
            cntrl_x = pos[0]
            cntrl_y = pos[1]
            
            if False:
                pass
                # TimeCtrl(
                     # parent, id = -1,
                     # value = '00:00:00',
                     # pos = wx.DefaultPosition,
                     # size = wx.DefaultSize,
                     # style = wxTE_PROCESS_TAB,
                     # validator = wx.DefaultValidator,
                     # name = "time",
                     # format = 'HHMMSS',
                     # fmt24hr = False,
                     # displaySeconds = True,
                     # spinButton = None,
                     # min = None,
                     # max = None,
                     # limited = None,
                     # oob_colour = "Yellow"
                    # )
                    # value
                        # If no initial value is set, the default will be midnight; 
                        # if an illegal string is specified, a ValueError will result. 
                        # (You can always later set the initial time with SetValue() after instantiation of the control.)
                    # size
                        # The size of the control will be automatically adjusted for 12/24 hour format if wx.DefaultSize is specified. 
                        # NOTE: due to a problem with wx.DateTime, if the locale does not use 'AM/PM' for its values, 
                        # the default format will automatically change to 24 hour format, and an AttributeError will be thrown 
                        # if a non-24 format is specified.
                    # style
                        # By default, TimeCtrl will process TAB events, by allowing tab to the different cells within the control.
                    # validator
                        # By default, TimeCtrl just uses the default (empty) validator, as all of its validation for entry control 
                        # is handled internally. However, a validator can be supplied to provide data transfer capability to the control.
                    # format
                        # This parameter can be used instead of the fmt24hr and displaySeconds parameters, respectively; 
                        # it provides a shorthand way to specify the time format you want. 
                        #Accepted values are 'HHMMSS', 'HHMM', '24HHMMSS', and '24HHMM'.  
                        # If the format is specified, the other two arguments will be ignored.
                    # fmt24hr
                        # If True, control will display time in 24 hour time format; if False, it will use 12 hour AM/PM format. 
                        # SetValue() will adjust values accordingly for the control, based on the format specified. 
                        # (This value is ignored if the format parameter is specified.)
                    # displaySeconds
                        # If True, control will include a seconds field; if False, it will just show hours and minutes. 
                        # (This value is ignored if the format parameter is specified.)
                    # spinButton
                        # If specified, this button's events will be bound to the behavior of the TimeCtrl, 
                        # working like up/down cursor key events. (See BindSpinButton.)
                    # min
                        # Defines the lower bound for "valid" selections in the control. By default, TimeCtrl doesn't have bounds. 
                        # You must set both upper and lower bounds to make the control pay attention to them, 
                        # (as only one bound makes no sense with times.) "Valid" times will fall between the min and max "pie wedge" of the clock.
                    # max
                        # Defines the upper bound for "valid" selections in the control. 
                        # "Valid" times will fall between the min and max "pie wedge" of the clock. 
                        # (This can be a "big piece", ie. min = 11pm, max= 10pm means all but the hour from 10:00pm to 11pm are valid times.)
                    # limited
                        # If True, the control will not permit entry of values that fall outside the set bounds.
                    # oob_colour
                        # Sets the background colour used to indicate out-of-bounds values for the control when the control is not limited. 
                        # This is set to "Yellow" by default. 			
                                
            
            t1 = property.GetY()
            
            # msg = ( "Grid: %s Property: %s Position: %s Size Y: %s") % ( str(propgrid.GetName()), str(property.GetName()), str(pos), str(sz) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            # msg = ( "Splitter pos: %s ClientSize: %s RowHeight: %s Property Y: %s") % ( str(x), str(x2), str(bw), str(t1) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            # msg = ( "TimeCtrl Position: %s,%s") % ( str(cntrl_x), str(cntrl_y) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            # Value_Time24 = wx.lib.masked.TimeCtrl(parent=propgrid, id=wx.propgrid.PG_SUBID1, pos=wx.Point(x, t1), size=wx.DefaultSize, name="Clock24", fmt24hr=True)
            Value_Time24 = wx.lib.masked.TimeCtrl(parent=propgrid, id=wx.propgrid.PG_SUBID1, pos=wx.Point(cntrl_x, cntrl_y), size=wx.DefaultSize, name="Clock24", fmt24hr=True)
            # wx.MessageBox( str(dir(Value_Time24)) )
            Value_Time24.Raise
            print Value_Time24.IsShown()
            print Value_Time24.IsShownOnScreen()
            
            h = Value_Time24.GetSize().height
            w = Value_Time24.GetSize().width
            
            # msg = ( "TimeCtrl Height: %s Width: %s") % ( str(h), str(w) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            # msg = ( "SpinCtrl Position: %s,%s") % ( str(cntrl_x + w), str(cntrl_y) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            # Value_Time24_spin1 = wx.SpinButton(parent=propgrid, id=wx.propgrid.PG_SUBID2, pos=wx.Point(x + w, t1), size=wx.Size(-1,h), style=wx.SP_VERTICAL)
            Value_Time24_spin1 = wx.SpinButton(parent=propgrid, id=wx.propgrid.PG_SUBID2, pos=wx.Point(cntrl_x + w, cntrl_y), size=wx.Size(-1,h), style=wx.SP_VERTICAL)
            Value_Time24.BindSpinButton(Value_Time24_spin1)
            Value_Time24_spin1.Raise
            
            Value_Time24.Value =  property.GetValue()
            # msg = ( "TimeCtrl: %s Height: %s Width: %s") % ( str(Value_Time24.GetName()), str(h), str(w) )
            # _v_log.write(("%s:%s") % (func_name, msg))
            
            print "MyTimeEditor.CreateControls.try2"
            
            return (Value_Time24, Value_Time24_spin1)
        except:
            import traceback
            print traceback.print_exc()

    def SetControlIntValue(self, ctrl, value):
        print "MyTimeEditor.SetControlIntValue"
        
    def UpdateControl(self, property, ctrl):
        print "MyTimeEditor.UpdateControl"
        # ctrl.SetValue(property.GetDisplayedString())
        ctrl.SetValue(property.GetValueAsString())

    def DrawValue(self, dc, property, rect):
        print "MyTimeEditor:DrawValue"
        
        if not (property.GetFlags() & wx.propgrid.PG_PROP_UNSPECIFIED):
            dc.DrawText( property.GetDisplayedString(), rect.x+5, rect.y );
        else:
            print "MyTimeEditor:DrawValue: check flags?"
        
        # print "Property name: ", str(property.GetName())
        # print "Property value: ", str(property.GetValue())
        
        
    def OnEvent(self, propgrid, property, ctrl, event):
        if not ctrl:
            # print "no control"
            return False
        
        print "MyTimeEditor.OnEvent"
        # wx.MessageBox( str(dir(ctrl)) )
        # print ctrl.Name
        # print ctrl.GetValue()
        
        # wx.MessageBox( str(dir(event)) )
        evtType = event.GetEventType()
        
        if evtType:
            # print "We have an event type"
            # print str(evtType)
            # evtObject = event.GetEventObject()
            # wx.MessageBox( str(dir(evtObject)) )
            # print evtObject.Name
            
            if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
                print "EVT_COMMAND_TEXT_ENTER"
                if propgrid.IsEditorsValueModified():
                    print "Value Modified"
                    return True
            elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
                print "EVT_COMMAND_TEXT_UPDATED"
                # print str(dir(property))
                # print property.GetName()
                # print property.GetValue()
                # print property.HasFlag(wx.propgrid.PG_PROP_UNSPECIFIED)
                # print ctrl.GetLastPosition()
                # print propgrid.GetId()
                if not property.HasFlag(wx.propgrid.PG_PROP_UNSPECIFIED) or ctrl.GetLastPosition() > 0:
                    # print "update"
                    
                    # We must check this since an 'empty' text event
                    # may be triggered when creating the property.
                    ## PG_FL_IN_SELECT_PROPERTY = 0x00100000
                    ## if not (propgrid.GetInternalFlags() & PG_FL_IN_SELECT_PROPERTY):
                        ## print "weird"
                        ## event.Skip();
                        ## event.SetId(propgrid.GetId());
                    ## else:
                        ## print "nothing2"
                        
                    # Now update the value
                    propgrid.EditorsValueWasModified();
                else:
                    print "no update"
                    
            elif evtType == wx.EVT_BUTTON:
                print "EVT_BUTTON"
                
            elif evtType == wx.EVT_TEXT:
                print "EVT_TEXT"
                
            elif evtType == wx.EVT_SPIN:
                print "EVT_SPIN"
                
            else:
                print "I don't know what event"
        else:
            print "no event type"
        
        return False


    def CopyValueFromControl(self, property, ctrl):
        print "MyTimeEditor.CopyValueFromControl"
        # wx.MessageBox( str(dir(ctrl)) )
        res = property.SetValueFromString(ctrl.GetValue(),0)
        # Changing unspecified always causes event (returning
        # true here should be enough to trigger it).
        if not res and property.IsFlagSet(wx.propgrid.PG_PROP_UNSPECIFIED):
            res = true
        
        return res

    def SetValueToUnspecified(self, ctrl):
        print "MyTimeEditor.SetValueToUnspecified"
        ctrl.Remove(0,len(ctrl.GetValue()));

    def SetControlStringValue(self, ctrl, txt):
        print "MyTimeEditor.SetControlStringValue"
        ctrl.SetValue(txt)

    def SetValue(self, ctrl, txt):
        print "MyTimeEditor.SetValue"
        ctrl.SetValue(txt)

    def OnFocus(self, property, ctrl):
        print "MyTimeEditor.OnFocus"


class MyTimeProperty(wx.propgrid.PyProperty):
    """
    Time string formatted like this: H:M:S
    H is a two-digit hour in the range 0-23.
    M is a two-digit minute in the range 0-59.
    S is a two-digit second in the range 0-59.
    """
    def __init__(self, label, name = wx.propgrid.LABEL_AS_NAME, value=datetime.datetime.now().strftime("%H:%M:%S") ):
        
        print "MyTimeProperty.__init__"
        wx.propgrid.PyProperty.__init__(self, label, name)
        self.DoSetValue(value)

    def GetClassName(self):
        print "MyTimeProperty.GetClassName"
        """\
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "MyTimeProperty"

    def GetType(self):
        print "MyTimeProperty.GetType"
        return "string"

    def GetEditor(self):
        print "MyTimeProperty.GetEditor"
        return "clock"

    def DoSetValue(self, v):
        print "MyTimeProperty.DoSetValue"
        self.value = v  # store it as a string.
        print self.value

    def DoGetValue(self):
        print "MyTimeProperty.DoGetValue"
        return self.value

    def GetPVTN(self):
        print "MyTimeProperty.GetPVTN"
        print "pvtn mytime1"
        return "MyTime1"

    def GetValueAsString(self, flags):
        print "MyTimeProperty.GetValueAsString"
        # return self.value.strftime("%H:%M:%S")
        return self.value

    def SetValueFromString(self, s, flags):
        print "MyTimeProperty.SetValueFromString"
        self.value = s
        return True
        
    def GetDisplayedString(self):
        print "MyTimeProperty.GetDisplayedString"
        return self.value
        
    def SetValue(self, s):
        print "MyTimeProperty.SetValue"
        self.value = s
        return True
        
