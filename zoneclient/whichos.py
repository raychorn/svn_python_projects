import wmi
c = wmi.WMI()
for os in c.Win32_OperatingSystem():
    #for k,v in os.properties.iteritems():
        #print '%s --> %s' % (k,eval('os.%s' % (k)))
    print '"%s","%s","%s"' % (os.Name,os.osarchitecture,os.Version)
