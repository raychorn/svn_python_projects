import os

import sys
import time
import base64
import hmac
import mimetypes

import urllib2

from hashlib import sha1

try:
    from poster.streaminghttp import register_openers
    #print 'BEGIN:'
    #for f in sys.path:
        #print f
    #print 'END!'
except ImportError:
    print 'BEGIN:'
    for f in sys.path:
        print f
    print 'END!'
    sys.exit()
        

def read_data(file_object):
    while True:
        r = file_object.read(64 * 1024)

        if not r:
            break
        yield r

def upload_file(filename, bucket, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    length = os.stat(filename).st_size
    content_type = mimetypes.guess_type(filename)[0]
    resource = "/%s/%s" % (bucket, filename)

    url = "http://%s.s3.amazonaws.com/%s" % (bucket, filename)

    date = time.strftime("%a, %d %b %Y %X GMT", time.gmtime())

    sig_data = "PUT\n\n%s\n%s\nx-amz-acl:public-read\n%s" % (content_type, date, resource)
    signature = base64.encodestring(
        hmac.new(
            AWS_SECRET_ACCESS_KEY, sig_data, sha1).digest()).strip()

    auth_string = "AWS %s:%s" % (AWS_ACCESS_KEY_ID, signature)

    register_openers()
    input_file = open(filename, 'r')

    data = read_data(input_file)
    request = urllib2.Request(url, data=data)

    request.add_header('Date', date)
    request.add_header('Content-Type', content_type)

    request.add_header('Content-Length', '%s' % (length))
    request.add_header('Authorization', auth_string)

    request.add_header('x-amz-acl', 'public-read')
    request.get_method = lambda: 'PUT'

    urllib2.urlopen(request).read()

if (__name__ == "__main__"):
    # python streaming-s3.py filename bucket AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

    filename = sys.argv[1]
    bucket = sys.argv[2]

    AWS_ACCESS_KEY_ID = sys.argv[3]
    AWS_SECRET_ACCESS_KEY = sys.argv[4]

    upload_file(filename, bucket, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
