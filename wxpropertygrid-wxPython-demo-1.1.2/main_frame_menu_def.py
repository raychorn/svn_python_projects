
import wx


class Menus():
    
    def __init__(self, parent = None):
        self.parent = parent
        
        self.create_menu_bar()
        
        
    def menu_data(self):
        regular = wx.ITEM_NORMAL
        radio = wx.ITEM_RADIO
        check = wx.ITEM_CHECK
        line = wx.ITEM_SEPARATOR
        enabled = True
        disabled = False
        id_any = 0
        id_line = -1
        id_about = wx.ID_ABOUT
        id_exit = wx.ID_EXIT
        id_copy = wx.ID_COPY
        id_cut = wx.ID_CUT
        id_paste = wx.ID_PASTE
        id_new = wx.ID_NEW
        id_open = wx.ID_OPEN
        id_save = wx.ID_SAVE
        id_save_as = wx.ID_SAVEAS
        id_close = wx.ID_CLOSE
        id_print = wx.ID_PRINT
        id_options = wx.ID_PREFERENCES
        
        tuple_menu = (
                ("&File", 
                    ("&New", "New File.", self.parent._v_menu.menu_file_new, regular, disabled, id_new),
                    ("&Open", "Open File.", self.parent._v_menu.menu_file_open, regular, disabled, id_open),
                    ("&Save", "Save File.", self.parent._v_menu.menu_file_save, regular, disabled, id_save),
                    ("&Close", "Close File.", self.parent._v_menu.menu_file_close, regular, disabled, id_close),
                    ("&Print", "Print.", self.parent._v_menu.menu_print_print, regular, disabled, id_print),
                    ("", "", "", line, enabled, id_line),
                    ("E&xit", "Exit.", self.parent._v_menu.menu_exit, regular, enabled, id_exit)
                    ),
                ("&Page", 
                    ("&Add", "Add a page.", self.parent._v_menu.menu_page_add, regular, enabled, id_any),
                    ("&Insert*", "Insert a page.", self.parent._v_menu.menu_page_insert, regular, enabled, id_any),
                    ("&Edit", "Edit the current page.", self.parent._v_menu.menu_page_edit, regular, enabled, id_any),
                    ("&Delete", "Delete the current page.", self.parent._v_menu.menu_page_delete, regular, enabled, id_any),
                    ("&Clear", "Deletes all properties on the current page.", self.parent._v_menu.menu_page_clear, regular, enabled, id_any),
                    ("", "", "", line, enabled, id_line),
                    ("Iterate over Categories", "List the categories on this page in the log window.", self.parent._v_menu.menu_page_iterate_cat_forward, regular, enabled, id_any),
                    ("Reverse Iterate over Categories", "List the categories on this page in the log window.", self.parent._v_menu.menu_page_iterate_cat_reverse, regular, disabled, id_any),
                    ("Iterate over Properties", "List the properties on this page in the log window.", self.parent._v_menu.menu_page_iterate_prop_forward, regular, enabled, id_any),
                    ("Reverse Iterate over Properties", "List the properties on this page in the log window.", self.parent._v_menu.menu_page_iterate_prop_reverse, regular, disabled, id_any),
                    ("Iterate over Visible Items*", "List the properties that are visible on this page in the log window.", self.parent._v_menu.menu_page_iterate_visible_forward, regular, enabled, id_any),
                    ("", "", "", line, enabled, id_line),
                    ("&Show All", "Displays all properties.  (Expand)  If not checked, the low-priority properties are hidden.", self.parent._v_menu.menu_page_show_all, check, enabled, id_any, True),
                    ("&Collapse All", "Collapse all categories on this page.", self.parent._v_menu.menu_page_collapse_all, regular, enabled, id_any),
                    ("E&xpand All", "Expands all categories on this page.", self.parent._v_menu.menu_page_expand_all, regular, enabled, id_any),
                    ("&Freeze", "Disables painting, auto-sorting, screen updates, etc.", self.parent._v_menu.menu_page_freeze, check, enabled, id_any),
                    ("&Hide Margin", "Disables left margin area.", self.parent._v_menu.menu_page_hide_margin, check, enabled, id_any),
                    ("&Static Splitter", "Locks the splitter in place.", self.parent._v_menu.menu_page_static_splitter, check, enabled, id_any),
                    ("&Static Layout", "Prevents user from adjusting layout.  Same as 'Hide Margin' combined with 'Static Splitter'.", self.parent._v_menu.menu_page_static_layout, check, enabled, id_any),
                    ("&Clear Modified Status", "Clear the modified flag of all properties.", self.parent._v_menu.menu_page_clear_modified_status, regular, enabled, id_any)
                    ),
                ("&Category", 
                    ("&Add", "Add a category.", self.parent._v_menu.menu_category_add, regular, enabled, id_any),
                    ("&Edit", "Edit the currently highlighted category.", self.parent._v_menu.menu_category_edit, regular, enabled, id_any),
                    ("&Delete", "Delete the currently highlighted category and all the properties it contains.", self.parent._v_menu.menu_category_delete, regular, enabled, id_any),
                    ("", "", "", line, enabled, id_line),
                    ("&Collapse", "Collapse category.", self.parent._v_menu.menu_category_collapse, regular, enabled, id_any),
                    ("E&xpand", "Expand category.", self.parent._v_menu.menu_category_expand, regular, enabled, id_any),
                    ),
                ("&Property", 
                    ("&Add", "Add a property.", self.parent._v_menu.menu_property_add, regular, enabled, id_any),
                    ("&Insert", "Insert a property.", self.parent._v_menu.menu_property_add, regular, disabled, id_any),
                    ("&Edit", "Edit the currently highlighted property.", self.parent._v_menu.menu_property_edit, regular, enabled, id_any),
                    ("&Delete", "Delete the currently highlighted property.", self.parent._v_menu.menu_property_delete, regular, enabled, id_any),
                    ("", "", "", line, enabled, id_line),
                    ("&Set as Default", "Set default to the currently highlighted property.", self.parent._v_menu.menu_property_set_default, regular, disabled, id_any),
                    ("Select De&fault", "Select default property.", self.parent._v_menu.menu_property_select_default, regular, disabled, id_any)
                    ),
                ("&Edit",
                    ("&Copy", "Copy.", self.parent._v_menu.menu_edit_copy, regular, disabled, id_copy),
                    ("C&ut", "Cut.", self.parent._v_menu.menu_edit_cut, regular, disabled, id_cut),
                    ("&Paste", "Paste.", self.parent._v_menu.menu_edit_paste, regular, disabled, id_paste),
                    ("", "", "", line, enabled, id_line),
                    ("&Options...", "Options.", self.parent._v_menu.menu_edit_options, regular, disabled, id_any)
                    ),
                ("&Format",
                    ("&Font", "Font.", self.parent._v_menu.menu_format_font, regular, disabled, id_any),
                    ("&Colour Scheme",
                        (
                        ("&Standard", "Standard background.", self.parent._v_menu.menu_format_colour, radio, enabled, id_any),
                        ("&White", "White.", self.parent._v_menu.menu_format_colour, radio, enabled, id_any),
                        ("&.Net", "Microsoft .Net colours.", self.parent._v_menu.menu_format_colour, radio, enabled, id_any),
                        ("&Cream", "Cream background.", self.parent._v_menu.menu_format_colour, radio, enabled, id_any),
                        ("&Category Specific", "Shades each category in a different colour.", self.parent._v_menu.menu_format_colour, radio, enabled, id_any),
                        ), ),
                    ),
                ("&Advanced",
                    ("Display Values as List", "Tests GetAllValues method.", self.parent._v_menu.menu_adv_display_values_as_list, regular, disabled, id_any),
                    ("&Change Children of Flags Property", "to do.", self.parent._v_menu.menu_adv_change_children_of_flags_property, regular, disabled, id_any),
                    ("", "", "", line, enabled, id_line),
                    ("&Test Insert Property Choice", "A challenge to do.", self.parent._v_menu.menu_adv_insert_property_choice, regular, disabled, id_any),
                    ("&Test Delete Property Choice", "A challenge to do.", self.parent._v_menu.menu_adv_delete_property_choice, regular, disabled, id_any),
                    ("&Collapse Selected", "Collapse the selected categories.", self.parent._v_menu.menu_adv_collapse_selected, regular, disabled, id_any)
                    ),
                ("&Help",
                    ("&About...", "Display about dialog.", self.parent._v_menu.menu_help_about, regular, enabled, id_about),
                    ("&Contents...", "Display table of contents for help.", self.parent._v_menu.menu_help_contents, regular, disabled, id_any)
                    )
                )
        return tuple_menu
        
        
    def create_menu_bar(self):
        menu_bar = wx.MenuBar()
        for menu_datum in self.menu_data():
            menu_label = menu_datum[0]
            menu_items = menu_datum[1:]
            menu_bar.Append(self.create_menu(menu_data=menu_items), menu_label)
        self.parent.SetMenuBar(menu_bar)
        
        
    def create_menu(self, menu_data=None):
        menu = wx.Menu()
        for item in menu_data:
            if len(item) == 2:
                label = item[0]
                sub_menu = self.create_menu( item[1] )
                menu.AppendMenu(wx.NewId(), label, sub_menu)
            else:
                self.create_menu_item( menu, *item )
        return menu		
            
            
    def create_menu_item(self, menu, label, help_tip, handler, kind=wx.ITEM_NORMAL, enabled=True, id=wx.ID_ANY, checked=False):
        if (not label) or (kind==wx.ITEM_SEPARATOR):
            menu.AppendSeparator()
        else:
            if id == 0:
                id = wx.ID_ANY
            menu_item = menu.Append(id, label, help_tip, kind)
            menu_item.Enable(enable=enabled)
            if kind == wx.ITEM_CHECK:
                menu_item.Check(check=checked)
            self.parent.Bind(wx.EVT_MENU, handler, menu_item)
        
        