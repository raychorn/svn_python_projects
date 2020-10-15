#drscript

#By Daniel Pozmanter
#Released under the GPL

target = ""
newtext = ""
d = wx.TextEntryDialog(DrFrame, "Replace What?:", "Replace All In Selection", "")
if d.ShowModal() == wx.ID_OK:
    target = d.GetValue()
    d = wx.TextEntryDialog(DrFrame, ("Replace " + target +  " With:"), "Replace All In Selection", "")
    if d.ShowModal() == wx.ID_OK:
        newtext = d.GetValue()
DrDocument.SetSelectedText(DrDocument.GetSelectedText().replace(target, newtext))