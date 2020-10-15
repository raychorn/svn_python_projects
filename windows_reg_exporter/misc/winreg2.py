from vyperlogix.win.registry import winreg2

if __name__=="__main__":
    key = winreg2.Registry.open('HKEY_LOCAL_MACHINE', "SOFTWARE\\Python")
    print 'key=(%s)' % str(key)
    print 'key.getkeyname()=(%s)' % str(key.getkeyname())
    print 'key.getkey()=(%s)' % str(key.getkey())
    corekey = key.openkey(1)

    idx = 0
    while True:
        try:
            keyname = corekey.enumkey(idx)
            idx += 1
            print '(%s) :: keyname=(%s)' % (idx,keyname)
            if (float(str(keyname)) > 0.0):
                keyVersion = corekey.openkey(idx)
                print 'keyVersion=(%s)' % keyVersion
                print 'keyVersion.getkeyname()=(%s)' % keyVersion.getkeyname()
                keyPath = keyVersion.openkey(2)
                print 'keyPath=(%s)' % keyPath
                print 'keyPath.getkeyname()=(%s)' % keyPath.getkeyname()
                print 'Install path is %s' % keyPath.getvalue()
                keyPath.close()
                keyVersion.close()
                break
        except RegistryError:
            break

    corekey.close()
    key.close()

