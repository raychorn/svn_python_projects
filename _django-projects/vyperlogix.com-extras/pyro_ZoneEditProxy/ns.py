import sys
import Pyro.naming

opts = ['-v','-s','NSSecEx']

hostname = '10.1.10.55'
opts += ['-n','%s' % (hostname),'-p','8888']

Pyro.naming.main(opts)