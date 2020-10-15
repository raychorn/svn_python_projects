import os,sys
import py_compile

def sourcesFrom(fp):
    return [os.sep.join([fp,f]) for f in os.listdir(fp) if (f.split('.')[-1] == 'py')]

fp = os.path.abspath('daemons')
daemons = sourcesFrom(fp)

fp = os.path.abspath('daemons/dlib')
daemons_lib = sourcesFrom(fp)

fp = os.path.abspath('.')
sources = sourcesFrom(fp)

for f in daemons+sources+daemons_lib:
    py_compile.compile(f)
    
print 'Done !'