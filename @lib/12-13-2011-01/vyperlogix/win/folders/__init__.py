__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
from vyperlogix.classes.SmartObject import SmartFuzzyObject

__vectors__ = SmartFuzzyObject()

def AllUsersDesktop():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("AllUsersDesktop")

def AllUsersStartMenu():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("AllUsersStartMenu")

def AllUsersPrograms():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("AllUsersPrograms")

def AllUsersStartup():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("AllUsersStartup")

def Desktop():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Desktop")

def Favorites():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Favorites")

def Fonts():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Fonts")

def MyDocuments():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("MyDocuments")

def NetHood():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("NetHood")

def PrintHood():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("PrintHood")

def Recent():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Recent")

def SendTo():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("SendTo")

def StartMenu():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("StartMenu")

def Startup():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Startup")

def Templates():
    import win32com.client
    objShell = win32com.client.Dispatch("WScript.Shell")
    return objShell.SpecialFolders("Templates")

for k in ["AllUsersDesktop","AllUsersStartMenu","AllUsersPrograms","AllUsersStartup","Desktop","Favorites","Fonts","MyDocuments","NetHood","PrintHood","Recent","SendTo","StartMenu","Startup","Templates"]:
    __vectors__[k] = eval(k)
    
__symbols__ = ['%'+s+'%' for s in __vectors__.keys()]
