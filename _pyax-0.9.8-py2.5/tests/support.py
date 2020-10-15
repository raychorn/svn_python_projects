import logging, logging.config
from random import choice
import sys

from pyax.connection import Connection
from pyax.exceptions import NoConnectionError

class TestSession:
    """
    Singleton containing an apex connection for use across the test suite
    (aside from connection tests, of course)
    """
    _shared_state = {}
    
    @classmethod
    def bootstrap(cls, username, password, token=None):
        tsession = TestSession()
        tsession.username = username
        tsession.password = password
        tsession.token = token
        tsession.sfdc = Connection.connect(username, password, token)
        return tsession

    
    def __init__(self):
        self.__dict__ = self._shared_state
        
    def cleanup(self):
        queryString = "select Id, casenumber from Case where Subject like '%Test Create Case Subject%'"
        queryResultBatch = self.sfdc.query(queryString)
        deleteResult = queryResultBatch.delete()
        return

class TestData:
    @staticmethod
    def gen_cases(number):
        count = 0
        cases = []
        origin_list = ['Email', 'Phone', 'Web']
        status_list = ['New','Working','Escalated']
        priority_list = ['Low','Medium','High']
        desc_list = ['Hommina\nhommina hommina',
                     'Bippity\nboppity boo!',
                     'Tangible\nBicycle Fruit',
                     'Psitticula\nAlexandri Fasciata',
                     'Far out in\nthe uncharted backwaters']

        while len(cases) < number:
            subject = "!@#$%% Test Create Case Subject %s" %(len(cases) + 1)
            cases.append({'Subject': subject,
                          'Status': choice(status_list),
                          'Origin': choice(origin_list),
                          'Description': choice(desc_list),
                          'Priority': choice(priority_list)})

        return cases


class Mock(object):

    def __init__(self, return_value=None):
        self.called = False
        self.call_count = 0
        self.call_args = None
        self.call_args_list = []
        self.return_value = return_value

    def __call__(self, *args, **kwargs):
        self.called = True
        self.call_count += 1
        self.call_args = (args, kwargs)
        self.call_args_list.append(self.call_args)

        if callable(self.return_value):
            return self.return_value()
        else:
            return self.return_value

