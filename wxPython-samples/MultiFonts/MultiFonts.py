# test wx.Font() and wx.FontDialog on a given text
# wx.Font(pointSize, family, style, weight, underline=false, faceName="",
#     encoding=wx.FONTENCODING_DEFAULT)

import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title, data):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(600, 400))
        panel = wx.Panel(self, wx.ID_ANY)
        button = wx.Button(panel, wx.ID_ANY, label='Change Font',
            pos=(3, 3))
        button.Bind(wx.EVT_BUTTON, self.changeFont)

        # family: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, 
        # wx.SWISS, wx.MODERN
        # style: wx.NORMAL, wx.SLANT or wx.ITALIC
        # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
        font = wx.Font(16, wx.SCRIPT, wx.NORMAL, wx.LIGHT)
        # use additional fonts this way ...
        #face = u'Comic Sans MS'
        #font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, face)

        self.text = wx.StaticText(panel, wx.ID_ANY, data, pos=(10,35))
        self.text.SetFont(font)

    def changeFont(self, event):
        dialog = wx.FontDialog(None, wx.FontData())
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetFontData()
            font = data.GetChosenFont()
            self.text.SetForegroundColour(data.GetColour())
            self.text.SetFont(font)
        dialog.Destroy()


data = """\
Al Gore:  The Wild Years
America's Most Popular Lawyers
Career Opportunities for History Majors
Different Ways to Spell "Bob"
Ethiopian Tips on World Dominance
Everything Men Know About Women
Everything Women Know About Men
Staple Your Way to Success
The Amish Phone Book
The Engineer's Guide to Fashion
Ralph Nader's list of pleasures"""

app = wx.App(0)
# create instance of MyFrame and show
MyFrame(None, "Text and Font", data).Show()
# start the event loop
app.MainLoop()