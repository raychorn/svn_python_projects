from time import strftime,gmtime,time
import urllib2
import hmac
import hashlib
import base64
import string

def publishAmazonSnsMsg(Subject,TopicArn,Message,AWSAccessKeyId,privatekey):
    #http://docs.amazonwebservices.com/AWSSimpleQueueService/2008-01-01/SQSDeveloperGuide/
    amzsnshost = 'sns.us-east-1.amazonaws.com'
    params = {'Subject' : Subject,
              'TopicArn' : TopicArn,
              'Message' :Message,
              'Timestamp' : strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime(time())),
              'AWSAccessKeyId' : AWSAccessKeyId,
              'Action' : 'Publish',
              'SignatureVersion' : '2',
              'SignatureMethod' : 'HmacSHA256',
              }

    cannqs=string.join(["%s=%s"%(urllib2.quote(key),urllib2.quote(params[key], safe='-_~')) \
                        for key in sorted(params.keys())],'&')
    string_to_sign=string.join(["GET",amzsnshost,"/",cannqs],'\n')
    sig=base64.b64encode(hmac.new(privatekey,string_to_sign,digestmod=hashlib.sha256).digest())
    url="http://%s/?%s&Signature=%s"%(amzsnshost,cannqs,urllib2.quote(sig))

    try:
        return urllib2.urlopen(url).read()
    except urllib2.HTTPError, exception:
        return "Error %s (%s):\n%s"%(exception.code,exception.msg,exception.read())