import os
import zipfile

_files = [os.path.join('_code',f) for f in os.listdir('_code') if f.split('.')[-1] == 'py' ]

_mycode_zip = 'mycode.zip'
_mycode2_zip = '_code2.zip'
_mycode2a_zip = '_code2a.zip'

# To-Do:  Make a ZIP Maker that knows how to encrypt using a technique that allows the name of the file to seed the
#     encryption system.
def main():
    import os
    if (not any([os.path.exists(f) for f in _files])):
        print 'Missing one of %s' % _files
    else:
        zipOut = zipfile.PyZipFile(_mycode_zip,'w',zipfile.ZIP_DEFLATED)
        zipOut.debug = 3
        for f in _files:
            zipOut.writepy(f,f) # os.path.basename(f)
        zipOut.close()
    pass

#if (os.path.exists(_mycode_zip)):
    #os.remove(_mycode_zip)
    #pass

#main()

import sys
import traceback

#import imputil
#imputil._print_importers()

if (_mycode2a_zip not in sys.path):
    sys.path.append(_mycode2a_zip)
    can_test = False
    try:
        from _code2a import test
        can_test = True
    except ImportError, details:
        # To-Do: When there is an import error we unpack the ZIP 
        #    using the decryption technique then import the temp zip the normal way.
        #    Use an exit hook to make sure we clean-up when done.
        print 'ERROR due to "%s".' % details
        traceback.print_exc()
    if (can_test):
        test.test()
    else:
        print 'Cannot run test().'
    pass
