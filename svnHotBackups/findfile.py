import os

from vyperlogix.misc import _utils

fp = _utils.searchForFileNamed('svnserve.*',top='%s' % (os.sep))
print 'fp is "%s".' % (fp)