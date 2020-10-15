if (__name__ == '__main__'):
    #import os, sys
    #from vyperlogix.imports import monitor
    
    #fname = os.sep.join([os.path.dirname(sys.argv[0]),os.path.basename('%s.txt' % (sys.argv[0].split('.')[0]))])
    #if (os.path.exists(fname)):
        #os.remove(fname)

    #def myCallback(path,fullname):
        #_msg = '(%s) :: "%s" --> "%s".' % (os.path.basename(sys.argv[0]),path,fullname)
        #fOut = open(fname,'a')
        #try:
            #print >>fOut, _msg
        #finally:
            #fOut.flush()
            #fOut.close()
        #print _msg
    #monitor.hook(callback=myCallback)
    
    from vyperlogix.imports import monitor
    
    monitor.reporterHook(fname='Z:\\python projects\\importhooks\\test_monitor.txt')
    
    from vyperlogix import oodb

    #mnames = ("colorsys", "urlparse", "distutils.core", "compiler.misc")
    #for mname in mnames:
        #parent = mname.split(".")[0]
        #for n in sys.modules.keys():
            #if n.startswith(parent):
                #del sys.modules[n]
    #for mname in mnames:
        #m = __import__(mname, globals(), locals(), ["__dummy__"])
        #m.__loader__  # to make sure we actually handled the import
