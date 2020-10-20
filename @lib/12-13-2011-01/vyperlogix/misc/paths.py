__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def _findUsingPath(t,p):
    import time,Queue
    from vyperlogix import misc
    from vyperlogix.misc import threadpool
    
    Qs = {}
    Q = threadpool.ThreadQueue(10)
    q = Queue.Queue(10)
    
    @threadpool.threadify(Q)
    def do_scan_for_file(target,top,statsDict,topdown=True):
	for root, dirs, files in os.walk(top,topdown=topdown):
	    for f in files:
		if (f.split(os.sep)[-1] == target) or (f.find(target) > -1):
		    p = os.sep.join([root,f])
		    print '(+++).do_scan_for_file().1 q.put_nowait(%s)' % (p)
		    q.put_nowait(p)
		    print '(+++).do_scan_for_file().2 del statsDict["%s"]' % (top)
		    del statsDict[top]
		    return
	print '(+++).do_scan_for_file().3 del statsDict["%s"]' % (top)
	del statsDict[top]
    
    ptoks = p.split(';')
    if (len(ptoks) == 1):
        ptoks = p.split(':')
    ptoks = [p for p in ptoks if (len(p) > 0)]
    for i in xrange(len(ptoks)):
	f = ptoks[i]
	if (f.startswith('%') and f.endswith('%')):
	    f = f.replace('%','')
	    f = os.environ.get(f,None)
	    ptoks[i] = f
    for drive in [d for d in getCurrentWindowsLogicalDrives()]:
	try:
	    for dir in [os.path.join(drive,tt) for tt in os.listdir(drive) if (not tt.startswith('$')) and (tt.find('Program Files') > -1) and (os.path.isdir(os.path.join(drive,tt)))]:
		ptoks.append(dir)
	except WindowsError:
	    pass
    ptoks = list(set(ptoks))
    for f in ptoks:
	if (misc.isStringValid(f)) and (os.path.exists(f)) and (os.path.isdir(f)):
	    Qs[f] = 1
	    do_scan_for_file(t,f,Qs)
    isDone = False
    while (not isDone):
	try:
	    p = q.get_nowait()
	except:
	    p = None
	print '(+++)._findUsingPath().1 Sleeping on "%s".' % (p)
	time.sleep(1)
	if (misc.isStringValid(p)):
	    Q.setIsRunning = False
	    print '(+++)._findUsingPath().2 Return "%s".' % (p)
	    return p
	isDone = (len(Qs) == 0)
    print '(+++)._findUsingPath().3 Return None.'
    Q.setIsRunning = False
    return None

