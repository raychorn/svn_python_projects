from vyperlogix.classes.CooperativeClass import Cooperative

import os, sys, traceback

from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.misc import _utils

from vyperlogix.classes.SmartObject import SmartFuzzyObject

try:
    from cStringIO import StringIO as StringIO
except:
    from StringIO import StringIO as StringIO

import vyperlogix.sf
from pyax.sobject.classfactory import ClassFactory

from vyperlogix.hash import lists

__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

class SalesForceAbstract(Cooperative):
    def __init__(self, sfQuery, object_name=None):
        self.__sfQuery__ = sfQuery
	self.__lastError__ = ''
	self.__factory = None
	self.__save_result = []
	self.__save_result_isValid = False
	self.__description__ = None
	self.__descriptions__ = SmartFuzzyObject({})
	self.__names__ = None
	self.__fields_by_metadata__ = None
	self.__metadata_by_names__ = None
	self.object_name = object_name

    def object_name():
        doc = "object_name - read_only"
        def fget(self):
            return self.__object_name
        def fset(self,object_name):
	    if (misc.isString(object_name)):
		self.__object_name = object_name
		self.__description__ = self.__sfQuery__.sfdc.describeSObject(object_name)
		self.__factory = ClassFactory(self.__sfQuery__.sfdc, object_name)
        return locals()
    object_name = property(**object_name())

    def object_prefix():
        doc = "object_prefix - read_only"
        def fget(self):
	    oname = self.object_name
            return oname[0].lower() if (misc.isString(oname)) else ''
        return locals()
    object_prefix = property(**object_prefix())

    def names():
        doc = "names - read_only - list of fully qualified names from the description of the object"
        def fget(self):
	    if (self.__names__ is None) and (self.description is not None):
		self.__names__ = ['%s.%s' % (self.object_prefix,name) for name in self.description.fieldnames]
            return self.__names__
        return locals()
    names = property(**names())

    def _names(self,names=[]):
	'''Returns a list of names limited by the names argument based on the actual list of names which is based on the actual field names.'''
	names = names if (isinstance(names,list)) else [names]
	op = self.object_prefix
	all_names = self.names
	_names_ = ['%s.%s' % (op,aName) for aName in [n.split('.')[-1] for n in names]]
	_names = all_names if (len(names) == 0) else [aName for aName in _names_ if (aName in all_names)]
	return _names
    
    def namesCanonicalized(self,names=[]):
	self.__names__ = self._names(names=names)
	return self.names
    
    def canonicalizeNames(self,stack):
	fields = []
	names = self.description.fieldnames
	try:
	    while (len(stack) > 0):
		field = stack.pop()[0]
		if (field == '*'):
		    fields = names
		    break
		elif (field in names):
		    fields.append(field)
		else:
		    raise SalesForceFieldException('Field with name of "%s" is not present in the SalesForce object named "%s".' % (field,self.object_name))
	except Exception, _details:
	    info_string = _utils.formattedException(details=_details)
	    raise SalesForceParmException('Cannot process the field specifications for object named "%s".\n%s' % (self.object_name,info_string))
	return self.namesCanonicalized(fields)
    
    def fields_by_metadata():
        doc = "fields_by_metadata - returns the analysis of all fields based on their metadata values."
        def fget(self):
	    if (self.__fields_by_metadata__ is None):
		d = lists.HashedFuzzyLists2()
		for k,aField in self.description.metadata['fields'].iteritems():
		    for name,value in aField.iteritems():
			if (d[name] is None):
			    d[name] = lists.HashedFuzzyLists()
			_d = d[name][0] if (isinstance(d[name],list)) else d[name]
			_d[value] = aField
		self.__fields_by_metadata__ = d
	    return self.__fields_by_metadata__
        return locals()
    fields_by_metadata = property(**fields_by_metadata())
    
    def metadata_by_names():
        doc = "metadata by names - returns the analysis of all fields based on their metadata names."
        def fget(self):
	    if (self.__metadata_by_names__ is None):
		d = lists.HashedFuzzyLists2()
		for k,aField in self.description.metadata['fields'].iteritems():
		    d[k] = aField
		self.__metadata_by_names__ = d
	    return self.__metadata_by_names__
        return locals()
    metadata_by_names = property(**metadata_by_names())
    
    def fields_by_(self,name='idlookup',value='true'):
	'''
	name must be a valid name that appears in the self.fields_by_metadata property.
	knowing the idlookup fields can be useful when one wants to access SalesForce objects using a unique Id field.
	'''
	d = self.fields_by_metadata[name] if (self.fields_by_metadata.has_key(name)) else {}
	return d[value] if (d.has_key(value)) else None

    def description():
        doc = "description - read_only"
        def fget(self):
            return self.__description__
        return locals()
    description = property(**description())

    def descriptions():
        doc = "descriptions - read_only - SmartFuzzyObject"
        def fget(self):
            return self.__descriptions__
        return locals()
    descriptions = property(**descriptions())

    def save_result_isValid():
        doc = "save_result_isValid - read_only"
        def fget(self):
            return self.__save_result_isValid
        return locals()
    save_result_isValid = property(**save_result_isValid())

    def save_result():
        doc = "save_result - read_only"
        def fget(self):
            return self.__save_result
        return locals()
    save_result = property(**save_result())

    def factory():
        doc = "factory - read_only"
        def fget(self):
            return self.__factory
        return locals()
    factory = property(**factory())

    def lastError():
        doc = "lastError - read_only"
        def fget(self):
            return self.__lastError__
        return locals()
    lastError = property(**lastError())

    def sfQuery():
        doc = "sfQuery - read_only"
        def fget(self):
            return self.__sfQuery__
        return locals()
    sfQuery = property(**sfQuery())
    
    def today(self):
	import time, datetime
        return _utils.getAsDateTimeStr(time.mktime((datetime.datetime.fromtimestamp(time.time()) - _utils.utcDelta()).timetuple()),fmt=_utils.formatSalesForceDateStr())
    
    def contains_sf_objects(self,objects):
	return self.sfQuery.contains_sf_objects(objects)
    
    def describeSObject(self,object_name):
	if (not self.descriptions.has_key(object_name)):
	    descr = self.sfQuery.sfdc.describeSObject(object_name)
	    self.descriptions[object_name] = descr
	
    def get_names(self,use_as=False):
	names = []
	self.describeSObject(self.object_name)
	_descr = self.descriptions[self.object_name]
	if (_descr is not None):
	    if (use_as):
		_names = ["%s.%s as '%s_%s'" % (self.object_prefix,name,self.object_name,name) for name in _descr.fieldnames]
	    else:
		_names = ['%s.%s' % (self.object_prefix,name) for name in _descr.fieldnames]
	    names.append(_names)
	return names
    
    def get_related_names(self,related_to,use_as=False):
	related_to = related_to if (isinstance(related_to,list)) else [related_to] if (related_to is not None) else []
	related_names = []
	for related_object in related_to:
	    if (self.description.metadata['childRelationships'].has_key(related_object)):
		self.describeSObject(related_object)
		related_descr = self.descriptions[related_object]
		if (related_descr is not None):
		    if (use_as):
			_names = ["%s.%s.%s as '%s_%s'" % (self.object_prefix,related_object,name,related_object,name) for name in related_descr.fieldnames]
		    else:
			_names = ['%s.%s.%s' % (self.object_prefix,related_object,name) for name in related_descr.fieldnames]
		    related_names.append(_names)
	return related_names
    
    def sf_query(self,soql='',callback=None):
	self.__lastError__ = ''
	if (len(soql) > 0):
	    try:
		try:
		    _types = self.sfQuery.getObjectsFromSOQL(soql,callback=callback)
		except Exception, details:
		    self.__lastError__ = _utils.formattedException(details=details)
		    return None
		return _types
	    except Exception, details:
		self.__lastError__ = _utils.formattedException(details=details)
	return None
    
    def createBatch(self,list_of_schemas):
	try:
	    self.__save_result = self.factory.create(list_of_schemas)
	    self.__save_result_isValid = (len(self.save_result) == len(list_of_schemas))
	except Exception, details:
	    self.__lastError__ = _utils.formattedException(details=details)
	    return []
	return self.save_result
    
    def update(self,object_proxy):
	'''Returns True if there were no errors otherwise False if there were errors, see the lastError property for the specifics of the error.'''
	noErrors = True
	try:
	    object_proxy.update()
	except Exception, details:
	    noErrors = False
	    self.__lastError__ = _utils.formattedException(details=details)
	return noErrors

    def retrieveSaveResult(self):
	try:
	    return self.factory.retrieveSaveResult(self.save_result)
	except Exception, details:
	    self.__lastError__ = _utils.formattedException(details=details)
	return []

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
