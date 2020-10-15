import os, sys

from vyperlogix import misc

import wx
import  wx.wizard as wiz

import math

import common

import VyperLogixCorpIcon

__adt_bat__ = 'adt.bat'

adt_file_spec = "Adobe AIR adt (%s)|%s" % (__adt_bat__,__adt_bat__)

cert_file_spec = "Cert file (*.crt)|*.crt|"  \
           "Cert file (*.pfx)|*.pfx|"        \
           "Cert file (*.p12)|*.p12|"        \
           "All files (*.*)|*.*"

def makePageTitle(wizPg, title, font=None):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD) if (font == None) else font)
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

class TitledPage(wiz.WizardPageSimple):
    def __init__(self, parent, title, font=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, title, font)

class AndroidAIRPackager(wx.Frame):

    def __init__(self, parent, id):
        size = wx.GetDisplaySize()
        size_w = size.GetWidth()
        size_h = size.GetHeight()
        wx.Frame.__init__(self, parent, id, 'Android AIR Packager v%s' % (common.__version__), size=(min(700,size_w), min(500,size_h)))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.createMenuBar()
        self.createButtonBar(panel)
        bmp = VyperLogixCorpIcon.getVyperLogixCorpIconBitmap()
        siz = panel.GetSize()
        wx.StaticBitmap(panel, -1, bmp, (siz.GetWidth()-bmp.GetWidth()-5, 10), (bmp.GetWidth(), bmp.GetHeight()))
        #self.createTextFields(panel)
        
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wiz.EVT_WIZARD_CANCEL, self.OnWizCancel)
        self.Bind(wiz.EVT_WIZARD_FINISHED, self.OnWizFinished)
        
    def menuData(self):
        return (("&Package",
                    ("&New", "New Package (.APK)", self.OnNew),
                    ("&Quit", "Quit", self.OnCloseWindow)),
                )

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    def buttonData(self):
        return (("Make .APK", self.OnNew),
                ("Quit", self.OnCloseWindow),
                )

    def createButtonBar(self, panel, yPos = 0):
        xPos = 0
        for eachLabel, eachHandler in self.buttonData():
            pos = (xPos, yPos)
            button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
            xPos += button.GetSize().width

    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button

    #def textFieldData(self):
        #return (("First Name", (10, 50)),
                #("Last Name", (10, 80)))

    #def createTextFields(self, panel):
        #for eachLabel, eachPos in self.textFieldData():
            #self.createCaptionedText(panel, eachLabel, eachPos)

    #def createCaptionedText(self, panel, label, pos):
        #static = wx.StaticText(panel, wx.NewId(), label, pos)
        #static.SetBackgroundColour("White")
        #textPos = (pos[0] + 75, pos[1])
        #wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=textPos)

    def is_enabled_for_page_1(self):
        return os.path.exists(self.adt_fpath) if (self.adt_fpath) else False
    
    def is_enabled_for_page_2(self):
        return os.path.exists(self.cert_fpath) if (self.cert_fpath) else False
    
    def OnWizPageChanged(self, evt):
        if evt.GetDirection():
            dir = "forward"
            self.wizard_page += 1
        else:
            dir = "backward"
            self.wizard_page -= 1
            
        btn_forward = wx.FindWindowById(wx.ID_FORWARD)
        is_enabled = False
        if (self.wizard_page == 1):
            is_enabled = self.is_enabled_for_page_1()
            print >>sys.stderr, '(OnWizPageChanged) :: ID_FORWARD is_enabled=%s for page #%s' % (is_enabled,self.wizard_page)
        elif (self.wizard_page == 2):
            is_enabled = self.is_enabled_for_page_2()
            print >>sys.stderr, '(OnWizPageChanged) :: ID_FORWARD is_enabled=%s for page #%s' % (is_enabled,self.wizard_page)
        btn_forward.Enable(is_enabled)

        page = evt.GetPage()
        print "OnWizPageChanged: %s, %s (%s)" % (dir, page.__class__,self.wizard_page)
        
    def OnWizCancel(self, evt):
        page = evt.GetPage()
        print "OnWizCancel: %s\n" % page.__class__

        #if page is self.page1:
            #wx.MessageBox("Cancelling on the first page has been prevented.", "Sorry")
            #evt.Veto()
        wx.MessageBox("Cannot create your .APK unless you complete the wizard.", "Doh !")

    def OnWizFinished(self, evt):
        print "OnWizFinished\n"
        
    def OnNew(self, event):
        self.adt_fpath = None
        self.cert_fpath = None
        font0 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Verdana')
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Verdana')
        font2 = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Verdana')
        self.wizard = wiz.Wizard(self, -1, "Simple Wizard", VyperLogixCorpIcon.getVyperLogixCorpIconBitmap())
        self.wizard_pages = []
        page1 = TitledPage(self.wizard, "Locate your %s file..." % (__adt_bat__),font=font2)
        self.wizard_pages.append(page1)
        page2 = TitledPage(self.wizard, "Locate or Create your Signing Cert...",font=font2)
        self.wizard_pages.append(page2)
        page3 = TitledPage(self.wizard, "Locate your .XML file from your bin-debug folder...",font=font2)
        self.wizard_pages.append(page3)
        page4 = TitledPage(self.wizard, "Making your .APK file...",font=font2)
        self.wizard_pages.append(page4)
        
        btn_forward = wx.FindWindowById(wx.ID_FORWARD)
        btn_forward.Enable(False)

        btn_back = wx.FindWindowById(wx.ID_BACKWARD)
        btn_back.Enable(False)
        
        self.page1 = page1

        s_text = wx.StaticText(page1, -1, 'First, you must locate your %s file by clicking the Search button.' % (__adt_bat__))
        s_text.SetFont(font1)
        page1.sizer.Add(s_text)

        s_text = wx.StaticText(page1, -1, '')
        s_text.SetFont(font1)
        page1.sizer.Add(s_text)

        btn_search = wx.Button(page1, -1, "Search...")
        btn_search.SetFont(font1)
        page1.Bind(wx.EVT_BUTTON, self.OnSearchButton, btn_search)
        page1.sizer.Add(btn_search)

        s_text = wx.StaticText(page1, -1, '')
        s_text.SetFont(font1)
        page1.sizer.Add(s_text)

        self.page1_variable_text = wx.StaticText(page1, -1, 'Your %s file was found here: ??? (Click the search button...)' % (__adt_bat__))
        self.page1_variable_text.SetFont(font0)
        page1.sizer.Add(self.page1_variable_text)

        
        self.wizard.FitToPage(page1)
        page1.SetBackgroundColour("White")

        s_text = wx.StaticText(page2, -1, """
Next, you must locate or create your code Signing Cert.
""")
        s_text.SetFont(font1)
        page2.sizer.Add(s_text)

        s_text = wx.StaticText(page2, -1, '')
        s_text.SetFont(font1)
        page2.sizer.Add(s_text)

        btn_locate = wx.Button(page2, -1, "Locate...")
        btn_locate.SetFont(font1)
        page2.Bind(wx.EVT_BUTTON, self.OnLocateButton, btn_locate)
        page2.sizer.Add(btn_locate)

        s_text = wx.StaticText(page2, -1, '')
        s_text.SetFont(font1)
        page2.sizer.Add(s_text)

        s_text = wx.StaticText(page2, -1, 'OR')
        s_text.SetFont(font1)
        page2.sizer.Add(s_text)

        s_text = wx.StaticText(page2, -1, '')
        s_text.SetFont(font1)
        page2.sizer.Add(s_text)

        btn_create = wx.Button(page2, -1, "Create...")
        btn_create.SetFont(font1)
        page2.Bind(wx.EVT_BUTTON, self.OnCreateButton, btn_create)
        page2.sizer.Add(btn_create)

        s_text = wx.StaticText(page2, -1, '')
        s_text.SetFont(font0)
        page2.sizer.Add(s_text)

        self.page2_variable_text = wx.StaticText(page2, -1, 'Your cert file was found here: ??? (Click the locate or create button...)')
        self.page2_variable_text.SetFont(font0)
        page2.sizer.Add(self.page2_variable_text)


        self.wizard.FitToPage(page2)
        
        page4.sizer.Add(wx.StaticText(page4, -1, "\nThis is the last page."))

        # Use the convenience Chain function to connect the pages
        wiz.WizardPageSimple_Chain(page1, page2)
        wiz.WizardPageSimple_Chain(page2, page3)
        wiz.WizardPageSimple_Chain(page3, page4)

        self.wizard.GetPageAreaSizer().Add(page1)
        self.wizard_page = 0
        self.wizard.SetBackgroundColour("White")
        btn_forward = wx.FindWindowById(wx.ID_FORWARD)
        is_enabled = self.is_enabled_for_page_1()
        print >>sys.stderr, '(OnNew) :: is_enabled=%s' % (is_enabled)
        btn_forward.Enable(is_enabled)
        self.wizard.RunWizard(page1)
    
    def OnCloseWindow(self, event):
        self.Destroy()

    def OnSearchButton(self, evt):
        evt.EventObject.Enable(False)
        dlg = wx.FileDialog(
            self, message="Locate your %s file..." % (__adt_bat__),
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=adt_file_spec,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.adt_fpath = paths[0] if (misc.isList(paths) and len(paths) > 0) else paths
            btn_forward = wx.FindWindowById(wx.ID_FORWARD)
            is_enabled = self.is_enabled_for_page_1()
            print >>sys.stderr, '(OnSearchButton) :: is_enabled=%s' % (is_enabled)
            btn_forward.Enable(is_enabled)
            s = self.page1_variable_text.GetLabel().split('???')[0]
            self.page1_variable_text.SetLabel('%s %s' % (s,self.adt_fpath))
        evt.EventObject.Enable(True)
        dlg.Destroy()

    def OnLocateButton(self, evt):
        dlg = wx.FileDialog(
            self, message="Locate your code signing cert...",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=cert_file_spec,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.cert_fpath = paths[0] if (misc.isList(paths) and len(paths) > 0) else paths
            btn_forward = wx.FindWindowById(wx.ID_FORWARD)
            is_enabled = self.is_enabled_for_page_2()
            print >>sys.stderr, '(OnLocateButton) :: is_enabled=%s' % (is_enabled)
            btn_forward.Enable(is_enabled)
            s = self.page2_variable_text.GetLabel().split('???')[0]
            self.page2_variable_text.SetLabel('%s %s' % (s,self.cert_fpath))
        dlg.Destroy()

    def OnCreateButton(self, evt):
        dlg = wx.DirDialog(self, "Choose your new certs folder:",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print 'You selected: %s\n' % (paths)
            self.cert_fpath = paths[0] if (misc.isList(paths) and len(paths) > 0) else paths
            s = self.page2_variable_text.GetLabel().split('???')[0]
            self.page2_variable_text.SetLabel('%s %s' % (s,self.cert_fpath))
        dlg.Destroy()
        
if (__name__ == '__main__'):
    app = wx.PySimpleApp()
    frame = AndroidAIRPackager(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

