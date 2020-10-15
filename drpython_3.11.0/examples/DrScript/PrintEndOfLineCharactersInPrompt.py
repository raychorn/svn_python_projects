#drscript

#By Daniel Pozmanter
#Released under the GPL

drdoctext = DrDocument.GetText()
l = len(drdoctext)
x = 0
s = ""
while x < l:
    if drdoctext[x] == '\r':
        s = s + "<Carriage Return>\n"
    elif drdoctext[x] == '\n':
        s = s + "<Newline>\n"
    x = x + 1
DrFrame.ShowPrompt()
DrPrompt.SetText(s)