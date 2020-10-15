#### test program 
#!/usr/bin/env python 
# Author: Frank Wilder <frank.wil...@gmail.com> 
# License: GPLv2 
# 07/07/10 
# Python 2.5 / wxPython 2.8.0.1 
import gdata.apps.service 
def GetCaptcha( url) : 
    """ used to pop up a wx dialog to query user for captcha """ 
    import wx 
    import captcha_dialog 
    captcha_response = "" 
    app = wx.PySimpleApp() 
    dlg = captcha_dialog.CaptchaDialog(url) 
    if dlg.ShowModal() == wx.ID_OK: 
        captcha_response = dlg.GetCaptcha() 
    dlg.Destroy() 
    app.MainLoop() 
    return captcha_response 
def GoogleLogon() : 
    """ Used to authencated against Google """ 
    domain_opt = 'a-college.edu' 
    email_opt = 'administrator' 
    password_opt = 'abcde12345' 
    # get a handle 
    service = gdata.apps.service.AppsService(email=email_opt, domain=domain_opt, password=password_opt) 
    try : 
        # try to logon 
        service.ProgrammaticLogin() 
        return service 
    except gdata.service.CaptchaRequired: 
        # got a problem...google thinks this is a bot. we have to answer a captcha 
        # get the token and the url to the captcha to question 
        captcha_token = service._GetCaptchaToken() 
        url = service._GetCaptchaURL() 
        # display captcha to user and get answer 
        captcha_response = GetCaptcha(url) 
        # only try to logon it the user typed something 
        if captcha_response : 
            try : 
                # try to logon again with captcha response 
                service.ProgrammaticLogin(captcha_token, captcha_response) 
                return service 
            except gdata.service.CaptchaRequired: 
                print "Cannot logon: captcha does not match" 
                return None 
            except gdata.service.BadAuthentication: 
                print "Cannot logon: login service rejected the username or password" 
                return None 
        else : 
            return None 
    except gdata.service.BadAuthentication: 
        print "Cannot logon: login service rejected the username or password" 
        return None 
    return None 
############################### 
service = GoogleLogon() 
if service : 
    a = service.RetrieveUser('johndoe') 
    print a 
else : 
    print 'could not retrieve user info' 
#### end test program 
