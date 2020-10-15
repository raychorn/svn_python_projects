from vyperlogix.misc import _utils

import stackless
if (_utils.isBeingDebugged):
    import pdb

def testTasklet(x):
    if (_utils.isBeingDebugged):
        pdb.set_trace()
    print x, "hello"
    stackless.schedule()
    print "world"


class Main(object):
    def __init__(self):
        pass

    def execute(self):
        stackless.tasklet(testTasklet)("andrew")
        stackless.tasklet(testTasklet)("ted")

        while stackless.getruncount() > 1:
            stackless.schedule()

main = Main()
main.execute()