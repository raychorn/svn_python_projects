"""Tests for asynchronous aspects of beatbox's methods."""
import unittest
import sys

from pyax.beatbox import NoTwistedInstalledError, SoapEnvelope
from pyax.context import Context


class TwistedImporter(object):

    def __init__(self, raiseException=False):
        self.raiseException = raiseException

    def find_module(self, fullname, path=None):
        if fullname == 'twisted':
            if self.raiseException:
                raise ImportError


class SoapEnvelopeTestCase(unittest.TestCase):

    def setUp(self):
        if 'twisted' in sys.modules.keys():
            del sys.modules['twisted']
        self.importer = TwistedImporter()
        self.previous_meta_path = sys.meta_path[:]
        sys.meta_path = [self.importer]
        self.envelope = SoapEnvelope(Context(), 'operation')

    def tearDown(self):
        sys.meta_path = self.previous_meta_path

    def testCheckTwistedPresenceSuccess(self):
        """Check if exception is not raised when Twisted is installed."""
        self.importer.raiseException = False
        self.envelope.checkTwistedPresence()

    def testCheckTwistedPresenceFails(self):
        """Check if exception is raised when Twisted is not installed."""
        self.importer.raiseException = True
        self.assertRaises(NoTwistedInstalledError,
                          self.envelope.checkTwistedPresence)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SoapEnvelopeTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
