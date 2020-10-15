import sys, traceback

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class PrivateMethod(object):
    '''
    Make Method Private, well sort of, makes method inaccessible to module level use but allows unrestricted use from any context other than "module".
    To-Do:  Refine the method for the determination as to which specific context the caller of the private method is coming from.
    '''

    def __init__(self, f, *dec_args, **dec_kw):
        self.f = f

    def __call__(self, *fargs, **kw):
	from vyperlogix.misc import _utils
	ctx = _utils.callersContext()
	if (self.f.func_name in ctx.co_names) and (str(ctx.co_name).find('module') == -1):
	    ret=self.f(*fargs, **kw)
	    return ret
	else:
	    raise ReferenceError('Cannot issue a call to a private method (%s) from outside the context of the class where this method is defined.' % (self.f.func_name))

    def __repr__(self):
        return self.f.func_name

class PrivateTest:
    def __init__(self):
	pass
    
    def test(self):
	self.__private__('method1','2',3,4)
	pass
    
    def test2(self):
	self.method2(4,5)
	pass
    
    @PrivateMethod
    def method2(*args,**kw):
	print 'method2 args=%s, kw=%s' % (str(args),str(kw))
	    
    def __private__(self,entry,*args,**kwargs):
	from vyperlogix.misc import _utils
	
	def method1(args,kw):
	    print 'method1 args=%s, kw=%s' % (args,kw)
	    
	try:
	    ctx = _utils.callersContext()
	    if (ctx.co_name in dir(self)):
		x = eval('%s(args,kwargs)' % entry)
		return x
	except:
	    from vyperlogix import misc
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    logging.warning('(%s) :: Cannot call private method named "%s"...%s' % (misc.funcName(),entry,info_string))
	raise ReferenceError('Cannot issue a call to a private method (%s) from outside the context of the class where this method is defined.' % (entry))

class PrivateTest2:
    def __init__(self):
	pass
    
    def test2(self):
	pt = PrivateTest()
	pt.method2(1,2,3,4)
	pass
    
if __name__ == '__main__':
    pt2 = PrivateTest2()
    pt2.test2()
    
    pt = PrivateTest()
    pt.test2()
    pt.method2(1,2)
    pt.test()
    pt.__private__('method1','1',2,3)
