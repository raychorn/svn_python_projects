from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.win.registry import winreg

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

webstore_url = lambda item:'http://www.regnow.com/softsell/nph-softsell.cgi?items=%s' % (item)

class RegNowAffiliateTracking(Cooperative):
    def __init__(self, appName, publisherName='Vyper Logix Corp.'):
        self.__appName__ = '' if (appName is None) or (not misc.isString(appName)) else appName
        self.__publisherName__ = '' if (publisherName is None) or (not misc.isString(publisherName)) else publisherName
        self.__rootKeyName__ = '\\Software\\Digital River\\SoftwarePassport\\%s\\%s' % (self.publisherName,self.appName)
        self.__rootHKLM__ = winreg.get_key(winreg.HKEY.LOCAL_MACHINE, self.rootKeyName, winreg.KEY.ALL_ACCESS)
        self.__rootHKCU__ = winreg.get_key(winreg.HKEY.CURRENT_USER, self.rootKeyName, winreg.KEY.ALL_ACCESS)
        
    def __str__(self):
        return '%s("%s","%s") --> "%s"' % (ObjectTypeName.objectSignature(self),self.appName,self.publisherName,self.rootKeyName)
 
    def webstore(self,item='14605-1'):
        return webstore_url(item)
    
    def buyURL(self, root, item='14605-1'):
        if (root is not None):
            subKey = winreg.get_key(root, '0', winreg.KEY.ALL_ACCESS)
            try:
                url = subKey.values['BuyURL']
            except WindowsError:
                url = self.webstore(item=item)
            return url
        return None

    def rootKeyName():
        doc = "rootKeyName"
        def fget(self):
            return self.__rootKeyName__
        def fset(self, key):
            self.__rootKeyName__ = key
        return locals()
    rootKeyName = property(**rootKeyName())

    def rootHKLM():
        doc = "root for HKLM"
        def fget(self):
            return self.__rootHKLM__
        return locals()
    rootHKLM = property(**rootHKLM())

    def rootHKCU():
        doc = "root for HKCU"
        def fget(self):
            return self.__rootHKCU__
        return locals()
    rootHKCU = property(**rootHKCU())
    
    def appName():
        doc = "appName"
        def fget(self):
            return self.__appName__
        return locals()
    appName = property(**appName())
    
    def publisherName():
        doc = "publisherName"
        def fget(self):
            return self.__publisherName__
        return locals()
    publisherName = property(**publisherName())
