#drscript
#Updated to new namespace.

#By Daniel Pozmanter
#Released under the GPL

target = ""
newtext = ""
d = wx.TextEntryDialog(DrFrame, "Switch What?:", "Switch All In Selection", "")
if d.ShowModal() == wx.ID_OK:
    target = d.GetValue()
    d = wx.TextEntryDialog(DrFrame, ("Switch " + target +  " With:"), "Switch All In Selection", "")
    if d.ShowModal() == wx.ID_OK:
        newtext = d.GetValue()
        drpytemp = "DRPYTHON111TEMP"
        selection = DrDocument.GetSelectedText()
        selection = selection.replace(newtext, drpytemp)
        selection = selection.replace(target, newtext)
        selection = selection.replace(drpytemp, target)
        DrDocument.SetSelectedText(selection)