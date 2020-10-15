import os
import re

top = "/opt"

types = ['.py']

__re__ = re.compile(r"from\skombu\simport.*")

def __is__(fname,regex):
    try:
        for l in open(fname,'r'):
            if (regex.search(l)):
                return True
    except:
        pass
    return False

if (__name__ == '__main__'):
    for folder,dirs,files in os.walk(top):
        for f in [ff for ff in files if (os.path.splitext(ff)[-1] in types)]:
            fn = '%s%s%s' % (folder,os.sep,f)
            if (__is__(fn, __re__)):
                print fn, 'YES'
            else:
                #print fn, 'NO'
                pass
            