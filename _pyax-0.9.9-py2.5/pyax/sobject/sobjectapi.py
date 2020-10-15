"""
Base class for all sObject instances
"""
import copy
import types
import logging
import sys
from pprint import pprint

from pyax.collections.updatedict import UpdateDict, UpdateAttrDict
from pyax.sobject.metadata import Metadata, MetadataHelperMixin
from pyax.datatype.apexdatetime import ApexDate, ApexDatetime
from pyax.datatype.base64binary import ApexBase64Binary
from pyax.sobject.batch import Batch
from pyax.sobject.util import uniq_id_list
from pyax.util import listify, booleanize
from pyax.unpackomatic import Unpackomatic
from pyax.classproperty import ClassProperty

log = logging.getLogger('pyax.sobject')

class SObjectAPI(UpdateDict, MetadataHelperMixin):
    """ Abstract base class for all Apex sObject types
     
    Provides basic CRUD capabilities.
       
    @attention: Not intended to be instanced directly
    """

    # maintain the dictionary class' update method, but move it aside to make
    # room for the CRUD update
    dictupdate = UpdateDict.update

    # string of an official sObjectType from salesforce
    __sObjectType = None # Holder for the object type string
    
    # SObjectMetadata instance 
    _metadata = None

    # complete list of field names
    fields = []
    
    # temporarily take on the module's logger
    # will be replaced by sObject-specific logger
    # when instantiated by the ClassFactory
    log = log

    def __init__(self, field_map={}):
        """ 
        @param field_map: map of fields and values
        @param callback: when used for an async query

        Not called directly to instantiate salesforce objects - called by
        other static constructor methods
        """
        if self.__sObjectType is None:
            raise NotImplemetedError("Can't instantiate SObjectAPI directly")
        # call the data type parser here using a copy of the sobject field map
        # so that we're not at all beholden to the passed reference
        field_map_copy = self.__coerce_sobject_fields(copy.deepcopy(field_map))
        UpdateDict.__init__(self, field_map_copy)
    
    #############################
    ## sObjectType-specific utility class methods
    #############################
    def get_type(cls):
        """identify the sObject type of the class or instance
        
        @return: sObject type
        @rtype: String
        """
        return cls.__sObjectType
    type = ClassProperty(get_type)

    @classmethod
    def describe_sobject(cls):
        """Wrapper around Connection's describeSObject call specific to an
        sObject class instance
        
        @return: dictionary containing describeSObjectResult
        """
        describe_sobject_result = cls.sfdc.describe_sobject(cls.type)
        cls._metadata = describe_sobject_result
        return describe_sobject_result
    describe_sobject = describe_sobject

    @classmethod
    def describe_layout(cls):
        """
        Wrapper around Connection's describeLayout call specific to an
        sObject class instance
        """
        describe_layout_result = cls.sfdc.describe_layout(cls.type)
        return describe_layout_result
    describeLayout = describe_layout

    @classmethod
    def get_deleted(cls, start_datetime, end_datetime):
        get_deleted_result = cls.sfdc.get_deleted(cls.type,
                                                 start_datetime, end_datetime)
        return get_deleted_result
    getDeleted = get_deleted

    @classmethod
    def get_updated(cls, start_datetime, end_datetime):
        get_updated_result = cls.sfdc.get_updated(cls.type,
                                                  start_datetime, end_datetime)
        return get_updated_result
    getUpdated = get_updated

    def __coerce_sobject_fields(self, sobject_data_dict):
        """ Iterate over the fields of a single sObject and coerce them into
        the proper Python data types
        
        @param sobject_data_dict: Dictionary of sobject fieldnames & values
        
        @return: Dictionary of coerced field values
        @rtype: Dictionary
        """
        coerced_sobject_dict = {}
        for (key, value) in sobject_data_dict.items():
            if (key == 'type' and 
                value.lower() == self.type.lower()):
                # this is the special 'type' field that specifies the 
                # sObjectType. It's not necessary - skip it before adding
                # it to the coerced output dict
                continue
            coerced_sobject_dict[key] = self.__coerce_field_datatype(key, value)
        return coerced_sobject_dict
        
    def __coerce_field_datatype(self, field_name, field_value):
        """ Based on the field type (gleaned from the field's name) coerce
        the value to the proper Python type
        
        @param field_name: Name of the field
        @param field_value: Value for this field
        
        @return: coerced field value
        @rtype: varies
        """
        field_type = self.getFieldSoapType(field_name)
        if field_name in self._metadata.child_relationships.keys():
            # handle child relationships
            if field_value is None:
                # make a properly typed empty batch
                cr = self._metadata.child_relationships[field_name]
                field_value = Batch(self.sfdc, cr["childSObject"])
            else:
                field_value = self.sfdc._process_query_result(field_value)
        elif field_value is None:
            pass # Nothing to do, None is None
        elif field_name in self._metadata.parent_relationships.keys():
            # handle parent relationships
            parent_object_result = {field_value["Id"]: field_value}
            field_value = self.sfdc._result_to_object(parent_object_result)
            key, field_value = field_value.popitem()
        elif field_type == 'xsd:int':
            try:
                field_value = int(field_value)
            except:
                field_value = None
        elif field_type == 'xsd:double':
            try:
                field_value = float(field_value)
            except:
                field_value = None
        elif field_type == 'xsd:dateTime':
            try:
                field_value = ApexDatetime.from_iso(field_value)
            except Exception, e:
                field_value = None
        elif field_type == 'xsd:date':
            try:
                field_value = ApexDate.from_iso(field_value)
            except Exception, e:               
                field_value = None
        elif field_type == 'xsd:boolean' or field_value in ('true', 'false'):
            field_value = booleanize(field_value)
        elif field_type == 'xsd:base64Binary':
            field_value = ApexBase64Binary.from_encoded_string(field_value)
        else:
            pass       
        return field_value
    
    #############################
    ## CRUD support class methods
    #############################
    @classmethod
    def create(cls, sObjectMapList):
        """ Wrapper for connection create method
        
        @param sObjectMapList: List of like-typed sObject data maps to be 
                               created as new sObjects
        """
        save_result = cls.sfdc.create(cls, sObjectMapList)
        return save_result
        
    @classmethod
    def retrieve_save_result(cls, save_result, fieldList=None):
        """ Wrapper for Connection retrieveSaveResult method
        
        @note: sObject type is provided by sObjectClass instance from whence this is called
        @param SaveResult: SaveResult structure returned from a create call
        @param fieldList: optional list of fields to include in the retrieve. Not providing this parameter retrieves all fields
        """
        retrieve_result = cls.sfdc.retrieveSaveResult(cls.type, save_result, 
                                                      fieldList)
        return retrieve_result       

    @classmethod
    def retrieve(cls, ids):
        """ Wrapper for connection retrieve method
        
        @note: sObject type is provided by sObjectClass instance from which this is called
        @param ids: string of a single sObject Id or list of Id strings to retrieve
        """
        retrieve_result = cls.sfdc.retrieve(cls.type, ids)
        return retrieve_result


    #############################
    ## CRUD support instance methods
    #############################
    def create(self):
        """ Create this sobject in salesforce """
        if self.has_key('Id') is True:
            raise KeyError("Cannot create: %s sObject already has Id field set" 
                           %self.type)
        field_map = self.get_updates()
        save_result = self.sfdc.create(self.get_type(), field_map)
        return save_result
    
    def refresh(self, all_fields=False):
        """
        Re-retrieve this sObject from Salesforce.com and replace the reference 
        to the current object with the newly retrieved one.
        
        Parameters:
        allFields - boolean, if set to True, refresh will retrieve all the objects fields. If false
            will retrieve the same set of fields the object was originally retrieved with. Default
            is False.
        
        """
        if self.has_key('Id') is False:
            raise KeyError("Cannot refresh: %s sObject has no Id field set" 
                           %self.type)
            
        field_list = None
        if all_fields is False:
            self.clear()
            field_list = self.keys()
        
        refreshed_sobject = self.sfdc.retrieve(self.type, 
                                               self.get('Id'), 
                                               field_list)
        self._initialize(refreshed_sobject)
        return


    def delete(self):
        """
        Wrapper on connection delete call that deletes only this sObject
        """
        if self.has_key('Id') is False:
            raise KeyError("Cannot delete: %s sObject has no Id field set" 
                           %self.type)

        delete_result = self.sfdc.delete(self.get('Id'))
        return delete_result


    def get_updates(self):
        """
        Overridden UpdateDict getUpdates method to return a case-sensitive
        dictionary of updates, including the Sobject SOAP type and Id
        """
        updates = UpdateDict.get_updates(self)
        #updates = self._UpdateDict__update_dict.extractSensitiveDict()
        
        # remove fieldsToNull element if it exists and is empty
        if (updates.has_key('fieldsToNull') and 
            len(updates['fieldsToNull'])) == 0:
            del updates['fieldsToNull']

        updates['Id'] = self.get('Id')
        updates['type'] = self.type
        
        return updates
        
        
    def update(self):
        """
        Updates a changed CrudObject in salesforce.com

        Compares the sObject's data fields against a stored copy and commits
        any differences to apex.

        @attention: Even though an object based upon SObjectCrudBase is a 
        subclass of a python dictionary-like mapping object, this update 
        method is not equivalent to the dict.update method. To access the 
        latter method in an object of a class descended from SObjectCrudBase, 
        use 'dictupdate' instead.
        """
        if self.has_key('Id') is False:
            raise KeyError("Cannot update: %s sObject has no Id field set" 
                           %self.type)

        update_dict = self.get_updates()

        res = self.sfdc._call_apex(self.sfdc.svc.update, [update_dict])
        save_result = Unpackomatic.unpack(res)
    
        # commit the changes to the sObject if the update succeeded
        if booleanize(save_result.get('success', False)) is True:
            self.commit()
        
        return save_result
    
    def upsert(self, ext_id_fieldname):
        update_dict = self.get_updates()
        save_result = self.sfdc.upsert(self.type,
                                       ext_id_fieldname,
                                       update_dict)
        return save_result
        
