from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback, re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.hash import lists
from vyperlogix.misc import ObjectTypeName

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

from vyperlogix.sf.abstract import SalesForceAbstract

class SalesForceTempObject(SalesForceAbstract):
    def __init__(self, sfQuery):
        super(SalesForceTempObject, self).__init__(sfQuery,object_name='TEMP_OBJECT__c')

    def new_schema(self,address1__c, address2__c, address3__c, city__c, company__c, country__c, eMail__c, firstName__c, lastName__c, notes__c, phoneMobile__c, phoneOffice__c, Product__c, state__c, title__c, zipPostalCode__c):
        '''This method builds a schema that can be used to make a new instance of this object via a Factory.'''
        return {'eMail__c': eMail__c,
                'address1__c': address1__c,
                'address2__c': address2__c,
                'address3__c': address3__c,
                'city__c': city__c,
                'company__c': company__c,
                'country__c': country__c,
                'firstName__c': firstName__c,
                'lastName__c': lastName__c,
                'notes__c': notes__c,
                'phoneMobile__c': phoneMobile__c,
                'phoneOffice__c': phoneOffice__c,
                'Product__c': Product__c,
                'state__c': state__c,
                'title__c': title__c,
                'zipPostalCode__c': zipPostalCode__c
                }

    def getTempObjects(self):
        soql = "Select %s from TEMP_OBJECT__c t" % (','.join(self.names))
        return self.sf_query(soql)

