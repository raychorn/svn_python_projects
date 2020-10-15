__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""
def get_twitter_api(username,password):
    import twitter
    vers = '1.0'
    prod = 'Vyper-Twitz(tm)'
    xml = 'http://media.vyperlogix.com/twitter/client/vyper-twitz.xml'
    api = twitter.Api(username=username, password=password, request_headers={'X-Twitter-Client':prod,
                                                                             'X-Twitter-Client-Version':vers,
                                                                             'X-Twitter-Version':vers,
                                                                             'X-Twitter-Client-URL':xml,
                                                                             'X-Twitter-URL':xml
                                                                             })
    api.SetUserAgent('%s %s' % (prod,vers))
    api.SetXTwitterHeaders(prod,xml,vers)
    return api

def twitter_post_update(username,password,message):
    api = get_twitter_api(username,password)
    status = api.PostUpdate(message)

def twitter_post_update_simulated(username,password,message):
    l = len(message)
    if (l <= 140):
        print 'TWITTER (%s) :: %s' % (username,message)
    #else:
        #raise AttributeError('Your message is too long.  Must be less than 140 chars but yours is %d.' % (l))

from vyperlogix.classes.CooperativeClass import Cooperative
class Tweepy(Cooperative):
    @classmethod
    def update_status(cls,username,password,status):
        from django.utils import simplejson as json
        import tweepy
        auth = tweepy.BasicAuthHandler(username, password)
        bot = tweepy.API(auth)
        bot.update_status(str(unicode(status).encode("utf-8")))

