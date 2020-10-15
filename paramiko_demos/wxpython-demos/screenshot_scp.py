import wx
import paramiko
import sys
from time import sleep

class Screenshot(object):
    def __init__(self, filename = "snap.png"):
        self.filename = filename
        try:
            p = wx.GetDisplaySize()
            self.p = p
            bitmap = wx.EmptyBitmap( p.x, p.y)
            dc = wx.ScreenDC()
            memdc = wx.MemoryDC()
            memdc.SelectObject(bitmap)
            memdc.Blit(0,0, p.x, p.y, dc, 0,0)
            memdc.SelectObject(wx.NullBitmap)
            bitmap.SaveFile(filename, wx.BITMAP_TYPE_PNG )
            
        except:
            self.filename = ""
        
def main():               
    paramiko.util.log_to_file('snap.log')
    
    caption = u"Required data"
    path = "/var/www/html/screenshots" # change this to make it your default path
    hostname = "www.whateverdomain.com" # change this to make it your default targe host
    username = "batok" # change this to make it your default user
    port = 22 # change this to another port if necessary....
    
    app = wx.PySimpleApp()
    time_to_wait = wx.GetNumberFromUser(message = "Time", 
                                        prompt = "Secs.",
                                         caption = "Enter Seconds to Wait...",
                                          value = 5,
                                            min = 5,
                                             max = 20,
                                              parent= None )
    try:
        tw = int(time_to_wait)
    except:
        sys.exit(-1)
    sleep( tw  )
    try:
        wx.Bell()
    except:
        pass
    
    s_shot = Screenshot()
    
    filename = s_shot.filename
    if filename == "":
        sys.exit(-1)
        
    if wx.YES == wx.MessageBox("Do you want to see the screenshot/nreduced by the half ?", "Hey!", wx.YES_NO | wx.ICON_QUESTION):
        dlg = wx.Dialog(None,-1, "Your screenshot half the size")
        img = wx.Image("snap.png" , wx.BITMAP_TYPE_ANY)
        w = img.GetWidth()
        h = img.GetHeight()
        img2 = img.Scale(w/2,h/2)
        wx.StaticBitmap(dlg,-1, wx.BitmapFromImage(img2))
        dlg.Fit()
        dlg.Show()
        
    
    target = "%s/%s" % ( path, filename )
    wx.MessageBox("A %s X %s screenshot\nis at %s" % (s_shot.p.x, s_shot.p.y, filename ), "Hey!")
    hostname = wx.GetTextFromUser("Host", caption = caption , default_value=hostname)
    username = wx.GetTextFromUser("User Name", caption = caption , default_value=username)
    password = wx.GetPasswordFromUser("Password", caption = caption )
    s_target = wx.GetTextFromUser("Destination File", caption= caption, default_value = target)
    
    if "" in (hostname, username, s_target):
        wx.MessageBox("Mmmm... some required fields are empty", "Hey!")
        sys.exit(-1)
    
    # Now paramiko's stuff... a.k.a secure copy
    try:
        
        t = paramiko.Transport((hostname, port))
        t.use_compression(True)
        t.connect(username=username, password=password, hostkey=None)
        sftp = paramiko.SFTPClient.from_transport(t)
        data = open(filename, 'rb').read()
        sftp.open(s_target, 'wb').write(data)
        t.close()
        wx.MessageBox("The %s file was sent to server" % filename, "Hey!")
    
    except Exception, e:
        print e
        try:
            t.close()
        except:
            pass
        
    return

if __name__ == "__main__":
    main()