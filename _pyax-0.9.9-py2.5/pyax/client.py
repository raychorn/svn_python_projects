#Copyright 2005, 2006 Kevin Shuk, Magma Design Automation
#Copyright 2007, 2008, 2009 Kevin Shuk, Canonical Limited
#All rights reserved
#
#This file is part of pyax.
#
#pyax is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
#
#pyax is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyax.  If not, see <http://www.gnu.org/licenses/>.
"""Main client object that pyax end users instantiate """
import os
import sys
import re
import types
from pprint import pprint 

from pyax.beatbox.beatbox import Client as XMLClient
from pyax.beatbox.beatbox import _tPartnerNS, SoapFaultError
from pyax.beatbox.context import Context
from pyax.sobject.util import uniq_id_list
from pyax.util import booleanize, listify, uniq
from pyax.collections.cdict import cdict
from pyax.collections.clist import clist
from pyax.collections.odict import odict
from pyax.exceptions import ApiFault, NoConnectionError
from pyax.unpackomatic import Unpackomatic
from pyax.sobject.metadata import Metadata, MetadataCache
from pyax.sobject.classfactory import ClassFactory
from pyax.sobject.batch import Batch, batchdict
from pyax.datatype.apexdatetime import ApexDatetime

import logging

log = logging.getLogger('pyax.client')

sf = _tPartnerNS

class Client(object):

    __context = None

    @classmethod
    def connect(cls, username, password, token=None, context=None):
        """ Authenticate a Salesforce.com user

        @param username: username of user to authenticate
        @param password: user's password
        @param token: (if required by salesforce org) user's API security token
        @param context: (opt) Context object to modify default connection
            parameters

        @return: authenticated connection object
        @rtype: pyax.client.Client
        """
        if context is None:
            context = Context()

        fdc = cls(context)
        fdc.__username = username
        fdc.__password = password
        if token is not None:
            fdc.__password += token
        fdc.__org_id = None
        fdc.__login()
        fdc.describe_global_response = fdc.describeGlobal()
        fdc.global_types = fdc.describe_global_response.get('types', [])

        login_response = fdc.__login()

        # informative attrs - changing these does nothing
        fdc.user_id = login_response.get('userId')
        fdc.session_id = login_response.get('sessionId')
        fdc.user_info = login_response.get('userInfo')
        fdc.server_url = login_response.get('serverUrl')
        fdc.endpoint = fdc.svc.context.endpoint
        return fdc

    @classmethod
    def connect_self_service(cls, username, password, org_id, context=None):
        """ Authenticate a self-service user against a specified
        Salesforce.com organisation

        @param username: self-service username of user to authenticate
        @param password: user's password
        @param org_id: organization id of that contains the self-service user
        @param context: (opt) Context object to modify default connection
            parameters

        @return: session ID for the self-service user
        @rtype: str
        """
        if context is None:
            context = Context()
        fdc = cls(context)
        fdc.__username = username
        fdc.__password = password
        fdc.__org_id = org_id
        login_response = fdc.__login()
        return login_response.get('sessionId')

    def __init__(self, context):
        """ perform create an Apex connection that's ready to connect
        
        @param context: Contains the connection information such as endpoint
        """
        self.context = context
        # container for the session. Used for all calls.
        self.svc = XMLClient(context) 
        self.__session_api_call_count = 0
        
    def generate_class(self, class_name):
        """Uses ClassFactory to return an sobject class of the requested type
        
        @param class_name: String name of the class to return from 
                           the ClassFactory
        @return: SObject class
        """
        return ClassFactory(self, class_name)

    def get_session_api_call_count(self):
        return self.__session_api_call_count
    session_api_call_count = property(get_session_api_call_count)
    
    def reset_session_api_call_count(self):
        current_call_count = self.session_api_call_count
        self.__session_api_call_count = 0
        return current_call_count

    def _call_apex(self, apex_method, *args, **kw):
        """Wrapper with which to run all sForce calls (after login).

        Catches any faultType exception, parses it, then turns it into an
        exception of the specific type returned (the possibilites are
        documented in the sForce API docs). If it is an INVALID_SESSION
        error, we will re-login and retry the call.

        @param apexMethod: reference to the method we're calling
            parameters to apexMethod come in on *args

        @return: result of the call as returned by the underlying SOAP library
        """
        apex_result = None

        retry_count = kw.get('retry_count',0)
        if kw.has_key('retry_count'):
            del kw['retry_count']
            pass

        try:
            try:
                apex_result = apex_method(*args, **kw)
            except SoapFaultError, f:
                if hasattr(f, 'faultCode') and hasattr(f, 'faultString'):
                    self.__session_api_call_count += 1    
                    raise ApiFault(f.faultCode, f.faultString)
                raise f # the exception wasn't an ApiFault exception, rethrow
            else:
                self.__session_api_call_count += 1
        except ApiFault, f:
            retry_count += 1
            if f.exception_code == "INVALID_SESSION_ID" and \
                retry_count < self.context.max_retry:
                self.__login() #re-login the session

                apex_result = self._call_apex(apex_method,
                                             retry_count=retry_count,
                                             *args, **kw)
            else:
                 raise f # the ApiFault was some other kind - rethrow
        return apex_result

    def __login(self):
        """ Perform all the negotiation with the endpoint and login
        to initiate a session
        """
        try:
            self.__session_api_call_count += 1
            login_response = self.svc.login(self.__username, self.__password, 
                                            self.__org_id)
        except SoapFaultError, f:
            raise ApiFault(f.faultCode, f.faultString)
        login_result = Unpackomatic.unpack(login_response)
        if login_result['passwordExpired'] is True:
            raise NoConnectionError('Password for %s has expired'
                                    %self.__username)
        return login_result

    def logout(self):
        """ Calls logout to invalidate current user's active session """
        self._call_apex(self.svc.logout)

    def invalidate_sessions(self, id_list):
        """ Invalidates provided session ids 
        
        @param id_list: List of session ID strings
        
        @return: invalidateSessionResult structure
        @rtype: list
        """
        # use the delete slice size for now as it's the same as the max
        # sessions that may be invalidated simultaneously
        SLICE_SIZE = self.context.max_delete
        
        id_list = listify(id_list)
        id_list = uniq(id_list)
        
        invalidate_sessions_result = []
        slice_cursor = 0
        while len(id_list[slice_cursor:slice_cursor+SLICE_SIZE]):
            invalidate_slice = id_list[slice_cursor:slice_cursor+SLICE_SIZE]
            slice_cursor += SLICE_SIZE
            result = self._call_apex(self.svc.invalidateSessions, 
                                    invalidate_slice)
            invalidate_sessions_result.extend(listify(Unpackomatic.unpack(result)))        
        return invalidate_sessions_result
    invalidateSessions = invalidate_sessions
    
    def get_server_timestamp(self):
        """simple wrapper method for sforce API call of the same name.

        @return: ApexDatetime, which is a subclass of datetime
        """
        response = self._call_apex(self.svc.getServerTimestamp)
        timestamp_result = Unpackomatic.unpack(response)
        return ApexDatetime.from_iso(timestamp_result["timestamp"])
    getServerTimestamp = get_server_timestamp

    def get_user_info(self):
        """simple wrapper method for sforce API call of the same name.

        @return: dictionary containing the user info
        """
        return self._call_apex(self.svc.getUserInfo)
    getUserInfo = get_user_info

    def reset_password(self, user_id):
        """reset password for a user to a generated value.

        @param userId: user sObject ID
        @return: salesforce.com generated password as a String
        """
        res = self._call_apex(self.svc.resetPassword, user_id)
        reset_password_result = Unpackomatic.unpack(res)
        return reset_password_result.get('password')
    resetPassword = reset_password

    def set_password(self, user_id, password):
        """Set the password for a user to the specified value

        @param userId: user sObject ID
        @param password: new password for the user

        @return: None

        @raise ApiFault: Invalid
        """
        # setPasswordResult returns nothing
        self._call_apex(self.svc.setPassword, user_id, password)
    setPassword = set_password

    ###
    ### system metadata calls
    ###
    def describe_global(self):
        """ simple wrapper method for sforce API call of the same name.
        Since the returned object is of no further use than to look up
        values, we liberate it as a python dictionary before returning it
        """
        response = self._call_apex(self.svc.describeGlobal)
        describe_global_result = Unpackomatic.unpack(response)
        describe_global_result['types'] = clist(describe_global_result.get('types',[]))
        return describe_global_result
    describeGlobal = describe_global

    def describe_sobject(self, sobject_type):
        if not isinstance(sobject_type, str):
            #print type(sobject_type)
            raise ValueError
        return self.describeSObjects(sobject_type)
    describeSObject = describe_sobject

    def describe_sobjects(self, sobject_type_list):
        MAX_SOBJECT_TYPES = 100

        isList = False
        if isinstance(sobject_type_list, (list, tuple)):
            isList = True

        sobject_type_list = listify(sobject_type_list)
        sobject_type_list = uniq(sobject_type_list)

        describe_sobject_result_dict = {}
        while len(sobject_type_list):
            type_list_slice = sobject_type_list[:MAX_SOBJECT_TYPES]
            sobject_type_list = sobject_type_list[MAX_SOBJECT_TYPES:]

            res = self._call_apex(self.svc.describeSObjects, type_list_slice)
            unpacked_sobject_results = Unpackomatic.unpack(res)

            if len(type_list_slice):
                for describe_sobject_result in unpacked_sobject_results.values():
                    sobject_metadata = Metadata(describe_sobject_result)
                    describe_sobject_result_dict[sobject_metadata.type] = \
                        sobject_metadata
            else:
                # slice apparently has no length
                pass

        if isList is False and len(describe_sobject_result_dict) > 0:
            describe_sobject_result_dict = describe_sobject_result_dict.values()[0]

        return describe_sobject_result_dict
    describeSObjects = describe_sobjects

    def describe_tabs(self):
        response = self._call_apex(self.svc.describeTabs)
        describe_tab_set_result = Unpackomatic.unpack(response)
        return describe_tab_set_result
    describeTabs = describe_tabs

    def describe_layout(self, sobject_type):
        response = self._call_apex(self.svc.describeLayout,
                                   sobject_type)
        describe_layout_result = Unpackomatic.unpack(response)
        return describe_layout_result
    describeLayout = describe_layout

    ###
    ### session level CRUD operations
    ###
    def _result_to_object(self, result):
        """Translate a list of query or retrieve results into objects

        Parameters
        """
        sobject_batch = Batch(self)
        if isinstance(result, dict):
            result = result.values()
        result_list = listify(result)
        sobject_type = None
        if (len(result_list) 
            and result_list[0] is not None 
            and result_list[0].get('type') is not None):
            sobject_type = result_list[0].get('type')
            SObjectClass = ClassFactory(self, sobject_type)
            for sobject_result in result_list:
                if isinstance(sobject_result, dict):
                    # For some reason, the ID field comes back as a list of
                    # identical values. Grab only the first one.
                    if isinstance(sobject_result.get('Id'), list):
                        sobject_result['Id'] = sobject_result.get('Id')[0]
                    sobject = SObjectClass(sobject_result), 
                    sobject_batch.add(sobject)
        return sobject_batch

    def _generate_class_type(self, sobject_class):
        """ Ensure that an object is suitable for use as an sObject class

        @param sobject_class: String or SObjectClass instance

        @return: SObjectClass instance
        """
        if isinstance(sobject_class, str):
            sobject_class = ClassFactory(self, sobject_class)

        if not isinstance(sobject_class, ClassFactory):
            raise TypeError("argument sObjectClass must be String or sObjectClass instance")

        return sobject_class


    def create(self, sobject_class, sobject_map_list):
        """ perform the Apex create call

        @param sobject_class: String representing sobject type or
            sObjectClass instance
        @param sobject_map_list: dictionary or list of dictionaries of data
            to insert

        @return: single SaveResult dictionary or list of SaveResult
            dictionaries indicating the status of each object created.
        """
        MAX_CREATE = self.context.max_create
        is_list = True

        sobject_class = self._generate_class_type(sobject_class)

        # ensure that sobject_map_list is a sequence of dictionaries
        if isinstance(sobject_map_list, dict):
            is_list = False
            sobject_map_list = listify(sobject_map_list)
        elif type(sobject_map_list) not in [types.ListType, types.TupleType]:
            errmsg = "sobject_map_list not a dictionary, list or tuple"
            raise TypeError(errmsg)
        else:
            # sobject_map_list is of the appropriate type
            pass

        save_result = odict()
        no_key_count = 0
        slice_cursor = 0
        while len(sobject_map_list[slice_cursor:slice_cursor+MAX_CREATE]):
            sobject_list_slice = sobject_map_list[slice_cursor:slice_cursor+MAX_CREATE]
            slice_cursor += MAX_CREATE

            # add type designation to each object map - REQUIRED by sfdc
            for sobject_dict in sobject_list_slice:
                # if the user chose to use a case insensitive dictionary to
                # build their data structure, get the insensitive version
                if isinstance(sobject_dict, cdict):
                    sobject_dict = sobject_dict.extractSensitiveDict()

                # We're going to populate the field 'type' with the
                # sObjectType. If this already exists, we re-key it to
                # 'Type'. If 'Type' exists as well, you're SOL and
                # 'type' item will be overwritten.
                if sobject_dict.has_key('type') and \
                    not sobject_dict.has_key('Type'):
                    sobject_dict['Type'] = sobject_dict['type']
                sobject_dict['type'] = sobject_class.type

                # pick out any None fields - can't create any field with None
                #fix for bug #217958
                if None in sobject_dict.values():
                    for (key, value) in sobject_dict.items():
                        if value is None:
                            del sobject_dict[key]

            slice_create_response = self._call_apex(self.svc.create,
                                                    sobject_list_slice)
            save_result_unpacker = Unpackomatic(slice_create_response, 
                                                no_key_count=no_key_count)
            save_result.update(save_result_unpacker.result) # may be a list of result dicts, or a single result dict
            no_key_count = save_result_unpacker.no_key_count
#            if is_list:
#                save_result.extend(listify(unpacked_result))
#            else:
#                save_result = unpacked_result
        return save_result


    def upsert(self, sobject_class, ext_id_fieldname, sobject_map_list):
        """ Updates or inserts an sObject in salesforce.com

        Based on whether a record already exists with the value in the field
        designated by externalIdFieldname upsert will either insert a new
        object or update the existing one.

        @param sObjectClass: String representing sobject type or sObjectClass
            instance
        @param externalIdFieldname: the name of the field on which to base
            the upsert operation
        @param sObjectMapList: dictionary (or list of dicts) of data to insert

        @return: UpsertResult
        @rtype: Dictionary
        """
        MAX_CREATE = self.context.max_create
        is_list = True

        sobject_class = self._generate_class_type(sobject_class)

        # ensure that sObjectMapList is a sequence of dictionaries
        if isinstance(sobject_map_list, dict):
            is_list = False
            sobject_map_list = listify(sobject_map_list)
        elif not isinstance(sobject_map_list, list) and \
            not isinstance(sobject_map_list, tuple):
            errmsg = "sObjectMapList not a dictionary, list or tuple"
            raise TypeError(errmsg)

        upsert_result = []

        slice_cursor = 0
        while len(sobject_map_list[slice_cursor:slice_cursor+MAX_CREATE]):
            sobject_list_slice = sobject_map_list[slice_cursor:slice_cursor+MAX_CREATE]
            slice_cursor += MAX_CREATE

            # add type designation to each object map - REQUIRED by sfdc
            for sobject_dict in sobject_list_slice:
                # if the user chose to use a case insensitive dictionary to
                # build their data structure, get the insensitive version
                if isinstance(sobject_dict, cdict):
                    sobject_dict = sobject_dict.extractSensitiveDict()

                # We're going to populate the field 'type' with the
                # sObjectType. If this already exists, we re-key it to
                # 'Type'. If 'Type' exists as well, you're SOL and
                # 'type' item will be overwritten.
                if sobject_dict.has_key('type') and \
                    not sobject_dict.has_key('Type'):
                    sobject_dict['Type'] = sobject_dict['type']
                sobject_dict['type'] = sobject_class.type

            slice_upsertResult = self._call_apex(self.svc.upsert,
                                                ext_id_fieldname,
                                                sobject_list_slice)
            unpacked_result = Unpackomatic.unpack(slice_upsertResult)
            # above may be a list of result dicts, or a single result dict

            if is_list:
                upsert_result.extend(listify(unpacked_result))
            else:
                upsert_result = unpacked_result

        return upsert_result

    def resultToIdList(self, result_list, success_status=None):
        """ Helper method to convert either a save_result (or other result)
        OR a Batch into a list of Ids.

        @param result_list: result structure or sObject Batch
        @param success_status: (opt) only include entries with the specified
            boolean success status. If not specified, all entries are included

        @return: list of sObject IDs
        @rtype: list
        """
        id_list = []
        for result_map in result_list:
            process_result = True
            if isinstance(success_status, bool):
                # if we've specified a success status AND the result doesn't
                # match it, then don't process this particular result.
                if result_map.get('success', False) is not success_status:
                    process_result = False
            if process_result:
                if result_map.has_key('id'):
                    id_list.append(result_map['id'])
        return id_list

    def retrieveSaveResult(self, sobject_type, save_result, field_list=None):
        is_list = False
        if isinstance(save_result, list):
            is_list = True
            pass

        save_result_list = listify(save_result)
#        id_list = []
#        for save_result in save_result_list:
#            if save_result.get('success', False) is True:
#                id_list.append(save_result['id'])
#                pass
#            continue
        id_list = self.resultToIdList(save_result_list, success_status=True)

        if isinstance(save_result, dict) and len(id_list) == 1:
            # dealing with a single-result instance
            id_list = id_list[0]

        return self.retrieve(sobject_type, id_list, field_list)


    def retrieve(self, sobject_class, id_list, field_list=None):
        """Retrieves objects for the list of IDs

        @param idList: List of sObject IDs to retrieve. All IDs must be of the
            same sObject type. The maximum number of IDs to retrieve is 2000,
            and if more are supplied to this method, multiple retrieve calls
            will automatically be made and the results combined.
        @param fieldList: List of fields to retrieve for each sObject. If not
            provided or None, all fields for the object will be retrieved.
        """
        MAX_RETRIEVE_IDS = self.context.max_retrieve
        sobject_class = self._generate_class_type(sobject_class)
        is_list = False
        if isinstance(id_list, (list, tuple)):
            is_list = True
        id_list = listify(id_list)
        # we must insure that there are no duplicate IDs otherwise SOAPpy
        # generates a strange outgoing SOAP message that blows the
        # session ID
        if field_list is None:
            field_list = sobject_class.getFieldnames()
        retrieve_result = odict()
        sliceCursor = 0
        while len(id_list[sliceCursor:sliceCursor+MAX_RETRIEVE_IDS]):
            idListSlice = id_list[sliceCursor:sliceCursor+MAX_RETRIEVE_IDS]
            sliceCursor += MAX_RETRIEVE_IDS
            res = self._call_apex(self.svc.retrieve,
                                 ', '.join(field_list),
                                 sobject_class.type,
                                 idListSlice)
            res = Unpackomatic.unpack(res)
            retrieve_result.update(res)
        retrieved_objects = self._result_to_object(retrieve_result)
        if is_list is False:
            if len(retrieved_objects) > 0:
                retrieved_objects = retrieved_objects[0]
            else:
                retrieved_objects = None
        return retrieved_objects

    def _query_template(self, method_name, query_string, callback, errback):
        """
        Template method for running queries to salesforce.com

        If callable is supplied it will be asynchronous query, otherwise it
        will be regular synchronous call.

        @param method_name: query or queryAll method name
        @param query_string: SOQL query string
        @param callback: callable which would be called when results arrived
        @param errback: callable to invoke in case of errors during
                        asynchronous call, if None default error handling will
                        be used
        """
        assert method_name in ('query', 'queryAll'), \
               "method_name must be query or queryAll"
        query_string = query_string.strip()
        method = getattr(self.svc, method_name)
        if callback is not None:
            def process_query_response(query_response):
                query_result = Unpackomatic.unpack(query_response)
                self._process_async_query_result(query_result, 
                                                 callback, errback)
            # Make the query call
            self._call_apex(method, query_string, 
                            callback=process_query_response,
                            errback=errback)
        else:
            query_response = self._call_apex(method, query_string)
            query_result = Unpackomatic.unpack(query_response)
            return self._process_query_result(query_result)

    def query(self, query_string, callback=None, errback=None):
        """
        Runs a query for any type of object.

        In the event that more records are found than can be returned in a
        single batch, query will automatically call _queryMore until it has
        fetched all objects found by the query, returning the combined
        result.

        Returns a batch object containing all objects found by the query or
        an empty batch if none were found.

        If the Id field is not specified in the field list, the object returned
        will be "sterile" in that they cannot be used for updates or deletes.

        If callback is supplied whole call will be asynchronous. After finishing
        request callback will be called with batch object containing results.

        @param query_string: full SOQL query
        @param query_all: bool - should this be run as a query all?
        @param callbacks: if is not None query will be asynchronous and this
                          callable will be called with result when query will
                          be finished
        @param errback: if specified it will be passed to Twisted ass error
                        handler

        """
        return self._query_template('query', query_string, callback, errback)

    def query_all(self, query_string, callback=None, errback=None):
        """ Identical to query method, except it can include sobjects in
        the recycle bin:
        query isDeleted field to find records in the recycle bin
        query masterRecordId field to find records deleted as part of a merge
        query isArchived to find archived records

        @note: deleted records may be undeleted using the undelete call
        """
        return self._query_template('queryAll', query_string, callback, errback)
    queryAll = query_all

    def _old_query_more(self, query_locator):
        query_more_response = self._call_apex(self.svc.queryMore, query_locator)
        return Unpackomatic.unpack(query_more_response)
    
    def _query_more(self, query_locator, callback=None, errback=None):
        if callback is not None:
            def process_query_more_response(query_more_response):
                query_result = Unpackomatic.unpack(query_more_response)
                callback(query_result)
            # Make the query call
            self._call_apex(self.svc.queryMore, query_locator, 
                            callback=process_query_more_response,
                            errback=errback)
        else:
            query_more_response = self._call_apex(self.svc.queryMore, 
                                                  query_locator)
            return Unpackomatic.unpack(query_more_response)
        pass
    
    def _patch_query_result(self, query_result):
        """Normally does nothing, but gives tests a point to alter results

        @param query_result: result from Unpackomatic run on a query response
        @return: result from Unpackomatic run on a query response
        """
        return query_result

    def _process_async_query_result(self, query_result, callback, errback, result_batch=None):
        """
        Similar method to _process_query_result used with asynchronous queries.

        This is called when query is finished.
        """
        query_result = self._patch_query_result(query_result)
        records = query_result.get("records", odict())
        count_result = None
        if result_batch is None:
            if records == [None]:
                # this was a count query, just return the size
                count_result = int(query_result["size"])
            else:
                result_batch = self._result_to_object(records)
        else:
            result_batch.add(self._result_to_object(records))
            
        if query_result["done"] is not True:
            def process_result(result):
                self._process_async_query_result(result, 
                                                 callback, errback, 
                                                 result_batch)
                
            ## resume here - call _new_query_more
            self._query_more(query_result["queryLocator"], 
                                 callback=process_result, errback=errback)
        else:
            # No more results, send back the appropriate result
            if count_result is not None:
                callback(count_result)
            else:
                callback(result_batch)
            
    def _process_query_result(self, query_result):
        """ processes the result from a query or queryAll call into an
        Batch, calling queryMore as necessary to complete the query
        operation

        @param query_result: return result from a query or queryAll call
        @note: Although queryMore also returns a query_result this is not
            intended to be a primary input to this method. Rather, these are
            handled internally to this method and aggregated into the
            query_result_batch

        @return: a Batch populated with the sobject(s) found by the
            query call that produced the query_result parameter.
        @rtype: pyax.sobject.batch.Batch
        """
        query_result = self._patch_query_result(query_result)
        records = query_result.get("records", odict())
        if records == [None]:
            # this was a count query, just return the size
            return int(query_result["size"])
        done = query_result["done"]
        query_locator = query_result["queryLocator"]
        query_result_batch = self._result_to_object(records)
        while done is False:
            query_more_result = self._query_more(query_locator)
            query_more_result = self._patch_query_result(query_more_result)
            done = query_more_result["done"]
            query_locator = query_more_result["queryLocator"]
            records = query_more_result.get("records", odict())
            query_more_result_batch = self._result_to_object(records)
            query_result_batch.add(query_more_result_batch)
        return query_result_batch

    def search(self, search_string):
        """ Executes a text search over the organisation's data

        @param search_string: SForce Object Search Language (SOSL) string
            specifying the text expressions to search for, the scope of the
            fields to search, the list of objects and fields to retrieve, and
            the maximum number of objects to return.

        @return: Dictionary, keyed by object type containing batches of the
            objects found.
        @rtype: dict (str, pyax.sobject.Batch)

        @attention: if fields are specified in the RETURNING clause, Id must be
            included in order to get a valid sobject Id for the found objects.
            If no fields are specified in the RETRUNING clause, or the
            RETURNING clause is omitted entirely, then sobject Ids will be
            fetched automatically.
        """
        sf = _tPartnerNS
        search_string = search_string.strip()
        search_result = self._call_apex(self.svc.search, search_string)

        search_result_list = []
        for elt in search_result._dir:
            search_result_list.append(Unpackomatic.unpack(elt['record']))

        # sort the results into a dict of batches keyed by type
        search_result_dict = batchdict()
        for sr in search_result_list:
            SObjectClass = ClassFactory(self, sr['type'])
            sobject = SObjectClass(sr)
            if search_result_dict.has_key(sobject.type):
                search_result_dict[sobject.type].add(sobject)
            else:
                sobject_batch = Batch(self)
                sobject_batch.add(sobject)
                search_result_dict[sobject.type] = sobject_batch
        return search_result_dict

    def delete(self, id_list):
        """
        A connection version of the delete call that can take a list
        having any mix of sObject ids for deletion

        @param idList: list of sObject ids to delete

        @return: list of results indicating success or failure of the
            deletion of each batch object by id.
        @rtype: List
        """
        MAX_DELETE = self.context.max_delete
        id_list = listify(id_list)
        id_list = uniq_id_list(id_list)
        delete_result = odict()
        slice_cursor = 0
        while len(id_list[slice_cursor:slice_cursor+MAX_DELETE]):
            delete_slice = id_list[slice_cursor:slice_cursor+MAX_DELETE]
            slice_cursor += MAX_DELETE
            result = self._call_apex(self.svc.delete, delete_slice)
            delete_result.update(Unpackomatic.unpack(result))
        return delete_result

    def empty_recycle_bin(self, id_list):
        """
        Permanently removes objects from the recycle bin 
        after they've been deleted.

        @param idList: list of deleted sObject ids to remove
        
        @return: list of results indicating success or failure of the removal
        @rtype: List
        """
        SLICE_SIZE = self.context.max_delete
        id_list = listify(id_list)
        id_list = uniq_id_list(id_list)
        empty_result = odict()
        slice_cursor = 0
        while len(id_list[slice_cursor:slice_cursor+SLICE_SIZE]):
            empty_slice = id_list[slice_cursor:slice_cursor+SLICE_SIZE]
            slice_cursor += SLICE_SIZE
            result = self._call_apex(self.svc.emptyRecycleBin, empty_slice)
            empty_result.update(Unpackomatic.unpack(result))
        return empty_result
    emptyRecycleBin = empty_recycle_bin
    
    def undelete(self, id_list=None):
        """undelete can take a list having any mix of sObject ids for
        undeletion from the recycle bin

        @param idList: list of sObject ids to undelete

        @return: list of results indicating success or failure of the
            undeletion of each batch object by id.
        @rtype: List
        """
        MAX_DELETE = self.context.max_delete
        id_list = listify(id_list)
        id_list = uniq_id_list(id_list)
        undelete_result = odict()
        slice_cursor = 0
        while len(id_list[slice_cursor:slice_cursor+MAX_DELETE]):
            undelete_slice = id_list[slice_cursor:slice_cursor+MAX_DELETE]
            slice_cursor += MAX_DELETE
            result = self._call_apex(self.svc.undelete, undelete_slice)
            undelete_result.update(Unpackomatic.unpack(result))
        return undelete_result

    def get_deleted(self, sobject_type, start_datetime, end_datetime):
        """Retrieves list of individual objects that have been deleted within
        the given timespan for the specified object.

        @param sobject_type: string name of a valid object type for the
            salesforce organisation
        @param start_datetime: start UTC datetime of data to retrieve
        @param end_datetime: end UTC datetime of data to retrieve

        @return: GetDeletedResult struct with id, earliestDateAvailable,
            latestDateCovered and modifiedDate
        @rtype: dict
        """
        get_deleted_response = self._call_apex(self.svc.getDeleted, sobject_type,
                                            start_datetime, end_datetime)
        return Unpackomatic.unpack(get_deleted_response)
    getDeleted = get_deleted

    def get_updated(self, sobject_type, start_datetime, end_datetime):
        """Retrieves list of individual objects that have been updated (added
        or changed) within the given timespan for the specified object.

        @param sobject_type: string name of a valid object type for the
            salesforce organisation
        @param start_datetime: start UTC datetime of data to retrieve
        @param end_datetime: end UTC datetime of data to retrieve

        @return: GetDeletedResult struct with id and latestDateCovered
        @rtype: dict
        """
        get_updated_response = self._call_apex(self.svc.getUpdated, 
                                               sobject_type,
                                               start_datetime, end_datetime)
        return Unpackomatic.unpack(get_updated_response)
    getUpdated = get_updated
    
    def execute_anonymous(self, codeblock):
        ea_response = self._call_apex(self.svc.executeanonymous, codeblock)
        return Unpackomatic.unpack(ea_response)
    
    def execute_apex(self, pkg, method, args=None, is_array=False):
        pkg = pkg.replace(".", "/")    
        
        sobject_ns = "http://soap.sforce.com/schemas/package/%s" %pkg
        
        nsmap = [{"ns":sobject_ns, "prefix":""}]

        if args is None:
            args = {}

        param_list = [] 
            
        is_real_array = True
        if is_array is False:
            is_real_array = False
            
        url = "/services/Soap/package/%s" %pkg
        
        execute_response = self.svc.executeApex(method, args, is_real_array, 
                                                nsmap, url, 
                                                sobject_ns, sobject_ns)
        result = Unpackomatic.unpack(execute_response, namespace=sobject_ns)
        return result
