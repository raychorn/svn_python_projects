import sys
from vyperlogix.CooperativeClass import Cooperative
from vyperlogix.decorators.Property import Property
from pyax.connection import Connection
from pyax.exceptions import ApiFault
from vyperlogix import _utils
from vyperlogix.hash import lists
from vyperlogix.sf import sf

import logging

class SalesForceAuthentication(sf.SalesForceBaseQuery):
   def __init__(self,username,password):
      self.__isLoginSuccessful__ = False
      self.__user_record__ = lists.HashedLists2()
      
      self.isLoginSuccessful = super(SalesForceAuthentication, self).__init__(username,password)

      if (self.isLoginSuccessful):
         self.isLoginSuccessful = self.isUserMagmaAdmin()

   def isUserMagmaAdmin(self):
      rec = self.getUserRecord()
      if (rec):
         _userRoleName = rec['UserRole']['Name']
         return _userRoleName.find('Corp - Executive') > -1
      return False
   
   def getUserRecord(self): 
      soql = "Select u.Id, u.Username, u.Name, u.UserRoleId, u.UserRole.Id, u.UserRole.Name from User u WHERE u.Username = '%s'" % (self.username)
      ret = self.sfdc.query(soql)
      if ret in sf.BAD_INFO_LIST:
         msg ="Could not find any User Object(s) for %s.%s" % (self.__class__,_utils.funcName())
         logging.warning(msg)
      else:
         try:
            _key = ret.keys()[0]
            if (_key):
	       self.__user_record__ = self.dictFromSOQL(ret)
               return ret[_key]
         except:
	    exc_info = sys.exc_info()
	    info_string = '\n'.join(traceback.format_exception(*exc_info))
	    print >>sys.stderr, info_string
      return None

   @Property
   def userRecord():
      def fget(self):
         return self.__user_record__

   @Property
   def isLoginSuccessful():
      def fget(self):
         return self.__isLoginSuccessful__
      def fset(self,_bool):
         self.__isLoginSuccessful__ = _bool if (isinstance(_bool,bool)) else False

