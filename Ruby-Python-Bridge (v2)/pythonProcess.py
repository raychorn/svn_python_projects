import os,sys
import traceback
import rubypythonlib

_num_ruby_instances_spawned = 0

_ruby_process_path = 'ruby\\doprocess.rb'

_threadQ = rubypythonlib.ThreadQueue(10)

_details_symbol = '@details'

_auto_spawn_ruby = False # Set this True to perform a small Python-powered Stress Test that spawns 10 Ruby instances each running transactions against the Bridge.

@rubypythonlib.threadify(_threadQ)
def spawnRuby(progPath,instanceNum):
    import subprocess
    if (not os.path.exists(_details_symbol)):
        os.mkdir(_details_symbol)
    print '0. progPath=[%s]' % progPath
    _dirName = os.path.dirname(progPath[-1]) if len(progPath) == 2 else ''
    print '_dirName=[%s]' % _dirName
    progPath = [progPath] if not isinstance(progPath,list) else progPath
    _pp = [f for f in progPath if os.path.exists(f)][0]
    _logName = os.path.join(os.path.join(os.sep.join(_dirName.split(os.sep)[0:-1])),'%s_%s_%s.txt' % (os.sep.join([_details_symbol,'.'.join(rubypythonlib.timeStamp().replace(':','').split('.')[0:-1])]),os.path.basename(_pp).replace('.','_'),instanceNum))
    print '_logName=[%s]' % _logName
    fOut = open(_logName,'w')
    e = os.environ
    if (len(_dirName) > 0):
        os.chdir(_dirName)
    p = subprocess.Popen(progPath, env=e, stdout=fOut, shell=False)
    p.wait()
    fOut.flush()
    fOut.close()

@rubypythonlib.threadify(_threadQ)
def spawnPython():
    rubypythonlib.startPythonController('127.0.0.1','xxxShutdownxxx',rubypythonlib.salesForceConnector)

def spawnPython2():
    proxy = rubypythonlib.ReverseProxy('127.0.0.1',55555,'127.0.0.1',xrange(60000,60000+1000))
    proxy.handle_connections()

_root = os.path.abspath(_details_symbol)
if (os.path.exists(_root)):
    _files = os.listdir(_root)
    for f in _files:
        _fname = os.sep.join([_root,f])
        if (os.path.exists(_fname)):
            os.remove(_fname)

excp = rubypythonlib.ExceptionHandler()

if (_auto_spawn_ruby):
    _r = os.path.abspath(_ruby_process_path)
    for i in xrange(0,10):
        print 'Spawning Ruby Instance #%d' % (_num_ruby_instances_spawned)
        spawnRuby(['ruby',_r],_num_ruby_instances_spawned)
        _num_ruby_instances_spawned += 1

spawnPython2()

_threadQ.join()
