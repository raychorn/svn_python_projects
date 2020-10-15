#
# Stackless compatible file module:
#
# Author: Carlos E. de Paula <carlosedp@gmail.com>
#
# This code was written to serve as an example of Stackless Python usage.
# Feel free to email me with any questions, comments, or suggestions for
# improvement.
#
# This wraps the file class in order to have a file module replacement
# that uses channels and a threadpool to allow calls to it to
# block just the calling tasklet until a delayed event occurs.
#
# Not all methods of the file module are wrapped as unbloking by this file.
# Examples of it in use can be seen at the bottom of this file.
#

# In the app, import stacklessfile class directly like the example below
#
import stackless
from vyperlogix.stackless.stacklessfileThreadPool import stacklessfile as file
from vyperlogix.stackless.stacklessfileThreadPool import stdfile
open = file

if __name__ == '__main__':
    import time
    import glob
    import os

    # Function to copy a file
    def copyfile(who, infile, out):
        st = time.time()
        f1 = file(infile, 'rb')
        f2 = file(out, 'wb')
        print "%s started reading %s ..." % (who, infile)
        a = f1.read()
        print "%s started writing %s -> %s ..." % (who, infile, out)
        f2.write(a)
        f1.close()
        f2.close()
        print "Finished tasklet %s (%s) in %s" % (who, infile, time.time()-st)

    # Creating two dummy files
    newfile = stdfile('test.txt','w')
    for x in xrange(10000):
        newfile.write(str(x))
    newfile.close()

    newfile2 = stdfile('test2.txt','w')
    for x in xrange(500000):
        newfile2.write(str(x))
    newfile2.close()

    # Launching tasklets to perform the file copy
    for i in xrange(10):
        stackless.tasklet(copyfile)(i, 'test2.txt','x%s.txt' % i)

    for i in xrange(30):
        stackless.tasklet(copyfile)(i, 'test.txt','xx%s.txt' % i)

    st = time.time()
    stackless.run()
    print "Total time is %s seconds." % (time.time() - st)

    # Cleanup all test files used
    for f in glob.glob('x*.txt'):
        try:
            os.unlink(f)
        except WindowsError, e:
            pass
    os.unlink('test.txt')
    os.unlink('test2.txt')
