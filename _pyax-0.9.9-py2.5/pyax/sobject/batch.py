"""
List of related apex objects

Provides UD facilities
"""
from types import ListType, TupleType, IntType, SliceType, StringType

from pyax.util import listify, booleanize
from pyax.unpackomatic import Unpackomatic
from pyax.sobject.util import id_15_to_18
from pyax.sobject.type import verify_type

from pyax.collections.cdict import cdict
from pyax.collections.odict import odict

import logging
log = logging.getLogger('pyax.batch')

class Batch(odict):
    """ An ordered dictionary of like-typed Apex sObjects
    
    @note: Unless sobject_type is provided at instantiation, batch is typeless
           until the first sObject is added, then type is construed from that
    """

    def __init__(self, sfdc, sobject_type=None, member_object_list=None):
        """Creates a batch object to contain like-typed sObjects

        @param sfdc: established Apex API session
        @param sobject_type: (opt) sObject type of the batch as a String
        @param member_object_list: (opt) list of sObject to initialize with
        """
        odict.__init__(self)
        self.no_id_count = 0
        self.cxn = sfdc
        self.data = {}

        self.__sobject_type = None

        if sobject_type is not None:
            verify_type(self.cxn, sobject_type)
            self.type = sobject_type
        if member_object_list is not None:
            self.add(member_object_list)

    ## define the "type" property
    def _get_type(self):
        """provide the sObject type of this batch
        
        @note: may return None if the batch instance hasn't yet been typed
        
        @return: sObject type
        @rtype: String or None
        """    
        return self.__sobject_type
    
    def _set_type(self, typeval):
        """ set the sObject type of this batch object, only if it's unset.
        
        @param typeval: A type of sObject
        
        @rtype: None
        """
        if self.__sobject_type is None:
            self.__sobject_type = typeval  
    type = property(_get_type, _set_type)

    def __getitem__(self, key):
        """ Get and returns a single sObject
        
        @param key: either an integer list index or slice, or it may be
                    an sObject Id

        @note: If key is a slice returns a Batch containing the slice
               of items
               
        @return: a single sObject or an sObject Batch
        @rtype: SObject or Batch of sObjects
        """
        if isinstance(key, int):
            return self.values()[key]
        elif isinstance(key, slice):
            keys = self._keys[key]
            retlist = []
            for key in keys:
                retlist.append(self.get(key))
                continue
            return Batch(self.cxn, self.type, retlist)
        else:
            # assume key is an Id
            # translate to id18
            key = id_15_to_18(key)
            return self.get(key)

    def __delitem__(self, key):
        """ Deletes an index, slice, Id or list of IDs from the batch
        
        @param key: either an integer list index or slice, or it may be
                    an sObject Id
        """
        if isinstance(key, int):
            key = self._keys[key]
            self.__delitem__(key)
        elif isinstance(key, slice):
            keys = self._keys[key]
            self.__delitem__(keys)
        elif isinstance(key, (list, tuple)):
            keys = key
            for key in keys:
                del self[key]
        elif isinstance(key, str):
            # key is a string (most likely an sObject ID)
            key = id_15_to_18(key)
            odict.__delitem__(self, key)
        else:
            raise KeyError

    def add(self, obj_list):
        """Adds an sObject or list of sObjects 
        """
        reject_list = []
        if isinstance(obj_list, dict):
            obj_list = obj_list.values()
        obj_list = listify(obj_list)
        if self.type is None and len(obj_list) > 0:
            self.type = obj_list[0].type
        for obj in obj_list:
            if obj.type == self.type:
                try:
                    batch_key = obj.get('Id')
                    if batch_key is None:
                        self.no_id_count += 1
                        batch_key = "no_id_%s" %self.no_id_count
                    self[batch_key] = obj
                except Exception, e:
                    print "Batch.add error: %s" %e
            else:
                reject_list.append(obj)
        return reject_list

    def move(self, key, index):
        key = id_15_to_18(key)
        odict.move(self, key, index)

    def items(self):
        """ Override odict.items() method to return an explicit list of tuples
        instead of a generator so that the batch may be pprinted. Batches are 
        typically not *that* big so as to cause memory problems by doing this
        """
        item_list = []
        for i in self._keys:
            item_list.append((i, self[i]))
        return item_list
    
    def update(self):
        """ Performs an Apex API update for all items in this Batch
        @return: ordered dictionary of saveResults, keyed by sObject id
        @rtype: odict
        """
        MAX_CREATE = self.cxn.context.max_create
        update_list = []
        is_list = True
        for sobject in self.values():
            update_list.append(sobject.get_updates())
        
        update_result_batch = None

        slice_cursor = 0
        while len(update_list[slice_cursor:slice_cursor+MAX_CREATE]):
            update_list_slice = update_list[slice_cursor:slice_cursor+MAX_CREATE]
            slice_cursor += MAX_CREATE

            # add type designation to each object map - REQUIRED by sfdc
            for sobject_dict in update_list_slice:
                # if the user chose to use a case insensitive dictionary to
                # build their data structure, get the insensitive version
                if isinstance(sobject_dict, cdict):
                    sobject_dict = sobject_dict.extractSensitiveDict()
            slice_updateResult = self.cxn._call_apex(self.cxn.svc.update,
                                                    update_list_slice)
            unpacked_result = Unpackomatic.unpack(slice_updateResult)
            # above may be a list of result dicts, or a single result dict
            for save_result in unpacked_result.values():
                if booleanize(save_result.get('success', False)) is True:
                    self[save_result['id']].commit()

            if update_result_batch is None:
                update_result_batch = unpacked_result
            else:
                update_result_batch.update(unpacked_result)

        return update_result_batch

    def delete(self):
        """Delete all sObjects in this batch
        
        @return: ordered dictionary of deleteResults, keyed by sObject id
        @rtype: odict
        """
        delete_result_batch = self.cxn.delete(self.keys())
        # remove all successfully deleted sObjects from the batch
        for delete_result in delete_result_batch.values():
            if booleanize(delete_result.get('success', False)) is True:
                del self[delete_result['id']]
        return delete_result_batch

    def refresh(self, all_fields=False):
        """
        Re-retrieves all the sObjects in the batch and repopulates the batch
        with the results. 
        
        @param all_fields: (opt) Boolean, if True will retrieve all fields on
            the object, otherwise will retrieve only the existing set of fields.
            Default: False
            
        @rtype: None
        """
        batch_sobject_id_list = self.keys()

        field_list = None
        if all_fields is False:
            field_list = self[0].keys()

        retrieved_batch = self.cxn.retrieve(self.type, 
                                            batch_sobject_id_list, 
                                            field_list)
        # clear the existing batch and add all elements of the retrieved batch
        self.clear()
        self.add(list(retrieved_batch))

class batchdict(dict):
    """ just a plain dictionary with one additional property
    """
    def get_count(self):
        """ returns the sum of the length of each batch of sobjects
        """
        count = 0
        for sobject_batch in self.values():
            count += len(sobject_batch)
        return count
    count = property(get_count)
    