# Copyright 2007, 2008, 2009 Kevin Shuk and Canonical Limited
# All rights reserved
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
"""Unpack an xmltramp parsed response from a Salesforce call into a 
dictionary"""
import re
from pprint import pprint

import pyax.beatbox.xmltramp as xmltramp
from pyax.beatbox.beatbox import _tPartnerNS, _tSoapNS, _tSObjectNS, _tXsiNS
from pyax.collections.odict import odict
from pyax.datatype.apexdatetime import UTC, ApexDate, ApexDatetime


class Unpackomatic:
    @classmethod
    def unpack(cls, parsed_xml_tree, 
               namespace=_tPartnerNS, sobject_metadata=None):
        """Typical entry point for Unpackomatic
        
        @param parsed_xml_tree: xmltramp parsed xml tree
        @param sobject_metadata: (optional) metadata object
        
        @return: dictionay of unpacked xml response
        @rtype: odict
        """
        unpacker = cls(parsed_xml_tree, 
                       namespace=namespace,
                       sobject_metadata=sobject_metadata)
        return unpacker.result
        
    def __init__(self, xml_tree_root, 
                 namespace=_tPartnerNS, sobject_metadata=None,
                 no_key_count=0):
        self.__no_key_count = no_key_count
        self.sobject_metadata = sobject_metadata
        self.namespace = namespace
        #root = xmltramp.parse(xml_response)
        body = xml_tree_root[_tSoapNS.Body]        
        self.response_type = body.keys()[0]
        response_elt_tag = self.build_ns_tag_name(self.namespace, 
                                                  self.response_type)
        response = body[response_elt_tag]
        self.result = self.unpack_tree(response).get("result")
        
    def get_no_key_count(self):
        return self.__no_key_count
    no_key_count = property(fget=get_no_key_count)
        
    def build_ns_tag_name(self, namespace, tag_name):
        if isinstance(namespace, str):
            namespace = xmltramp.Namespace(namespace)
        ns_tag_name = eval("namespace.%s" %(tag_name))
        return ns_tag_name
        
    def unpack_tree(self, tree, level=0):
        # If the response comes in multiple <result> elements, list it here
        multiple_result_response_types = ("createResponse",
                                          "deleteResponse",
                                          "retrieveResponse",
                                          "undeleteResponse",
                                          "updateResponse",
                                          "upsertResponse",
                                          "describeSObjectsResponse",
                                          "emptyRecycleBinResponse",
                                         )
        is_sobject = False
        tree_map = {}
        type_attr = self.build_ns_tag_name(_tXsiNS, "type")
        namespace = self.namespace
        element_type = None
        if tree._attrs.has_key(type_attr):
            element_type = tree(type_attr) 
            if element_type == "sf:sObject":
                is_sobject = True
                namespace = _tSObjectNS
        for tag_name in tree.keys():
            ns_tag_name = self.build_ns_tag_name(namespace, tag_name)
            tag_count = len(tree[ns_tag_name:])
            if is_sobject and tag_name == "Id":
                # handle the duplicate Id situation
                tag_count = 1
            if (tag_count > 1
                or tag_name == "records" # records elt of queryResult should always be a list
                or (tag_name == "result" 
                    and self.response_type in multiple_result_response_types)):
                #treat as a list
                node_content = []
                for tag_content in tree[ns_tag_name:]:
                    unpacked_elt = self.unpack_element(tag_content, 
                                                       tag_name, 
                                                       level=level)
                    if tag_name == "result" and unpacked_elt is None:
                        # skip null result elements altogether.
                        continue
                    node_content.append(unpacked_elt)
            else:
                # there is zero or one instance of this tag at this level
                tag_content = tree[ns_tag_name]
                tag_type = None
                if tag_content._attrs.has_key(type_attr):
                    tag_type = tag_content(type_attr)
                unpacked_elt = self.unpack_element(tag_content, tag_name, 
                                                   level=level, 
                                                   is_sobject=is_sobject)
                if (isinstance(unpacked_elt, dict) and level > 1 
                    and tag_type not in ("QueryResult", "sf:sObject")):
                    # the tag contains structured content - make it a list
                    # but not if it's first-level or if it's a 
                    # higher level QueryResult (child relationship)
                    # or higher level sObject (parent relationship)
                    node_content = [unpacked_elt,]
                else:
                    node_content = unpacked_elt
            # attempt conversion of list to a map
            if isinstance(node_content, list):
                list_key_field = self.find_key_field(node_content, tag_name)
                if list_key_field is not None:
                    node_content = self.map_list(node_content, list_key_field)
                elif len(node_content) == 0:
                    node_content = {}
            tree_map[tag_name] = node_content
        return tree_map
    
    def unpack_element(self, content, tag_name, level=0, is_sobject=False):
        """Given the content of a single element, determine if it is a scalar value or a structure
        of data. If the former, type it and return it; if the latter, have it unpacked as a tree
        
        @param content: The content of a single element of the response message tree
        @param tag_name: Tag of the element we're unpacking - may provide a hint as to how to unpack
        @param level: level of recursion in unpacking this tree
        @param is_sobject: indicate if this is an sobject.
        
        @return: unpacked scalar value or dictionary subtree
        @rtype: scalar value varies, subtree will be dict
        """
        if len(content.keys()):            
            value = self.unpack_tree(content, level+1)
        else:
            # element's content is scalar
            value = self.type_content(content, tag_name, is_sobject)
        return value
        
    is_float_re = re.compile("^[-+]?\d*\.\d+$")
    is_int_re = re.compile("^[-+]?\d+$")
#    is_date_re = re.compile("^(\d\d\d\d)-(\d\d)-(\d\d)$")
#    is_datetime_re = re.compile("(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.\d{3}Z$")
    def type_content(self, scalar_content, tag_name, is_sobject):
        """ Determine the appropriate python data type for the element content
        If unpacking sobject fields, use metadata for typing.
        
        @param scalar_content: the single-value content of the element
        @param tag_name: name of the element's tag - may provide a hint in some cases
        @param is_sobject: boolean to indicate if the we're unpacking an sobject field in
                           which case we'd want to use metadata for typing
        """
       
        content_str = str(scalar_content)
        if len(content_str) == 0:
            # no length is a null value
            typed_content = None
        elif content_str in ("true", "false"):
            # booleanize - booleans always come in as literal "true" or "false"
            if content_str == "true":
                typed_content = True
            else:
                typed_content = False
        elif self.is_int_re.match(content_str):
            # content is int
            typed_content = int(content_str)
        elif self.is_float_re.match(content_str):
            # content is float
            typed_content = float(content_str)
        else:
            typed_content = content_str
        return typed_content
            
    def find_key_field(self, dict_list, member_key_name=None):
        """Try to deduce the key field of a list of like dicts
        
        @param dict_list: list of dictionaries for which to find the key field
        @param member_key_name: (optional) key that the dict_list will stored 
                                under - may provide a hint as to the key field 
                                to use
        @return: tag name of key field or None if one couldn't be determined
        @rtype: str
        """
        if len(dict_list):
            analyze_dict = dict_list[0]  
            if isinstance(analyze_dict, dict):
                # leave these as lists
                # childRelationships must be left as list as the only
                # potential key field is not unique.
                leave_as_list = ("childRelationships")
                if member_key_name in leave_as_list:
                    return None
                
                # specific list fields - try these first
                key_map = {}
                key = key_map.get(member_key_name)
                if key is not None:
                    return key
                
                # then, try these keys in order
                try_keys = ("id", "Id", "name", "label")
                for key in try_keys:
                    if analyze_dict.has_key(key):
                        return key
    
    def map_list(self, dict_list, key_field):
        """Takes a list of dicts and turns it into a map keyed by the value in 
        the key field
        
        @param dict_list: list of dictionaries to turn into a map
        @param key_field: field from the member dicts to use as the key to the 
                          map of dicts
        @return: map of the dictionaries, keyed by the value in the specified 
                 field of each
        @rtype: dict
        
        @note: map to odict to preserve ordering
        """
        map_dict = odict()
        for member_dict in dict_list:
            if not member_dict.has_key(key_field):
                raise KeyError("Every member dictionary must have the "
                               "specified key field '%s'"
                                %key_field)
            if map_dict.has_key(key_field):
                raise KeyError("The value of the key field '%s' is not "
                               "unique among all members "
                               "of the list" %key_field)
            key = member_dict[key_field]
            # handle the specific case of a createResponse where some 
            # inserted items failed therefore do not have a unique ID.
            if self.response_type == "createResponse" and key is None:
                self.__no_key_count += 1
                key = "FailedCreate-%s" %self.__no_key_count
            elif self.response_type == "queryResponse" and key is None:
                self.__no_key_count += 1
                key = "QueryNoId-%s" %self.__no_key_count
            map_dict[key] = member_dict
        return map_dict
