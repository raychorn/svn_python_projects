#!/usr/bin/env python

import sys
import unittest
from optparse import OptionParser

from support import TestSession

from pyax.exceptions import ApiFault


class Harness:
    def __init__(self, username, password, token):
        try:
            self.tsession = TestSession.bootstrap(username, password, token)
        except ApiFault, a:
            print str(a)
            sys.exit(1)

    def cleanup(self):
        self.tsession.cleanup()

    def runTests(self, opts):
        self.cleanup()

        suite = unittest.TestSuite()
        
        import context_test
        context_suite = context_test.suite()
        suite.addTest(context_suite)
        
        import updatedict_test
        updatedict_suite = updatedict_test.suite()
        suite.addTest(updatedict_suite)

        import connection_test
        connection_suite = connection_test.suite()
        suite.addTest(connection_suite)

        import create_test
        create_suite = create_test.suite()
        suite.addTest(create_suite)

        import retrieve_test
        retrieve_suite = retrieve_test.suite()
        suite.addTest(retrieve_suite)

        import query_test
        query_suite = query_test.suite()
        suite.addTest(query_suite)
        
        import large_query_test
        large_query_suite = large_query_test.suite()
        suite.addTest(large_query_suite)

        import update_test
        update_suite = update_test.suite()
        suite.addTest(update_suite)

        import delete_test
        delete_suite = delete_test.suite()
        suite.addTest(delete_suite)

        import beatbox_test
        beatbox_suite = beatbox_test.suite()
        suite.addTest(beatbox_suite)

        import clist_test
        clist_suite = clist_test.suite()
        suite.addTest(clist_suite)
        
        if opts.include_apex is True:
            import apexwebservice_test
            apex_suite = apexwebservice_test.suite()
            suite.addTest(apex_suite)

        unittest.TextTestRunner(verbosity=2).run(suite)


def usage(msg=None):
    print "usage: %prog [options] username password [token]" %sys.argv[0]
    if msg is not None:
        print
        print msg
        pass
    print
    sys.exit(1)
    return

def grok_args():
    usage = "usage: %prog [options] username password [token]"
    op = OptionParser(usage=usage)
    op.add_option("-c", "--cleanup-only", action="store_true", dest="cleanup",
                  default=False, help="Only run cleanup - no tests")
    op.add_option("-a", "--include-apex", action="store_true",
                  dest="include_apex", default=False,
                  help="Include Apex webservice tests - only valid if "
                  "PyaxApexTestMethods class has been installed in SFDC org.")
    (opts, args) = op.parse_args()

    if len(args) < 2:
        op.error("Incorrect number of arguments")

    return (opts, args)

def main():
    (opts, args) = grok_args()
    username = str(args[0])
    password = str(args[1])
    token = None
    if len(args) >= 3:
        token = str(args[2])

    h = Harness(username, password, token)
    if opts.cleanup is True:
        h.cleanup()
    else:
        h.runTests(opts)



if __name__ == "__main__":
    main()
