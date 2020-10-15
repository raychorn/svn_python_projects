

import wx


class Events():
    if False:
        pass
        #Event Bindings
        #Bind(event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY)
        #event is one of EVT_* objects. It specifies the type of the event.
        #handler is an object to be called. In other words, it is a method, that a programmer binds to an event.
        #source parameter is used when we want to differentiate between the same event type from different widgets.
        #id parameter is used, when we have multiple buttons, menu items etc. The id is used to differentiate among them.
        #id2 is used when it is desirable to bind a handler to a range of ids, such as with EVT_MENU_RANGE.

        # Possible events
        # wx.Event				the event base class
        # wx.ActivateEvent			a window or application activation event
        # wx.CloseEvent			a close window or end session event
        # wx.EraseEvent			an erase background event
        # wx.FocusEvent			a window focus event
        # wx.KeyEvent				a keypress event
        # wx.IdleEvent				an idle event
        # wx.InitDialogEvent		a dialog initialisation event
        # wx.JoystickEvent			a joystick event
        # wx.MenuEvent			a menu event
        # wx.MouseEvent			a mouse event
        # wx.MoveEvent			a move event
        # wx.PaintEvent			a paint event
        # wx.QueryLayoutInfoEvent	used to query layout information
        # wx.SetCursorEvent		used for special cursor processing based on current mouse position
        # wx.SizeEvent				a size event
        # wx.scroll_winEvent		a scroll event sent by a built-in Scrollbar
        # wx.ScrollEvent			a scroll event sent by a stand-alone scrollbar
        # wx.SysColourChangedEvent	a system colour change event 
                
                
    def __init__(self, parent = None):
        self.parent = parent
        
        self.parent.Bind(wx.EVT_SIZE, self.parent._v_event.on_size)
        self.parent.Bind(wx.EVT_CLOSE, self.parent._v_menu.menu_window_close)
        self.parent.Bind(wx.EVT_WINDOW_DESTROY, self.parent._v_menu.menu_window_close)
                

