from vyperlogix.misc import _utils

import stackless
if (_utils.isBeingDebugged):
    import pdb

tasklet = stackless.tasklet
def new_call(self, *args, **kwargs):
    f = self.tempval
    def new_f(old_f, args, kwargs):
        print "wrapper.start", args, kwargs
        old_f(*args, **kwargs)
        print "wrapper.end"
    self.tempval = new_f
    tasklet.setup(self, f, args, kwargs)

tasklet.__call__ = new_call

def test(*args, **kwargs):
    if (_utils.isBeingDebugged):
        pdb.set_trace()
    print "test.enter", args, kwargs
    stackless.schedule()
    print "test.exit"

tasklet(test)(1,2,3, x=1, y=2, z=3)
stackless.run()