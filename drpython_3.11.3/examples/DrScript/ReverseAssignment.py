#drscript

#By Daniel Pozmanter
#Released under the GPL

endOfLineChar = DrDocument.GetEndOfLineCharacter()
targets = DrDocument.GetSelectedText().split(endOfLineChar)
l = len(targets)
c = 0
newselection = ""
while c < l:
    x = targets[c].find('=')
    
    if x > -1:  
        targets[c] = targets[c][x+2:] + " = " + targets[c][0:x] 
    newselection = newselection + targets[c]
    if c < (l - 1):
        newselection = newselection + endOfLineChar
    c = c + 1
        
DrDocument.SetSelectedText(newselection)