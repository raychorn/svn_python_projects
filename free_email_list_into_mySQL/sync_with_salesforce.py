import os, sys

import sqlalchemy_models

from vyperlogix.sf.magma.free_email_hosts import SalesForceFreeEmailHosts

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

from maglib.salesforce.cred import credentials
from maglib.salesforce.auth import magma_molten_passphrase
from maglib.salesforce.auth import CredentialTypes

account_type = CredentialTypes.Magma_Production.value
__sf_account__ = credentials(magma_molten_passphrase,account_type)

from vyperlogix.wx.pyax.SalesForceLoginModel import SalesForceLoginModel
sf_login_model = SalesForceLoginModel(username=__sf_account__['username'],password=__sf_account__['password'])

def process_bundle(items):
    batches = lists.HashedLists()

    try:
        from vyperlogix.sf.sf import SalesForceQuery
        sfQuery = SalesForceQuery(sf_login_model)
        
        free_hosts = SalesForceFreeEmailHosts(sfQuery)
        
        for item in items:
            d_obj = free_hosts.new_schema(item.Domain__c,'%d' % item.IsActive__c)
            batches[1] = d_obj
        for k,v in batches.iteritems():
            free_hosts.createBatch(v)
            print free_hosts.lastError
    except Exception, details:
        info_string = _utils.formattedException(details=details)
        print >>sys.stderr, info_string

def main():
    from sqlalchemy_models import viewing_items
    viewing_items(callback=process_bundle)

if (__name__ == '__main__'):
    if (account_type == CredentialTypes.Magma_Sandbox.value):
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
    