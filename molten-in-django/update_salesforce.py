import os, sys

import sqlalchemy_models

from vyperlogix.sf.magma.case_views import SalesForceMoltenCaseViews
from vyperlogix.sf.magma.solution_views import SalesForceMoltenSolutionViews

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import magma_molten_passphrase

_use_staging = True

__sf_account__ = credentials(magma_molten_passphrase,0 if (not _use_staging) else 1)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

def update_salesforce():
    cache = lists.HashedLists()

    try:
        from vyperlogix.sf.sf import SalesForceQuery
        sfQuery = SalesForceQuery(sf_login_model)
        
        solution_views = SalesForceMoltenSolutionViews(sfQuery)
        
        print 'BEGIN: solution_views.getSolutionViews()'
        views = solution_views.getSolutionViews()
        print 'END!   solution_views.getSolutionViews()'
        
        for view in views:
            if (view['Account__c'] is None):
                pass
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

def main():
    update_salesforce()

if (__name__ == '__main__'):
    if (_use_staging):
        sf_login_model.isStaging = True
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['sandbox']))
    else:
        sf_login_model.isStaging = False
        sf_login_model.perform_login(end_point=sf_login_model.get_endpoint(sf_login_model.sfServers['production']))
    if (sf_login_model.isLoggedIn):
        print 'Logged-in Successfully.'
        main()
    else:
        print >>sys.stderr, sf_login_model.lastError
        print str(sf_login_model)
    pass
    