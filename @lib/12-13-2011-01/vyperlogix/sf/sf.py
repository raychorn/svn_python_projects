from vyperlogix.classes.CooperativeClass import Cooperative
from vyperlogix.hash import lists

import logging

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName

from vyperlogix.classes import SmartObject

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR  DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

BAD_INFO_LIST = [None, [], [{}], {}, '', 'fail', 'warn']

class SalesForceBaseQuery(Cooperative):
    def __init__(self,username,password):
        self.__username__ = username
        self.__password__ = password
        self.__sfdc__ = None

	from pyax.connection import Connection
	from pyax.exceptions import ApiFault
        try:
            self.__sfdc__ = Connection.connect(self.username, self.password)
            return True
        except AttributeError, details:
	    from vyperlogix.misc import _utils
	    info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        except ApiFault, details:
	    from vyperlogix.misc import _utils
	    info_string = _utils.formattedException(details=details)
            print >>sys.stderr, info_string
        return False

    def dictFromSOQL(self, ret):
        d = lists.HashedLists2()
        try:
            for k in ret.keys():
                v = ret[k]
                for vk in v.keys():
                    d[vk] = v[vk]
        except Exception, details:
	    from vyperlogix.misc import _utils
	    info_string = _utils.formattedException(details=details)
            logging.warning(info_string)
        return d

    def get_username(self):
        return self.__username__

    username = property(get_username)

    def get_password(self):
        return self.__password__

    password = property(get_password)

    def get_sfdc(self):
        return self.__sfdc__

    sfdc = property(get_sfdc)

class SalesForceQuery(Cooperative):
    def __init__(self,sfdc):
        '''This object connects with any other object that holds an sfdc object.'''
        try:
            self.__sfdc__ = sfdc.sfdc
        except:
            self.__sfdc__ = sfdc
        self.__lastError__ = ''

    def sfdc():
        doc = "sfdc property"
        def fget(self):
            return self.__sfdc__
        def fset(self, sfdc):
            self.__sfdc__ = sfdc
        return locals()
    sfdc = property(**sfdc())
    
    def lastError():
        doc = "lastError property"
        def fget(self):
            return self.__lastError__
        return locals()
    lastError = property(**lastError())
    
    def sf_query(self,soql,callback=None):
	from pyax.exceptions import ApiFault
	try:
	    ret = self.sfdc.queryAll(soql,callback=callback)
	    return ret
	except ApiFault, details:
	    from vyperlogix.misc import _utils
	    info_string = _utils.formattedException(details=details)
	    self.__lastError__ = info_string
	return None

    def contains_sf_objects(self,objects):
	try:
	    return False if any([( item.has_key('done') and item.has_key('size') ) for item in objects]) else True
	except:
	    pass
	return True if (objects is not None) else False
    
    def getObjectsFromSOQL(self,soql,callback=None,useRealObjects=True):
        try:
            ret = self.sf_query(soql,callback=callback)
            if (ret not in BAD_INFO_LIST):
                objects = []
                for k in ret.keys():
                    v = ret[k]
                    if (not useRealObjects):
                        val = lists.copyAsDict(v)
                        objects.append(val.asDict())
                    else:
                        objects.append(v)
		if (not self.contains_sf_objects(objects)):
		    objects = [SmartObject.SmartObject(objects[0])]
                return objects
        except Exception, details:
	    from vyperlogix.misc import _utils
	    info_string = _utils.formattedException(details=details)
	    self.__lastError__ = info_string

        return None

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
