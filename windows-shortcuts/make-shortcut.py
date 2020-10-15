import os, sys
from vyperlogix.misc import _utils
from vyperlogix.win import folders
from vyperlogix.win import windowsShortcuts

def does_nothing(root):
    return True

def requires_vcvatime(root):
    if (_isVerbose):
	print 'DEBUG: requires_vcvatime --> %s' % (root)
    return root.find('vcva-time') > -1

__required_links__ = {
    'start-hpcs.cmd':{'target':r'C:\workspaces\voyage\start-hpcs.cmd','start-in':r'C:\workspaces\voyage','top':r'C:\workspaces','lambda':does_nothing},
    'start-server.cmd':{'target':r'C:\workspaces\voyage\start-server.cmd','start-in':r'C:\workspaces\voyage','top':r'C:\workspaces','lambda':does_nothing},
    'start-uim.cmd':{'target':r'C:\workspaces\voyage\start-uim.cmd','start-in':r'C:\workspaces\voyage','top':r'C:\workspaces','lambda':does_nothing},
    'stop-all.cmd':{'target':r'C:\workspaces\voyage\stop-all.cmd','start-in':r'C:\workspaces\voyage','top':r'C:\workspaces','lambda':does_nothing},
    'vcva-time':{'target':r'C:\Program Files (x86)\_utils\vcva-time\run.cmd','start-in':r'C:\workspaces\voyage','top':r'C:\Program Files (x86)','lambda':requires_vcvatime}
}

def locateFileByName(likethis,top='c:/',func=does_nothing):
    found = []
    for root, dirs, files in os.walk(top):
	if (root.find('.svn') == -1) and (func(root)):
	    if (_isVerbose):
		print "%s..." % (root),
	    for f in files:
		if (str(f).lower() == str(likethis).lower()):
		    found.append(os.sep.join([root,f]))
		    break
	    if (_isVerbose):
		print
    return found

def validate_required_link_targets(required):
    for k,v in required.iteritems():
	target = v.get('target',None)
	if (target):
	    fname = os.path.basename(target)
	    func = v.get('lambda',does_nothing)
	    top = v.get('top','C:\\')
	    found = (locateFileByName(fname,func=func) if (top is None) else locateFileByName(fname,top=top,func=func))
	    if (len(found) == 0):
		found = locateFileByName(fname,func=func)
		if (_isVerbose):
		    assert len(found) > 0, 'Check this out !!!'
	    v['target'] = found[0] if (len(found) > 0) else v['target']
	    v['start-in'] = os.path.dirname(v['target'])
	    top = v['start-in']
	    required[k] = v

def locateShortcut(likethis,top=folders.Desktop()):
    shortcuts = []
    for root, dirs, files in os.walk(top):
	for f in files:
	    if (_isVerbose):
		print f
	    if (f.find('.lnk') > -1):
		_fname = os.sep.join([root,f])
		_path = windowsShortcuts.getPathFromShortcut(_fname)
		fname = os.path.basename(_path[0])
		if (likethis.find(fname) > -1):
		    shortcuts.append([_fname,_path[0]])
    return shortcuts

def locateShortcuts(required,top=folders.Desktop()):
    missing_shortcuts = []
    for k,v in required.iteritems():
	target = v.get('target',None)
	if (target):
	    shortcuts = locateShortcut(target, top=top)
	    if (len(shortcuts) == 0):
		missing_shortcuts.append(k)
    return missing_shortcuts

if (__name__ == '__main__'):
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('-v', '--verbose', dest='verbose', help="verbose", action="store_true")
    
    options, args = parser.parse_args()
    
    _isVerbose = False
    if (options.verbose):
	_isVerbose = True
    
    __desktop__ = 'C:/@6/Desktop' if (_utils.isBeingDebugged) else folders.Desktop()
    validate_required_link_targets(__required_links__)
    missing = locateShortcuts(__required_links__,top=__desktop__)
    if (_isVerbose):
	print '='*40
	print missing
	print '='*40
    
    for item in missing:
	data = __required_links__.get(item,None)
	if (data):
	    print 'Creating shortcut for %s in %s.' % (item, __desktop__)
	    lnkPath = os.sep.join([__desktop__,item+'.lnk'])
	    targetPath = data.get('target',None)
	    workingPath = data.get('starts-in',None)
	    description = data.get('description',item)
	    iconLocation = data.get('icon',None)
	    if (1):
		windowsShortcuts.makeWindowsShortcut(lnkPath, targetPath, workingPath, description, iconLocation)
	    elif (0):
		import win32com.client
		ws = win32com.client.Dispatch("wscript.shell")
		scut = ws.CreateShortcut('run_idle.lnk')
		scut.TargetPath = '"c:/python27/python.exe"'
		scut.Arguments = '-m idlelib.idle'
		scut.Save()
    
