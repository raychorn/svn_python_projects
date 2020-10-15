import os, sys

import requests

from vyperlogix.boto import s3, __passphrase__, get_aws_credentials

from vyperlogix.misc import _utils
from vyperlogix.hash.lists import HashedLists2
from vyperlogix.crypto import blowfish
from vyperlogix.classes import SmartObject

from vyperlogix.requests import download_file

from vyperlogix import oodb

from vyperlogix import ssl

#__bucket_name__ = '__vyperlogix_svn_backups__'

__bucket_name__ = 'vyperlogix-business-history-08-11-2013a'

#__url__ = 'http://cdn-python.s3-website-us-east-1.amazonaws.com/credentials_secure.txt'

def callback(num,total):
    print 'PROGRESS: %d of %d.' % (num,total)

if (__name__ == '__main__'):
    #from vyperlogix.misc import GenPasswd
    #print GenPasswd.GenPasswd(length=128,chars=GenPasswd.chars_printable)

    #try:
        #_credentials_secure_ = ssl.fetch_from_web(__url__)
    #except Exception, ex:
        #_credentials_secure_ = None
        #info_string = _utils.formattedException(details=ex)
        #print >> sys.stderr, info_string

    #_credentials_secure_ = None
    #if (not _credentials_secure_) or (len(_credentials_secure_) == 0):
        #fname = os.path.abspath('./credentials.txt')
        #toks = list(os.path.splitext(fname))
        #toks[0] += '_secure'
        #fnameOut = ''.join(toks)
        #if (not os.path.exists(fnameOut)):
            #c = _utils.readBinaryFileFrom(fname)
            #f_out = open(fnameOut, mode='wb', buffering=1)
            #d = HashedLists2(fromDict=dict([tt.split('=') for tt in [t.strip() for t in c.split('\n')] if (len(tt) > 0)]))
            #dE = d.asDict(isCopy=True)
            #for k,v in dE.iteritems():
                #_k_ = oodb.strToHex(blowfish.encryptData(k, __passphrase__))
                #del dE[k]
                #_v_ = oodb.strToHex(blowfish.encryptData(v, __passphrase__))
                #dE[_k_] = _v_
                #print >>f_out, '%s=%s' % (_k_,_v_)
            #f_out.flush()
            #f_out.close()
            #dP = HashedLists2(fromDict=dE).asDict()
            #for k,v in dP.iteritems():
                #_k_ = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(k), __passphrase__))
                #dP[_k_] = _utils.ascii_only(blowfish.decryptData(oodb.hexToStr(v), __passphrase__))
                #del dP[k]
                #assert dP[_k_] == d[_k_], 'WARNING: Expected %s to match %s.' % (dP[_k_],d[_k_])
        #if (os.path.exists(fnameOut)):
            #soCredentials = get_aws_credentials(filename='./credentials_secure.txt')
        #else:
            #soCredentials = get_aws_credentials(url=__url__,filename=None)
    #else:
        #soCredentials = get_aws_credentials(url=__url__,filename=None)

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
        base = os.sep.join(toks)
        for item in bucket.get_all_versions():
            if (not str(item.name).endswith('/')):
                print item.name
                try:
                    url = item.generate_url(3600)
                    fname=base+item.name
                    _utils.makeDirs(fname)
                    download_file(url,fpath=fname)
                    cnt += 1
                    if (cnt % 10) == 0:
                        print
                except Exception, ex:
                    print _utils.formattedException(details=ex)
        print
        #aKey = key.Key(bucket=bucket,name='vyperlogix/__init__.pyc')
        #aKey.set_contents_from_filename(r'J:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01\vyperlogix\__init__.pyc')
        
    