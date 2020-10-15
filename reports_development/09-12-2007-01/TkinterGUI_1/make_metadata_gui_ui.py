""" make_metadata_gui_ui.py --

 UI generated by GUI Builder Build 146 on 2007-09-06 11:40:16 from:
    Z:/python projects/reports_development/make_metadata_gui.ui
THIS IS AN AUTOGENERATED FILE AND SHOULD NOT BE EDITED.
The associated callback file should be modified instead.
"""

import Tkinter
import os # needed for relative image paths

# Using new-style classes: create empty base class object
# for compatibility with older python interps
#if sys.version_info < (2, 2):
#    class object:
#        pass

class Make_metadata_gui(object):
    _images = [] # Holds image refs to prevent GC
    def __init__(self, root):
        self._progressScale = Tkinter.StringVar(root)


        # Widget Initialization
        self._label_1_title = Tkinter.Label(root,
            borderwidth = 0,
            font = "Garamond 14",
            text = "SQLAlchemy 0.4.0beta4 Utility v0.1",
        )
        self._scale_1 = Tkinter.Scale(root,
            font = "Garamond 8",
            length = 200,
            orient = "horizontal",
            sliderlength = 200,
            variable = self._progressScale,
        )
        self.menu = Tkinter.Menu(root,
            font = "Garamond 11",
        )

        # widget commands

        self._scale_1.configure(
            command = self._scale_1_command
        )
        self.menuitem1 = Tkinter.Menu(self.menu,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menu.add_cascade(
            label = "File...",
            menu = self.menuitem1,
        )
        self.menuitem3 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem1.add_cascade(
            label = "Conversion(s)...",
            menu = self.menuitem3,
        )
        self.menuitem4 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem3.add_cascade(
            label = "mySQL to MSSQL",
            menu = self.menuitem4,
        )
        self.menuitem5 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem3.add_cascade(
            label = "MSSQL to mySQL",
            menu = self.menuitem5,
        )
        self.menuitem6 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem1.add_cascade(
            label = "Metadata...",
            menu = self.menuitem6,
        )
        self.menuitem7 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem6.add_cascade(
            label = "From mySQL",
            menu = self.menuitem7,
        )
        self.menuitem8 = Tkinter.Menu(root,
            font = "Garamond 11",
            tearoff = 0,
        )
        self.menuitem6.add_cascade(
            label = "From MSSQL",
            menu = self.menuitem8,
        )


        # Geometry Management
        self._label_1_title.grid(
            in_    = root,
            column = 2,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = ""
        )
        self._scale_1.grid(
            in_    = root,
            column = 2,
            row    = 2,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "ns"
        )


        # Resize Behavior
        root.grid_rowconfigure(1, weight = 0, minsize = 40, pad = 0)
        root.grid_rowconfigure(2, weight = 1, minsize = 201, pad = 0)
        root.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        root.grid_columnconfigure(2, weight = 0, minsize = 545, pad = 0)
        root.configure(menu = self.menu)


