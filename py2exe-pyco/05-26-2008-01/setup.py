from distutils.core import setup
import py2exe, sys, os, shutil
import pycoutil

sys.argv.append('py2exe')
#~ sys.argv.append('--xref')

# - - - - - user options - - - - -
#these are used in several places and are therfore variables
#dont use absolute path names or subdirectories here
script = "test.py"
zipfile = "shared.lib"
windows = False
excludes = ['popen2', 'os2emxpath', 'macpath']
includes = []

# - - - - - normaly you do not edit below this line - - - - - - -
dist_dir = 'dist'

setup(
    options = {
        'py2exe': {
        'optimize': 2,
        'dist_dir': dist_dir,
        'excludes': excludes,
        'includes': includes,
        }
    },
    console = [{'script': script}],
    zipfile = zipfile,
)

if 'popen2' in excludes:                                #if popen2 is excluded
    os.remove(os.path.join(dist_dir, 'w9xpopen.exe'))   #remove unneeded hack


#- - - - here comes the pyco specific part - - - - - 
#now create the single file executable

filename = os.path.splitext(script)[0]                  #name the scrip w/o ext
exefile = filename + '.exe'                             #name of the exe

os.remove(os.path.join(dist_dir, exefile))              #remove exe from py2exe
shutil.copyfile(script, os.path.join(dist_dir, script)) #copy original script

#create a loader stub
#load the zip file with the shared info into sys.path
#set sys path to the temp dir + zip file
#the PATH environment is also set, so that the DLLs can be loaded
#it's added as first path to reduce problems in the DLL hell
#__file__ is set to the users script name instead of the loaders
#as much as possible is cleaned up just before running the users script
file(os.path.join(dist_dir, '_pyco_loader.py'), 'w').write("""
import sys
sys.path.append(%(zipfile)r)
import os

os.environ['PYTHONHOME'] = os.path.abspath(os.curdir)
sys.prefix = os.environ['PYTHONHOME']
sys.path = [os.path.join(os.environ['PYTHONHOME'], %(zipfile)r), os.environ['PYTHONHOME']]
os.environ['PATH'] = os.environ['PYTHONHOME'] + ';' + os.environ['PATH']

os.chdir(os.environ['PYCOSTARTDIR'])
__file__ = os.path.join(os.environ['PYTHONHOME'], %(script)r)
del sys, os

execfile(__file__)
""" % vars())


#make single file exe
if windows:
    pycoutil.CreateBundle('pycostub_w.exe', exefile, dist_dir)
else:
    pycoutil.CreateBundle('pycostub.exe', exefile, dist_dir)

#test output
pycoutil.DumpBundle(exefile)
