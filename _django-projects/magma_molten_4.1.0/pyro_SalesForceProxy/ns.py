import sys
import Pyro.naming

opts = ['-v','-s','NSSecEx']

if (sys.platform != 'win32'): # Linux requires the following options...
    hostname = '0.0.0.0' # tide.magma-da.com requires the hostname to be 0.0.0.0 (cannot be 127.0.0.1) otherwise the server and client cannot find the Name Server...
    opts += ['-n','%s' % (hostname),'-p','9999']

Pyro.naming.main(opts)