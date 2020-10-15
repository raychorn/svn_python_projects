import sys, platform

isUsingWindows = (sys.platform.lower().find('win') > -1) and (os.name.lower() == 'nt')
isUsingMacOSX = (sys.platform.lower().find('darwin') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows)
isUsingLinux = (sys.platform.lower().find('linux') > -1) and (os.name.find('posix') > -1) and (not isUsingWindows) and (not isUsingMacOSX)

if (__name__ == '__main__'):
    pass
