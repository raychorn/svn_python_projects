import os, sys

import requests

from vyperlogix.boto import s3, __passphrase__, get_aws_credentials

from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedLists2
from vyperlogix.classes import SmartObject

from vyperlogix.misc.ObjectTypeName import typeClassName

from vyperlogix.requests import download_file

__bucket_name__ = 'vyperlogix-business-history-08-11-2013a'

def callback(num,total):
    print 'PROGRESS: %d of %d.' % (num,total)

if (__name__ == '__main__'):
    from boto.s3 import connection
    from boto.s3 import key
    soCredentials = get_aws_credentials(filename='./credentials_secure.txt')
    aConnection = connection.S3Connection(aws_access_key_id=soCredentials.AWSAccessKeyId, aws_secret_access_key=soCredentials.AWSSecretKey)

    if (0):
        buckets = aConnection.get_all_buckets()
        for bucket in buckets:
            print '%s %s' % (bucket.name,bucket.creation_date)

    bucket = aConnection.get_bucket(__bucket_name__)
    print bucket
    if (bucket):
        cnt = 0
        toks = os.path.abspath('.').split(os.sep)[0:3]
        if ('Volumes' not in toks):
            toks = toks[0:2]
        toks.append(__bucket_name__)
        base = os.sep.join(toks)
        for item in bucket.get_all_versions():
            if (not str(item.name).endswith('/')):
                #print item.name

                key = bucket.get_key(item.name)
                if (key and (not key.ongoing_restore)):
                    print 'Restoring: %s' % (item.name)
                    key.restore(days=100)
                else:
                    print '\n%s: %s\n' % ('UNKNOWN-KEY' if (not key) else 'RESTORING' if (key.ongoing_restore) else 'RESTORED',item.name)

                if (0):
                    if ('DeleteMarker' in typeClassName(item).split('.')):
                        key = bucket.get_key(item.name)
                        if (key and (not key.ongoing_restore)):
                            print 'Restoring: %s' % (item.name)
                            key.restore(days=100)
                        else:
                            print '\n%s: %s\n' % ('UNKNOWN-KEY' if (not key) else 'RESTORING' if (key.ongoing_restore) else 'RESTORED',item.name)
                    else:
                        try:
                            print 'Downloading: %s' % (item.name)
                            url = item.generate_url(3600)
                            fname = os.sep.join([base,'@S3',item.name])
                            _utils.makeDirs(fname)
                            download_file(url,fpath=fname)
                            cnt += 1
                            if (cnt % 10) == 0:
                                print
                        except Exception, ex:
                            print _utils.formattedException(details=ex)
        print
        
    