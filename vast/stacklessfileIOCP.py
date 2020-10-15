#
# Stackless Asynchronous file module:
#
# Author:Richard Tew (IOCP.py)
#        Carlos E. de Paula <carlosedp@gmail.com>
#
# This module has been heavily based on Richard Tew's work on IOCP.py
# Here the manager runs in a tasklet and write function works expectdly.
# I have added a sleep function like the one found on Ed Faulkner as a
# convenience if you dont have one implemented.
#
# This code was written to serve as an example of Stackless Python usage.
# Feel free to email me with any questions, comments, or suggestions for
# improvement.
#
# This is an asynchronous file class in order to have a file module replacement
# that uses channels and a windows async API to allow its methods to
# block just the calling tasklet not the entire interpreter.
#
#
#----------------------------------------------------------------------------

# On your stackless apps, use these 2 lines below
from vyperlogix.stackless.stacklessfileIOCP import stacklessfile as file
from vyperlogix.stackless.stacklessfileIOCP import mng
open = file

if __name__ == '__main__':
    import time
    import glob
    import os
    stdfile = file

    #file = stacklessfile
    #open = file
    sleep = mng.sleep
    
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
    newfile = stdfile('test-small.txt','w')
    for x in xrange(10000):
        newfile.write(str(x))
    newfile.close()

    newfile2 = stdfile('test-big.txt','w')
    for x in xrange(500000):
        newfile2.write(str(x))
    newfile2.close()

    # Launching tasklets to perform the file copy
    for i in xrange(1,11):
        stackless.tasklet(copyfile)(i, 'test-big.txt','big%s.txt' % i)

    for i in xrange(1,21):
        stackless.tasklet(copyfile)(i, 'test-small.txt','sm%s.txt' % i)

    def sl(s):
        st = time.time()
        print "Sleeping for %s seconds" % s
        sleep(s)
        print "returned %s seconds later (real: %s)" % (s, time.time()-st)
        
    #stackless.tasklet(sl)(3)

    st = time.time()
    stackless.run()
    print "Total time is %s seconds." % (time.time() - st)

    # Cleanup all test files used
    for f in glob.glob('test*.txt'):
        os.unlink(f)
    for f in glob.glob('sm*.txt'):
        os.unlink(f)
    for f in glob.glob('big*.txt'):
        os.unlink(f)
