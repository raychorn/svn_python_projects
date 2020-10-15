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

# style properties

def convertStyleToColorArray(StyleString):
    ''' Returns a two arrays, one for the foreground, and one for the background '''
    #Returns the Red, Green Blue Values for a string formatted: #00FF33
    return (convertColorPropertyToColorArray(getStyleProperty("fore", StyleString)), convertColorPropertyToColorArray(getStyleProperty("back", StyleString)))

def convertColorPropertyToColorArray(ColorString):
    #Returns the Red, Green Blue Values for a string formatted: #00FF33
    return int(ColorString[1:3], 16), int(ColorString[3:5], 16), int(ColorString[5:7], 16)

def convertStyleStringToWXFontArray(StyleString):
    #This returns an array to be used as arguments in the wx.Font constructor,
    #Face, Size, Underline, Bold, Italic

    t = getStyleProperty("size", StyleString)
    size = int(t)

    t = getStyleProperty("italic", StyleString)
    italic = (len(t) > 0)

    t = getStyleProperty("bold", StyleString)
    bold = (len(t) > 0)

    t = getStyleProperty("underline", StyleString)
    underline = (len(t) > 0)

    t = getStyleProperty("face", StyleString)
    face = t

    return face, size, underline, bold, italic


def getStyleProperty(Property, StyleString):

    if (Property == "bold") or (Property == "italic") or (Property == "underline"):
        if StyleString.find(Property) != -1:
            return Property
        else:
            return ""

    i = StyleString.find(Property)
    if i != -1:
        lindex = i + len(Property) + 1
        rindex = StyleString[lindex:].find(",")
        if rindex == -1:
            return StyleString[lindex:]
        rindex = rindex + lindex
        return StyleString[lindex:rindex]
    return ""

def setStyleProperty(Property, StyleString, newValue):

    i = StyleString.find(Property)
    if Property == "bold":
        if i != -1:
            return StyleString[0:i] + "," + newValue + StyleString[(i + len(Property)):]
        else:
            prop = getStyleProperty("face", StyleString)
            i = StyleString.find(prop) + len(prop)
            return StyleString[0:i] + "," + newValue + StyleString[i:]
    if Property == "italic":
        if i != -1:
            return StyleString[0:i] + "," + newValue + StyleString[(i + len(Property)):]
        else:
            prop = getStyleProperty("face", StyleString)
            i = StyleString.find(prop) + len(prop)
            return StyleString[0:i] + "," + newValue + StyleString[i:]
    if Property == "underline":
        if i != -1:
            return StyleString[0:i] + "," + newValue + StyleString[(i + len(Property)):]
        else:
            prop = getStyleProperty("face", StyleString)
            i = StyleString.find(prop) + len(prop)
            return StyleString[0:i] + "," + newValue + StyleString[i:]

    if i != -1:
        lindex = i + len(Property) + 1
        rindex = StyleString[lindex:].find(",")
        if rindex == -1:
            return StyleString[0:lindex] + newValue
        rindex = rindex + lindex
        return StyleString[0:lindex] + newValue + StyleString[rindex:]
    return ""
