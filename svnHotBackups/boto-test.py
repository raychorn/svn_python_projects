import os, sys

import re

from boto.s3 import connection

from vyperlogix.cfg import config

from vyperlogix.misc import _utils

from vyperlogix.lists import ListWrapper
from vyperlogix.misc import ioTimeAnalysis

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

__bucket_name__ = '__vyperlogix_svn_backups__'

__boto_cfg__ = 'boto.cfg'

__host__ = 's3.amazonaws.com'

if (__name__ == '__main__'):

    ioTimeAnalysis.initIOTime(__name__)
    ioTimeAnalysis.ioBeginTime(__name__)

    if (_utils.isUsingWindows):
        __boto_cfg__ = os.path.abspath('./%s' % (__boto_cfg__))
    elif (_utils.isUsingLinux):
        __boto_cfg__ = os.path.abspath('/etc/%s' % (__boto_cfg__))
    else:
        print 'WARNING: Cannot locate "%s" "for your system.' % (__boto_cfg__)
    so = config.reader(__boto_cfg__)

    from boto.s3 import connection
    aConnection = connection.S3Connection(host=__host__,aws_access_key_id=so.Credentials.aws_access_key_id, aws_secret_access_key=so.Credentials.aws_secret_access_key)

    bucket = aConnection.get_bucket(__bucket_name__)
    
    for key in bucket.get_all_keys():
        print key.generate_url(10,encrypt_key=True)
        
    aConnection.close()

    ioTimeAnalysis.ioEndTime(__name__)
    ioTimeAnalysis.ioTimeAnalysisReport(fOut=sys.stdout)