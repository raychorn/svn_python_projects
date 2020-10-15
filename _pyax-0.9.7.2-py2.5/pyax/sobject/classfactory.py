import types

from pyax.sobject.sobjectapi import SObjectAPI
from pyax.sobject.type import verify_type

import logging
log = logging.getLogger('pyax.sobject')
    
class ClassFactory(type):
    """ Class factory for all Salesforce.com objects which inherit sObjectAPI
    """
    sobject_type_dict = {}
    
    def __new__(cls, sfdc, sobject_type, base_arg=[], attr_arg={}):
        listBase = cls.procBases(base_arg, sobject_type)
        mapAttr = cls.procAttrs(attr_arg)

        if type(sobject_type) != types.StringType:
            raise TypeError("argument sobject_type must be a String")
        verify_type(sfdc, sobject_type)

        if not cls.sobject_type_dict.has_key(sobject_type):
            newclass = type.__new__(cls, sobject_type, listBase, mapAttr)
            newclass.cxn = sfdc
            # fetch and install the metadata for this sObjectType
            
            newclass._SObjectAPI__sObjectType = sobject_type
            newclass._metadata = newclass.describeSObject()

            # install a custom logger for the sobject type
            newclass.log = logging.getLogger('pyax.sobject.%s' %sobject_type)
            
            # cache the class
            cls.sobject_type_dict[sobject_type] = newclass

        return cls.sobject_type_dict.get(sobject_type)



    def __init__(cls, sfdc, sobject_type, basr_arg=[], attr_arg={}):
        list_base = cls.procBases(basr_arg, sobject_type) 
        map_attr = cls.procAttrs(attr_arg)
        
        super(ClassFactory, cls).__init__(sobject_type,
                                                   list_base, map_attr)
        return


    @staticmethod
    def procBases(base_arg, sobject_type):
        """ Accept either a list, tuple or single base class. Return a tuple
        that contains at least SfCrudBase as a blase class. """
        list_base = []
        if type(base_arg) == types.TupleType:
            list_base.extend(base_arg)
        elif type(base_arg) != types.ListType:
            list_base.append(base_arg)
        else:
            pass

        # Ensure that we always include SfCrudBase as a base class
        if SObjectAPI not in list_base:
            list_base.append(SObjectAPI)
            pass

        # if we're creating a lead, include lead-specific mixin base
        if sobject_type.lower() == 'lead':
            from leadapi import LeadAPI
            list_base.append(LeadAPI)
            pass
        
        return tuple(list_base)


    @classmethod
    def procAttrs(cls, attr_arg):
        """ Simply ensure that attrArg is a dictionary """
        if type(attr_arg) != types.DictType:
            raise TypeError

        return attr_arg
