import os, sys

import sqlalchemy_models

from vyperlogix.sf.magma.case_views import SalesForceMoltenCaseViews
from vyperlogix.sf.magma.solution_views import SalesForceMoltenSolutionViews

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

symbol_Sfcase = 'Sfcase'
symbol_Sfsolution = 'Sfsolution'

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import magma_molten_passphrase

_use_staging = False

__sf_account__ = credentials(magma_molten_passphrase,0 if (not _use_staging) else 1)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

def process_bundle(items):
    batches = lists.HashedLists()

    try:
        from vyperlogix.sf.sf import SalesForceQuery
        sfQuery = SalesForceQuery(sf_login_model)
        
        case_views = SalesForceMoltenCaseViews(sfQuery)
        
        solution_views = SalesForceMoltenSolutionViews(sfQuery)
        
        for item in items:
            if (item.viewable_type == symbol_Sfcase):
                d_obj = case_views.new_schema(item.sfcontact_id,item.created_at,item.viewable_id)
                pass
            elif (item.viewable_type == symbol_Sfsolution):
                d_obj = solution_views.new_schema(item.sfcontact_id,item.created_at,item.viewable_id)
            batches[item.viewable_type] = d_obj
        for k,v in batches.iteritems():
            if (k == symbol_Sfcase):
                print >>sys.stderr, 'Creating %d Case View objects.' % (len(v))
                case_views.createBatch(v)
            elif (k == symbol_Sfsolution):
                solution_views.createBatch(v)
                print >>sys.stderr, 'Creating %d Solution View objects.' % (len(v))
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

def main():
    from sqlalchemy_models import viewing_items
    viewing_items(callback=process_bundle)

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
    