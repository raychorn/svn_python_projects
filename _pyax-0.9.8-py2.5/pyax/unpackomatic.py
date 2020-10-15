"""Unpacker for apex SOAP responses from beatbox
that are composed of xmltramp Entity instances

@author: Kevin Shuk
@contact: surf@surfous.com
@copyright: 2007 Kevin Shuk and Canonical Ltd.
"""
import types
from pprint import pprint

import pyax.xmltramp as xmltramp
import pyax.beatbox as beatbox
from pyax.util import booleanize, listify
from pyax.datatype.apexdatetime import ApexDate, ApexDatetime

dummy_element = xmltramp.Element('dummy')
sf = beatbox._tPartnerNS

class Unpackomatic:
    
    def __init__(self, instance):
        """
        @param instance: xmltramp Element instance to unpack
        """
        self.parsed_instance = self.__parseItem(instance)[1]
        return


    @classmethod
    def unpack(cls, instance):
        """Most typical way to instantiate & run Unpackomatic
        
        @instance: SOAP response having the type "instance"
        
        @return: the unpacked SOAP response
        @rtype: Dictionary or List
        """
        unpacker = Unpackomatic(instance)
        return unpacker.parsed_instance


    def __parseItem(self, instance):
        """Deal with an item depending if it is a list of values 
        or a single value
        
        @param instance: xmltramp Element
        
        @return: name of element and value of element
        @rtype: Tuple
        """
        instance_name = None
        if hasattr(instance, '_name'):
            instance_name = instance._name[1]
            pass

        if type(instance) == types.ListType:
            instance_value = self.__parseList(instance)
        elif len(instance._dir) > 1:
            instance_value = self.__parseVector(instance)
        else:
            instance_value = self.__parseScalar(instance)
            pass
        #print "%s: %s" %(instance_name, instance_value)
        return (instance_name, instance_value)
    

    def __parseScalar(self, instance):
        """Unpacks a single value element
        
        @param instance: xmltramp element holding a single value (leaf node)
        """
        instance_value = str(instance)
            
        # handle special cases
        if len(instance._dir) == 0:
            instance_value = None
        elif instance_value in ('true', 'false'):
            instance_value = booleanize(instance_value)
            pass
        
        return instance_value


    def __parseVector(self, instance):
        """Unpack a multi-valued xmltramp Element
        
        @param instance: xmltramp Element
        """
        instance_list = instance._dir
            
        instance_dict = None
        if instance_list is not None:
            instance_dict = {}
    
            for instance in instance_list:
                instance_name, instance_value = self.__parseItem(instance)
                key_field = self.__determineKeyField(instance, instance_name)
                if instance_dict.has_key(instance_name):
                    # duplicate key - treat as a list or map of values
                    if isinstance(instance_dict[instance_name], dict) \
                        and key_field is not None:
                        # found a valid key field, build as map
                        # if the existing element is not a map or the existing 
                        # map has no key field, then convert to a dict
                        
                        # determine if the existing map has already been 
                        #sub-mapped
                        if instance_dict[instance_name].has_key(key_field):
                            instance_dict[instance_name] = \
                                {instance_dict[instance_name][key_field]: \
                                 instance_dict[instance_name]}
                            pass
                        instance_key = instance_value[key_field]
                        instance_dict[instance_name][instance_key] = \
                            instance_value
                            
                        pass
                    elif instance_dict[instance_name] == instance_value:
                        # skip it - the field is duplicated
                        # we've seen this with the Id field in a query. Maybe 
                        # we'll have to make this exception specific to Id
                        pass
                    else:
                        # found no key field, build as list
                        if not isinstance(instance_dict[instance_name], list):
                            # whoops - the elt isn't a list yet - listify it
                            instance_dict[instance_name] = \
                                listify(instance_dict[instance_name])

                        instance_dict[instance_name].append(instance_value)
                else:
                    instance_dict[instance_name] = instance_value

                continue
            pass
        return instance_dict


    def __parseList(self, instance_list):
        """Parse a List of xmltramp Element instances
        
        @param instance_list: List of xmltramp Element instances
        
        @return: the same instances, unpacked recursively
        @rtype: Dictionary or List, depending if we could determine a key
        """
        result = []
        
        # based on a handful of rules, try to determine what kind of objects 
        #the list contains and the key field
        key_field = None
        if len(instance_list):
            test_instance = instance_list[0]
            key_field = self.__determineKeyField(test_instance)
            pass
        if key_field is not None:
             result = {}
        
        for instance in instance_list:
            instance_value = self.__parseItem(instance)[1]
            if key_field is not None:
                result[instance_value[key_field]] = instance_value
            else:
                result.append(instance_value)
            continue
        
        return result


    def __determineKeyField(self, instance, instance_name=None):
        """Based on a handful of rules, try to determine what kind of objects
        the list contains and thus the key field
        
        @param instance: the xmltramp Element we're trying to parse
        @param instance_name: (optional) name of the Element we're parsing
        
        @return: field name to use as a key for Elements of this class
        @rtype: String
        """
        key_field = None
        if instance.has_key(sf.tabs):
            # this is a describeTabs response
            key_field = 'label'
        elif instance.has_key(sf.name) and instance.has_key(sf.fields):
            # this is a describeSObjectResult
            key_field = 'name'
        elif instance_name == 'fields':
            key_field = 'name'
        elif instance_name == 'childRelationships':
            key_field = 'childSObject'
        elif instance_name == 'picklistValues':
            key_field = 'label'

            pass
        return key_field
    