from sys import stdout,stderr
from pdb import set_trace as bp

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

class DecoTrace(object):
    '''
    Decorator class with no arguments

    This can only be used for functions or methods where the instance
    is not necessary
    
    '''

    def __init__(self, f):
        self.f = f

    def _showargs(self, *fargs, **kw):
        print >> stderr, 'T: enter %s with args=%s, kw=%s' % (self.f.__name__, str(fargs), str(kw))

    def _aftercall(self, status):
        print >> stderr, 'T: exit %s with status=%s' % (self.f.__name__, str(status))

    def __call__(self, *fargs, **kw):
        '''pass just function arguments to wrapped function'''

        self._showargs(*fargs, **kw)
        ret=self.f(*fargs, **kw)
        self._aftercall(ret)
        return ret

    def __repr__(self):
        return self.f.func_name


class DecoTraceWithArgs(object):
    '''decorator class with ARGUMENTS

       This can be used for unbounded functions and methods.  If this wraps a
       class instance, then extract it and pass to the wrapped method as the
       first arg.
    '''
    
    def __init__(self, *dec_args, **dec_kw):
        '''The decorator arguments are passed here.  Save them for runtime.'''
        self.dec_args = dec_args
        self.dec_kw = dec_kw

        self.label = dec_kw.get('label', 'T')
        self.fid = dec_kw.get('stream', stderr)

    def _showargs(self, *fargs, **kw):

        print >> self.fid, \
              '%s: enter %s with args=%s, kw=%s' % (self.label, self.f.__name__, str(fargs), str(kw))
        print >> self.fid, \
              '%s:   passing decorator args=%s, kw=%s' % (self.label, str(self.dec_args), str(self.dec_kw))

    def _aftercall(self, status):
        print >> self.fid, '%s: exit %s with status=%s' % (self.label, self.f.__name__, str(status))
    def _showinstance(self, instance):
        print >> self.fid, '%s: instance=%s' % (self.label, instance)
        
    def __call__(self, f):
        def wrapper(*fargs, **kw):
            '''
              Combine decorator arguments and function arguments and pass to wrapped
              class instance-aware function/method.

              Note: the first argument cannot be "self" because we get a parse error
              "takes at least 1 argument" unless the instance is actually included in
              the argument list, which is redundant.  If this wraps a class instance,
              the "self" will be the first argument.
            '''

            self._showargs(*fargs, **kw)

            # merge decorator keywords into the kw argument list
            kw.update(self.dec_kw)

            # Does this wrap a class instance?
            if (fargs and getattr(fargs[0], '__class__', None)):

                # pull out the instance and combine function and
                # decorator args
                instance, fargs = fargs[0], fargs[1:]+self.dec_args
                self._showinstance(instance)

                # call the method
                ret=f(instance, *fargs, **kw)
            else:
                # just send in the give args and kw
                ret=f( *(fargs + self.dec_args), **kw)

            self._aftercall(ret)
            return ret

        # Save wrapped function reference
        self.f = f
        wrapper.__name__ = f.__name__
        wrapper.__dict__.update(f.__dict__)
        wrapper.__doc__ = f.__doc__
        return wrapper
