import pprint, sys
import types
import sets

from pyax.util import booleanize
from pyax.collections.cdict import cdict

from pyax.cache import Cache

import logging
log = logging.getLogger('pyax.metadata')


METADATA_STRUCTURE = {'boolean': ['activateable',
             'creatable',
             'custom',
             'deletable',
             'layoutable',
             'queryable',
             'retrievable',
             'replicatable',
             'searchable',
             'undeletable',
             'updateable'],
 'contains': ['sobjectfield', 'sobjectchildren'],
 'sobjectchildren': {'boolean': ['cascadeDelete'],
                     'key': 'childSObject',
                     'parentfield': 'childRelationships',
                     'string': ['childSObject', 'field'],
                     'type': 'multi'},
 'sobjectfield': {'boolean': ['autonumber',
                              'calculated',
                              'creatable',
                              'custom',
                              'defaultedOnCreate',
                              'filterable',
                              'nameField',
                              'nillable',
                              'restrictedPicklist',
                              'selectable',
                              'updateable'],
                  'contains': ['sobjectpick'],
                  'int': ['byteLength',
                          'digits',
                          'length',
                          'precision',
                          'scale'],
                  'key': 'name',
                  'list': ['referenceTo'],
                  'parentfield': 'fields',
                  'sobjectpick': {'boolean': ['active', 'defaultValue'],
                                  'key': 'value',
                                  'parentfield': 'picklistValues',
                                  'string': ['value', 'label'],
                                  'type': 'multi'},
                  'string': ['name', 'label', 'soapType', 'type'],
                  'type': 'multi'},
 'string': ['name', 'label', 'labelPlural', 'urlDetail', 'urlEdit', 'urlNew'],
 'type': 'single'}

class Metadata(object):
    """ Represents an SObject's metadata structure
    """

    def __init__(self, describeSObjectResultDict):
        if type(describeSObjectResultDict) != types.DictType:
            raise ValueError
        self.metadata = describeSObjectResultDict
        self.metadata['fields'] = cdict(describeSObjectResultDict.get('fields',{}))
        self.__brew_field_data()
        return

    def __getattr__(self, key):
        if self.__dict__['metadata'].has_key(key):
            return self.__dict__['metadata'][key]
        elif self.__dict__.has_key(key):
            return self.__dict__[key]
        
        raise AttributeError
    ## END __getattr__

    def __str__(self):
        global METADATA_STRUCTURE
        buf = "Object: %s\n" %self.name
        buf += "-"*20 + "\n"
        buf += self.__format(self.metadata,
                             METADATA_STRUCTURE)
        return buf
    ## END __str__
    
    def __repr__(self):
        return "Metadata(%s)" %self.metadata

    def __format(self, metadata, metadata_structure, level=0):
        order = ('string', 'int', 'boolean', 'list', 'contains')
        indent = '\t'*level
        buf = ''
        for part in order:
            fields = metadata_structure.get(part, [])
            if part == 'contains':
                for contained in fields:
                    partStructData = metadata_structure[contained]
                    field = metadata_structure[contained]['parentfield']
                    partMetadata = metadata.get(field)

                    if partMetadata is not None:
                        buf += "%s%s:\n" %(indent, field)
                        #buf += "%s\n" %partMetadata
                        pass
                    
                    
                    if isinstance(partMetadata, dict):
                        plusIndent = "\t"*(level + 1)
                        for name, partMetadataMember in partMetadata.items():
                            buf += "%s%s\n" %(plusIndent, name)
                            buf += plusIndent + "-"*20 + "\n"
                            buf += self.__format(partMetadataMember,
                                                 partStructData,
                                                 level + 1)
                            buf += '\n'
                            continue
                            
                        pass
                    continue
                pass
            else:
                for field in fields:
                    if metadata.get(field) is not None:
                        buf += "%s%s: %s\n" %(indent, field, metadata.get(field))
                        continue
                    continue
                pass
        return buf
        
    def __brew_field_data(self):
        """
        iterate over the fields metadata element and build lookups for various attributes
        
        Note that only a couple attrs are currently summarized
        
        """
        self.updateableFields = []
        self.nillableFields = []
        
        for fieldname, fielddata in self.fields.items():
            if fielddata.get('updateable', False) is True:
                self.updateableFields.append(fieldname)
                pass
            
            if fielddata.get('nillable', False) is True:
                self.nillableFields.append(fieldname)
                pass
            
            continue
        return
    
    
    def getFieldnames(self):
        fieldnames = self.fields.keys()
        fieldnames.sort()

        if fieldnames[0] != 'Id':
            try:
                fieldnames.remove('Id')
                fieldnames.insert(0, 'Id')
            except:
                # I forget exactly why we're swallowing all exceptions...
                pass

        
        return fieldnames
    fieldnames = property(getFieldnames)
    
    def getFieldSoapType(self, fieldname):
        soap_type = None
        field_data = self.fields.get(fieldname)
        if field_data is not None:
            soap_type = field_data.get('soapType') 
        return soap_type
    pass



class MetadataHelperMixin:
    """Methods for a SObjectCrudBase-descended object to provide for easy 
    access to metadata
    """
    @classmethod
    def getFieldnames(cls):
        """
        Return a list of fieldnames from the metadata, sorted with Id as the
        first fieldname
        """
        return cls._metadata.fieldnames

    
    @classmethod
    def getFieldSoapType(cls, fieldname):
        """find a field's soap type given its API name"""
        return cls._metadata.getFieldSoapType(fieldname)
    
    


class MetadataCache(Cache):
    def __init__(self, sfdc, max_timedelta):
        """
        cxn -  connected AppforceConnection object
        maxTimeDelta - datetime.timedelta object of the maximum age an entry may be before it is considered to be expired.
        
        """
        self.sfdc = sfdc
        self.maxTimedelta = max_timedelta
        
        max_size = 0
        Cache.__init__(self, max_size)
        return
    ## END __init__


    def check(self, name, entry):
        nowTstamp = datetime.datetime.utcnow()

        try:
            entryAge = nowTstamp - entry._tstamp
            if entryAge < self.maxTimedelta:
                return None
            pass
        except AttributeError:
            pass

        opened = self.sfdc.describeSObject()
