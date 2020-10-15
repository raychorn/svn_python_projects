import unittest

from pyax.beatbox import SoapFaultError

from pyax.exceptions import ApiFault
from pyax.sobject.metadata import Metadata
from pyax.datatype.apexdatetime import ApexDatetime
from pyax.collections.clist import clist
from pyax.connection import Connection
from pyax.context import Context
from pyax.unpackomatic import Unpackomatic

from support import TestSession, Mock

import types
import datetime
from pprint import pprint


class Connection_test(unittest.TestCase):

    def setUp(self):
        self.tsession = TestSession()
        self.sfdc = self.tsession.sfdc

    def testLogin(self):
        """Connection constructor should succeed with good credentials"""
        try:
            sfdc = Connection.connect(self.tsession.username,
                                      self.tsession.password,
                                      self.tsession.token)
        except SoapFaultError, f:
            self.fail('login call returned fault: %s' %f)
        except Exception, e:
            self.fail('login call raised exception: %s' %e)
            pass

        return

    def testInvalidSession(self):
      sfdc = Connection.connect(self.tsession.username,
                                self.tsession.password,
                                self.tsession.token)

      #invert the session id to invalidate it
      original_session_id = sfdc.svc.sessionId
      invalid_session_id = ''.join(reversed(original_session_id))
      sfdc.svc.sessionId = invalid_session_id

      self.assertNotEqual(sfdc.svc.sessionId, original_session_id)
      sfdc.getServerTimestamp()

      # pyax should have re-logged in to "heal" the invalidated session Id
      self.assertNotEqual(sfdc.svc.sessionId, invalid_session_id)

      return


    def testFailLogin(self):
        """Connection constructor should raise an INVALID_LOGIN fault when
        logging in with bad credentials"""
        wrongPassword = '%sZZ' %self.tsession.password

        try:
            sfdc = Connection.connect(self.tsession.username,
                                      wrongPassword,
                                      self.tsession.token)
        except ApiFault, f:
            self.assertEqual(f.exception_code, 'INVALID_LOGIN')
        except Exception, e:
            self.fail('login call with bad credentials raised an exception other than an ApiFault: %s' %e)
        else:
            self.fail('login call with bad credentials did not raise a fault at all')

        return

    def testCxnUserInfo(self):
        """ Test that connection object got populated with user information """
        ui = self.sfdc.user_info

        self.assert_(type(ui) == types.DictType)
        self.assert_(len(ui) > 0)
        self.assert_(ui.has_key('userFullName'))
        self.assert_(ui.has_key('userTimeZone'))
        self.assert_(ui.has_key('roleId'))
        self.assert_(ui.has_key('profileId'))
        return

    def testGetServerTimestamp(self):
        """ Ensure that getServerTimestamp returns a datetime object """
        ts = self.sfdc.getServerTimestamp()
        self.assert_(isinstance(ts, ApexDatetime))
        return

#    def testSetPassword(self):
#        pass
#
#    def testResetPassword(self):
#        pass
#
    def test_CxnGlobalData(self):
        """ Test that connection object got populated with describeGlobal information """
        dg = self.sfdc.describe_global_response
        self.assert_(type(dg) == types.DictType)
        self.assert_(len(dg) > 0)
        self.assert_(dg.has_key('types'))
        self.assert_(isinstance(dg.get('types'), clist))
        return

    def test_describeSObject(self):
        do = self.sfdc.describeSObject('Account')
        self.failUnless(isinstance(do, Metadata),
                        "test_DescribeSObject did not return an sobject.Metadata instance")
        pass

    def test_describeSObject_list(self):
        self.failUnlessRaises(ValueError, self.sfdc.describeSObject, ['Account',])
        pass

    def test_describeSObjects(self):
        objects = ['Account', 'Case', 'Contact']
        do = self.sfdc.describeSObjects(objects)
        self.failUnless(type(do) == types.DictType,
                        "test_DescribeSObjects did not return a Map")
        objects_described = do.keys()
        objects_described.sort()
        self.failUnless(objects_described == objects,
                        "Keys of described objects do not match objects requested")
        pass

    def test_describeSObjects_string(self):
        do = self.sfdc.describeSObjects('Account')
        self.failUnless(isinstance(do, Metadata),
                        "describeSObjects on a single object type as a String did not return an sobject.Metadata instance")
        pass

    def test_describeSObjects_list(self):
        do = self.sfdc.describeSObjects(['Account',])
        self.failUnless(type(do) == types.DictType,
                        "describeSObjects on a single object type as a List did not return a Map")
        pass

    def testDescribeTabs(self):
        """ Testing the describeTabs call """
        tabs = self.sfdc.describeTabs()
        self.assert_(type(tabs) == types.DictType)
        self.assert_(type(tabs[tabs.keys()[0]]) == types.DictType)
        return

    def testLogout(self):
        """ testing the logout call """
        original_session_id = self.sfdc.svc.sessionId
        self.sfdc.logout()
        self.sfdc.getServerTimestamp()
        self.assertNotEqual(self.sfdc.svc.sessionId, original_session_id)
        return
        
    def testInvalidateSessions(self):
        """ testing the invalidateSessions call """
        original_session_id = self.sfdc.svc.sessionId
        invalidate_result = self.sfdc.invalidateSessions([original_session_id])
        self.sfdc.getServerTimestamp()
        self.assertNotEqual(self.sfdc.svc.sessionId, original_session_id)
        return
    pass
    

class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.cnx = Connection(Context())
        self.ca = Mock()
        self.cnx._callApex = self.ca

        self.return_value = object()

    def testQueryTemplateSync(self):
        """Test _query_template method with sync (regular) call"""
        self.pqr = Mock(self.return_value)
        self.cnx._Connection__processQueryResult = self.pqr

        result = self.cnx._query_template('query', 'query_string', None, None)
        assert result is self.return_value
        assert self.pqr.called
        assert self.ca.call_args[0] == (self.cnx.svc.query, 'query_string')

    def testQueryTemplateAsync(self):
        """Test _query_template method with asynchronous call"""
        self.paqr = Mock()
        self.cnx._Connection__processAsyncQueryResult = self.paqr

        callable = object()

        result = self.cnx._query_template('queryAll', 'query_string', callable, None)
        assert self.ca.call_args[0][0] == self.cnx.svc.queryAll
        assert self.ca.call_args[0][1] == 'query_string'

        query_result = object()
        self.ca.call_args[1]['callback'](query_result)
        assert self.paqr.call_args[0] == (query_result, callable, None)

    def testQuery(self):
        """Check that query is properly calling _query_template."""
        qt = Mock()
        self.cnx._query_template = qt
        callback = object()
        self.cnx.query('query_string', callback)

        assert qt.call_args[0] == ('query', 'query_string', callback, None)

    def testQueryAll(self):
        """Check that queryAll is properly calling _query_template."""
        qt = Mock()
        self.cnx._query_template = qt
        callback = object()
        self.cnx.queryAll('query_string', callback)

        assert qt.call_args[0] == ('queryAll', 'query_string', callback, None)

    def patchUnpackQueryResult(self):
        unpackResults = iter([([1], False, 'locator', 0),
                              ([2], True,  'locator', 0)])
        self.cnx._unpackQueryResult = Mock(return_value=unpackResults.next)

    def testProcessAsyncQueryResult(self):
        """Check internals of __processAsyncQueryResult."""
        self.patchUnpackQueryResult()
        query_result_batch = object()
        self.cnx._Connection__resultToObject = Mock(query_result_batch)

        callback = Mock()
        self.cnx._Connection__processAsyncQueryResult(object(), callback, None)

        # It must be done manually, normally it would be done by Twisted
        self.ca.call_args[1]['callback'](object())

        assert self.cnx._unpackQueryResult.call_count == 2
        assert callback.call_args[0] == (query_result_batch,)

    def testProcessQueryResult(self):
        """Check internals of __processQueryResult."""
        self.patchUnpackQueryResult()
        query_result_batch = object()
        query_result = {}
        self.cnx._Connection__resultToObject = Mock(query_result_batch)
        self.cnx._Connection__queryMore = Mock(query_result
                                               )
        result = self.cnx._Connection__processQueryResult(object)

        assert result is query_result_batch
        assert self.cnx._unpackQueryResult.call_count == 2


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Connection_test))
    suite.addTest(unittest.makeSuite(ConnectionTestCase))
    return suite

if __name__ == "__main__":
    unittest.main()
