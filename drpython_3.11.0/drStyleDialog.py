#   Programmer: Daniel Pozmanter
#   E-mail:     drpython@bluebottle.com
#   Note:       You must reply to the verification e-mail to get through.
#
#   Copyright 2003-2007 Daniel Pozmanter
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#    DrPython is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import string, os.path
import wx
import wx.stc
from drProperty import *
import drScrolledMessageDialog
from drPrefsFile import ExtractPreferenceFromText

class drColorPanel(wx.Panel):

    def __init__(self, parent, id, point, size, fg):
        wx.Panel.__init__(self, parent, id, point, size)

        self.ID_COLOR = 105
        self.ID_RED = 106
        self.ID_GREEN = 107
        self.ID_BLUE = 108

        self.theSizer = wx.BoxSizer(wx.VERTICAL)

        self.txtColor = wx.TextCtrl(self, self.ID_COLOR, "", wx.Point(0, 10), wx.Size(100, -1))

        self.isForeground = fg

        self.red = wx.Slider(self, self.ID_RED, 0, 0, 255, wx.Point(0, 40), wx.Size(100, 35), wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.green = wx.Slider(self, self.ID_GREEN, 0, 0, 255, wx.Point(0, 70), wx.Size(100, 35), wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.blue = wx.Slider(self, self.ID_BLUE, 0, 0, 255, wx.Point(0, 100), wx.Size(100, 35), wx.SL_HORIZONTAL | wx.SL_LABELS)

        self.theSizer.Add(self.txtColor, 0, wx.SHAPED)
        self.theSizer.Add(self.red, 0, wx.SHAPED)
        self.theSizer.Add(self.green, 0, wx.SHAPED)
        self.theSizer.Add(self.blue, 0, wx.SHAPED)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.red.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.green.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.blue.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_TEXT,  self.OnTextChange, id=self.ID_COLOR)

    def GetValue(self):
        return self.txtColor.GetValue()

    def OnLeftUp(self, event):
        self.txtColor.SetEditable(True)
        event.Skip()

    def OnScroll(self, event):
        self.txtColor.SetEditable(False)
        i = event.GetId()
        if i == self.ID_RED:
            r = self.red.GetValue()
            sr = ''
            if r < 16:
                sr = '0'
            sr = sr + hex(r)[2:]
            sr = sr.upper()
            text = self.txtColor.GetValue()
            if len(text) != 7:
                drScrolledMessageDialog.ShowMessage(self, ("The text box above should be formatted as follows:\n#0033AA,\nStart with the # character, followed by 6 characters which can be 0-9 or a-f.\nDrPython will ignore any changes to the color until this is fixed."), "Error")
                return
            self.txtColor.SetValue(text[0:1] + sr + text[3:])
        elif i == self.ID_GREEN:
            g = self.green.GetValue()
            sr = ''
            if g < 16:
                sr = '0'
            sr = sr + hex(g)[2:]
            sr = sr.upper()
            text = self.txtColor.GetValue()
            if len(text) != 7:
                drScrolledMessageDialog.ShowMessage(self, ("The text box above should be formatted as follows:\n#0033AA,\nStart with the # character, followed by 6 characters which can be 0-9 or a-f.\nDrPython will ignore any changes to the color until this is fixed."), "Error")
                return
            self.txtColor.SetValue(text[0:3] + sr + text[5:])
        elif i == self.ID_BLUE:
            b = self.blue.GetValue()
            sr = ''
            if b < 16:
                sr = '0'
            sr = sr + hex(b)[2:]
            sr = sr.upper()
            text = self.txtColor.GetValue()
            if len(text) != 7:
                drScrolledMessageDialog.ShowMessage(self, ("The text box above should be formatted as follows:\n#0033AA,\nStart with the # character, followed by 6 characters which can be 0-9 or a-f.\nDrPython will ignore any changes to the color until this is fixed."), "Error")
                return
            self.txtColor.SetValue(text[0:5] + sr + text[7:])
        event.Skip()

    def OnTextChange(self, event):
        v = self.txtColor.GetValue()
        if self.txtColor.IsEditable():
            if not v:
                self.red.Enable(False)
                self.green.Enable(False)
                self.blue.Enable(False)
                return
            if (v[0] == "#") and (len(v) == 7):
                #Update Sliders
                self.red.Enable(True)
                self.green.Enable(True)
                self.blue.Enable(True)
                try:
                    self.red.SetValue(int(v[1:3], 16))
                    self.green.SetValue(int(v[3:5], 16))
                    self.blue.SetValue(int(v[5:7], 16))
                except:
                    drScrolledMessageDialog.ShowMessage(self, ("Bad Color Data.  Should be in the form #00A3F4\nUse only digits 0-9, characters A-F"), "Error")
            else:
                self.red.Enable(False)
                self.green.Enable(False)
                self.blue.Enable(False)
        if len(v) == 7:
            if v[0] == "#":
                #Update Parent
                if self.isForeground:
                    self.GetParent().foreground = v
                else:
                    self.GetParent().background = v
                self.GetParent().SetColor()
        event.Skip()

    def SetValue(self, colorstring):
        self.txtColor.SetValue(colorstring)
        r = int(colorstring[1:3], 16)
        g = int(colorstring[3:5], 16)
        b = int(colorstring[5:7], 16)
        self.red.SetValue(r)
        self.green.SetValue(g)
        self.blue.SetValue(b)

#*****************************************

class drSeparatorDialog(wx.Dialog):

    def __init__(self, parent, title):

        wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(-1, -1))

        self.parent = parent

        self.ID_CANCEL = 101
        self.ID_OK = 102
        self.ID_SAVE = 103

        self.favorites = {0:('#000000', '#CAFFFF'), 1:('#000000', '#FFFFC6'), 2:('#000000', '#BEFFC6'),
        3:('#000000', '#FFA400'), 4:('#00FF00', '#000000')}

        self.favoritefile = self.parent.datdirectory + '/.separator.favorite.colours.dat'

        self.txtLabel = wx.TextCtrl(self, -1, 'Label', size=wx.Size(300, -1), style=wx.TE_PROCESS_ENTER|wx.TE_RICH2)

        self.txtLabel.SetSelection(0, 5)

        self.btn0 = wx.Button(self, 0, '&0', style=wx.BU_EXACTFIT)
        self.btn1 = wx.Button(self, 1, '&1', style=wx.BU_EXACTFIT)
        self.btn2 = wx.Button(self, 2, '&2', style=wx.BU_EXACTFIT)
        self.btn3 = wx.Button(self, 3, '&3', style=wx.BU_EXACTFIT)
        self.btn4 = wx.Button(self, 4, '&4', style=wx.BU_EXACTFIT)

        self.btnSave = wx.Button(self, self.ID_SAVE, '&Save Favorite')

        self.fgPanel = drColorPanel(self, -1, wx.Point(10, 200), wx.Size(400, 350), True)

        self.bgPanel = drColorPanel(self, -1, wx.Point(220, 200), wx.Size(400, 350), False)

        self.fgPanel.SetValue('#000000')
        self.bgPanel.SetValue('#FFFFFF')

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "&Cancel", wx.Point(5, 0), wx.Size(-1, -1))
        self.btnOk = wx.Button(self, self.ID_OK, "&Ok", wx.Point(400, 0), wx.Size(-1, -1))

        self.LoadFavorites()

        #Sizer:

        self.theSizer = wx.BoxSizer(wx.VERTICAL)
        self.textSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.favoritesSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.favoritesSizer.Add(self.btn0, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.favoritesSizer.Add(self.btn1, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.favoritesSizer.Add(self.btn2, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.favoritesSizer.Add(self.btn3, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.favoritesSizer.Add(self.btn4, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.favoritesSizer.Add(self.btnSave, 0, wx.SHAPED | wx.ALIGN_CENTER)

        self.panelSizer.Add(self.fgPanel, 1, wx.SHAPED)
        self.panelSizer.Add(self.bgPanel, 1, wx.SHAPED | wx.ALIGN_RIGHT)

        self.buttonSizer.Add(self.btnCancel, 1, wx.SHAPED)
        self.buttonSizer.Add(self.btnOk, 1, wx.SHAPED | wx.ALIGN_RIGHT)

        self.textSizer.Add(self.txtLabel, 1, wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(self.textSizer, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, 'Favorite Colours:'), 0, wx.SHAPED)
        self.theSizer.Add(self.favoritesSizer, 0, wx.SHAPED)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.theSizer.Add(self.panelSizer, 1, wx.EXPAND)
        self.theSizer.Add(wx.StaticText(self, -1, '   '), 0, wx.SHAPED)
        self.theSizer.Add(self.buttonSizer, 0, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        #End Sizer

        self.Bind(wx.EVT_BUTTON,  self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnOk, id=self.ID_OK)
        self.Bind(wx.EVT_BUTTON,  self.OnFavorite, id=0)
        self.Bind(wx.EVT_BUTTON,  self.OnFavorite, id=1)
        self.Bind(wx.EVT_BUTTON,  self.OnFavorite, id=2)
        self.Bind(wx.EVT_BUTTON,  self.OnFavorite, id=3)
        self.Bind(wx.EVT_BUTTON,  self.OnFavorite, id=4)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnSave, id=self.ID_SAVE)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.txtLabel.Bind(wx.EVT_CHAR, self.OnChar)

    def GetLabel(self):
        return '#---' + self.txtLabel.GetValue() + '---' + self.fgPanel.GetValue() + self.bgPanel.GetValue() + '---------------------------------'

    def LoadFavorites(self):
        if os.path.exists(self.favoritefile):
            try:
                f = file(self.favoritefile, 'rb')
                text = f.read()
                f.close()

                for fL in range(5):
                    result = ExtractPreferenceFromText(text, str(fL))
                    if result:
                        results = result.split(',')
                        if len(results) == 2:
                            self.favorites[fL] = results
            except:
                self.parent.ShowMessage('Error Loading Favorite Colours', 'Error')

    def OnbtnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnbtnOk(self, event):
        self.EndModal(wx.ID_OK)

    def OnbtnSave(self, event):
        d = wx.SingleChoiceDialog(self, "Store Current Colour in Which Slot?", "Save Favorite", ['0', '1', '2', '3', '4'], wx.OK|wx.CANCEL)
        answer = d.ShowModal()
        i = d.GetSelection()
        d.Destroy()
        if answer == wx.ID_OK:
            try:
                self.favorites[i] = (self.fgPanel.GetValue(), self.bgPanel.GetValue())
                f = file(self.favoritefile, 'wb')
                x = 0
                l = len(self.favorites)
                while x < l:
                    f.write('<' + str(x) + '>' + self.favorites[x][0] + ',' + self.favorites[x][1] + '</' + str(x) + '>')
                    x += 1
                f.close()
            except:
                self.parent.ShowMessage('Error Saving Favorite Colours', 'Error')


    def OnChar(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.OnbtnCancel(event)
        elif event.GetKeyCode() == wx.WXK_RETURN:
            self.OnbtnOk(event)
        else:
            event.Skip()

    def OnFavorite(self, event):
        i = event.GetId()

        self.fgPanel.SetValue(self.favorites[i][0])
        self.bgPanel.SetValue(self.favorites[i][1])

    def SetColor(self):
        self.txtLabel.SetForegroundColour(wx.Colour(self.fgPanel.red.GetValue(), self.fgPanel.green.GetValue(), self.fgPanel.blue.GetValue()))
        self.txtLabel.SetBackgroundColour(wx.Colour(self.bgPanel.red.GetValue(), self.bgPanel.green.GetValue(), self.bgPanel.blue.GetValue()))

#*****************************************

class drSimpleStyleDialog(wx.Dialog):

    def __init__(self, parent, id, title, stylestring, defaultstylestring, ChangeSpec = 0):

        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(-1, -1))

        self.ID_CANCEL = 101
        self.ID_OK = 102

        self.ID_FONTS = 103
        self.ID_SIZE = 104

        self.ID_BOLD = 109
        self.ID_ITALIC = 110
        self.ID_UNDERLINE = 111

        self.Enum = wx.FontEnumerator()
        self.Enum.EnumerateFacenames()
        self.FontList = self.Enum.GetFacenames()
        self.FontList.sort()

        self.OK = False

        self.font = getStyleProperty("face", stylestring)
        if not self.font:
            self.font = getStyleProperty("face", defaultstylestring)
        self.size = getStyleProperty("size", stylestring)
        if not self.size:
            self.size = getStyleProperty("size", defaultstylestring)
        self.foreground = getStyleProperty("fore", stylestring)
        if not self.foreground:
            self.foreground = getStyleProperty("fore", defaultstylestring)
        self.background = getStyleProperty("back", stylestring)
        if not self.background:
            self.background = getStyleProperty("back", defaultstylestring)
        self.bold = getStyleProperty("bold", stylestring)
        self.italic = getStyleProperty("italic", stylestring)
        self.underline = getStyleProperty("underline", stylestring)
        self.txtPreview = wx.stc.StyledTextCtrl(self, id, wx.Point(225, 15), wx.Size(225, 150))

        if ChangeSpec > 0:
            self.font = getStyleProperty("face", defaultstylestring)
            self.size = getStyleProperty("size", defaultstylestring)
            if ChangeSpec == 1:
                self.background = getStyleProperty("back", defaultstylestring)
            elif ChangeSpec == 3:
                self.foreground = getStyleProperty("fore", defaultstylestring)

        if self.font not in self.FontList:
            old=self.font
            self.size = '12'
            options=['Courier','Courier 10 Pitch','Monospace','Sans','']
            for font in options:
                if font in self.FontList:
                    self.font=font
                    break
            drScrolledMessageDialog.ShowMessage(self, ("Default font [%s] not found! \nChoosed [%s] instead." %(old,self.font)), "Error")

        self.txtPreview.SetText("Preview\n()[]{}\n0123")
        self.txtPreview.SetUseHorizontalScrollBar(0)

        self.txtPreview.SetReadOnly(1)
        self.txtPreview.SetMarginWidth(0, 0)
        self.txtPreview.SetMarginWidth(1, 0)
        self.txtPreview.SetMarginWidth(2, 0)

        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))

        self.txtPreview.StyleClearAll()

        self.txtPreview.StartStyling(0, 0xff)

        self.boxFonts = wx.ListBox(self, self.ID_FONTS, wx.Point(10, 10), wx.Size(250, 250), self.FontList)

        try:
            #self.boxFonts.SetStringSelection(self.font)
            i=self.boxFonts.FindString(self.font)
            if i<0:
                i=0
            self.boxFonts.Select(i)
            #self.boxFonts.EnsureVisible(i) # Bug: Doesn't work 
            self.boxFonts.SetFirstItem(i)
            
            
            
            
        except:
            drScrolledMessageDialog.ShowMessage(self, ("Something awful happened trying to \nset the font to the default."), "Error")
            self.boxFonts.SetSelection(0)

        self.boxSize = wx.ComboBox(self, self.ID_SIZE, self.size, wx.Point(10, 175), wx.Size(150, 50), ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])

        self.fgPanel = drColorPanel(self, id, wx.Point(10, 200), wx.Size(400, 225), True)
        self.fgPanel.SetValue(self.foreground)
        self.bgPanel = drColorPanel(self, id, wx.Point(220, 200), wx.Size(400, 225), False)
        self.bgPanel.SetValue(self.background)

        self.chkBold = wx.CheckBox(self, self.ID_BOLD, "Bold", wx.Point(10, 345))
        if self.bold:
            self.chkBold.SetValue(1)
        self.chkItalic = wx.CheckBox(self, self.ID_ITALIC, "Italic", wx.Point(110, 345))
        if self.italic:
            self.chkItalic.SetValue(1)
        self.chkUnderline = wx.CheckBox(self, self.ID_UNDERLINE, "Underline", wx.Point(210, 345))
        if self.underline:
            self.chkUnderline.SetValue(1)

        if ChangeSpec > 0:
            self.boxFonts.Enable(False)
            self.boxSize.Enable(False)
            self.chkBold.Enable(False)
            self.chkItalic.Enable(False)
            self.chkUnderline.Enable(False)
            if ChangeSpec == 1:
                self.bgPanel.Enable(False)
            elif ChangeSpec == 3:
                self.fgPanel.Enable(False)

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "&Cancel", wx.Point(5, 0), wx.Size(-1, -1))
        self.btnOk = wx.Button(self, self.ID_OK, "&Ok", wx.Point(300, 0), wx.Size(-1, -1))

        #Sizer:

        self.theSizer = wx.FlexGridSizer(2, 2, 5, 1)
        self.styleSizerLeft = wx.BoxSizer(wx.VERTICAL)
        self.styleSizerRight = wx.BoxSizer(wx.VERTICAL)

        self.styleSizerLeft.Add(wx.StaticText(self, -1, "Font:"), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(self.boxFonts, 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "Size:"), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(self.boxSize, 0, wx.ALL|wx.SHAPED,4)

        self.styleSizerLeft.Add(self.chkBold, 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "   "), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(self.chkItalic, 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "   "), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerLeft.Add(self.chkUnderline, 0, wx.ALL|wx.SHAPED,4)

        self.styleSizerRight.Add(self.txtPreview, 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerRight.Add(wx.StaticText(self, -1, 'Foreground:'), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerRight.Add(self.fgPanel, 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerRight.Add(wx.StaticText(self, -1, 'Background:'), 0, wx.ALL|wx.SHAPED,4)
        self.styleSizerRight.Add(self.bgPanel, 1, wx.ALL|wx.SHAPED,4)

        self.theSizer.Add(self.styleSizerLeft, 0, wx.ALL|wx.SHAPED,4)
        self.theSizer.Add(self.styleSizerRight, 0, wx.ALL|wx.SHAPED,4)
        self.theSizer.Add(self.btnCancel, 0, wx.ALL|wx.SHAPED|wx.ALIGN_RIGHT,4)
        self.theSizer.Add(self.btnOk, 0, wx.ALL | wx.SHAPED|wx.ALIGN_LEFT ,4)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.theSizer)

        self.btnCancel.SetDefault()

        #End Sizer

        self.Bind(wx.EVT_LISTBOX,  self.OnFontSelect, id=self.ID_FONTS)
        self.Bind(wx.EVT_COMBOBOX,  self.OnSizeSelect, id=self.ID_SIZE)
        self.Bind(wx.EVT_TEXT,  self.OnChangeSize, id=self.ID_SIZE)
        self.Bind(wx.EVT_CHECKBOX,  self.OnBold, id=self.ID_BOLD)
        self.Bind(wx.EVT_CHECKBOX,  self.OnItalic, id=self.ID_ITALIC)
        self.Bind(wx.EVT_CHECKBOX,  self.OnUnderline, id=self.ID_UNDERLINE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnOk, id=self.ID_OK)

    def OnChangeSize(self, event):
        self.size = self.boxSize.GetValue()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnFontSelect(self, event):
        self.font = self.boxFonts.GetStringSelection()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnSizeSelect(self, event):
        self.size = self.boxSize.GetStringSelection()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def SetColor(self):
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnBold(self, event):
        if self.chkBold.IsChecked():
            self.bold = "bold"
        else:
            self.bold = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnItalic(self, event):
        if self.chkItalic.IsChecked():
            self.italic = "italic"
        else:
            self.italic = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnUnderline(self, event):
        if self.chkUnderline.IsChecked():
            self.underline = "underline"
        else:
            self.underline = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnbtnCancel(self, event):
        self.EndModal(0)

    def OnbtnOk(self, event):
        self.OK = True
        self.EndModal(0)

    def ClickedOk(self):
        return self.OK

    def GetBackground(self):
        return self.background

    def GetColorString(self):
        return ("fore:" + self.foreground + ",back:" + self.background)

    def GetForeground(self):
        return self.foreground

    def GetStyleString(self):
        return ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline)

class drStyleDialog(wx.Dialog):

    def __init__(self, parent, id, title, isPrompt = False):

        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(640, 480))

        self.ancestor = parent.grandparent.parent

        self.ID_CANCEL = 101
        self.ID_OK = 102

        self.ID_FONTS = 103
        self.ID_SIZE = 104

        self.ID_BOLD = 109
        self.ID_ITALIC = 110
        self.ID_UNDERLINE = 111

        self.ID_STYLE = 121
        self.ID_LANGUAGE = 122

        self.last = 0

        if isPrompt:
            self.txtPromptStyleDictionary = self.ancestor.prefs.txtPromptStyleDictionary.copy()
        else:
            self.PythonStyleDictionary = self.ancestor.prefs.PythonStyleDictionary.copy()
            self.CPPStyleDictionary = self.ancestor.prefs.CPPStyleDictionary.copy()
            self.HTMLStyleDictionary = self.ancestor.prefs.HTMLStyleDictionary.copy()

        self.targetArray = []

        self.ChangeSpec = 0

        self.Enum = wx.FontEnumerator()
        self.Enum.EnumerateFacenames()
        self.FontList = self.Enum.GetFacenames()
        self.FontList.sort()

        self.txtPreview = wx.stc.StyledTextCtrl(self, id, wx.Point(225, 15), wx.Size(225, 125))

        self.Ok = False

        self.isPrompt = isPrompt

        i = self.ancestor.txtDocument.filetype
        if i > 2:
            i = 0
        self.boxLanguage = wx.Choice(self, self.ID_LANGUAGE, wx.Point(150, 135), wx.Size(-1, -1), ["Python", "C/C++", "HTML"])
        self.boxLanguage.SetSelection(i)

        if isPrompt:
            self.boxLanguage.Enable(False)

        self.txtPreview.SetText("Preview\n()[]{}\n0123")
        self.txtPreview.SetUseHorizontalScrollBar(0)

        self.txtPreview.SetMarginWidth(0, 0)
        self.txtPreview.SetMarginWidth(1, 0)
        self.txtPreview.SetMarginWidth(2, 0)

        self.txtPreview.SetReadOnly(1)

        self.boxFonts = wx.ListBox(self, self.ID_FONTS, wx.DefaultPosition, wx.Size(200, 250), self.FontList)

        self.boxSize = wx.ComboBox(self, self.ID_SIZE, "10", wx.DefaultPosition, wx.Size(150, 50), ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])

        self.fgPanel = drColorPanel(self, id, wx.DefaultPosition, wx.Size(400, 225), True)
        self.bgPanel = drColorPanel(self, id, wx.DefaultPosition, wx.Size(400, 225), False)

        self.chkBold = wx.CheckBox(self, self.ID_BOLD, "Bold")
        self.chkItalic = wx.CheckBox(self, self.ID_ITALIC, "Italic")
        self.chkUnderline = wx.CheckBox(self, self.ID_UNDERLINE, "Underline")

        self.btnCancel = wx.Button(self, self.ID_CANCEL, "&Cancel")
        self.btnCancel.SetDefault()
        self.btnOk = wx.Button(self, self.ID_OK, "&Ok")

        self.boxStyle = wx.ListBox(self, self.ID_STYLE, wx.DefaultPosition, wx.Size(150, 350), "")

        #Sizer:

        self.theSizer = wx.FlexGridSizer(2, 3, 5, 1)
        self.selectSizer = wx.FlexGridSizer(3, 3, 5, 10)
        self.listSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.styleSizerLeft = wx.BoxSizer(wx.VERTICAL)
        self.styleSizerRight = wx.BoxSizer(wx.VERTICAL)

        self.styleSizerLeft.Add(wx.StaticText(self, -1, "Font:"), 0, wx.SHAPED)
        self.styleSizerLeft.Add(self.boxFonts, 0, wx.SHAPED)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "Size:"), 0, wx.SHAPED)
        self.styleSizerLeft.Add(self.boxSize, 0, wx.SHAPED)

        self.styleSizerLeft.Add(self.chkBold, 0, wx.SHAPED)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.styleSizerLeft.Add(self.chkItalic, 0, wx.SHAPED)
        self.styleSizerLeft.Add(wx.StaticText(self, -1, "   "), 0, wx.SHAPED)
        self.styleSizerLeft.Add(self.chkUnderline, 0, wx.SHAPED)

        self.styleSizerRight.Add(self.txtPreview, 0, wx.SHAPED)
        self.styleSizerRight.Add(wx.StaticText(self, -1, 'Foreground:'), 0, wx.SHAPED)
        self.styleSizerRight.Add(self.fgPanel, 0, wx.SHAPED)
        self.styleSizerRight.Add(wx.StaticText(self, -1, 'Background:'), 0, wx.SHAPED)
        self.styleSizerRight.Add(self.bgPanel, 1, wx.SHAPED)

        self.listSizer.Add(wx.StaticText(self, -1, "Language: "), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.listSizer.Add(self.boxLanguage, 0, wx.ALIGN_CENTER | wx.SHAPED)

        self.selectSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.SHAPED)
        self.selectSizer.Add(self.listSizer, 0, wx.ALIGN_LEFT | wx.SHAPED)
        self.selectSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_LEFT | wx.SHAPED)

        self.selectSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.SHAPED)
        self.selectSizer.Add(wx.StaticText(self, -1, "Text Type:"), 0, wx.ALIGN_LEFT | wx.SHAPED)
        self.selectSizer.Add(wx.StaticText(self, -1, "   "), 0, wx.ALIGN_LEFT | wx.SHAPED)

        self.selectSizer.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_CENTER | wx.SHAPED)
        self.selectSizer.Add(self.boxStyle, 1, wx.SHAPED | wx.ALIGN_CENTER)
        self.selectSizer.Add(wx.StaticText(self, -1, ""), 1,  wx.SHAPED | wx.ALIGN_CENTER)

        self.theSizer.Add(self.selectSizer, 0, wx.SHAPED)
        self.theSizer.Add(self.styleSizerLeft, 0, wx.SHAPED)
        self.theSizer.Add(self.styleSizerRight, 0, wx.SHAPED)
        self.theSizer.Add(self.btnCancel, 0, wx.SHAPED | wx.ALIGN_CENTER)
        self.theSizer.Add(wx.StaticText(self, -1, ""), 0, wx.SHAPED)
        self.theSizer.Add(self.btnOk, 1, wx.SHAPED | wx.ALIGN_CENTER)

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        #End Sizer

        self.OnSelectLanguage(None)

        self.Bind(wx.EVT_LISTBOX,  self.OnFontSelect, id=self.ID_FONTS)
        self.Bind(wx.EVT_LISTBOX,  self.OnSelectStyle, id=self.ID_STYLE)
        self.Bind(wx.EVT_CHOICE,  self.OnSelectLanguage, id=self.ID_LANGUAGE)
        self.Bind(wx.EVT_COMBOBOX,  self.OnSizeSelect, id=self.ID_SIZE)
        self.Bind(wx.EVT_TEXT,  self.OnChangeSize, id=self.ID_SIZE)
        self.Bind(wx.EVT_CHECKBOX,  self.OnBold, id=self.ID_BOLD)
        self.Bind(wx.EVT_CHECKBOX,  self.OnItalic, id=self.ID_ITALIC)
        self.Bind(wx.EVT_CHECKBOX,  self.OnUnderline, id=self.ID_UNDERLINE)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnCancel, id=self.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON,  self.OnbtnOk, id=self.ID_OK)

    def OnChangeSize(self, event):
        self.size = self.boxSize.GetValue()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnFontSelect(self, event):
        self.font = self.boxFonts.GetStringSelection()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnSizeSelect(self, event):
        self.size = self.boxSize.GetStringSelection()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def SetColor(self):
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnBold(self, event):
        if self.chkBold.IsChecked():
            self.bold = "bold"
        else:
            self.bold = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnItalic(self, event):
        if self.chkItalic.IsChecked():
            self.italic = "italic"
        else:
            self.italic = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnUnderline(self, event):
        if self.chkUnderline.IsChecked():
            self.underline = "underline"
        else:
            self.underline = ""
        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

    def OnbtnCancel(self, event):
        self.EndModal(0)

    def OnbtnOk(self, event):

        if self.ChangeSpec == 0:
            self.targetArray[self.last] = self.GetStyleString()
        elif self.ChangeSpec == 1:
            self.targetArray[self.last] = self.GetForeground()
        elif self.ChangeSpec == 2:
            self.targetArray[self.last] = self.GetColorString()
        elif self.ChangeSpec == 3:
            self.targetArray[self.last] = self.GetBackground()

        self.Ok = True

        self.EndModal(0)

    def ClickedOk(self):
        return self.Ok

    def GetArrays(self):
        if self.isPrompt:
            return self.txtPromptStyleDictionary
        return self.PythonStyleDictionary, self.CPPStyleDictionary, self.HTMLStyleDictionary

    def GetBackground(self):
        return self.background

    def GetColorString(self):
        return ("fore:" + self.foreground + ",back:" + self.background)

    def GetForeground(self):
        return self.foreground

    def GetStyleString(self):
        return ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline)

    def OnSelectLanguage(self, event):
        sel = self.boxLanguage.GetSelection()

        try:
            if self.ChangeSpec == 0:
                self.targetArray[self.last] = self.GetStyleString()
            elif self.ChangeSpec == 1:
                self.targetArray[self.last] = self.GetForeground()
            elif self.ChangeSpec == 2:
                self.targetArray[self.last] = self.GetColorString()
            elif self.ChangeSpec == 3:
                self.targetArray[self.last] = self.GetBackground()
        except:
            #This will happen the first time this function is called.
            pass

        if self.isPrompt:
            self.targetArray = self.txtPromptStyleDictionary
            array = ["Normal", "Line Number (Margin)", "Brace-Selected (Match)", "Brace-Selected (No Match)", "Character (Single Quoted String)", "Class Name", "Comment", "Comment Block", "Function Name", "Keyword", "Number", "Operator", "String", "String EOL", "Triple Quoted String", "Caret Foreground", "Selection"]
        else:
            if sel == 1:
                self.targetArray = self.CPPStyleDictionary
                array = ["Normal", "Line Number (Margin)", "Brace-Selected (Match)", "Brace-Selected (No Match)", "Character", "Preprocessor", "Comment", "Verbatim", "Keyword", "C Identifier", "Number", "Operator", "String", "String EOL", "Global Class", "Regex", "UUID", "Caret Foreground", "Selection", "Folding", "Long Line Indicator"]
            elif sel == 2:
                self.targetArray = self.HTMLStyleDictionary
                array = ["Normal", "Line Number (Margin)", "Brace-Selected (Match)", "Brace-Selected (No Match)", "Tag", "Unkown Tag", "Atrribute", "Unkown Attribute", "Number", "String", "Character (Single Quoted String)", "Comment", "Entity", "Tag End", "XML Start", "XML End", "Script", "Value", "Caret Foreground", "Selection", "Folding", "Long Line Indicator", "Current Line Highlight"]
            else:
                self.targetArray = self.PythonStyleDictionary
                array = ["Normal", "Line Number (Margin)", "Brace-Selected (Match)", "Brace-Selected (No Match)", "Character (Single Quoted String)", "Class Name", "Comment", "Comment Block", "Function Name", "Keyword", "Number", "Operator", "String", "String EOL", "Triple Quoted String", "Caret Foreground", "Selection", "Folding", "Long Line Indicator", "Current Line Highlight", "Indentation Guide"]

        self.last = -1

        self.boxStyle.Set(array)
        self.boxStyle.SetSelection(0)
        self.OnSelectStyle(event)

    def OnSelectStyle(self, event):
        current = self.boxStyle.GetSelection()
        seltext = self.boxStyle.GetStringSelection()

        if self.last > -1:
            if self.ChangeSpec == 0:
                self.targetArray[self.last] = self.GetStyleString()
            elif self.ChangeSpec == 1:
                self.targetArray[self.last] = self.GetForeground()
            elif self.ChangeSpec == 2:
                self.targetArray[self.last] = self.GetColorString()
            elif self.ChangeSpec == 3:
                self.targetArray[self.last] = self.GetBackground()

        self.ChangeSpec = 0

        stylestring = self.targetArray[current]
        if (seltext == "Caret Foreground") or (seltext == "Long Line Indicator") or (seltext == "Indentation Guide"):
            self.ChangeSpec = 1
            stylestring = "fore:" + stylestring
        elif (seltext == "Selection") or (seltext == "Folding"):
            self.ChangeSpec = 2
        elif seltext == "Current Line Highlight":
            self.ChangeSpec = 3
            stylestring = "back:" + stylestring

        self.font = getStyleProperty("face", stylestring)
        if not self.font:
            self.font = getStyleProperty("face", self.targetArray[0])
        self.size = getStyleProperty("size", stylestring)
        if not self.size:
            self.size = getStyleProperty("size", self.targetArray[0])
        self.foreground = getStyleProperty("fore", stylestring)
        if not self.foreground:
            self.foreground = getStyleProperty("fore", self.targetArray[0])
        self.background = getStyleProperty("back", stylestring)
        if not self.background:
            self.background = getStyleProperty("back", self.targetArray[0])
        self.bold = getStyleProperty("bold", stylestring)
        self.italic = getStyleProperty("italic", stylestring)
        self.underline = getStyleProperty("underline", stylestring)

        if self.ChangeSpec > 0:
            self.font = getStyleProperty("face", self.targetArray[0])
            self.size = getStyleProperty("size", self.targetArray[0])
            if self.ChangeSpec == 1:
                self.background = getStyleProperty("back", self.targetArray[0])
            elif self.ChangeSpec == 3:
                self.foreground = getStyleProperty("fore", self.targetArray[0])

        if self.font not in self.FontList:
            f1 = string.capwords(self.font)
            f2 = string.lower(self.font)
            if f1 in self.FontList:
                self.font = f1
            elif f2 in self.FontList:
                self.font = f2

        if self.font not in self.FontList:
            old=self.font
            self.size = '12'
            options=['Courier','Courier 10 Pitch','Monospace','Sans','']
            for font in options:
                if font in self.FontList:
                    self.font=font
                    break
            #I don't know why this a traceback: no foreground !!!
            #drScrolledMessageDialog.ShowMessage(self, ("Default font [%s] not found! \nChoosed [%s] instead." %(old,self.font)), "Error")
            print "Default font [%s] not found! \nChoosed [%s] instead." %(old,self.font)

        self.txtPreview.StyleResetDefault()
        self.txtPreview.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, ("fore:" + self.foreground + ",back:" + self.background + ",size:" + self.size + ",face:" + self.font + "," + self.bold + "," + self.italic + "," + self.underline))
        self.txtPreview.StyleClearAll()
        self.txtPreview.StartStyling(0, 0xff)

        try:
            #self.boxFonts.SetStringSelection(self.font)
            i=self.boxFonts.FindString(self.font)
            if i<0:
                i=0
            self.boxFonts.Select(i)
            #self.boxFonts.EnsureVisible(i) # Bug: Doesn't work 
            self.boxFonts.SetFirstItem(i)
        except:
            drScrolledMessageDialog.ShowMessage(self, ("Something awful happened trying to \nset the font to the default."), "Error")
            self.boxFonts.SetSelection(0)

        try:
            tsizearray = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
            if not self.size in tsizearray:
                self.boxSize.SetValue(self.size)
            else:
                i = tsizearray.index(self.size)
                self.boxSize.SetSelection(i)
        except:
            drScrolledMessageDialog.ShowMessage(self, ("Something awful happened trying to \nset the font to the default."), "Error")
            self.boxSize.SetSelection(0)

        self.OnSizeSelect(event)

        self.fgPanel.SetValue(self.foreground)
        self.bgPanel.SetValue(self.background)

        self.chkBold.SetValue((len(self.bold) > 0))
        self.chkItalic.SetValue((len(self.italic) > 0))
        self.chkUnderline.SetValue((len(self.underline) > 0))

        self.boxFonts.Enable(self.ChangeSpec == 0)
        self.boxSize.Enable(self.ChangeSpec == 0)
        self.chkBold.Enable(self.ChangeSpec == 0)
        self.chkItalic.Enable(self.ChangeSpec == 0)
        self.chkUnderline.Enable(self.ChangeSpec == 0)
        if self.ChangeSpec == 1:
            self.fgPanel.Enable(True)
            self.bgPanel.Enable(False)
        elif self.ChangeSpec == 3:
            self.fgPanel.Enable(False)
            self.bgPanel.Enable(True)
        else:
            self.fgPanel.Enable(True)
            self.bgPanel.Enable(True)

        self.last = current